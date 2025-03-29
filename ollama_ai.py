import ollama
import re
import random

def get_best_job_based_on_preference_and_resume(job1, job2, preferences, resume, mode="both"):
    prompt = f"{preferences} these are preferences of a jobseeker, {resume} this is his resume.\n"

    if mode == "preferences":
        prompt += (f"There are two jobs:\n1. {job1['title']} {job1['description']}\n"
                   f"2. {job2['title']} {job2['description']}\n"
                   f"Based only on the jobseeker's preferences, which job is better? Say 1 or 2 or 0(if both are good or bad). don't say anything else")
    elif mode == "resume":
        prompt += (f"There are two jobs:\n1. {job1['title']} {job1['description']}\n"
                   f"2. {job2['title']} {job2['description']}\n"
                   f"Based only on the jobseeker's resume, which job is better? Say 1 or 2 or (if both are good or bad). don't say anything else")
    else:
        prompt += (f"There are two jobs:\n1. {job1['title']} {job1['description']}\n"
                   f"2. {job2['title']} {job2['description']}\n"
                   f"Based on both preferences and resume, which job is better? Say 1 or 2 or 0(if both are good or bad). don't say anything else")

    print(f"\nPrompt: {prompt}")
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    response_text = response["message"]["content"].strip()
    print(f"\nAI response: {response_text}\n")

    match = re.search(r'\b(1|2|0)\b', response_text)

    if match:
        winner = int(match.group(1))
        if winner == 0:
            winner = random.choice([1, 2])  # Choose randomly if no clear winner
        return winner
    else:
        print("AI failed to answer")
        return random.choice([1, 2])
