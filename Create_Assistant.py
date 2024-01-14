# For developer use
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)

Name = input("Name of the AI Assistant: ")
Instructions = input("Give the AI instructions on how it should behave: ")
Tool = input("AI tool: ")
if Tool != "retrieval" or Tool != "code_interpreter":
    print("Invalid Input")
    exit(0)

# Dataset for AI knowledge
def upload_file(path):
    file = client.files.create(file = open(path, "rb"), purpose = "assistants")
    return file


file = upload_file("data/dataset.json")

def create_assistant(file):
    assistant = client.beta.assistants.create(
        name = Name,
        instructions = Instructions,
        tools = [{"type": Tool}],
        model = "gpt-4-1106-preview",
        file_ids=  [file.id],
    )
    return assistant