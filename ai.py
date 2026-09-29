import requests
import requests
import json
import os

def auth():
    with open('keys.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read()).get('openrouter.ai', None)

def ask(key, prompt, history=[]):
    # history = [
    #     {
    #         'role':'user',
    #         'content':'previous message'
    #     },
    #     {
    #         'role':'assistant',
    #         'content':'previous message',
    #         'reasoning_details':'reasoning string produced last time'
    #     }
    # ]

    system_prompt = get_system_prompt()
    if history[0] != system_prompt:
        messages = get_system_prompt() + history + [{
            'role':'user',
            'content':prompt
        }]
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "openrouter/free",
            "messages": messages,
            "reasoning": {"enabled": True}
        })
    )

    response = response.json()
    save_json(response, 'response.json')
    try:
        response = response['choices'][0]['message']
    except:
        print(json.dumps(response, indent=4))

    new_history = messages + [{
        'role': 'assistant',
        'content': response.get('content'),
        'reasoning_details':response.get('reasoning')
    }]

    return response.get('content'), response.get('reasoning'), new_history

def chat():
    key = auth()
    if key is not None:
        history = []
        while True:
            message = input(' 👤 ')
            print(' 💻 ...', end='\r')
            response, reasoning, history = ask(
                key,
                message,
                history
            )
            print(f' 💻 {response}')
            if len(history) > 10:
                history = history[-10:]

def get_system_prompt():
    if os.path.exists('system_prompt.json'):
        with open('system_prompt.json', 'r', encoding='utf-8') as f:
            return [json.loads(f.read())]
    else:
        return []
    

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4))
        
if __name__ == '__main__':
    chat()

    # TODO:
    #   - Textual UI
    #   - Save conversation history
    #   - Pass larger history/context with each message

