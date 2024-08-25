import requests
from bs4 import BeautifulSoup

all_jobs = []


def extract_web3_jobs(keyword):
    page_number = 0
    url = f"https://web3.career/{keyword}-jobs"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 페이지를 넘겨가며 데이터를 추출하다 ("li", class_="page-item next disabled") 발견시 루프 탈출
    while True:
        page_number += 1
        response = requests.get(f"{url}?page={page_number}", headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # 광고에만 id가 있어 id가 있는 tr을 제외하고 추출
        jobs = soup.find_all("tr", class_="table_row", id=None)

        # 추출한 데이터 앞/뒤 공백 제거, csv파일 추출시 불필요한 컬럼 나뉨 방지...뭔가 코드가 지저분해졌는데 더 좋은 방법이 있지 싶음
        for job in jobs:
            position = job.find("div", class_="job-title-mobile").find(
                class_="my-primary").text.strip()

            company = job.find_all("td", class_="job-location-mobile")[0].find(
                "h3").text.strip().replace(",", "")

            location_segmented = job.find_all(
                "td", class_="job-location-mobile")[1].children
            location = " / ".join([
                segment.text.replace(",", "").strip()
                for segment in location_segmented
            ])

            tags = job.find_all("span", class_="my-badge")
            tag_container = " | ".join([tag.text.strip() for tag in tags])

            link = job.find_all(
                "td", class_="job-location-mobile")[0].find("a")["href"]

            job_data = {
                "position": position,
                "company": company,
                "location": location[3:-3].replace(" /  /  / ", " / "),
                "keywords": tag_container,
                "link": f"https://web3.career{link}"
            }

            all_jobs.append(job_data)

        if soup.find("li", class_="page-item next disabled"):
            return all_jobs
