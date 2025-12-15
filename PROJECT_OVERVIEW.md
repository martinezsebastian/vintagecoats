# 🧥 Vintage Coat Finder Bot - Project Overview

## What You've Got

A fully functional automated web scraper that:
- Searches eBay Kleinanzeigen, Vinted, and Google daily
- Sends beautiful email notifications for new vintage coats
- Runs completely free on GitHub Actions (no server needed!)
- Tracks items to prevent duplicate notifications
- Is fully customizable and extensible

## 📁 Project Structure

```
vintage_coat_finder/
│
├── scraper.py                    # Main bot logic (web scraping + email)
├── config.json                   # Your search terms and settings
├── requirements.txt              # Python dependencies
├── test_scraper.py              # Test suite for local testing
├── setup.sh                      # Setup helper script
│
├── .github/
│   └── workflows/
│       └── daily_search.yml     # GitHub Actions workflow (daily automation)
│
├── README.md                     # Full documentation
├── QUICKSTART.md                 # 5-minute setup guide
├── email_example.html           # Preview of email notifications
├── .env.example                 # Template for local testing
├── .gitignore                   # Git ignore rules
│
└── seen_items.db                # SQLite database (auto-created on first run)
```

## 🚀 How to Deploy

### Quick Version (5 minutes)
1. Read `QUICKSTART.md`
2. Push to GitHub
3. Set up 3 secrets (email config)
4. Enable GitHub Actions
5. Done!

### Detailed Version
See `README.md` for comprehensive instructions, troubleshooting, and customization options.

## 📧 Email Configuration

You need 3 GitHub Secrets:
- `SENDER_EMAIL` - Your Gmail address
- `SENDER_PASSWORD` - Gmail App Password (not your regular password!)
- `RECIPIENT_EMAIL` - Where to send notifications

**Get Gmail App Password:** https://myaccount.google.com/apppasswords

## 🎯 Customization

### Search Terms
Edit `config.json`:
```json
{
  "search_terms": [
    "vintage mantel",
    "vintage coat",
    "70s coat"
  ]
}
```

### Run Schedule
Edit `.github/workflows/daily_search.yml`:
```yaml
cron: '0 9 * * *'  # Daily at 9 AM UTC
```

### Add New Websites
Edit `scraper.py` - add methods like `search_your_site()`

## 🔧 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SENDER_EMAIL="your@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="recipient@email.com"

# Run test suite
python test_scraper.py

# Or run directly
python scraper.py
```

## 📊 How It Works

1. **GitHub Actions** triggers daily (or manually)
2. **Scraper** searches multiple sources for your terms
3. **Database** checks if items have been seen before
4. **Email** sends notification with new items only
5. **Database** updates with new items
6. **Repeat** tomorrow!

## 💰 Cost Breakdown

**Totally FREE!**
- GitHub Actions: 2,000 free minutes/month (you'll use ~60-90)
- Email: Free with Gmail
- Storage: GitHub repo (free)

## 🎨 Features

✅ Multi-source search (eBay Kleinanzeigen, Vinted, Google)
✅ Smart duplicate detection (SQLite database)
✅ Beautiful HTML email notifications
✅ Configurable search terms
✅ Adjustable run schedule
✅ Retry logic for failed requests
✅ Error handling and logging
✅ Easy to extend with new sources

## 🚧 Future Enhancements

Want to add more features? Here are ideas:

- **Selenium integration** - For JavaScript-heavy sites (full Vinted results)
- **Price filtering** - Only notify for items under €X
- **Image analysis** - Filter by color/style using AI
- **Telegram notifications** - Alternative to email
- **Size filtering** - Match your size preferences
- **Distance calculation** - Show items near you
- **Web dashboard** - View all found items in browser
- **Multiple search configs** - Different terms for different items

## 🤝 Contributing

This is your personal bot, but if you make improvements:
1. Fork the repo
2. Make changes
3. Submit pull request
4. Share with the community!

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `scraper.py` | Core bot - searching, database, email |
| `config.json` | Your search settings |
| `daily_search.yml` | GitHub Actions automation |
| `test_scraper.py` | Local testing tools |
| `setup.sh` | Interactive setup helper |
| `README.md` | Complete documentation |
| `QUICKSTART.md` | Fast setup guide |
| `email_example.html` | Email preview |
| `.env.example` | Local config template |

## 🐛 Common Issues

### No email received
→ Check Actions logs, verify secrets, check spam folder

### No items found
→ Normal if items were already seen, try clearing database

### Scraping errors
→ Websites may change HTML, update selectors in scraper.py

### Rate limiting
→ Reduce search frequency or add delays

## 📚 Learn More

- **GitHub Actions Docs:** https://docs.github.com/actions
- **BeautifulSoup Tutorial:** https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Web Scraping Ethics:** Be respectful, check robots.txt, add delays

## 🎉 You're Ready!

Everything is set up and ready to deploy. Just:
1. Push to GitHub
2. Configure secrets
3. Enable Actions
4. Wait for your first vintage coat!

Questions? Check README.md or open a GitHub issue.

Happy hunting! 🧥✨

---

**Created with ❤️ for vintage coat enthusiasts**
