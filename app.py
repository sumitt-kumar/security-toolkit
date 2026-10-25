from flask import Flask, render_template, request
import re

app = Flask(__name__)

def check_password(pw):
    score = 0
    if len(pw) >= 12:
        score += 2
    elif len(pw) >= 8:
        score += 1
    for p in [r"[a-z]", r"[A-Z]", r"\d", r"[^\w\s]"]:
        if re.search(p, pw):
            score += 1
    return "Weak" if score <= 2 else "Medium" if score <= 4 else "Strong"

def check_url(url):
    flags = []
    if len(url) > 75:
        flags.append("URL bahut lamba hai")
    if "@" in url:
        flags.append("'@' symbol hai")
    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        flags.append("IP address use hua hai")
    if not url.startswith("https"):
        flags.append("HTTPS nahi hai")
    if any(w in url.lower() for w in ["login", "verify", "bank", "update"]):
        flags.append("Suspicious words hain")
    return flags or ["Koi red flag nahi mila"]

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        if request.form.get("pw"):
            result = "Password: " + check_password(request.form["pw"])
        elif request.form.get("url"):
            result = check_url(request.form["url"])
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=False)
