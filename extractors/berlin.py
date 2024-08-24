import requests
from bs4 import BeautifulSoup

all_jobs = []

def extarct_berlin_jobs(work):
  url = f"https://berlinstartupjobs.com/skill-areas/{work}"
  response = requests.get(
      url,
      headers={
          "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      })
  soup = BeautifulSoup(response.content, "html.parser")
  jobs = soup.find_all("div", class_="bjs-jlid__wrapper")

  for job in jobs:
    position = job.find("h4", class_="bjs-jlid__h").find("a").text
    company = job.find("a", class_="bjs-jlid__b").text
    location = "Berlin, Germany"
    stacks = job.find("div", class_="links-box").find_all("a")
    stack_container = []
    for stack in stacks:
      stack_container.append(f"{stack.text}".replace("\n\t", ""))
    job_data = {
        "position": position,
        "company": company,
        "location": location,
        "stacks": stack_container
    }
    all_jobs.append(job_data)
  return all_jobs
