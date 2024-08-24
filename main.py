from flask import Flask, render_template

app = Flask("JobScrapper")

@app.route("/")
def home():
    return render_template("home.html", name="nico")

@app.route("/hello")
def hello():
    return 'hello!'

app.run("0.0.0.0")

