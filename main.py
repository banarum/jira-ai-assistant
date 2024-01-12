import json
from pprint import pprint

import openai

from utils import createTicket

with open('credentials.json', 'r') as f:
    credentials = json.load(f)

openai.api_key = credentials['openai_api_key']

with open('prompts/bot-init.prmpt.txt') as f:
    bot_init = f.read()

with open('prompts/map-to-create-ticket-request.prmpt.txt') as f:
    map_to_create_ticket_request = f.read()

with open('prompts/bot-greetings.prmpt.txt') as f:
    bot_greetings = f.read()

context = [ {'role':'system', 'content': bot_init}]  # accumulate messages


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def collect_messages(value_input):
    context.append({'role': 'user', 'content': f"{value_input}"})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': f"{response}"})
    return response


def finalise_order():
    messages = context.copy()
    messages.append(
        {'role': 'system', 'content': map_to_create_ticket_request},
    )

    response = get_completion_from_messages(messages, temperature=0)
    response_obj = json.loads(response)
    createTicket(credentials["jira_username"], credentials["jira_password"], response_obj['title'], response_obj['description'], response_obj['type'], response_obj['priority'])


print(collect_messages(bot_greetings))

while True:
    message = input()
    response = collect_messages(message)
    print(response.split('{"ticket_is_finalised": true}')[0])
    if len(response.split('{"ticket_is_finalised": true}')) > 1 or message == "finalize":
        print("We are preparing your order...")
        finalise_order()
        break