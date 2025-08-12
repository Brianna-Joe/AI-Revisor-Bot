#!/usr/bin/env python3
"""
SimpliDOTS Slack Bot - Main application
Following SOLID principles with clean architecture
"""

import os
import json
import threading
import time
from typing import Dict, Any
from dotenv import load_dotenv

# Import services following Dependency Inversion Principle
from app import SimpliDOTSApp
from slack_client_service import SlackClientService
from slack_command_service import SimpliDOTSSlackCommandService
from background_task_service import BackgroundTaskService

class SimpliDOTSSlackBot:
    """Main Slack bot class following Open/Closed Principle"""
    
    def __init__(self, bot_token: str, app_token: str = None):
        # Initialize core services (Dependency Injection)
        self.app = SimpliDOTSApp()
        self.slack_client = SlackClientService(bot_token)
        self.command_service = SimpliDOTSSlackCommandService(self.app)
        self.background_service = BackgroundTaskService(self.app, self.slack_client)
        
        # Bot configuration
        self.app_token = app_token
        self.running = False
        
        print("🤖 SimpliDOTS Slack Bot initialized successfully!")
    
    def handle_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming Slack events"""
        try:
            event = event_data.get("event", {})
            event_type = event.get("type")
            user_id = event.get("user")
            bot_id = event.get("bot_id")
            subtype = event.get("subtype")
            text = event.get("text", "")
            
            # Multiple safeguards to prevent infinite loops
            
            # 1. Ignore any bot messages
            if bot_id or subtype == "bot_message":
                print("🤖 Skipping bot message")
                return {"status": "ignored_bot"}
            
            # 2. Ignore bot's own messages
            if user_id == self.slack_client.bot_user_id:
                print("🚫 Skipping own message")
                return {"status": "ignored_self"}
            
            # 3. Ignore empty messages
            if not text.strip():
                print("📭 Skipping empty message")
                return {"status": "ignored_empty"}
            
            # 4. Ignore messages that don't require response
            if event_type not in ["app_mention", "message"]:
                print(f"⏭️ Skipping event type: {event_type}")
                return {"status": "ignored_type"}
            
            print(f"✅ Processing {event_type} from user {user_id}")
            
            response_text = None
            
            if event_type == "app_mention":
                response_text = self.command_service.handle_app_mention(event)
            elif event_type == "message":
                channel_type = event.get("channel_type", "")
                if self.slack_client.is_direct_message(channel_type):
                    response_text = self.command_service.handle_direct_message(event)
                elif self.slack_client.is_bot_mentioned(text):
                    response_text = self.command_service.handle_app_mention(event)
            
            # Send response if we have one
            if response_text and response_text.strip():
                channel = event.get("channel")
                thread_ts = event.get("ts")
                print(f"📤 Sending response to channel {channel}")
                self.slack_client.send_message(channel, response_text, thread_ts)
                return {"status": "responded"}
            
            return {"status": "processed"}
            
        except Exception as e:
            print(f"❌ Error handling event: {e}")
            return {"status": "error", "error": str(e)}
    
    def handle_slash_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle slash commands like /simplidots"""
        try:
            command = command_data.get("command", "")
            text = command_data.get("text", "")
            user_id = command_data.get("user_id", "")
            channel_id = command_data.get("channel_id", "")
            response_url = command_data.get("response_url", "")
            
            # Handle refresh command asynchronously
            if text.strip().lower() == "refresh":
                # Start background refresh
                self.background_service.refresh_data_async(channel_id, user_id)
                return {
                    "response_type": "ephemeral",
                    "text": "🔄 Starting data refresh in background... I'll notify you when complete!"
                }
            
            # Handle other commands synchronously
            response_text = self.command_service.handle_command(command, text, user_id)
            
            return {
                "response_type": "ephemeral",
                "text": response_text
            }
            
        except Exception as e:
            return {
                "response_type": "ephemeral",
                "text": f"❌ Error processing command: {str(e)}"
            }
    
    def handle_interactive_component(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle interactive components (buttons, select menus, etc.)"""
        try:
            # Future: Handle button clicks, menu selections, etc.
            return {"status": "not_implemented"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_bot_status(self) -> Dict[str, Any]:
        """Get bot status information"""
        try:
            notes = self.app.data_manager.load_notes()
            running_tasks = self.background_service.get_running_tasks()
            
            return {
                "bot_user_id": self.slack_client.bot_user_id,
                "notes_available": len(notes) if notes else 0,
                "running_tasks": len(running_tasks),
                "status": "healthy"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.background_service.cleanup_finished_tasks()
            print("🧹 Bot cleanup completed")
        except Exception as e:
            print(f"❌ Error during cleanup: {e}")

def create_bot_from_env() -> SimpliDOTSSlackBot:
    """Factory method to create bot from environment variables"""
    load_dotenv()
    
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    app_token = os.getenv("SLACK_APP_TOKEN")
    
    if not bot_token:
        raise ValueError("SLACK_BOT_TOKEN environment variable is required")
    
    return SimpliDOTSSlackBot(bot_token, app_token)

def verify_slack_request(request):
    """Simple request verification (can be enhanced with signature verification)"""
    # For now, just check if request has required fields
    # In production, you should verify the Slack signature
    return True

# Flask/FastAPI integration example
def create_flask_app():
    """Create Flask app for Slack bot"""
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("❌ Flask not installed. Install with: pip install flask")
        return None
    
    app = Flask(__name__)
    bot = create_bot_from_env()
    
    @app.route("/slack/events", methods=["POST"])
    def slack_events():
        """Handle Slack events"""
        data = request.json
        
        # Handle URL verification
        if data.get("type") == "url_verification":
            return {"challenge": data.get("challenge")}
        
        # Add event logging to debug the loop
        event = data.get("event", {})
        event_type = event.get("type")
        user_id = event.get("user")
        bot_id = event.get("bot_id")
        subtype = event.get("subtype")
        
        print(f"📥 Event received: {event_type}, user: {user_id}, bot_id: {bot_id}, subtype: {subtype}")
        
        # Ignore bot messages completely (including our own responses)
        if bot_id or subtype == "bot_message":
            print("🤖 Ignoring bot message")
            return {"status": "ignored"}
        
        # Ignore messages from the bot user itself
        if user_id == bot.slack_client.bot_user_id:
            print("🚫 Ignoring message from bot user")
            return {"status": "ignored"}
        
        # Handle events
        result = bot.handle_event(data)
        return jsonify(result)
    
    @app.route("/slack/commands", methods=["POST"])
    def slack_commands():
        """Handle slash commands with immediate response"""
        import threading
        import requests
        
        try:
            # Parse command data
            form_data = request.form.to_dict()
            command = form_data.get('command', '')
            text = form_data.get('text', '').strip()
            user_id = form_data.get('user_id', '')
            channel_id = form_data.get('channel_id', '')
            response_url = form_data.get('response_url', '')
            
            print(f"📝 Slash command received: {command} {text}")
            
            # Quick commands - respond immediately
            if text.lower() in ['help', '']:
                help_text = """🤖 *SimpliDOTS Bot Commands:*
• `/simplidots summary` - Get latest release summary
• `/simplidots ask <question>` - Ask about releases  
• `/simplidots status` - Check bot status
• `/simplidots help` - Show this help
• `/simplidots refresh` - Update data"""
                
                return jsonify({
                    "text": help_text,
                    "response_type": "ephemeral"
                })
            
            elif text.lower() == 'status':
                try:
                    status = bot.get_bot_status()
                    status_text = f"""✅ *Bot Status:* {status.get('status', 'Unknown')}
📊 *Notes Available:* {status.get('notes_available', 0)}
🔄 *Running Tasks:* {status.get('running_tasks', 0)}"""
                    
                    return jsonify({
                        "text": status_text,
                        "response_type": "ephemeral"
                    })
                except Exception as e:
                    return jsonify({
                        "text": f"❌ Status check failed: {str(e)}",
                        "response_type": "ephemeral"
                    })
            
            # Slow commands - process in background
            else:
                def process_slow_command():
                    try:
                        # Process the command
                        result = bot.handle_slash_command(form_data)
                        response_text = result.get('text', 'Command processed successfully')
                        
                        # Send follow-up response
                        requests.post(response_url, json={
                            "text": response_text,
                            "response_type": "in_channel"
                        })
                        
                    except Exception as e:
                        # Send error response
                        requests.post(response_url, json={
                            "text": f"❌ Error processing command: {str(e)}",
                            "response_type": "ephemeral"
                        })
                
                # Start background thread
                thread = threading.Thread(target=process_slow_command)
                thread.daemon = True
                thread.start()
                
                # Return immediate response
                return jsonify({
                    "text": "🤖 Processing your request... I'll get back to you shortly!",
                    "response_type": "ephemeral"
                })
            
        except Exception as e:
            print(f"❌ Command error: {e}")
            return jsonify({
                "text": f"❌ Command failed: {str(e)}",
                "response_type": "ephemeral"
            }), 500
    
    @app.route("/slack/interactive", methods=["POST"])
    def slack_interactive():
        """Handle interactive components"""
        payload = json.loads(request.form.get("payload", "{}"))
        result = bot.handle_interactive_component(payload)
        return jsonify(result)
    
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint"""
        status = bot.get_bot_status()
        return jsonify(status)
    
    return app

if __name__ == "__main__":
    # Example usage
    print("🚀 Starting SimpliDOTS Slack Bot...")
    
    try:
        # Create Flask app
        flask_app = create_flask_app()
        if flask_app:
            print("✅ Flask app created successfully")
            
            # Use PORT from .env file instead of hardcoded 4000
            port = int(os.getenv("PORT", 4000))
            print("🌐 Bot ready to receive Slack events at:")
            print(f"   - Events: http://localhost:{port}/slack/events")
            print(f"   - Commands: http://localhost:{port}/slack/commands")
            print(f"   - Interactive: http://localhost:{port}/slack/interactive")
            print(f"   - Health: http://localhost:{port}/health")
            
            # Run Flask app (development only)
            flask_app.run(host="0.0.0.0", port=port, debug=True)
        else:
            print("❌ Failed to create Flask app")
            
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("💡 Make sure you have SLACK_BOT_TOKEN in your .env file")
