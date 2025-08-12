#!/usr/bin/env python3
"""
AI-powered analysis service for SimpliDOTS release notes
Handles summarization and Q&A using DeepSeek API
"""

import os
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

class SimpliDOTSAIAnalyzer:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://www.chataiapi.com/v1"
        )
        self.model_name = "deepseek-r1"
    
    def summarize_notes(self, notes: List[Dict], max_notes: int = 20) -> str:
        """Generate AI summary of release notes"""
        if not notes:
            return "No notes to summarize."
        
        # Limit notes to prevent token overflow
        selected_notes = notes[:max_notes]
        notes_text = "\n".join([
            f"{note['date']} - {note['title']}: {note['content'][:500]}..." 
            for note in selected_notes
        ])
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user", 
                    "content": f"Summarize these SimpliDOTS release notes in 5 key bullet points:\n{notes_text}"
                }]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {e}"
    
    def ask_question(self, question: str, notes: List[Dict], max_notes: int = 25) -> str:
        """Ask AI questions about the release notes"""
        if not notes:
            return "No notes available to answer questions."
        
        # Create context from notes
        selected_notes = notes[:max_notes]
        context = "\n".join([
            f"{note['date']}: {note['title']} - {note['content'][:800]}..."
            for note in selected_notes
        ])
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": f"Answer this question based on SimpliDOTS release notes:\n\nContext:\n{context}\n\nQuestion: {question}"
                }]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error answering question: {e}"
    
    def analyze_features(self, notes: List[Dict], max_notes: int = 20) -> Dict[str, str]:
        """Analyze and categorize features from release notes"""
        predefined_questions = [
            "What are the most recent features added to SimpliDOTS?",
            "What improvements have been made to the Sales Management Hub (SMH)?",
            "Are there any new integrations or API features?",
            "What tax-related updates (PPN) have been implemented?",
            "What warehouse and inventory management features were added?",
            "Are there any collection or payment-related features?",
            "What dashboard or interface improvements were made?"
        ]
        
        results = {}
        for i, question in enumerate(predefined_questions, 1):
            try:
                print(f"\n🤔 Question {i}: {question}")
                answer = self.ask_question(question, notes, max_notes)
                results[question] = answer
                print(f"💡 Answer: {answer}")
                print("-" * 40)
            except Exception as e:
                error_msg = f"Error with question {i}: {e}"
                results[question] = error_msg
                print(f"❌ {error_msg}")
                print("-" * 40)
        
        return results
    
    def perform_full_analysis(self, notes: List[Dict], max_notes: int = 20):
        """Perform summary analysis of release notes"""
        if not notes:
            print("❌ No notes to analyze")
            return
        
        # Use recent notes for analysis
        recent_notes = notes[:max_notes]
        
        print(f"\n🤖 ANALYZING {len(recent_notes)} SIMPLIDOTS RELEASE NOTES")
        print("=" * 80)
        
        try:
            # Generate comprehensive summary only
            print("\n📋 GENERATING SUMMARY...")
            print("-" * 50)
            summary = self.summarize_notes(recent_notes)
            print("📋 RELEASE NOTES SUMMARY:")
            print(summary)
            
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
