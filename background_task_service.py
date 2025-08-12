#!/usr/bin/env python3
"""
Background task service for handling long-running operations
Following Single Responsibility Principle (SRP)
"""

import threading
import time
from typing import Callable, Dict, Any, Optional
from app import SimpliDOTSApp

class BackgroundTaskService:
    """Service for handling background tasks like data refresh"""
    
    def __init__(self, app: SimpliDOTSApp, slack_client_service):
        self.app = app
        self.slack_client = slack_client_service
        self.running_tasks = {}
    
    def refresh_data_async(self, channel: str, user_id: str, message_ts: Optional[str] = None):
        """Refresh SimpliDOTS data in background"""
        task_id = f"refresh_{channel}_{user_id}_{int(time.time())}"
        
        def refresh_task():
            try:
                # Update user about progress
                self.slack_client.send_message(
                    channel, 
                    "🔄 Starting data refresh... Scraping SimpliDOTS release notes...",
                    thread_ts=message_ts
                )
                
                # Force scrape fresh data
                notes = self.app.get_or_scrape_notes(force_scrape=True)
                
                if notes:
                    summary = self.app.data_manager.get_notes_summary(notes)
                    success_msg = f"✅ *Data refresh complete!*\n" \
                                f"• Scraped {summary['total_notes']} release notes\n" \
                                f"• Total content: {summary['total_content_chars']:,} characters\n" \
                                f"• Latest update: {summary['latest_date']}\n" \
                                f"• Use `/simplidots summary` to get the latest insights!"
                else:
                    success_msg = "❌ Data refresh failed. Please try again later."
                
                self.slack_client.send_message(channel, success_msg, thread_ts=message_ts)
                
            except Exception as e:
                error_msg = f"❌ Error during data refresh: {str(e)}"
                self.slack_client.send_message(channel, error_msg, thread_ts=message_ts)
            
            finally:
                # Remove task from running tasks
                if task_id in self.running_tasks:
                    del self.running_tasks[task_id]
        
        # Start background thread
        thread = threading.Thread(target=refresh_task, daemon=True)
        self.running_tasks[task_id] = {
            'thread': thread,
            'started_at': time.time(),
            'channel': channel,
            'user_id': user_id
        }
        thread.start()
        
        return task_id
    
    def get_running_tasks(self) -> Dict[str, Any]:
        """Get information about running tasks"""
        return {
            task_id: {
                'started_at': task_info['started_at'],
                'duration': time.time() - task_info['started_at'],
                'channel': task_info['channel'],
                'user_id': task_info['user_id']
            }
            for task_id, task_info in self.running_tasks.items()
        }
    
    def cleanup_finished_tasks(self):
        """Clean up finished tasks"""
        finished_tasks = [
            task_id for task_id, task_info in self.running_tasks.items()
            if not task_info['thread'].is_alive()
        ]
        
        for task_id in finished_tasks:
            del self.running_tasks[task_id]
