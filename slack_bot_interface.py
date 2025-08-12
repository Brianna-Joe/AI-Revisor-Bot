#!/usr/bin/env python3
"""
Interface for Slack bot operations
Following Interface Segregation Principle (ISP)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ISlackMessageHandler(ABC):
    """Interface for handling Slack messages"""
    
    @abstractmethod
    def handle_message(self, event: Dict[str, Any]) -> Optional[str]:
        """Handle incoming Slack message"""
        pass

class ISlackCommandHandler(ABC):
    """Interface for handling Slack slash commands"""
    
    @abstractmethod
    def handle_command(self, command: str, text: str, user_id: str) -> str:
        """Handle slash command"""
        pass

class ISlackEventHandler(ABC):
    """Interface for handling Slack events"""
    
    @abstractmethod
    def handle_app_mention(self, event: Dict[str, Any]) -> Optional[str]:
        """Handle app mention events"""
        pass
    
    @abstractmethod
    def handle_direct_message(self, event: Dict[str, Any]) -> Optional[str]:
        """Handle direct message events"""
        pass
