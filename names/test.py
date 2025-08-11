import requests
from bs4 import BeautifulSoup
import re
import csv
import time

API_KEY = "#########################"
CSE_ID = "Dummy"

company_names = [
  "GIFTED CHILD CARE, LLC",
  "BEYOND BARREL ART, LLC",
  "AAA BACKFLOW PREVENTION, INC.",
  "JMDL PERFORMANCE LLC",
  "ORION AWAKENING TIME, INC.",
  "HMHU MARKETING & ADVERTISING, LLC",
  "SPIN CITY LAUNDROMAT",
  "COSTA LAKE INSTALLATIONS, INC.",
  "COLMELATI ICE CREAM, INC.",
  "LIARA HOSPICE, INC.",
  "JOEYRAE",
  "RM WEBER PAINTING, LLC",
  "CENTREX PEST CONTROL SERVICES, INC.",
  "ELITE COLLISION CENTER",
  "SWEET GARLIC COMPANY, LLC",
  "TRC TRANSMISSIONS, LLC",
  "BAY AREA RESIDENTIAL CONSTRUCTION, INC.",
  "OVER THE TOP, INC.",
  "SAHARA, LLC",
  "TINTWORKS, INC.",
  "CRAFTMAN PLUMBING INC",
  "TRUSTED HOME CONTRACTORS, INC.",
  "CONCRETE CHEMICALS OF CALIFORNIA, INC.",
  "THE BASKET TACO",
  "TOP SCORE ENTERPRISES, INC.",
  "RUBIDOUX TIRE AND BRAKE, INC.",
  "CONTOUR MEDICAL SPA, INC.",
  "TAKASHIMA INTEGRATIVE HEALTH, INC.",
  "VENETIANGLASSART.COM",
  "MOON TIRES & AUTO SERVICES",
  "SKY RISE, INC.",
  "HEALTH FOR ALL IN HOME CARE SERVICES, INC.",
  "OZZY'S APIZZA, LLC",
  "THE REEL ELECTRIC COMPANY",
  "PERVANA, INC.",
  "DWELLPOINT",
  "FOUR ACE ELECTRICAL SERVICES, INC.",
  "FOUR ACE ELECTRICAL SERVICES, INC.",
  "LAVIEDOVE, LLC",
  "AFFORDABLE BUILDING SOLUTIONS, INC.",
  "ENACT SYSTEMS, INC.",
  "PROPRIOCEPTIVE SOLUTIONS: A MOVEMENT HOSPITAL & HUMAN PERFORMANCE INSTITUTE",
  "PORKY'S PIZZA MV, LLC",
  "INSIDELINES GRAPHIX INC",
  "ASTERA.AI, INC.",
  "SLS DESIGN, LLC",
  "STRIVE SOBER LIVING, LLC",
  "BEADSATBEADS, INC.",
  "VICTORVILLE COUNSELING",
  "GSM FLOORING, INC.",
  "AFFORDABLE TREE EXPERTS, INC.",
  "BLIKIAN CHIROPRACTIC AND ACUPUNCTURE, INC.",
  "MAREENI T. STANISLAUS, M.D., A MEDICAL, INC.",
  "JENKINS ROOM & BOARD, LLC",
  "MI CASITA VENEZUELAN CUISINE, LLC",
  "KELTIC AVIATION, INC.",
  "COMPREHENSIVE HEALTH CARE SERVICES, LLC",
  "VALHALLA INDOOR AXE THROWING, LLC",
  "WJ WELLNESS GROUP, LLC",
  "BEATRIX PRESENTS, LLC.",
  "MARKETING MAVEN PUBLIC RELATIONS, INC."



    # Add more company names here
]

def extract_email_phone(text):
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    email = email_match.group() if email_match else ""
    phone = phone_match.group() if phone_match else ""
    return email, phone

def get_page_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return ""

def search_company(company):
    query = f"{company} contact OR email OR phone"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": 3
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        for item in data.get("items", []):
            link = item.get("link")
            if link:
                print(f"🔎 Searching: {link}")
                page_text = get_page_text(link)
                email, phone = extract_email_phone(page_text)
                if email or phone:
                    return email, phone
        return "", ""
    except Exception as e:
        print(f"❌ Search failed for {company}: {e}")
        return "", ""

# Run for all companies
results = []
for company in company_names:
    print(f"\n▶ Searching for: {company}")
    email, phone = search_company(company)
    results.append({
        "Company": company,
        "Email": email,
        "Phone": phone
    })
    time.sleep(2)  # Avoid API rate limit

# Save to CSV
with open("contact_info_simple.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Company", "Email", "Phone"])
    writer.writeheader()
    writer.writerows(results)

print("\n✅ Done! Saved to 'contact_info_simple.csv'")

