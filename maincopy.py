from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

all_jobs = []

def extract_jobs(work):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(f"https://berlinstartupjobs.com/?s={work}")

        while True:
            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            jobs = soup.find_all("div", class_="bjs-jlid__wrapper")

            for job in jobs:
                position = job.find("h4", class_="bjs-jlid__h").find("a").text
                company = job.find("a", class_="bjs-jlid__b").text
                location = "Berlin, Germany"
                stacks = job.find("div", class_="links-box").find_all("span") if job.find("div", class_="links-box") else None
                stack_container = []
                if stacks:
                    for stack in stacks:
                        stack_container.append(f"{stack.text}".replace("\n\t", ""))
                job_data = {
                    "position": position,
                    "company": company,
                    "location": location,
                    "stacks": stack_container
                }
                all_jobs.append(job_data)

            next_page = soup.find("li", class_="ais-Pagination-item ais-Pagination-item--page ais-Pagination-item--selected").next_sibling
            print(next_page)
            if next_page is None or "ais-Pagination-item--disabled" in next_page.get("class", []):
                break

            page.click("next_page a")
            time.sleep(5)
            
        browser.close()

