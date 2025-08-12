#!/usr/bin/env python3
"""
SimpliDOTS Release Notes Bot Integration
Combines the enhanced scraper with your release notes bot
"""

import json
import os
from enhanced_scraper import SimpliDOTSGitBookScraper
from release_notes_bot import summarize_notes, ask_question

def load_simplidots_notes():
    """Load SimpliDOTS release notes from JSON file"""
    filename = 'simplidots_release_notes.json'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            notes = json.load(f)
        print(f"📂 Loaded {len(notes)} release notes from {filename}")
        return notes
    except FileNotFoundError:
        print(f"📭 No cached notes found at {filename}")
        return None
    except Exception as e:
        print(f"❌ Error loading notes: {e}")
        return None

def scrape_fresh_notes():
    """Scrape fresh release notes from SimpliDOTS"""
    print("🕷️ Scraping fresh SimpliDOTS release notes...")
    scraper = SimpliDOTSGitBookScraper()
    notes = scraper.scrape_all_years()
    return notes

def analyze_with_bot(notes, max_notes=20):
    """Analyze release notes using your bot"""
    if not notes:
        print("❌ No notes to analyze")
        return
    
    # Use recent notes for analysis
    recent_notes = notes[:max_notes]
    
    print(f"\n🤖 ANALYZING {len(recent_notes)} SIMPLIDOTS RELEASE NOTES")
    print("=" * 80)
    
    try:
        # 1. Generate comprehensive summary
        print("\n1️⃣ GENERATING SUMMARY...")
        print("-" * 50)
        summary = summarize_notes(recent_notes)
        print("📋 SUMMARY:")
        print(summary)
        
        # 2. Ask targeted questions
        print("\n2️⃣ ASKING QUESTIONS...")
        print("-" * 50)
        
        questions = [
            "What are the most recent features added to SimpliDOTS?",
            "What improvements have been made to the Sales Management Hub (SMH)?",
            "Are there any new integrations or API features?",
            "What tax-related updates (PPN) have been implemented?",
            "What warehouse and inventory management features were added?",
            "Are there any collection or payment-related features?",
            "What dashboard or interface improvements were made?"
        ]
        
        for i, question in enumerate(questions, 1):
            try:
                print(f"\n🤔 Question {i}: {question}")
                answer = ask_question(question, recent_notes)
                print(f"💡 Answer: {answer}")
                print("-" * 40)
            except Exception as e:
                print(f"❌ Error with question {i}: {e}")
                print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error during bot analysis: {e}")

def interactive_qa(notes):
    """Interactive Q&A session"""
    if not notes:
        print("❌ No notes available for Q&A")
        return
    
    print(f"\n🗣️ INTERACTIVE Q&A MODE")
    print("=" * 60)
    print(f"Ask questions about SimpliDOTS features ({len(notes)} release notes loaded)")
    print("Type 'quit' to exit")
    print("-" * 60)
    
    while True:
        try:
            question = input("\n🤔 Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not question:
                continue
                
            print("🤖 Analyzing SimpliDOTS release notes...")
            answer = ask_question(question, notes[:25])  # Use top 25 notes
            print(f"💡 Answer: {answer}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def show_notes_summary(notes):
    """Show summary of available notes"""
    if not notes:
        print("📭 No notes available")
        return
    
    print(f"\n📊 SIMPLIDOTS RELEASE NOTES SUMMARY")
    print("=" * 70)
    print(f"Total notes: {len(notes)}")
    
    # Get date range
    dates = [note['date'] for note in notes if note['date']]
    if dates:
        latest_date = max(dates)
        oldest_date = min(dates)
        print(f"Date range: {oldest_date} to {latest_date}")
    
    # Show recent features
    print(f"\n🚀 Recent Features (last 10):")
    for i, note in enumerate(notes[:10], 1):
        print(f"{i:2d}. [{note['date']}] {note['title']}")
    
    if len(notes) > 10:
        print(f"    ... and {len(notes) - 10} more features")

def main_menu():
    """Main interactive menu"""
    while True:
        print(f"\n🎯 SIMPLIDOTS RELEASE NOTES ANALYZER")
        print("=" * 60)
        print("1. Load cached notes and analyze")
        print("2. Scrape fresh notes and analyze") 
        print("3. Interactive Q&A mode")
        print("4. Show notes summary")
        print("5. Scrape fresh notes only (no analysis)")
        print("6. Exit")
        print("-" * 60)
        
        try:
            choice = input("Choose an option (1-6): ").strip()
            
            if choice == '1':
                notes = load_simplidots_notes()
                if notes:
                    analyze_with_bot(notes)
                else:
                    print("⚠️ No cached notes. Choose option 2 to scrape fresh data.")
                    
            elif choice == '2':
                notes = scrape_fresh_notes()
                if notes:
                    analyze_with_bot(notes)
                else:
                    print("❌ Failed to scrape notes")
                    
            elif choice == '3':
                notes = load_simplidots_notes()
                if not notes:
                    print("⚠️ No cached notes. Scraping fresh data...")
                    notes = scrape_fresh_notes()
                interactive_qa(notes)
                
            elif choice == '4':
                notes = load_simplidots_notes()
                show_notes_summary(notes)
                
            elif choice == '5':
                notes = scrape_fresh_notes()
                if notes:
                    print(f"✅ Successfully scraped {len(notes)} notes")
                else:
                    print("❌ Failed to scrape notes")
                    
            elif choice == '6':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main_menu()
