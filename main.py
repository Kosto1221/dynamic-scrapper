from extractors.berlin import extarct_berlin_jobs
from extractors.web3 import extract_web3_jobs

keyword = input("What do you want to search for?")

berlin = extarct_berlin_jobs(keyword)
web3 = extract_web3_jobs(keyword)
jobs = berlin + web3

file = open(f"{keyword}.csv", "w")
file.write("Position, Company, Location, Stacks\n")

for job in jobs:
    file.write(
        f"{job['position']}, {job['company']}, {job['location']}, {job['stacks']}\n"
    )

file.close()