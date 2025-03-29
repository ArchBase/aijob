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
    print(f"job1:{job1['description']}\njob2:{job2['description']}\npreferences:{preferences}\nresume:{resume}\n")
    winner = 1
    if int(job2['description']) > int(job1['description']):
        winner = 2
    print(f"Winner:{winner}\n\n")
    return winner
