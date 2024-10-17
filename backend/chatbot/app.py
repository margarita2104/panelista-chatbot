import json
import os
import time
from pathlib import Path

import openai
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

sambanova_api_key = os.getenv("SAMBANOVA_API_KEY")
openai_client = openai.OpenAI(
    api_key=sambanova_api_key,
    base_url="https://api.sambanova.ai/v1",
)

json_file_path = Path(__file__).resolve().parent.parent / 'user' / 'speakers.json'


def get_response(model, prompt):
    if not prompt:
        raise ValueError("The prompt provided is None or empty.")

    start_time = time.time()
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model
    )
    end_time = time.time()
    response_time = end_time - start_time

    response_text = chat_completion.choices[0].message.content.strip()

    return response_text, response_time


def create_speaker_suggestion_prompt(user_input):
    if not json_file_path.exists():
        print("Error: 'speakers.json' file not found.")
        return None

    with json_file_path.open('r') as file:
        try:
            speakers = json.load(file)
        except json.JSONDecodeError:
            print("Error: Failed to parse 'speakers.json'.")
            return None

    if not speakers:
        print("Error: No speakers found in 'speakers.json'.")
        return None

    # Dynamically generate the list of speakers in the prompt
    speaker_list = ""
    for i, speaker in enumerate(speakers, start=1):
        speaker_list += f"{i}. {speaker['first_name']} {speaker['last_name']} - {speaker['topics']}\n"

    prompt = f"""
        You are a helpful assistant tasked with suggesting speakers for an event based on the organizer's request. Below is a list of available speakers:

        {speaker_list}

        Example queries:

        - "I need a speaker who can talk about Web Development." → 1
        - "Looking for an expert on UX/UI Design." → 2
        - "Can you suggest someone for a DevOps panel?" → 3

        User query: "{user_input}"

        Return only the number of the most relevant speaker. Do not include any additional text.
        """
    return prompt


def extract_speaker_details(speaker_number):
    if not json_file_path.exists():
        print("Error: 'speakers.json' file not found.")
        return None

    with json_file_path.open('r') as file:
        try:
            speakers = json.load(file)
        except json.JSONDecodeError:
            print("Error: Failed to parse 'speakers.json'.")
            return None

    # Convert speaker_number to integer and find the corresponding speaker
    try:
        speaker_number = int(speaker_number.strip())
    except ValueError:
        print(f"Error: Invalid speaker number '{speaker_number}' received.")
        return None

    if 1 <= speaker_number <= len(speakers):
        speaker = speakers[speaker_number - 1]
        return {
            'name': f"{speaker['first_name']} {speaker['last_name']}",
            'expertise': speaker['topics'],
            'bio': speaker['career_description']
        }

    print(f"Error: Speaker number '{speaker_number}' out of range.")
    return None


def suggest_speakers_from_user_input(user_input: str):
    suggestion_prompt = create_speaker_suggestion_prompt(user_input)

    if not suggestion_prompt:
        print("Error: Failed to generate speaker suggestion prompt.")
        return "No suitable speaker found."

    selected_model = "llama3-8b-8192"

    speaker_number, response_time = get_response(selected_model, suggestion_prompt)

    speaker_details = extract_speaker_details(speaker_number)

    if speaker_details:
        return f"Suggested Speaker: {speaker_details['name']}\nExpertise: {speaker_details['expertise']}\nBio: {speaker_details['bio']}"
    else:
        return "No suitable speaker found based on the input."
