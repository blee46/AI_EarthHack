from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)

# Thread Database
def check_if_thread_exists(uid):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(uid, None)

def store_thread(uid, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[uid] = thread_id

# AI Response
def generate_response(message_body, uid, name):
    thread_id = check_if_thread_exists(uid)

    if thread_id is None:
        print(f"Creating new thread for {name} with Uid: {uid}")
        thread = client.beta.threads.create()
        store_thread(uid, thread.id)
        thread_id = thread.id
    else:
        print(f"Retrieving existing thread for {name} with Uid: {uid}")
        thread = client.beta.threads.retrieve(thread_id)

    message = client.beta.threads.messages.create(
        thread_id = thread_id,
        role = "user",
        content = message_body,
    )

    new_message = run_assistant(thread)
    print(f"To {name}:", new_message)
    return new_message

# Running the Assistant
def run_assistant(thread):
    assistant = client.beta.assistants.retrieve("asst_3orkRUQUygdi9jrBQwCGnEap")

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    return new_message


# Test case for assistant

new_message = generate_response("Give me an idea to reduce emissions and carbon footprints.", "123", "John")