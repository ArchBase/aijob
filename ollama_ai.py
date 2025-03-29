import ollama
import re
import random

def get_best_job_based_on_preference_and_resume(job1, job2, preferences, resume):
    # Print reference for debugging
    print(f"job1: {job1['title'] + " " + job1['description']}\njob2:{job2['title'] + " " + job2['description']}\npreferences: {preferences}\nresume: {resume}\n")

    # Construct the prompt
    prompt = (
        f"{preferences} these are preferences of a jobseeker, {resume} this is his resume.\n"
        f"There are two jobs:\n"
        f"1. {job1['title'] + " " + job1['description']}\n"
        f"2. {job2['title'] + " " + job2['description']}\n"
        f"Based on jobseeker's preferences and resume, which job is the best for him? Say 1 or 2 or 0(represents both jobs isn't good for jobseeker), nothing else."
    )

    # Get response from Ollama
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

    # Extract response text
    response_text = response["message"]["content"].strip()
    
    # Use regex to extract the first occurrence of '1' or '2' as a standalone number
    match = re.search(r'\b(1|2|0)\b', response_text)

    if match:
        winner = int(match.group(1))
        print(f"winner: {winner}\n")
        if winner == 0:
            print("no one won, choosing a random\n")
            winner = random.choice([1, 2])
        return winner
    else:
        raise ValueError(f"Unexpected response from AI: {response_text}")
