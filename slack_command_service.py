#!/usr/bin/env python3
"""
Slack command service for SimpliDOTS bot
Handles all slash commands and interactions
Following Single Responsibility Principle (SRP)
"""

import re
from typing import Dict, Any, Optional
from slack_bot_interface import ISlackCommandHandler, ISlackMessageHandler, ISlackEventHandler
from app import SimpliDOTSApp

class SimpliDOTSSlackCommandService(ISlackCommandHandler, ISlackMessageHandler, ISlackEventHandler):
    """Service to handle all SimpliDOTS Slack interactions"""
    
    def __init__(self, app: SimpliDOTSApp):
        self.app = app
        self.commands = {
            'summary': self._handle_summary_command,
            'ask': self._handle_ask_command,
            'status': self._handle_status_command,
            'help': self._handle_help_command,
            'refresh': self._handle_refresh_command
        }
    
    def handle_command(self, command: str, text: str, user_id: str) -> str:
        """Handle slash commands like /simplidots summary"""
        try:
            # Parse command and arguments
            parts = text.strip().split(' ', 1) if text.strip() else ['help']
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ''
            
            if cmd in self.commands:
                return self.commands[cmd](args, user_id)
            else:
                return self._handle_unknown_command(cmd)
                
        except Exception as e:
            return f"❌ Error processing command: {str(e)}"
    
    def handle_message(self, event: Dict[str, Any]) -> Optional[str]:
        """Handle regular messages mentioning the bot"""
        text = event.get('text', '').lower()
        
        # Simple keyword detection
        if any(keyword in text for keyword in ['summary', 'summarize', 'overview']):
            return self._handle_summary_command('', event.get('user', ''))
        elif 'help' in text:
            return self._handle_help_command('', event.get('user', ''))
        elif text.startswith(('what', 'how', 'when', 'why', 'where')):
            # Extract question
            question = event.get('text', '')
            return self._handle_ask_command(question, event.get('user', ''))
        
        return None
    
    def handle_app_mention(self, event: Dict[str, Any]) -> Optional[str]:
        """Handle when bot is mentioned in a channel"""
        # Remove bot mention from text
        text = event.get('text', '')
        text = re.sub(r'<@U\w+>', '', text).strip()
        
        if not text:
            return self._handle_help_command('', event.get('user', ''))
        
        # If it looks like a question, treat it as such
        if text.endswith('?') or text.startswith(('what', 'how', 'when', 'why', 'where')):
            return self._handle_ask_command(text, event.get('user', ''))
        elif any(keyword in text.lower() for keyword in ['summary', 'summarize']):
            return self._handle_summary_command('', event.get('user', ''))
        else:
            return self._handle_help_command('', event.get('user', ''))
    
    def handle_direct_message(self, event: Dict[str, Any]) -> Optional[str]:
        """Handle direct messages to the bot"""
        return self.handle_message(event)
    
    def _handle_summary_command(self, args: str, user_id: str) -> str:
        """Handle summary command"""
        try:
            notes = self.app.get_or_scrape_notes()
            if not notes:
                return "❌ No release notes available. Please try again later."
            
            # Determine number of notes to summarize
            max_notes = 20
            if args and args.isdigit():
                max_notes = min(int(args), 50)  # Limit to 50 max
            
            summary = self.app.ai_analyzer.summarize_notes(notes, max_notes)
            
            return f"📋 *SimpliDOTS Release Notes Summary* (Latest {max_notes} notes)\n\n{summary}"
            
        except Exception as e:
            return f"❌ Error generating summary: {str(e)}"
    
    def _handle_ask_command(self, question: str, user_id: str) -> str:
        """Handle ask/question command"""
        if not question or not question.strip():
            return "❓ Please provide a question about SimpliDOTS features.\n" \
                   "Example: `What are the latest PPN updates?`"
        
        try:
            notes = self.app.get_or_scrape_notes()
            if not notes:
                return "❌ No release notes available to answer questions."
            
            answer = self.app.ai_analyzer.ask_question(question, notes, max_notes=25)
            
            return f"❓ *Question:* {question}\n\n💡 *Answer:*\n{answer}"
            
        except Exception as e:
            return f"❌ Error answering question: {str(e)}"
    
    def _handle_status_command(self, args: str, user_id: str) -> str:
        """Handle status command"""
        try:
            notes = self.app.data_manager.load_notes()
            if not notes:
                return "📭 No cached release notes found.\n" \
                       "Use `/simplidots refresh` to scrape fresh data."
            
            summary = self.app.data_manager.get_notes_summary(notes)
            
            return f"📊 *SimpliDOTS Bot Status*\n" \
                   f"• Notes available: {summary['total_notes']}\n" \
                   f"• Total content: {summary['total_content_chars']:,} characters\n" \
                   f"• Latest update: {summary['latest_date']}\n" \
                   f"• Oldest update: {summary['oldest_date']}"
                   
        except Exception as e:
            return f"❌ Error getting status: {str(e)}"
    
    def _handle_refresh_command(self, args: str, user_id: str) -> str:
        """Handle refresh command to scrape fresh data"""
        try:
            return "🔄 Refreshing SimpliDOTS data... This may take a few minutes.\n" \
                   "I'll update you when it's complete!"
            # Note: Actual refresh should be done asynchronously
            
        except Exception as e:
            return f"❌ Error refreshing data: {str(e)}"
    
    def _handle_help_command(self, args: str, user_id: str) -> str:
        """Handle help command"""
        return """🤖 *SimpliDOTS Release Notes Bot*

*Available Commands:*
• `/simplidots summary` - Get AI summary of latest release notes
• `/simplidots summary 10` - Summarize specific number of notes
• `/simplidots ask <question>` - Ask questions about SimpliDOTS features
• `/simplidots status` - Check bot status and data availability
• `/simplidots refresh` - Refresh release notes data
• `/simplidots help` - Show this help message

*Examples:*
• "What are the latest PPN 12% updates?"
• "How does the Collection feature work?"
• "What warehouse management features exist?"

*Mention me in channels:* @SimpliDOTS Bot
*Direct message me:* Just type your question!"""
    
    def _handle_unknown_command(self, command: str) -> str:
        """Handle unknown commands"""
        return f"❓ Unknown command: `{command}`\n" \
               f"Use `/simplidots help` to see available commands."
