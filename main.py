import os
import json
from textual.containers import Container, ScrollableContainer
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, ListView, ListItem, Label, Markdown, Input
from textual import work

from themes import *
import ai

dirname, _ = os.path.split(os.path.abspath(__file__))
THIS_DIRECTORY = f'{dirname}{os.sep}'

class Importer(App):
    BINDINGS = [
        ('^s', 'session_list', 'session list')
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
        
    '''

    key = ai.auth()
    session_list = None
    current_session = None
    session_history = []
    history_limit = 30

    def compose(self) -> ComposeResult:
        '''Create child widgets for the app.'''   
        yield Header(show_clock=True)

        self.session_list = ListView(
            ListItem(Label('  NEW  ')),
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

        # load previous sessions
        session_ids = self.list_sessions()
        for session in session_ids:
            self.session_list.append(ListItem(Label(f' {session} ')))
        self.current_session = session_ids[0]
        self.session_list.index = 1
        self.session_history = self.load_session(self.current_session)

    # =========================
    #  Actions
    # =========================

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

    def action_session_list(self) -> None:
        '''Move focus to date panel'''
        self.notify(
           'Focus on left panel',
            title='DEBUG',
            severity='warning'
        )
        self.query_one('#session_list').focus()

    def action_focus_right(self) -> None:
        '''Move focus to task panel'''
        self.notify(
           'Focus on right panel',
            title='DEBUG',
            severity='warning'
        )
        self.query_one('#right').focus()

    # =========================
    #  General functions
    # =========================

    def list_sessions(self):
        session_files = list_files(f'{THIS_DIRECTORY}sessions{os.sep}', ['.json'])
        return [f.split(os.sep)[-1].replace('.json', '') for f in session_files]

    def load_session(self, session_id):
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
        response, reasoning, self.session_history = ai.ask(
            self.key,
            user_message,
            self.session_history
        )
        self.save_session(self.current_session)
        if len(self.session_history) > self.history_limit:
            self.session_history = self.session_history[-self.history_limit:]
        self.call_from_thread(
            self.show_ai_response,
            response
        )

    def save_session(self, session_id):
        save_as = f'{THIS_DIRECTORY}sessions{os.sep}{session_id}.json'
        save_json(self.session_history, save_as)

    def show_ai_response(self, response):
        self.query_one('#message_history').mount(Markdown(f'\n{response.lstrip()}', classes='ai_response'))
        self.query_one('#message_history').scroll_end()

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

