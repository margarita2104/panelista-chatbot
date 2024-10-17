import json
import os
import time
from pathlib import Path
import re

import openai
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize API clients
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
    speaker_list = "\n".join(
        f"{i}. {speaker['first_name']} {speaker['last_name']} - {speaker['topics']}"
        for i, speaker in enumerate(speakers, start=1)
    )

    prompt = f"""
    You are a helpful assistant tasked with suggesting speakers for an event based on the organizer's request. Below is a list of available speakers:

    {speaker_list}

    User query: "{user_input}"

    Please return the matching speakers' numbers in a comma-separated format, and only their numbers. If no speakers match, return "No suitable speaker found."
    """
    return prompt


def extract_speaker_by_numbers(speaker_numbers):
    """
    Extracts speakers' details based on the provided speaker numbers.
    """
    if not json_file_path.exists():
        print("Error: 'speakers.json' file not found.")
        return []

    with json_file_path.open('r') as file:
        try:
            speakers = json.load(file)
        except json.JSONDecodeError:
            print("Error: Failed to parse 'speakers.json'.")
            return []

    matched_speakers = []

    for speaker_number in speaker_numbers:
        try:
            speaker_number = int(speaker_number.strip())
        except ValueError:
            print(f"Error: Invalid speaker number '{speaker_number}' received.")
            continue

        if 1 <= speaker_number <= len(speakers):
            speaker = speakers[speaker_number - 1]
            matched_speakers.append({
                'name': f"{speaker['first_name']} {speaker['last_name']}",
                'expertise': speaker['topics'],
                'bio': speaker['career_description']
            })
        else:
            print(f"Error: Speaker number '{speaker_number}' out of range.")

    return matched_speakers


def suggest_speakers_from_user_input(user_input: str):
    suggestion_prompt = create_speaker_suggestion_prompt(user_input)

    if not suggestion_prompt:
        print("Error: Failed to generate speaker suggestion prompt.")
        return "No suitable speaker found."

    selected_model = "llama3-8b-8192"

    response_text, response_time = get_response(selected_model, suggestion_prompt)

    # Debugging: Print the response text
    print("Response Text:", response_text)

    # Use regex to extract numbers from the response text
    speaker_numbers = re.findall(r'\d+', response_text)
    print("Speaker Numbers:", speaker_numbers)  # Debugging

    # Directly extract speakers based on the matched numbers
    matched_speakers = extract_speaker_by_numbers(speaker_numbers)
    print("Matched Speakers:", matched_speakers)

    if matched_speakers:
        response = "Suggested Speakers:\n"
        for speaker in matched_speakers:
            response += f"- {speaker['name']}\n  Expertise: {speaker['expertise']}\n  Bio: {speaker['bio']}\n"
        print("Response to Frontend:", response)  # Debugging
        return response
    else:
        print("No suitable speaker found based on the input.")  # Debugging
        return "No suitable speaker found based on the input."
