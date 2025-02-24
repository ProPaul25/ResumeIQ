# ResumeIQ - Smart CV Parser Bot

## 📌 Overview
ResumeIQ is an intelligent Telegram bot designed to parse and format CVs automatically. It extracts key details such as education, work experience, skills, projects, and contact information from PDF and DOCX files, presenting them in a structured and readable format.

## 🚀 Features
- 📄 Supports PDF & DOCX CVs
- 📚 Extracts structured information including:
  - Education
  - Work Experience
  - Skills
  - Projects
  - Certifications
  - Contact Information
- 📝 Formats extracted data for better readability
- 📱 Sends formatted results via Telegram
- 🔍 Recognizes key details like emails, phone numbers, LinkedIn, and GitHub links

## 🛠️ Installation
### 1. Clone the repository
```sh
git clone https://github.com/ProPaul25/ResumeIQ.git
cd ResumeIQ
```
### 2. Install dependencies
```sh
pip install -r requirements.txt
```
### 3. Set up your Telegram bot
- Create a bot on Telegram using [@BotFather](https://t.me/BotFather)
- Get your bot token and replace it in the script:
  ```python
  BOT_TOKEN = "your-telegram-bot-token"
  ```

### 4. Run the bot
```sh
python bot.py
```

## 📜 Usage
1. Start the bot with `/start`
2. Upload a CV in PDF or DOCX format
3. The bot processes the document and sends a structured response

## 📦 Dependencies
- `python-telegram-bot`
- `PyPDF2`
- `python-docx`
- `re` (Regular Expressions)
- `io`, `os`, `logging`

## 🏗️ Future Enhancements
- 🌍 Multi-language support
- 🎨 Improved formatting and customization options
- 🔍 AI-based skill extraction and job-matching

## 🤝 Contributing
Pull requests are welcome! Feel free to submit issues or suggest new features.

## 📜 License
MIT License

## 📬 Contact
- Telegram: [YourBotName](https://t.me/YourBotUsername)
- GitHub: [Your Repository](https://github.com/yourusername/ResumeIQ)

