import os
import openai
import requests
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

gpt_functions = [
    {
        "name": "get_mentee_data",
        "description": "Get the mentee's current data",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the mentee, e.g. Bob Ross",
                },
                "focus": {
                    "type": "string",
                    "description": "The topic of focus for the mentee.",
                },
                "degree": {
                    "type": "string",
                    "description": "The type of degree the mentee has, e.g bachelors in business",
                },
                "years": {
                    "type": "integer",
                    "description": "The number of years of experience in the particular topic",
                },
                "values": {
                    "type": "string",
                    "description": "The specific topic the mentee values",
                },

            },
            "required": ["name", "focus", "degree", "years", "values"],
        },
    }

]

response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

def get_gpt_response(messages):
    # response = openai.ChatCompletion.create(
    #     model = "gpt-3.5-turbo",
    #     messages=messages
    # )
    response = chat_completion_request(messages, functions = gpt_functions)
    return response.json()["choices"][0]["message"]

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "I am Ethan. I want to learn AI"},
        {"role": "assistant", "content": "Hi Ethan. What do you want to know about AI"}
    ]

while True:
    print(messages)
    user_input = input()
    messages = update_chat(messages, "user", user_input) #updating messages with user's chat
    model_response = get_gpt_response(messages)
    messages = update_chat(messages, "assistant", model_response)
    
