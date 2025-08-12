#!/usr/bin/env python3
"""
Comprehensive SimpliDOTS Scraper - Extract detailed content from all available release notes
"""

from enhanced_scraper import SimpliDOTSGitBookScraper
import json

def scrape_all_detailed_content():
    """Scrape all available SimpliDOTS release notes with maximum detail"""
    print("🚀 Starting COMPREHENSIVE SimpliDOTS content extraction...")
    print("📋 This will scrape ALL available release notes with detailed content")
    print("-" * 80)
    
    scraper = SimpliDOTSGitBookScraper()
    
    # Scrape all years with detailed content
    all_detailed_notes = scraper.scrape_all_years(detailed_content=True)
    
    if all_detailed_notes:
        print(f"\n🎉 Successfully extracted {len(all_detailed_notes)} detailed release notes!")
        
        # Show statistics
        total_content_chars = sum(len(note['content']) for note in all_detailed_notes)
        avg_content_length = total_content_chars / len(all_detailed_notes)
        
        print(f"📊 CONTENT STATISTICS:")
        print(f"   📄 Total notes: {len(all_detailed_notes)}")
        print(f"   📝 Total content: {total_content_chars:,} characters")
        print(f"   📏 Average length: {avg_content_length:.0f} characters per note")
        
        # Find longest and shortest notes
        longest_note = max(all_detailed_notes, key=lambda x: len(x['content']))
        shortest_note = min(all_detailed_notes, key=lambda x: len(x['content']))
        
        print(f"   📈 Longest note: '{longest_note['title'][:50]}...' ({len(longest_note['content'])} chars)")
        print(f"   📉 Shortest note: '{shortest_note['title'][:50]}...' ({len(shortest_note['content'])} chars)")
        
        # Show sample of a detailed note
        print(f"\n📄 SAMPLE DETAILED CONTENT:")
        print(f"Title: {longest_note['title']}")
        print(f"Date: {longest_note['date']}")
        print(f"Length: {len(longest_note['content'])} characters")
        print(f"URL: {longest_note['source_url']}")
        print(f"\nContent preview:\n{longest_note['content'][:1500]}...")
        
        # Save to different files
        scraper.save_to_json(all_detailed_notes, "comprehensive_detailed_notes.json")
        
        # Also save a summary version
        summary_notes = []
        for note in all_detailed_notes:
            summary_notes.append({
                'date': note['date'],
                'title': note['title'],
                'content_length': len(note['content']),
                'content_preview': note['content'][:300] + '...' if len(note['content']) > 300 else note['content'],
                'source_url': note['source_url']
            })
        
        with open("content_summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary_notes, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Files saved:")
        print(f"   📁 comprehensive_detailed_notes.json - Full detailed content")
        print(f"   📁 content_summary.json - Summary with content lengths")
        
        return all_detailed_notes
    else:
        print("❌ No detailed notes were extracted!")
        return []

def analyze_content_quality(notes):
    """Analyze the quality and completeness of extracted content"""
    print("\n🔍 CONTENT QUALITY ANALYSIS:")
    print("-" * 50)
    
    if not notes:
        print("❌ No notes to analyze")
        return
    
    # Check for truncated content (likely incomplete)
    truncated_count = 0
    detailed_count = 0
    
    for note in notes:
        content_length = len(note['content'])
        if content_length >= 9500:  # Close to our 10k limit
            truncated_count += 1
        elif content_length >= 2000:  # Good detailed content
            detailed_count += 1
    
    basic_count = len(notes) - truncated_count - detailed_count
    
    print(f"📊 Content Distribution:")
    print(f"   🔥 Detailed (2k+ chars): {detailed_count} notes")
    print(f"   ⚠️  Possibly truncated (9.5k+ chars): {truncated_count} notes")
    print(f"   📝 Basic content: {basic_count} notes")
    
    # Check for specific features we want to ensure are captured
    important_features = [
        'ppn 12', 'collection', 'customer limit', 'log activity', 
        'warehouse', 'stock', 'integration', 'accurate'
    ]
    
    found_features = {}
    for feature in important_features:
        found_features[feature] = []
        for note in notes:
            if feature.lower() in note['title'].lower() or feature.lower() in note['content'].lower():
                found_features[feature].append(note['title'])
    
    print(f"\n🎯 Important Features Found:")
    for feature, matches in found_features.items():
        if matches:
            print(f"   ✅ {feature.upper()}: {len(matches)} notes")
            for match in matches[:2]:  # Show first 2 matches
                print(f"      - {match[:60]}...")
        else:
            print(f"   ❌ {feature.upper()}: Not found")

if __name__ == "__main__":
    # Run comprehensive scraping
    detailed_notes = scrape_all_detailed_content()
    
    # Analyze the quality
    analyze_content_quality(detailed_notes)
    
    print("\n" + "=" * 80)
    print("🎉 COMPREHENSIVE SCRAPING COMPLETE!")
    print("📁 Check the generated files for the detailed content")
    print("=" * 80)
