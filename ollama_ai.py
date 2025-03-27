import ollama
import re

def compare_resume_job(resume, job_desc):
    prompt = f"Compare this resume:\n{resume}\nwith this job description:\n{job_desc}\nGive a match score (0-1). Just give the score as output, don't explain anything else."
    response = ollama.chat("mistral:7b-instruct", messages=[{"role": "user", "content": prompt}])
    
    # Extract numeric score using regex
    match = re.search(r"([0-1](?:\.\d+)?)", response["message"]["content"])
    
    if match:
        return float(match.group(1))
    else:
        raise ValueError(f"Unexpected response: {response['message']['content']}")

