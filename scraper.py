import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_anapec(keyword=None, region=None, sector=None, contract_type=None, limit=50):
    """
    Scrapes job listings from ANAPEC.
    Note: The specific URL and form data parameters might need to be adjusted
    based on the current live structure of ANAPEC's search portal.
    """
    # Use the tout:all endpoint to get the listings
    base_url = "http://www.anapec.org/sigec-app-rv/fr/chercheurs/resultat_recherche/tout:all"
    
    params = {}
    if keyword:
        params['mot_cle'] = keyword
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        response.encoding = 'utf-8'
    except requests.RequestException as e:
        print(f"Error fetching from ANAPEC: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    jobs = []
    
    tables = soup.find_all('table')
    if len(tables) >= 2:
        job_table = tables[1]
        job_elements = job_table.find_all('tr')
        
        # Skip header row or empty rows
        for element in job_elements:
            tds = element.find_all('td')
            if len(tds) < 7:
                continue
                
            title = tds[3].text.strip()
            company = tds[5].text.strip()
            if not company or company == "-":
                company = "Confidential"
                
            location = tds[6].text.strip()
            posted_date = tds[2].text.strip()
            
            job = {
                "title": title,
                "company": company,
                "location": location,
                "contract_type": "Not specified",
                "experience": "Not specified",
                "sector": "Not specified",
                "posted_date": posted_date,
                "url": base_url
            }
            
            # Apply filters in Python if the site doesn't support them via query params
            if keyword and keyword.lower() not in title.lower():
                continue
            if region and region.lower() not in location.lower():
                continue
                
            jobs.append(job)
            
            if len(jobs) >= limit:
                break
                
    return jobs

if __name__ == "__main__":
    # Test the scraper
    print(scrape_anapec(limit=2))
