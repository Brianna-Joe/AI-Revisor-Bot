#!/usr/bin/env python3
"""
Enhanced SimpliDOTS Release Notes Scraper
Specifically designed for fitur-sap.simplidots.id GitBook structure
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
from urllib.parse import urljoin
import time

class SimpliDOTSGitBookScraper:
    def __init__(self):
        self.base_url = "https://fitur-sap.simplidots.id/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.release_notes = []

    def fetch_page(self, url):
        """Fetch a webpage with error handling"""
        try:
            print(f"🌐 Fetching: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            return None

    def extract_feature_links_from_year_page(self, soup, year):
        """Extract individual feature links from year page"""
        feature_links = []
        
        # Look for links that contain feature descriptions
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text().strip()
            
            # Filter for feature update links
            if (href and text and 
                ('fitur' in text.lower() or 'penambahan' in text.lower() or 
                 'pembaharuan' in text.lower() or 'updates' in text.lower() or
                 '🚀' in text or '🔥' in text)):
                
                # Extract date from the text
                date_match = re.search(r'(\d{1,2}\s+\w+\s+\d{4}|\w+\s+\d{4}|\d{1,2}\s+\w{3}\s+\d{4})', text)
                date_str = date_match.group(1) if date_match else f"01 Jan {year}"
                
                full_url = urljoin(self.base_url, href)
                
                feature_links.append({
                    'title': self.clean_title(text),
                    'url': full_url,
                    'date_str': date_str,
                    'year': year
                })
        
        return feature_links

    def clean_title(self, title):
        """Clean the title text"""
        # Remove emojis and clean up
        title = re.sub(r'[🚀🔥]', '', title)
        title = re.sub(r'\s*-\s*\[.*?\]', '', title)  # Remove date brackets
        title = title.strip()
        return title[:100]  # Limit length

    def extract_content_from_feature_page(self, soup):
        """Extract main content from individual feature page - Enhanced to get full content"""
        content_parts = []
        
        # Look for main content areas with better selectors
        content_selectors = [
            'div[data-lexical-editor="true"]',  # GitBook content
            '.content-body',
            'article',
            '.page-content', 
            'main',
            '.markdown-body',
            '[role="main"]',
            '.gitbook-content'
        ]
        
        for selector in content_selectors:
            content_area = soup.select_one(selector)
            if content_area:
                # Extract text, clean it up
                text = content_area.get_text()
                # Remove excessive whitespace but preserve structure
                text = re.sub(r'\n\s*\n', '\n\n', text)  # Keep paragraph breaks
                text = re.sub(r'[ \t]+', ' ', text)  # Clean horizontal whitespace
                # Remove common GitBook elements
                text = re.sub(r'(Was this helpful\?|Table of contents|Copy|Ctrl|⌘K|Last updated.*ago)', '', text)
                # Remove cookie notices
                text = re.sub(r'This site uses cookies.*?AcceptReject', '', text, flags=re.DOTALL)
                content_parts.append(text.strip())
                break
        
        # If no specific content area found, try alternative approach
        if not content_parts:
            # Look for headings and paragraphs
            main_content = []
            
            # Get all headings and content
            for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'div', 'li', 'ul', 'ol']):
                text = element.get_text().strip()
                if (len(text) > 15 and 
                    'cookie' not in text.lower() and 
                    'was this helpful' not in text.lower() and
                    'table of contents' not in text.lower()):
                    main_content.append(text)
            
            content_parts = main_content
        
        # Combine and return full content (increased limit significantly)
        full_content = '\n'.join(content_parts)
        
        # Clean up the final content
        full_content = re.sub(r'\n{3,}', '\n\n', full_content)  # Max 2 consecutive newlines
        full_content = full_content.strip()
        
        # Return full content with much higher limit (increased from 3000 to 10000 chars)
        return full_content[:10000] if full_content else "Feature update details"

    def parse_date(self, date_str, year):
        """Parse various date formats to standard format"""
        try:
            # Common Indonesian month abbreviations
            month_map = {
                'jan': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'apr': 'Apr',
                'mei': 'May', 'jun': 'Jun', 'jul': 'Jul', 'agu': 'Aug',
                'sep': 'Sep', 'okt': 'Oct', 'nov': 'Nov', 'des': 'Dec',
                'january': 'Jan', 'february': 'Feb', 'march': 'Mar', 'april': 'Apr',
                'may': 'May', 'june': 'Jun', 'july': 'Jul', 'august': 'Aug',
                'september': 'Sep', 'october': 'Oct', 'november': 'Nov', 'december': 'Dec',
                'maret': 'Mar', 'juni': 'Jun', 'juli': 'Jul', 'agustus': 'Aug',
                'september': 'Sep', 'oktober': 'Oct', 'november': 'Nov', 'desember': 'Dec'
            }
            
            # Replace Indonesian months
            date_lower = date_str.lower()
            for indo_month, eng_month in month_map.items():
                date_lower = date_lower.replace(indo_month, eng_month)
            
            # Try parsing different formats
            formats = ['%d %b %Y', '%b %Y', '%d %B %Y', '%B %Y']
            
            for fmt in formats:
                try:
                    if '%Y' not in fmt:
                        date_lower += f' {year}'
                        fmt += ' %Y'
                    dt = datetime.strptime(date_lower.title(), fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            # If all fails, use year and try to extract month/day
            numbers = re.findall(r'\d+', date_str)
            if len(numbers) >= 2:
                day = numbers[0].zfill(2)
                month = numbers[1].zfill(2)
                return f"{year}-{month}-{day}"
            elif len(numbers) == 1:
                return f"{year}-01-{numbers[0].zfill(2)}"
            
        except Exception as e:
            print(f"⚠️ Date parsing error for '{date_str}': {e}")
        
        return f"{year}-01-01"

    def scrape_year_features(self, year, detailed_content=False):
        """Scrape features for a specific year"""
        year_url = f"{self.base_url}smh/fitur-pada-smh-sales-management-hub/{year}"
        year_soup = self.fetch_page(year_url)
        
        if not year_soup:
            return []
        
        # Extract feature links from the year page
        feature_links = self.extract_feature_links_from_year_page(year_soup, year)
        print(f"📋 Found {len(feature_links)} feature links for {year}")
        
        year_notes = []
        
        # Visit each feature page
        limit = 25 if not detailed_content else 20  # More pages for comprehensive extraction
        for i, link in enumerate(feature_links[:limit], 1):
            print(f"   📄 {i}/{min(limit, len(feature_links))}: {link['title'][:50]}...")
            
            feature_soup = self.fetch_page(link['url'])
            if feature_soup:
                if detailed_content:
                    content = self.extract_detailed_content(feature_soup)
                else:
                    content = self.extract_content_from_feature_page(feature_soup)
                
                note = {
                    'date': self.parse_date(link['date_str'], year),
                    'title': link['title'],
                    'content': content,
                    'source_url': link['url']
                }
                
                year_notes.append(note)
                time.sleep(1)  # Be respectful to the server
            
        return year_notes

    def extract_detailed_content(self, soup):
        """Extract very detailed content including steps, notes, and structured information"""
        content_sections = []
        
        # First try to get the main content
        main_content = self.extract_content_from_feature_page(soup)
        if main_content and main_content != "Feature update details":
            return main_content  # If we got good content, return it as is
        
        # If main content extraction failed, try a more aggressive approach
        # Remove unwanted elements first
        for unwanted in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
            unwanted.decompose()
        
        # Look for structured content
        content_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'li', 'strong', 'b'])
        
        current_section = []
        for element in content_elements:
            text = element.get_text().strip()
            
            # Skip if too short or contains unwanted content
            if (len(text) < 10 or 
                any(skip in text.lower() for skip in ['cookie', 'was this helpful', 'last updated', 'copy', 'ctrl'])):
                continue
            
            # If it's a heading, start new section
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                if current_section:
                    content_sections.append('\n'.join(current_section))
                current_section = [f"\n## {text}"]
            else:
                current_section.append(text)
        
        # Add the last section
        if current_section:
            content_sections.append('\n'.join(current_section))
        
        # Combine all sections
        full_detailed_content = '\n\n'.join(content_sections)
        
        # Clean up
        full_detailed_content = re.sub(r'\n{3,}', '\n\n', full_detailed_content)
        full_detailed_content = full_detailed_content.strip()
        
        # Return up to 15000 characters for detailed content (increased from 5000)
        return full_detailed_content[:15000] if full_detailed_content else "Feature update details"

    def scrape_all_years(self, detailed_content=False):
        """Scrape release notes from all available years"""
        content_type = "detailed" if detailed_content else "standard"
        print(f"🚀 Starting SimpliDOTS GitBook scraping ({content_type} content)...")
        
        years = ['2024', '2023', '2025']  # Available years
        all_notes = []
        
        for year in years:
            print(f"\n📅 Scraping {year} features...")
            year_notes = self.scrape_year_features(year, detailed_content)
            all_notes.extend(year_notes)
            print(f"✅ Extracted {len(year_notes)} notes from {year}")
        
        # Sort by date (newest first)
        all_notes.sort(key=lambda x: x['date'], reverse=True)
        
        print(f"\n🎉 Total release notes extracted: {len(all_notes)}")
        return all_notes

    def save_to_json(self, notes, filename="simplidots_release_notes.json"):
        """Save release notes to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(notes, f, indent=2, ensure_ascii=False)
            print(f"💾 Release notes saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")

    def display_preview(self, notes, count=5):
        """Display a preview of scraped notes"""
        if not notes:
            print("📭 No release notes found")
            return
        
        print(f"\n📊 PREVIEW OF RELEASE NOTES (showing {min(count, len(notes))} of {len(notes)})")
        print("=" * 80)
        
        for i, note in enumerate(notes[:count], 1):
            print(f"{i}. [{note['date']}] {note['title']}")
            print(f"   {note['content'][:150]}...")
            print(f"   Source: {note['source_url']}")
            print()

def main():
    """Main function"""
    scraper = SimpliDOTSGitBookScraper()
    
    # Scrape all years
    notes = scraper.scrape_all_years()
    
    if notes:
        # Save to JSON
        scraper.save_to_json(notes)
        
        # Display preview
        scraper.display_preview(notes)
        
        print(f"\n🤖 Release notes ready for bot analysis!")
        return notes
    else:
        print("❌ No release notes could be extracted")
        return []

if __name__ == "__main__":
    main()
