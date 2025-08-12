# 🤖 SimpliDOTS Slack Bot

An intelligent Slack bot that provides AI-powered analysis and Q&A for SimpliDOTS release notes. Built with clean architecture principles and designed for production deployment.

## 🎥 Demo Video

[![SimpliDOTS Slack Bot Demo](https://img.youtube.com/vi/e_w4CGT-4aY/maxresdefault.jpg)](https://youtu.be/e_w4CGT-4aY)

**[🎬 Watch the Demo Video](https://youtu.be/e_w4CGT-4aY)** - See the bot in action with live Slack commands and AI responses!

## ✨ Features

- 🔍 **AI-Powered Analysis**: Intelligent summaries and Q&A using DeepSeek API
- 💬 **Slack Integration**: Full support for slash commands, @mentions, and DMs
- 🕷️ **Automated Scraping**: Extracts detailed content from SimpliDOTS GitBook
- ⚡ **Background Processing**: Handles long-running tasks without timeouts
- 🏗️ **Clean Architecture**: Follows SOLID principles with dependency injection
- 🚀 **Multiple Deployment Options**: HTTP Mode, Socket Mode, and cloud deployment

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/AI-Revisor.git
cd AI-Revisor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual API keys and tokens
nano .env  # or use your preferred editor
```

Required environment variables:
```env
# DeepSeek API Configuration
OPENAI_API_KEY=your_deepseek_api_key_here
OPENAI_API_BASE=https://chataiapi.com/v1

# Slack Bot Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
PORT=4000
```

### 3. Test Your Setup
```bash
# Test the scraper and AI analysis
python app.py

# Test the Slack bot components
python slack_bot.py
```

## 🤖 Slack App Configuration

### Step 1: Create Slack App
1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name: "SimpliDOTS Bot"
4. Choose your workspace

### Step 2: Bot Configuration
**OAuth & Permissions:**
- Bot Token Scopes:
  - `app_mentions:read`
  - `channels:history`
  - `channels:read`
  - `chat:write`
  - `im:history`
  - `im:read`
  - `im:write`
  - `users:read`

**Event Subscriptions:**
- Enable Events: ✅
- Request URL: `https://your-domain.com/slack/events`
- Bot Events:
  - `app_mention`
  - `message.channels`
  - `message.im`

**Slash Commands:**
- Command: `/simplidots`
- Request URL: `https://your-domain.com/slack/commands`
- Description: "Get SimpliDOTS release notes and AI analysis"
- Usage Hint: `[summary|ask <question>|status|help|refresh]`

**Interactive Components:**
- Request URL: `https://your-domain.com/slack/interactive`

### Step 3: Install to Workspace
1. Go to "Install App" in sidebar
2. Click "Install to Workspace"
3. Copy the "Bot User OAuth Token" to your `.env` file

## 🌐 Deployment Options

### Option 1: Local Development (ngrok)
```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com/

# Start your Flask app
python slack_bot.py

# In another terminal, expose local server
ngrok http 3000

# Use the ngrok URL in Slack app configuration
# Example: https://abc123.ngrok.io/slack/events
```

### Option 2: Cloud Deployment (Heroku)
```bash
# Create Procfile
echo "web: python slack_bot.py" > Procfile

# Deploy to Heroku
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
heroku config:set SLACK_BOT_TOKEN=your_token
git add .
git commit -m "Deploy SimpliDOTS Slack Bot"
git push heroku main
```

### Option 3: Cloud Deployment (Railway/Render)
1. Connect your GitHub repo
2. Set environment variables in dashboard
3. Deploy automatically

## 📱 Bot Usage

> 🎥 **Want to see it in action?** [Watch the demo video](https://youtu.be/e_w4CGT-4aY) to see all these commands working live!

### Slash Commands
```
/simplidots summary          # Get latest release notes summary
/simplidots ask What's new?  # Ask questions about releases
/simplidots status           # Check bot status
/simplidots help             # Show help message
/simplidots refresh          # Refresh data (background task)
```

### Direct Messages
- Send any message to the bot
- Ask questions about SimpliDOTS releases
- Get summaries and analysis

### Channel Mentions
```
@SimpliDOTS Bot summary
@SimpliDOTS Bot what are the new features?
```

## 🛠️ Architecture Overview

```
SimpliDOTS Slack Bot
├── Core Services (SOLID Principles)
│   ├── app.py                    # Main application controller
│   ├── data_manager.py           # Data management service
│   ├── ai_analyzer.py            # AI analysis service
│   └── scraping_service.py       # Web scraping service
├── Slack Integration
│   ├── slack_bot.py              # Main bot orchestrator
│   ├── slack_client_service.py   # Slack API wrapper
│   ├── slack_command_service.py  # Command handling
│   ├── slack_bot_interface.py    # Interface definitions
│   └── background_task_service.py # Async task management
└── Configuration
    ├── .env                      # Environment variables
    ├── requirements.txt          # Dependencies
    └── README.md                 # This file
```

## 🔧 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Install missing packages
pip install slack_sdk flask
```

**2. Slack Token Issues**
- Verify bot token starts with `xoxb-`
- Check bot has required permissions
- Ensure app is installed to workspace

**3. API Rate Limits**
- DeepSeek API: Implement exponential backoff
- Slack API: Bot respects rate limits automatically

**4. Data Refresh Delays**
- Refresh runs in background (30-60 seconds)
- Check status with `/simplidots status`

### Debugging
```bash
# Enable debug logging
export FLASK_DEBUG=1
python slack_bot.py

# Check bot health
curl http://localhost:3000/health
```

## 📊 Features

### ✅ Implemented
- 🕷️ Web scraping of SimpliDOTS release notes
- 🤖 AI-powered content analysis with DeepSeek
- 💬 Slack slash commands and mentions
- 🔄 Background data refresh
- 📊 Interactive Q&A system
- 🏗️ SOLID principle architecture

### 🔮 Future Enhancements
- 📅 Scheduled automatic updates
- 📈 Release trend analysis
- 🎯 Custom notification preferences
- 🔍 Advanced search capabilities
- 📱 Interactive buttons and menus

---

## 🎯 Next Steps

1. **Install dependencies:** `pip install -r requirements.txt`
2. **Configure Slack app** following the guide above
3. **Set environment variables** in `.env` file
4. **Deploy to your preferred platform**
5. **Test all bot commands** in Slack

Your SimpliDOTS Slack Bot is ready to provide AI-powered release note analysis! 🚀
