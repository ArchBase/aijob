from flask import Flask, render_template, request, redirect, session
import sqlite3
from ollama_ai import get_best_job_based_on_preference_and_resume

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

    applied_jobs = db.execute("""
        SELECT applications.job_id, applications.status, jobs.title 
        FROM applications 
        JOIN jobs ON applications.job_id = jobs.id 
        WHERE applications.user_id = ?
    """, (session["user_id"],)).fetchall()

    return render_template("user_dashboard.html", user=user, applied_jobs=applied_jobs)

def tournament_ranking(jobs, user_preferences, user_resume, mode="both"):
    ranking = []

    while jobs:
        current_round = jobs[:]
        while len(current_round) > 1:
            next_round = []
            for i in range(0, len(current_round), 2):
                if i + 1 < len(current_round):
                    winner_index = get_best_job_based_on_preference_and_resume(
                        current_round[i], current_round[i + 1], user_preferences, user_resume, mode
                    )
                    winner = current_round[i] if winner_index == 1 else current_round[i + 1]
                    loser = current_round[i] if winner_index == 2 else current_round[i + 1]
                    next_round.append(winner)
                else:
                    next_round.append(current_round[i])
            current_round = next_round

        best_job = current_round[0]
        ranking.append(best_job)
        jobs.remove(best_job)

    return ranking


@app.route("/user/find_jobs")
def find_jobs():
    if "user_id" not in session:
        return redirect("/user/login")

    db = get_db()
    jobs = db.execute("SELECT * FROM jobs").fetchall()
    user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()

    if not jobs:
        return render_template("find_jobs.html", jobs=[], jobs_pref=[], jobs_resume=[], jobs_both=[])

    # Generate rankings based on different criteria
    ranked_by_preferences = tournament_ranking(jobs[:], user["preferences"], user["resume"], mode="preferences")
    ranked_by_resume = tournament_ranking(jobs[:], user["preferences"], user["resume"], mode="resume")
    ranked_by_both = tournament_ranking(jobs[:], user["preferences"], user["resume"], mode="both")

    return render_template("find_jobs.html", 
                           jobs_pref=ranked_by_preferences, 
                           jobs_resume=ranked_by_resume, 
                           jobs_both=ranked_by_both)


@app.route("/user/apply/<int:job_id>")
def apply_job(job_id):
    if "user_id" not in session:
        return redirect("/user/login")
    
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    job = db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    
    match_score = 0
    
    db.execute("INSERT INTO applications (user_id, job_id, status, match_score) VALUES (?, ?, ?, ?)", 
               (session["user_id"], job_id, "Pending", match_score))
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
    jobs = db.execute("""
        SELECT id, title FROM jobs WHERE recruiter_id = ?
    """, (session["recruiter_id"],)).fetchall()

    return render_template("recruiter_dashboard.html", jobs=jobs)

# --- Create Job ---
@app.route("/recruiter/create_job", methods=["GET", "POST"])
def create_job():
    if "recruiter_id" not in session:
        return redirect("/recruiter/login")
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        db = get_db()
        db.execute("INSERT INTO jobs (recruiter_id, title, description) VALUES (?, ?, ?)", 
                   (session["recruiter_id"], title, description))
        db.commit()
        return redirect("/recruiter/dashboard")
    return render_template("create_job.html")


# --- View Statistics ---
# --- View Statistics ---
@app.route("/recruiter/view_statistics/<int:job_id>")
def view_statistics(job_id):
    if "recruiter_id" not in session:
        return redirect("/recruiter/login")
    
    db = get_db()
    applications = db.execute(
        "SELECT * FROM applications JOIN users ON applications.user_id = users.id "
        "WHERE job_id = ? ORDER BY match_score DESC",  # Sorting by match_score in descending order
        (job_id,)
    ).fetchall()
    
    return render_template("view_statistics.html", applications=applications)


 # --- View Applicant ---
@app.route("/recruiter/view_application/<int:application_id>", methods=["GET", "POST"])
def view_applicant(application_id):
    if "recruiter_id" not in session:
        return redirect("/recruiter/login")
    
    db = get_db()
    
    application = db.execute(
        "SELECT applications.id AS app_id, users.resume, applications.status, jobs.title "
        "FROM applications "
        "JOIN users ON applications.user_id = users.id "
        "JOIN jobs ON applications.job_id = jobs.id "
        "WHERE applications.id = ?",
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

    return render_template("view_application.html", resume=application["resume"], title=application["title"])


@app.route("/user/update_preferences", methods=["POST"])
def update_preferences():
    if "user_id" not in session:
        return redirect("/user/login")
    
    preferences = request.form["preferences"]
    db = get_db()
    db.execute("UPDATE users SET preferences = ? WHERE id = ?", (preferences, session["user_id"]))
    db.commit()
    
    return redirect("/user/dashboard")

@app.route("/user/update_resume", methods=["POST"])
def update_resume():
    if "user_id" not in session:
        return redirect("/user/login")

    new_resume = request.form["resume"]
    db = get_db()
    db.execute("UPDATE users SET resume = ? WHERE id = ?", (new_resume, session["user_id"]))
    db.commit()

    return redirect("/user/dashboard")

@app.route("/user/apply_now/<int:job_id>")
def apply_now(job_id):
    if "user_id" not in session:
        return redirect("/user/login")
    
    db = get_db()
    job = db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()

    return render_template("apply_now.html", job=job)



if __name__ == "__main__":
    app.run(debug=True)
