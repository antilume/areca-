import requests
from bs4 import BeautifulSoup
import cloudscraper
import random
import time
from datetime import datetime
from app.models.models import SourceType
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

class BaseScraper:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )
        self.fake_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]

    def random_delay(self, min_s=2, max_s=5):
        time.sleep(random.uniform(min_s, max_s))

    def get_ua(self):
        return random.choice(self.fake_agents)

class EntrackrScraper(BaseScraper):
    """Scrapes Entrackr for funding and leadership signals."""

    def scrape_funding(self):
        url = "https://entrackr.com/category/funding/"
        try:
            response = self.scraper.get(url, headers={"User-Agent": self.get_ua()})
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            results = []
            for article in articles:
                title_tag = article.find('h3')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag.find('a')['href']
                    results.append({
                        "title": title,
                        "url": link,
                        "source": "entrackr",
                        "type": SourceType.FUNDING,
                        "timestamp": datetime.now().isoformat()
                    })
            return results
        except Exception as e:
            print(f"Error scraping Entrackr funding: {e}")
            return []

    def scrape_leadership(self):
        url = "https://entrackr.com/category/leadership-hiring/"
        try:
            response = self.scraper.get(url, headers={"User-Agent": self.get_ua()})
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            results = []
            for article in articles:
                title_tag = article.find('h3')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag.find('a')['href']
                    results.append({
                        "title": title,
                        "url": link,
                        "source": "entrackr",
                        "type": SourceType.LEADERSHIP_CHANGE,
                        "timestamp": datetime.now().isoformat()
                    })
            return results
        except Exception as e:
            print(f"Error scraping Entrackr leadership: {e}")
            return []

class WellfoundScraper(BaseScraper):
    """Scrapes Wellfound for job openings using Playwright Stealth."""

    def scrape_jobs(self):
        url = "https://wellfound.com/jobs"
        results = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=self.get_ua(),
                    viewport={"width": 1280, "height": 800}
                )
                page = context.new_page()
                stealth_sync(page)

                page.goto(url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(5000)

                # Scroll to load more
                for _ in range(2):
                    page.evaluate("window.scrollBy(0, window.innerHeight)")
                    page.wait_for_timeout(2000)

                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')

                for tag in soup.find_all('a', href=lambda h: h and '/jobs/' in h):
                    title = tag.get_text(strip=True)
                    if len(title) > 5:
                        results.append({
                            "title": title,
                            "url": "https://wellfound.com" + tag['href'],
                            "source": "wellfound",
                            "type": SourceType.STARTUP_JOB_POST,
                            "company": "See post",
                            "timestamp": datetime.now().isoformat()
                        })
                browser.close()
            return results
        except Exception as e:
            print(f"Error scraping Wellfound with Playwright: {e}")
            return []

class InternshalaScraper(BaseScraper):
    """Scrapes Internshala using Playwright Stealth."""

    def scrape_internships(self):
        url = "https://internshala.com/internships/"
        results = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=self.get_ua(),
                    viewport={"width": 1366, "height": 768}
                )
                page = context.new_page()
                stealth_sync(page)

                page.goto(url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(4000)

                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')

                for card in soup.find_all('div', class_='individual_internship'):
                    title_tag = (card.find('h3') or card.find('a', class_='job-title') or card.find('h4'))
                    company_tag = card.find('p', class_='company-name') or card.find('a', class_='link_display_like_text')
                    link_tag = card.find('a', href=True)

                    if title_tag:
                        href = link_tag['href'] if link_tag else ''
                        full_url = "https://internshala.com" + href if href.startswith('/') else href
                        results.append({
                            "title": title_tag.get_text(strip=True),
                            "company": company_tag.get_text(strip=True) if company_tag else 'Unknown Startup',
                            "url": full_url,
                            "source": "internshala",
                            "type": SourceType.STARTUP_JOB_POST,
                            "location": "India/Remote",
                            "timestamp": datetime.now().isoformat()
                        })
                browser.close()
            return results
        except Exception as e:
            print(f"Error scraping Internshala with Playwright: {e}")
            return []
