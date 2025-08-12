#!/usr/bin/env python3
"""
SimpliDOTS Slack Bot using official Slack Bolt framework
Following Slack's recommended patterns and security practices
"""

import os
import re
from typing import Dict, Any
from dotenv import load_dotenv

# Slack Bolt imports
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# Our services
from app import SimpliDOTSApp
from slack_command_service import SimpliDOTSSlackCommandService
from background_task_service import BackgroundTaskService

class SimpliDOTSSlackBoltBot:
    """Main Slack bot using Bolt framework"""
    
    def __init__(self):
        load_dotenv()
        
        # Initialize Slack Bolt app
        self.slack_app = App(
            token=os.getenv("SLACK_BOT_TOKEN"),
            signing_secret=os.getenv("SLACK_SIGNING_SECRET")
        )
        
        # Initialize our services
        self.simplidots_app = SimpliDOTSApp()
        self.command_service = SimpliDOTSSlackCommandService(self.simplidots_app)
        self.background_service = BackgroundTaskService(self.simplidots_app, None)
        
        # Register event handlers
        self._register_handlers()
        
        print("🤖 SimpliDOTS Slack Bolt Bot initialized successfully!")
    
    def _register_handlers(self):
        """Register all Slack event handlers"""
        
        # Handle app mentions (@bot_name)
        @self.slack_app.event("app_mention")
        def handle_app_mention(event, say, logger):
            try:
                response = self.command_service.handle_app_mention(event)
                if response:
                    say(text=response, thread_ts=event.get("ts"))
            except Exception as e:
                logger.error(f"Error in app mention: {e}")
                say("❌ Sorry, I encountered an error processing your request.")
        
        # Handle direct messages
        @self.slack_app.event("message")
        def handle_direct_message(event, say, logger):
            try:
                # Only respond to direct messages (not channel messages)
                if event.get("channel_type") == "im":
                    response = self.command_service.handle_direct_message(event)
                    if response:
                        say(text=response)
            except Exception as e:
                logger.error(f"Error in direct message: {e}")
                say("❌ Sorry, I encountered an error processing your message.")
        
        # Handle slash commands
        @self.slack_app.command("/simplidots")
        def handle_slash_command(ack, command, respond, logger):
            try:
                # Acknowledge the command request
                ack()
                
                # Handle refresh command asynchronously
                text = command.get("text", "").strip()
                if text.lower() == "refresh":
                    # Start background refresh
                    channel_id = command.get("channel_id")
                    user_id = command.get("user_id")
                    self.background_service.refresh_data_async(channel_id, user_id)
                    respond("🔄 Starting data refresh in background... I'll notify you when complete!")
                    return
                
                # Handle other commands
                response = self.command_service.handle_command(
                    command.get("command", ""),
                    text,
                    command.get("user_id", "")
                )
                
                respond(response)
                
            except Exception as e:
                logger.error(f"Error in slash command: {e}")
                respond("❌ Sorry, I encountered an error processing your command.")
        
        # Handle bot startup
        @self.slack_app.event("app_home_opened")
        def handle_app_home_opened(event, say, logger):
            try:
                user_id = event.get("user")
                welcome_message = f"👋 Welcome to SimpliDOTS Bot, <@{user_id}>!\n\n" + \
                                self.command_service._handle_help_command("", user_id)
                say(text=welcome_message)
            except Exception as e:
                logger.error(f"Error in app home opened: {e}")
    
    def get_flask_handler(self):
        """Get Flask request handler for deployment"""
        return SlackRequestHandler(self.slack_app)
    
    def start_socket_mode(self):
        """Start in Socket Mode (for development)"""
        if not os.getenv("SLACK_APP_TOKEN"):
            print("❌ SLACK_APP_TOKEN required for Socket Mode")
            return False
        
        self.slack_app.start(port=int(os.getenv("PORT", 3000)))
        return True

def create_flask_app_with_bolt():
    """Create Flask app integrated with Slack Bolt"""
    try:
        from flask import Flask, request
        
        # Initialize bot
        bot = SimpliDOTSSlackBoltBot()
        handler = bot.get_flask_handler()
        
        # Create Flask app
        app = Flask(__name__)
        
        # Slack events endpoint
        @app.route("/slack/events", methods=["POST"])
        def slack_events():
            return handler.handle(request)
        
        # Health check
        @app.route("/health", methods=["GET"])
        def health():
            try:
                notes = bot.simplidots_app.data_manager.load_notes()
                return {
                    "status": "healthy",
                    "notes_available": len(notes) if notes else 0,
                    "bot_ready": True
                }
            except Exception as e:
                return {"status": "unhealthy", "error": str(e)}, 500
        
        return app
        
    except ImportError:
        print("❌ Flask not installed. Install with: pip install flask")
        return None

if __name__ == "__main__":
    print("🚀 Starting SimpliDOTS Slack Bolt Bot...")
    
    # Check environment variables
    if not os.getenv("SLACK_BOT_TOKEN"):
        print("❌ SLACK_BOT_TOKEN environment variable required")
        print("📋 Please follow the setup guide in SLACK_SETUP.md")
        exit(1)
    
    if not os.getenv("SLACK_SIGNING_SECRET"):
        print("❌ SLACK_SIGNING_SECRET environment variable required")
        print("📋 Please follow the setup guide in SLACK_SETUP.md")
        exit(1)
    
    # Try Socket Mode first (if app token available)
    bot = SimpliDOTSSlackBoltBot()
    if bot.start_socket_mode():
        print("✅ Started in Socket Mode")
    else:
        # Fall back to Flask/HTTP mode
        print("📡 Starting in HTTP mode with Flask...")
        flask_app = create_flask_app_with_bolt()
        if flask_app:
            print("✅ Flask app created with Bolt integration")
            print("🌐 Bot ready to receive Slack events at:")
            print("   - Events: http://localhost:3000/slack/events")
            print("   - Health: http://localhost:3000/health")
            
            flask_app.run(host="0.0.0.0", port=3000, debug=True)
        else:
            print("❌ Failed to create Flask app")
