import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_jobs(url):
    jobs = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            job_elements = soup.find_all('div', class_='job_seen_beacon')
            for job in job_elements:
                title = job.find('h2').text.strip()
                company = job.find('span', class_='companyName').text.strip()
                location = job.find('div', class_='companyLocation').text.strip()
                jobs.append({'title': title, 'company': company, 'location': location})
            
            next_page = soup.find('a', {'aria-label': 'Next'})
            url = 'https://www.indeed.com' + next_page['href'] if next_page else None
        else:
            print("Failed to retrieve the page")
            break
    return jobs

jobs = get_jobs('https://www.indeed.com/jobs?q=software+developer')
df = pd.DataFrame(jobs)
df.to_csv('job_listings.csv', index=False)
