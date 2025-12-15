# 🚀 Quick Start Guide

Get your vintage coat finder running in 5 minutes!

## Prerequisites

- GitHub account
- Gmail account (or other email provider)

## Step-by-Step Setup

### 1️⃣ Fork or Create Repository (2 minutes)

**Option A: Fork this repo**
- Click "Fork" button (top right)
- Clone to your computer

**Option B: Create new repo**
```bash
# On GitHub: Create new repository called "vintage-coat-finder"
git clone https://github.com/YOUR_USERNAME/vintage-coat-finder.git
cd vintage-coat-finder

# Copy all files from this project into your repo
git add .
git commit -m "Initial setup"
git push
```

### 2️⃣ Get Gmail App Password (2 minutes)

1. Visit: https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already on)
3. Visit: https://myaccount.google.com/apppasswords
4. Select app: **Mail**, device: **Other** (name it "Vintage Coat Bot")
5. Click **Generate**
6. **Copy the 16-character password** (you'll need this next)

### 3️⃣ Configure GitHub Secrets (1 minute)

1. In your GitHub repo: **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** for each:

   | Name | Value | Example |
   |------|-------|---------|
   | `SENDER_EMAIL` | Your Gmail | `yourname@gmail.com` |
   | `SENDER_PASSWORD` | App password from step 2 | `abcd efgh ijkl mnop` |
   | `RECIPIENT_EMAIL` | Where to send emails | `yourname@gmail.com` |

3. Click **Add secret** for each

### 4️⃣ Customize Your Search (Optional)

Edit `config.json`:

```json
{
  "search_terms": [
    "vintage mantel",
    "vintage wool coat",
    "retro mantel",
    "70s coat"
  ]
}
```

Commit and push:
```bash
git add config.json
git commit -m "Customize search terms"
git push
```

### 5️⃣ Enable and Test (1 minute)

1. Go to **Actions** tab in your repo
2. Click **"I understand my workflows, go ahead and enable them"**
3. Click **"Daily Vintage Coat Search"** (left sidebar)
4. Click **"Run workflow"** → **"Run workflow"** (green button)
5. Wait ~1 minute
6. **Check your email!** 📧

## What Happens Next?

- Bot runs **automatically every day at 9 AM UTC** (10 AM CET / 11 AM CEST)
- You'll get an **email only if new items are found**
- Database tracks seen items (no duplicate notifications)

## Customization

### Change Run Time

Edit `.github/workflows/daily_search.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * *'  # Change this
```

**Common schedules:**
- `0 6 * * *` - 6 AM UTC (7 AM CET)
- `0 12 * * *` - 12 PM UTC (1 PM CET)
- `0 18 * * *` - 6 PM UTC (7 PM CET)
- `0 */6 * * *` - Every 6 hours

### Add More Search Terms

Just edit `config.json` and push:

```json
{
  "search_terms": [
    "vintage mantel",
    "vintage coat",
    "vintage wollmantel",
    "retro jacke",
    "70s coat",
    "80s mantel",
    "vintage trenchcoat",
    "vintage peacoat"
  ]
}
```

## Troubleshooting

### No email received?

1. Check **Actions** tab for errors
2. Verify secrets are spelled correctly
3. Check spam folder
4. Try sending a test email from Gmail to verify credentials

### "No new items found"?

- This is normal! It means the bot found items but they were already in the database
- Try clearing the database: Delete `seen_items.db` and push

### Want to reset everything?

```bash
# Delete database to start fresh
git rm seen_items.db
git commit -m "Reset database"
git push
```

## Tips for Best Results

🎯 **Search terms:** Use mix of English/German, decades, brands
📍 **Location:** Add city name to search terms for local results
💰 **Price range:** Add "under €100" or "günstig" to filter
🔍 **Specificity:** "vintage camel wool coat" > "vintage coat"

## Support

- **Issues?** Check full README.md
- **Questions?** Open a GitHub issue
- **Ideas?** Pull requests welcome!

---

**That's it!** You now have a personal vintage coat hunting assistant. 🧥✨

Happy hunting! The bot is now working 24/7 to find your perfect vintage coat.
