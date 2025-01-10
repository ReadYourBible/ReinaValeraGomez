from bs4 import BeautifulSoup
import requests
import re

class SessionManager:
    """Handles HTTP sessions and requests."""
    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url

    def fetch_page(self, path):
        response = self.session.get(f"{self.base_url}{path}")
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text


class VerseExtractor:
    """Extracts verses (text only) from the HTML content."""
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")
        
    def get_text_container(self):
        """Find all divs with class 'm' which contain the verses."""
        return self.soup.find_all("div", class_="m")
    
    def extract_all_text(self, containers):
        """Extracts only the verse text (ignoring numbers) from each container."""
        verses_text = []
        for container in containers:
            verse_span = container.find("span", class_="verse")
            if verse_span:
                # The text after the verse number
                verse_text = container.get_text(strip=True)
                # Remove the verse number and any other extra parts like spaces, additional spans
                verse_text = verse_text.replace(verse_span.get_text(strip=True), '').strip()
                if verse_text:
                    verses_text.append(verse_text)
                    
        return verses_text
