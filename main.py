from flask import Flask, render_template, request, redirect, send_file
from extractors.berlin import extract_berlin_jobs
from extractors.web3 import extract_web3_jobs
from file import save_to_file

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        berlin = extract_berlin_jobs(keyword)
        web3 = extract_web3_jobs(keyword)
        jobs = berlin + web3
        db[keyword] = jobs
    return render_template("search.html",
                           keyword=keyword,
                           jobs=jobs,
                           length=len(jobs))

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

if __name__ == "__main__":
    app.run("0.0.0.0")
