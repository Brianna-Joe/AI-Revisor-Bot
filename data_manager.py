#!/usr/bin/env python3
"""
Data management for SimpliDOTS release notes
Handles loading, saving, and caching of release notes data
"""

import json
import os
from typing import List, Dict, Optional

class SimpliDOTSDataManager:
    def __init__(self, data_file: str = 'comprehensive_detailed_notes.json'):
        self.data_file = data_file
    
    def load_notes(self) -> Optional[List[Dict]]:
        """Load release notes from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                notes = json.load(f)
            print(f"📂 Loaded {len(notes)} release notes from {self.data_file}")
            return notes
        except FileNotFoundError:
            print(f"📭 No cached notes found at {self.data_file}")
            return None
        except Exception as e:
            print(f"❌ Error loading notes: {e}")
            return None
    
    def save_notes(self, notes: List[Dict]) -> bool:
        """Save release notes to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(notes, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(notes)} notes to {self.data_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving notes: {e}")
            return False
    
    def get_notes_summary(self, notes: List[Dict]) -> Dict:
        """Get summary statistics of notes"""
        if not notes:
            return {}
        
        dates = [note['date'] for note in notes if note['date']]
        total_chars = sum(len(note['content']) for note in notes)
        
        return {
            'total_notes': len(notes),
            'total_content_chars': total_chars,
            'avg_content_length': total_chars / len(notes),
            'latest_date': max(dates) if dates else None,
            'oldest_date': min(dates) if dates else None
        }
    
    def show_notes_summary(self, notes: List[Dict]):
        """Display formatted summary of available notes"""
        if not notes:
            print("📭 No notes available")
            return
        
        summary = self.get_notes_summary(notes)
        
        print(f"\n📊 SIMPLIDOTS RELEASE NOTES SUMMARY")
        print("=" * 70)
        print(f"Total notes: {summary['total_notes']}")
        print(f"Total content: {summary['total_content_chars']:,} characters")
        print(f"Average length: {summary['avg_content_length']:.0f} chars per note")
        
        if summary['latest_date'] and summary['oldest_date']:
            print(f"Date range: {summary['oldest_date']} to {summary['latest_date']}")
        
        # Show recent features
        print(f"\n🚀 Recent Features (last 10):")
        for i, note in enumerate(notes[:10], 1):
            print(f"{i:2d}. [{note['date']}] {note['title']}")
        
        if len(notes) > 10:
            print(f"    ... and {len(notes) - 10} more features")
