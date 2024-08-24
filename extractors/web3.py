from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

all_jobs = []

def extract_web3_jobs(work):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(f"https://web3.career/{work}-jobs")

        while True:
            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            jobs = soup.find_all("tr", class_="table_row", id=None)

            for job in jobs:
                position = job.find("div", class_="job-title-mobile").find(class_="my-primary").text.strip()
                company = job.find_all("td", class_="job-location-mobile")[0].find("h3").text.strip()

                location_segmented = job.find_all("td", class_="job-location-mobile")[1].children
                location = ""
                for segment in location_segmented:
                    if segment.string:
                        location += segment.string.strip()
                    else:
                        location = "Not mentioned" 

                stacks = job.find_all("span", class_="my-badge")
                stack_container = [stack.text.strip() for stack in stacks]

                job_data = {
                    "position": position,
                    "company": company,
                    "location": location,
                    "stacks": stack_container
                }
                all_jobs.append(job_data)

            next_button = soup.find("li", class_="page-item next")
            if next_button is None or "disabled" in next_button.get("class", []):
                break

            page.click("li.page-item.next a")
            time.sleep(5) 

        browser.close()
    return all_jobs

extract_web3_jobs("python")