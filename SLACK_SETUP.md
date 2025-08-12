# 🔧 Slack App Configuration Guide

## Required OAuth Scopes (OAuth & Permissions → Bot Token Scopes)
✅ Add these scopes:
- `app_mentions:read` - Read messages that directly mention @your_bot
- `channels:history` - View messages in public channels  
- `channels:read` - View basic information about public channels
- `chat:write` - Send messages as the bot
- `im:history` - View messages in direct messages
- `im:read` - View basic information about direct message conversations
- `im:write` - Start direct messages with people
- `users:read` - View people in a workspace

## Event Subscriptions (Features → Event Subscriptions)
✅ Enable Events and add Request URL:
- URL: https://faster-considerable-pubmed-volleyball.trycloudflare.com/slack/events
- Subscribe to Bot Events:
  - `app_mention` - When bot is mentioned
  - `message.channels` - Messages in channels where bot is added
  - `message.im` - Direct messages to the bot

## Slash Commands (Features → Slash Commands)
✅ Create slash command:
- Command: `/simplidots`
- Request URL: https://faster-considerable-pubmed-volleyball.trycloudflare.com/slack/commands
- Short Description: "Get SimpliDOTS release notes and AI analysis"
- Usage Hint: `[summary|ask <question>|status|help|refresh]`

## Install App (Settings → Install App)
✅ Install to Workspace to get:
- Bot User OAuth Token (starts with xoxb-)
- Signing Secret (from Basic Information → App Credentials)

## Required Environment Variables
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
