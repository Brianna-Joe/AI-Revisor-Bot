#!/usr/bin/env python3
"""
Scraping service for SimpliDOTS release notes
Wrapper around the enhanced scraper for clean API
"""

from typing import List, Dict, Optional
from enhanced_scraper import SimpliDOTSGitBookScraper

class SimpliDOTSScrapingService:
    def __init__(self):
        self.scraper = SimpliDOTSGitBookScraper()
    
    def scrape_all_notes(self, detailed_content: bool = True) -> Optional[List[Dict]]:
        """Scrape all available release notes with detailed content"""
        print("🕷️ Scraping SimpliDOTS release notes...")
        print("📋 This may take a few minutes to get detailed content...")
        print("-" * 60)
        
        try:
            notes = self.scraper.scrape_all_years(detailed_content=detailed_content)
            if notes:
                total_chars = sum(len(note['content']) for note in notes)
                avg_chars = total_chars / len(notes)
                
                print(f"\n✅ Successfully scraped {len(notes)} release notes!")
                print(f"📊 Total content: {total_chars:,} characters")
                print(f"📏 Average length: {avg_chars:.0f} characters per note")
                
                # Show sample of what was scraped
                if notes:
                    sample_note = notes[0]
                    print(f"\n📄 Sample: {sample_note['title']}")
                    print(f"📅 Date: {sample_note['date']}")
                    print(f"📝 Content length: {len(sample_note['content'])} chars")
                    print(f"🔗 URL: {sample_note['source_url']}")
                
            return notes
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            return None
    
    def scrape_specific_year(self, year: str, detailed_content: bool = True) -> Optional[List[Dict]]:
        """Scrape notes from a specific year"""
        print(f"🕷️ Scraping {year} release notes...")
        
        try:
            notes = self.scraper.scrape_year_features(year, detailed_content=detailed_content)
            if notes:
                print(f"✅ Successfully scraped {len(notes)} notes from {year}")
            return notes
        except Exception as e:
            print(f"❌ Error scraping year {year}: {e}")
            return None
    
    def scrape_and_save(self, data_manager, detailed_content: bool = True) -> Optional[List[Dict]]:
        """Scrape notes and automatically save them"""
        notes = self.scrape_all_notes(detailed_content)
        if notes:
            success = data_manager.save_notes(notes)
            if success:
                print("💾 Notes successfully saved for future use!")
            else:
                print("⚠️ Notes scraped but failed to save")
        return notes
