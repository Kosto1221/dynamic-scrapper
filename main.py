from flask import Flask, render_template, request
from extractors.berlin import extarct_berlin_jobs
from extractors.web3 import extract_web3_jobs

app = Flask("JobScrapper")

@app.route("/")
def home():
    return render_template("home.html", name="nico")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    berlin = extarct_berlin_jobs(keyword)
    web3 = extract_web3_jobs(keyword)
    jobs = berlin + web3
    return render_template("search.html", keyword=keyword, jobs=jobs)

app.run("0.0.0.0")

