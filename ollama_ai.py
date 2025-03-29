import ollama
import re
import random

import re
import random
import ollama

def get_best_job_based_on_preference_and_resume(job1, job2, preferences, resume, mode="both"):
    if mode == "preferences":
        prompt = (f"These are the jobseeker's preferences: '{preferences}'\n"
                  f"There are two jobs:\n"
                  f"1. 'title: {job1['title']} description: {job1['description']}'\n"
                  f"2. 'title: {job2['title']} description: {job2['description']}'\n"
                  f"Soley based only on the jobseeker's preferences, which job is better? "
                  f"Say 1 or 2 or 0 (if both are equally good or bad). Don't say anything else.")
    elif mode == "resume":
        prompt = (f"This is the jobseeker's resume: '{resume}'\n"
                  f"There are two jobs:\n"
                  f"1. 'title: {job1['title']} description: {job1['description']}'\n"
                  f"2. 'title: {job2['title']} description: {job2['description']}'\n"
                  f"Solely based only on the jobseeker's resume, which job is better? "
                  f"Say 1 or 2 or 0 (if both are equally good or bad). Don't say anything else.")
    else:
        prompt = (f"These are the jobseeker's preferences: '{preferences}'\n"
                  f"This is the jobseeker's resume: '{resume}'\n"
                  f"There are two jobs:\n"
                  f"1. 'title: {job1['title']} description: {job1['description']}'\n"
                  f"2. 'title: {job2['title']} description: {job2['description']}'\n"
                  f"Based on both preferences and resume, which job is better? "
                  f"Say 1 or 2 or 0 (if both are equally good or bad). Don't say anything else.")

    print(f"\nPrompt: {prompt}")
    response = ollama.chat(model="gemma3", messages=[{"role": "user", "content": prompt}])
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
