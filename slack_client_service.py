#!/usr/bin/env python3
"""
Slack client service for managing Slack API interactions
Following Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP)
"""

import os
from typing import Dict, Any, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackClientService:
    """Service for Slack API interactions"""
    
    def __init__(self, bot_token: str):
        self.client = WebClient(token=bot_token)
        self.bot_user_id = None
        self._initialize_bot_info()
    
    def _initialize_bot_info(self):
        """Initialize bot information"""
        try:
            response = self.client.auth_test()
            self.bot_user_id = response["user_id"]
            print(f"✅ Bot authenticated as {response['user']} (ID: {self.bot_user_id})")
        except SlackApiError as e:
            print(f"❌ Failed to authenticate bot: {e}")
            raise
    
    def send_message(self, channel: str, text: str, thread_ts: Optional[str] = None) -> bool:
        """Send a message to a Slack channel"""
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text,
                thread_ts=thread_ts,
                unfurl_links=False,
                unfurl_media=False
            )
            return response["ok"]
        except SlackApiError as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def send_ephemeral_message(self, channel: str, user: str, text: str) -> bool:
        """Send an ephemeral message (only visible to specific user)"""
        try:
            response = self.client.chat_postEphemeral(
                channel=channel,
                user=user,
                text=text
            )
            return response["ok"]
        except SlackApiError as e:
            print(f"❌ Error sending ephemeral message: {e}")
            return False
    
    def send_response_to_command(self, response_url: str, text: str, response_type: str = "ephemeral") -> bool:
        """Send response to a slash command"""
        try:
            import requests
            payload = {
                "text": text,
                "response_type": response_type
            }
            response = requests.post(response_url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error sending command response: {e}")
            return False
    
    def update_message(self, channel: str, ts: str, text: str) -> bool:
        """Update an existing message"""
        try:
            response = self.client.chat_update(
                channel=channel,
                ts=ts,
                text=text
            )
            return response["ok"]
        except SlackApiError as e:
            print(f"❌ Error updating message: {e}")
            return False
    
    def add_reaction(self, channel: str, timestamp: str, emoji: str) -> bool:
        """Add reaction to a message"""
        try:
            response = self.client.reactions_add(
                channel=channel,
                timestamp=timestamp,
                name=emoji
            )
            return response["ok"]
        except SlackApiError as e:
            print(f"❌ Error adding reaction: {e}")
            return False
    
    def is_bot_mentioned(self, text: str) -> bool:
        """Check if bot is mentioned in text"""
        return f"<@{self.bot_user_id}>" in text if self.bot_user_id else False
    
    def is_direct_message(self, channel_type: str) -> bool:
        """Check if message is a direct message"""
        return channel_type == "im"
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        try:
            response = self.client.users_info(user=user_id)
            return response["user"] if response["ok"] else None
        except SlackApiError as e:
            print(f"❌ Error getting user info: {e}")
            return None
