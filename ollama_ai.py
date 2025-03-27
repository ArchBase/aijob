import ollama

def compare_resume_job(resume, job_desc):
    prompt = f"Compare this resume:\n{resume}\nwith this job description:\n{job_desc}\nGive a match score (0-1). just give score only as output don't explain anything else"
    response = ollama.chat("llama3.2", messages=[{"role": "user", "content": prompt}])
    return float(response["message"]["content"])  # Ensure response is a number
