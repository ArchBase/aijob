import ollama
import re
import random


def compare_resume_job(resume, job_desc):
    return 1
    prompt = f"Compare this resume:'\n{resume}\n'with this job description:'\n{job_desc}\n'Give a match score (0-1). Just give the score as output, don't explain anything else."
    print(f"prompt: {prompt}")
    response = ollama.chat("mistral:7b-instruct", messages=[{"role": "user", "content": prompt}])

    # Extract numeric score using regex
    match = re.search(r"([0-1](?:\.\d+)?)", response["message"]["content"])
    
    if match:
        print(f"score: {float(match.group(1))}")
        print()
        return float(match.group(1))
    else:
        raise ValueError(f"Unexpected response: {response['message']['content']}")

def compare_description_job(description, job_desc):
    return 1
    prompt = f"Compare this conditions:'\n{description}\n'with this job description:'\n{job_desc}\n'Give a match score (0-1). Just give the score as output, don't explain anything else."
    print(f"prompt: {prompt}")
    response = ollama.chat("mistral:7b-instruct", messages=[{"role": "user", "content": prompt}])
    
    # Extract numeric score using regex
    match = re.search(r"([0-1](?:\.\d+)?)", response["message"]["content"])
    
    if match:
        print(f"score: {float(match.group(1))}")
        print()
        return float(match.group(1))
    else:
        raise ValueError(f"Unexpected response: {response['message']['content']}")


def get_best_job_based_on_preference_and_resume(job1, job2, preferences, resume):
    # Print reference for debugging
    print(f"job1: {job1['description']}\njob2: {job2['description']}\npreferences: {preferences}\nresume: {resume}\n")

    # Construct the prompt
    prompt = (
        f"{preferences} these are preferences of a jobseeker, {resume} this is his resume.\n"
        f"There are two jobs:\n"
        f"1. {job1['title'] + " " + job1['description']}\n"
        f"2. {job2['title'] + " " + job2['description']}\n"
        f"Based on jobseeker's preferences and resume, which job is the best for him? Say 1 or 2, nothing else."
    )

    # Get response from Ollama
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

    # Extract response text
    response_text = response["message"]["content"].strip()
    
    # Use regex to extract the first occurrence of '1' or '2' as a standalone number
    match = re.search(r'\b(1|2)\b', response_text)

    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"Unexpected response from AI: {response_text}")
