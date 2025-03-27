from flask import Flask, render_template, request, redirect, session
import sqlite3
from ollama_ai import compare_resume_job

app = Flask(__name__)
app.secret_key = "secret"  # Needed for session handling

# Database Helper
def get_db():
    conn = sqlite3.connect("jobs.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Home ---
@app.route("/")
def home():
    return render_template("home.html")

# --- User Signup ---
@app.route("/user/signup", methods=["GET", "POST"])
def user_signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        resume = request.form["resume"]
        db = get_db()
        db.execute("INSERT INTO users (username, password, resume) VALUES (?, ?, ?)", 
                   (username, password, resume))
        db.commit()
        return redirect("/user/login")
    return render_template("user_signup.html")

# --- User Login ---
@app.route("/user/login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                          (username, password)).fetchone()
        if user:
            session["user_id"] = user["id"]
            return redirect("/user/dashboard")
    return render_template("user_login.html")

# --- User Dashboard ---
@app.route("/user/dashboard")
def user_dashboard():
    if "user_id" not in session:
        return redirect("/user/login")
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    applied_jobs = db.execute("SELECT * FROM applications WHERE user_id = ?", (session["user_id"],)).fetchall()
    return render_template("user_dashboard.html", user=user, applied_jobs=applied_jobs)

# --- Find Jobs ---
@app.route("/user/find_jobs")
def find_jobs():
    if "user_id" not in session:
        return redirect("/user/login")
    db = get_db()
    jobs = db.execute("SELECT * FROM jobs").fetchall()
    user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    
    # AI Filtering (resume vs job description)
    filtered_jobs = [job for job in jobs if compare_resume_job(user["resume"], job["description"]) > 0.5]
    
    return render_template("find_jobs.html", jobs=filtered_jobs)

# --- Apply Job ---
@app.route("/user/apply/<int:job_id>")
def apply_job(job_id):
    if "user_id" not in session:
        return redirect("/user/login")
    db = get_db()
    db.execute("INSERT INTO applications (user_id, job_id, status) VALUES (?, ?, ?)", 
               (session["user_id"], job_id, "Pending"))
    db.commit()
    return redirect("/user/dashboard")

# --- Recruiter Signup ---
@app.route("/recruiter/signup", methods=["GET", "POST"])
def recruiter_signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        db.execute("INSERT INTO recruiters (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return redirect("/recruiter/login")
    return render_template("recruiter_signup.html")

# --- Recruiter Login ---
@app.route("/recruiter/login", methods=["GET", "POST"])
def recruiter_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        recruiter = db.execute("SELECT * FROM recruiters WHERE username = ? AND password = ?", 
                               (username, password)).fetchone()
        if recruiter:
            session["recruiter_id"] = recruiter["id"]
            return redirect("/recruiter/dashboard")
    return render_template("recruiter_login.html")

# --- Recruiter Dashboard ---
@app.route("/recruiter/dashboard")
def recruiter_dashboard():
    if "recruiter_id" not in session:
        return redirect("/recruiter/login")
    db = get_db()
    jobs = db.execute("SELECT * FROM jobs WHERE recruiter_id = ?", (session["recruiter_id"],)).fetchall()
    return render_template("recruiter_dashboard.html", jobs=jobs)

# --- Create Job ---
@app.route("/recruiter/create_job", methods=["GET", "POST"])
def create_job():
    if "recruiter_id" not in session:
        return redirect("/recruiter/login")
    if request.method == "POST":
        description = request.form["description"]
        db = get_db()
        db.execute("INSERT INTO jobs (recruiter_id, description) VALUES (?, ?)", 
                   (session["recruiter_id"], description))
        db.commit()
        return redirect("/recruiter/dashboard")
    return render_template("create_job.html")

# --- View Statistics ---
@app.route("/recruiter/view_statistics/<int:job_id>")
def view_statistics(job_id):
    if "recruiter_id" not in session:
        return redirect("/recruiter/login")
    db = get_db()
    applicants = db.execute("SELECT * FROM applications JOIN users ON applications.user_id = users.id WHERE job_id = ?", 
                            (job_id,)).fetchall()
    return render_template("view_statistics.html", applicants=applicants)

 # --- View Applicant ---
@app.route("/recruiter/view_applicant/<int:application_id>", methods=["GET", "POST"])
def view_applicant(application_id):
    if "recruiter_id" not in session:
        return redirect("/recruiter/login")
    
    db = get_db()
    
    # Fetch applicant details
    application = db.execute(
        "SELECT applications.id AS app_id, users.resume, applications.status FROM applications "
        "JOIN users ON applications.user_id = users.id WHERE applications.id = ?",
        (application_id,)
    ).fetchone()
    
    if not application:
        return "Application not found", 404
    
    if request.method == "POST":
        action = request.form.get("action")
        if action in ["Accept", "Reject"]:
            db.execute("UPDATE applications SET status = ? WHERE id = ?", (action, application_id))
            db.commit()
            return redirect("/recruiter/dashboard")

    return render_template("view_applicant.html", resume=application["resume"])


if __name__ == "__main__":
    app.run(debug=True)
