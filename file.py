def save_to_file(file_name, jobs):
  file = open(f"{file_name}.csv", "w")
  file.write("Position, Company, Location, Keywords\n")

  for job in jobs:
    file.write(
        f"{job['position']}, {job['company']}, {job['location']}, {job['keywords']}, {job['link']}\n"
    )

  file.close()
