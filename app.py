#!/usr/bin/env python3
"""
Main application controller for SimpliDOTS Release Notes Bot
Clean entry point that coordinates all services
"""

from data_manager import SimpliDOTSDataManager
from ai_analyzer import SimpliDOTSAIAnalyzer
from scraping_service import SimpliDOTSScrapingService
from interactive_qa import InteractiveQAService

class SimpliDOTSApp:
    def __init__(self):
        self.data_manager = SimpliDOTSDataManager()
        self.ai_analyzer = SimpliDOTSAIAnalyzer()
        self.scraping_service = SimpliDOTSScrapingService()
        self.qa_service = InteractiveQAService()
        self._cached_notes = None
    
    def get_or_scrape_notes(self, force_scrape: bool = False):
        """Get notes from cache or scrape fresh data"""
        if not force_scrape and self._cached_notes:
            return self._cached_notes
        
        if not force_scrape:
            notes = self.data_manager.load_notes()
            if notes:
                self._cached_notes = notes
                return notes
        
        # Scrape fresh data
        print("🚀 No cached data found or force scraping requested...")
        notes = self.scraping_service.scrape_and_save(self.data_manager)
        if notes:
            self._cached_notes = notes
        return notes
    
    def scrape_only(self):
        """Scrape notes without analysis"""
        print("🕷️ SCRAPING SIMPLIDOTS RELEASE NOTES")
        print("=" * 60)
        
        notes = self.scraping_service.scrape_and_save(self.data_manager)
        if notes:
            self._cached_notes = notes
            print(f"\n✅ Scraping completed successfully!")
            print(f"📊 {len(notes)} release notes are now available for analysis")
        else:
            print("❌ Scraping failed. Please check your internet connection.")
        
        return notes
    
    def analyze_notes(self, max_notes: int = 20):
        """Complete analysis of release notes"""
        print("🤖 SIMPLIDOTS ANALYSIS MODE")
        print("=" * 60)
        
        notes = self.get_or_scrape_notes()
        if not notes:
            print("❌ No notes available for analysis")
            print("💡 Try option 2 to scrape fresh data first")
            return
        
        self.ai_analyzer.perform_full_analysis(notes, max_notes)
        
        print(f"\n🎉 Analysis complete!")
        print(f"📊 Analyzed {min(max_notes, len(notes))} of {len(notes)} available notes")
    
    def interactive_qa(self):
        """Start interactive Q&A session"""
        print("💬 INTERACTIVE Q&A MODE")
        print("=" * 60)
        
        notes = self.get_or_scrape_notes()
        if not notes:
            print("❌ No notes available for Q&A")
            print("💡 Try option 2 to scrape fresh data first")
            return
        
        self.qa_service.start_qa_session(notes)
    
    def show_data_summary(self):
        """Show summary of available data"""
        print("📊 DATA SUMMARY")
        print("=" * 60)
        
        notes = self.data_manager.load_notes()
        if notes:
            self.data_manager.show_notes_summary(notes)
        else:
            print("📭 No cached data found")
            print("💡 Use option 2 to scrape fresh data")
    
    def quick_demo(self):
        """Run a quick demo of the system"""
        print("🎬 QUICK DEMO MODE")
        print("=" * 60)
        
        notes = self.get_or_scrape_notes()
        if not notes:
            print("❌ No notes available for demo")
            return
        
        print("Running a quick demonstration of SimpliDOTS analysis...")
        self.qa_service.quick_demo(notes)

def main():
    """Main entry point with interactive menu"""
    app = SimpliDOTSApp()
    
    while True:
        print(f"\n🎯 SIMPLIDOTS RELEASE NOTES ANALYZER")
        print("=" * 60)
        print("1. 🤖 Analyze notes (load cached or scrape if needed)")
        print("2. 🕷️  Scrape fresh notes and analyze")
        print("3. 💬 Interactive Q&A mode")
        print("4. 📊 Show data summary")
        print("5. 🕷️  Scrape fresh notes only (no analysis)")
        print("6. 🎬 Quick demo")
        print("7. 🚪 Exit")
        print("-" * 60)
        
        try:
            choice = input("Choose an option (1-7): ").strip()
            
            if choice == '1':
                app.analyze_notes()
                
            elif choice == '2':
                notes = app.scrape_only()
                if notes:
                    print(f"\n🤖 Starting analysis of freshly scraped data...")
                    app.analyze_notes()
                    
            elif choice == '3':
                app.interactive_qa()
                
            elif choice == '4':
                app.show_data_summary()
                
            elif choice == '5':
                app.scrape_only()
                
            elif choice == '6':
                app.quick_demo()
                
            elif choice == '7':
                print("👋 Thank you for using SimpliDOTS Analyzer! Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please choose 1-7.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
