import requests
from bs4 import BeautifulSoup

all_jobs = []


def extract_berlin_jobs(keyword):
    url = f"https://berlinstartupjobs.com/skill-areas/{keyword}"
    response = requests.get(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find_all("div", class_="bjs-jlid__wrapper")
    # csv파일 추출시 불필요한 컬럼이 나뉨을 방지코자 replace(",", "/") 활용
    for job in jobs:
        position = job.find("h4", class_="bjs-jlid__h").find("a").text.replace(
            ",", "/")

        company = job.find("a", class_="bjs-jlid__b").text

        location = "Berlin / Germany"

        tags = job.find("div", class_="links-box").find_all("a")
        tag_container = " | ".join([tag.text.strip() for tag in tags])

        link = job.find("h4", class_="bjs-jlid__h").find("a")["href"]

        job_data = {
            "position": position,
            "company": company,
            "location": location,
            "keywords": tag_container,
            "link": link
        }
        all_jobs.append(job_data)

    return all_jobs
