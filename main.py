from datetime import datetime
import os
import json
from textual.app import App, ComposeResult, Screen
from textual.containers import Container, ScrollableContainer, Horizontal, Vertical
from textual.events import Key
from textual.widgets import Footer, Header, ListView, ListItem, Label, Markdown, Input, Button
from textual import work, on

from themes import *
import ai

dirname, _ = os.path.split(os.path.abspath(__file__))
THIS_DIRECTORY = f'{dirname}{os.sep}'

class Importer(App):
    BINDINGS = [
        ('^s', 'session_list', 'session list'),
        ('^d', 'delete_session', 'delete session'),
    ]

    CSS = '''
        Screen {
            layout: horizontal;
        }

        #left, #right {
            height: 100%;
            border: solid black;
        }

        #left {
            width: 20%;
        }

        #right {
            width: 80%;
        }

        .ai_response, .user_message {
            padding: 1 1 0 1;
        }

        .ai_response {
            background: $surface;
            margin: 0 0 1 0;
        }

        .user_message, Input {
            color: $secondary;
        }

        .system_message {
            color: $primary;
        }

        ConfirmationPopup {
            layout: vertical;
            content-align: center middle;
            align: center middle;
        }
        
        ConfirmationPopup Vertical {
            width: auto;
            height: auto;
        }
        
        ConfirmationPopup Label {
            text-align: center;
            width: auto;
            margin-bottom: 1;
        }
        
        ConfirmationPopup Horizontal {
            width: auto;
            content-align: center middle;
        }
        
        ConfirmationPopup Button {
            width: 10;
            margin: 0 1;
        }
        
    '''

    key = ai.auth()
    current_focus = 'right'
    session_list = None
    current_session = None
    session_history = []
    history_limit = 30

    class ConfirmationPopup(Screen):
        def __init__(self, session_to_delete):
            super().__init__()
            self.session_to_delete = session_to_delete

        def compose(self):
            with Vertical():
                yield Label(f'Permanently delete the "{self.session_to_delete}" session?')
                with Horizontal():
                    yield Button("Yes", id="yes")
                    yield Button("No", id="no")

        def on_mount(self):
            self.query_one(Button).focus()

        @on(Button.Pressed)
        def on_button_pressed(self, event):
            if event.button.id == "yes":
                os.remove(
                    f'{THIS_DIRECTORY}sessions{os.sep}{self.session_to_delete}.json'
                )
                self.app.update_session_list(selected=0, show_all=True)
                self.notify(
                    f'The "{self.session_to_delete}" session has been deleted',
                    title='Session deleted'
                ) 
            self.app.pop_screen()

        def on_key(self, event: Key):
            buttons = list(self.query(Button))
            if event.key == 'left':
                buttons[0].focus()
            if event.key == 'right':
                buttons[1].focus()

    class CustomListItem(ListItem):
        def __init__(self, description: str):
            super().__init__()
            self.description = description

        def compose( self ):
            yield Label(f'  {self.description}  ')

    def compose(self) -> ComposeResult:
        '''Create child widgets for the app.'''   
        yield Header(show_clock=True)

        self.session_list = ListView(
            id='session_list'
        )
      
        yield Container(
            self.session_list,
            id='left'
            )

        input_widget = Input(
            placeholder='Message...',
            id='user_message_input'
        )
        message_history = ScrollableContainer(
            Markdown(''),
            id='message_history'
        )
        yield Container(
            message_history,
            input_widget,
            id='right'
        )

        input_widget.focus()

        yield Footer()

    def on_mount(self):
        self.title = 'Assistant'
        self.register_theme(arasaka_theme)
        self.register_theme(night_city_theme)
        self.register_theme(decker_theme)
        self.register_theme(kusanagi_theme)
        self.register_theme(pipboy_theme)
        self.register_theme(lcars_theme)
        self.theme = 'arasaka'
        self.bind(keys='ctrl+s', action='session_list')
        self.bind(keys='ctrl+d', action='delete_session')

        self.update_session_list()

    # =========================
    #  Actions
    # =========================

    def action_delete_session(self):
        self.app.push_screen(self.ConfirmationPopup(self.current_session))

    def action_session_list(self):
        self.current_focus = 'left'
        self.query_one('#session_list').focus()

    def on_input_submitted(self, event: Input.Submitted):
        user_message = event.value
        if user_message != '':
            self.query_one('#user_message_input').value = ''
            self.query_one('#message_history').mount(
                Markdown(
                    f'\n{user_message}',
                    classes='user_message'
                )
            )
            self.query_one('#message_history').scroll_end()
            self.query_ai(user_message)

    def on_key(self, event: Key):
        if event.key == 'enter' or event.key == 'right':
            if self.current_focus == 'left':
                if self.session_list.index == 0:
                    self.current_session = 'NEW'
                    self.session_history = self.load_session(None)
                else:
                    self.current_session = self.list_sessions()[self.session_list.index -1]
                    self.session_history = self.load_session(self.current_session)
                self.query_one('#user_message_input').focus()
        # if event.key == 'left':
        #     self.current_focus = 'left'
        #     self.query_one('#session_list').focus()

    # =========================
    #  General functions
    # =========================

    def list_sessions(self):
        session_files = list_files(f'{THIS_DIRECTORY}sessions{os.sep}', ['.json'])
        return [f.split(os.sep)[-1].replace('.json', '') for f in session_files]

    def load_session(self, session_id):
        self.query_one('#message_history').remove_children()
        history = []
        if session_id is not None:
            history = load_json(f'{THIS_DIRECTORY}sessions{os.sep}{session_id}.json')
            for message in history[-self.history_limit:]:
                if message['role'] == 'user':
                    self.query_one('#message_history').mount(
                        Markdown(
                            f"\n{message['content']}",
                            classes='user_message'
                        )
                    )
                elif message['role'] == 'assistant':
                    self.query_one('#message_history').mount(
                        Markdown(
                            f"\n{message['content']}",
                            classes='ai_response'
                        )
                    )
        self.query_one('#message_history').scroll_end()
        return history

    @work(thread=True)
    def query_ai(self, user_message):
        result = ai.ask(
            self.key,
            user_message,
            self.session_history
        )
        if result['success']:
            response = result['data']['content']
            reasoning = result['data']['reasoning']
            self.session_history = result['data']['history']

            if self.current_session == 'NEW' or self.current_session is None:
                self.current_session = datetime.now().strftime('%d %b %H-%M')
                self.save_session(self.current_session)
                self.call_from_thread(
                    self.update_session_list,
                    -1,
                    False
                )
            else:
                self.save_session(self.current_session)
            if len(self.session_history) > self.history_limit:
                self.session_history = self.session_history[-self.history_limit:]
            self.call_from_thread(
                self.show_ai_response,
                response
            )

        else:
            self.notify(
                result['data']['content'],
                title='Error',
                severity='error'
            )      
        
    def save_session(self, session_id):
        save_as = f'{THIS_DIRECTORY}sessions{os.sep}{session_id}.json'
        save_json(self.session_history, save_as)

    def show_ai_response(self, response):
        if response is not None:
            self.query_one('#message_history').mount(Markdown(f'\n{response.lstrip()}', classes='ai_response'))
        
        self.query_one('#message_history').scroll_end()

    def update_session_list(self, selected=1, show_all=True):
        self.session_list.remove_children()
        self.session_list.append(self.CustomListItem('NEW'))
        session_ids = self.list_sessions()#[::-1]
        for session in session_ids:
            self.session_list.append(self.CustomListItem(session))
        if len(session_ids) > 0:
            self.current_session = session_ids[0]
            self.session_list.index = selected
        else:
            self.current_session = 'NEW'
            self.session_list.index = 0
        if show_all:
            self.session_history = self.load_session(self.current_session)

def list_files(folder, extensions=None):
    file_list = []
    all_files = os.listdir(folder)
    for name in all_files:
        if extensions is not None:
            for ext in extensions:
                if name.endswith(ext):
                    file_list.append(f'{folder}{os.sep}{name}')
        else:
            file_list.append(f'{folder}{os.sep}{name}')
    return file_list

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    app = Importer()
    app.run()

    # TODO:
    # - Switch between sessions
    # - Start new session from NEW option
    # - Option to delete a session
    # - Show model for each response
    # - Rename session

