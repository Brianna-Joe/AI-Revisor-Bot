#!/usr/bin/env python3
"""
Interactive Q&A service for SimpliDOTS release notes
Handles user interactions and question-answering sessions
"""

from typing import List, Dict
from ai_analyzer import SimpliDOTSAIAnalyzer

class InteractiveQAService:
    def __init__(self):
        self.ai_analyzer = SimpliDOTSAIAnalyzer()
    
    def start_qa_session(self, notes: List[Dict]):
        """Start an interactive Q&A session"""
        if not notes:
            print("❌ No notes available for Q&A")
            return
        
        self._display_qa_header(notes)
        
        while True:
            try:
                question = self._get_user_question()
                
                if self._should_exit(question):
                    print("👋 Thanks for using SimpliDOTS Q&A! Goodbye!")
                    break
                
                if not question.strip():
                    continue
                
                self._process_question(question, notes)
                
            except KeyboardInterrupt:
                print("\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("Please try again or type 'quit' to exit.")
    
    def _display_qa_header(self, notes: List[Dict]):
        """Display the Q&A session header"""
        print(f"\n🗣️ INTERACTIVE Q&A MODE")
        print("=" * 60)
        print(f"💡 Ask questions about SimpliDOTS features")
        print(f"📚 Knowledge base: {len(notes)} release notes loaded")
        print(f"🎯 Example questions:")
        print("   • What are the latest PPN 12% updates?")
        print("   • How does the Collection feature work?")
        print("   • What warehouse management features exist?")
        print("   • What integrations are available?")
        print(f"⌨️  Type 'quit', 'exit', or 'q' to exit")
        print("-" * 60)
    
    def _get_user_question(self) -> str:
        """Get a question from the user"""
        return input("\n🤔 Your question: ").strip()
    
    def _should_exit(self, question: str) -> bool:
        """Check if user wants to exit"""
        return question.lower() in ['quit', 'exit', 'q', 'stop', 'bye']
    
    def _process_question(self, question: str, notes: List[Dict]):
        """Process and answer a user question"""
        print("🤖 Analyzing SimpliDOTS release notes...")
        print("⏳ This may take a moment...")
        
        try:
            # Use top 25 notes for better context
            answer = self.ai_analyzer.ask_question(question, notes[:25])
            
            print(f"\n💡 Answer:")
            print("-" * 40)
            print(answer)
            print("-" * 40)
            
        except Exception as e:
            print(f"❌ Error processing question: {e}")
            print("Please try rephrasing your question or check your internet connection.")
    
    def get_suggested_questions(self) -> List[str]:
        """Get a list of suggested questions for users"""
        return [
            "What are the most recent features added to SimpliDOTS?",
            "How do I update PPN from 11% to 12%?",
            "What is the Collection feature and how does it work?",
            "What warehouse management improvements have been made?",
            "Are there any new integration features?",
            "What e-faktur capabilities are available?",
            "How do customer limits work in the system?",
            "What stock management features are new?",
            "What improvements were made to the Sales Management Hub?",
            "Are there any API updates or new endpoints?"
        ]
    
    def ask_suggested_question(self, notes: List[Dict], question_index: int = 0):
        """Ask one of the suggested questions"""
        suggested_questions = self.get_suggested_questions()
        
        if 0 <= question_index < len(suggested_questions):
            question = suggested_questions[question_index]
            print(f"🤔 Asking: {question}")
            self._process_question(question, notes)
        else:
            print(f"❌ Invalid question index. Available: 0-{len(suggested_questions)-1}")
    
    def quick_demo(self, notes: List[Dict]):
        """Run a quick demo with a few sample questions"""
        if not notes:
            print("❌ No notes available for demo")
            return
        
        print(f"\n🎬 QUICK DEMO - SimpliDOTS Q&A")
        print("=" * 50)
        print("Running a few sample questions...")
        
        demo_questions = [
            "What are the most recent SimpliDOTS features?",
            "What PPN 12% updates were implemented?",
            "What is the Collection feature?"
        ]
        
        for i, question in enumerate(demo_questions, 1):
            print(f"\n📍 Demo Question {i}: {question}")
            print("-" * 30)
            self._process_question(question, notes)
            
            if i < len(demo_questions):
                input("\nPress Enter to continue to next question...")
        
        print(f"\n🎉 Demo complete! Use interactive mode for custom questions.")
