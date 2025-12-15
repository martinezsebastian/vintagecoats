# 🧥 Vintage Coat Finder Bot

Automated daily scraper that searches multiple sources for vintage coats and sends email notifications with new findings.

## Features

- 🔍 **Multi-source search**: eBay Kleinanzeigen, Vinted, and Google
- 📧 **Email notifications**: Beautiful HTML emails with new items
- 🤖 **Automated**: Runs daily via GitHub Actions (completely free)
- 💾 **Smart tracking**: SQLite database prevents duplicate notifications
- ⚙️ **Configurable**: Easy to customize search terms and sources

## Quick Start

### 1. Fork this Repository

Click the "Fork" button at the top right of this page to create your own copy.

### 2. Set Up Email Notifications

You'll need to configure three GitHub secrets for email notifications:

1. Go to your forked repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these three secrets:

#### For Gmail:

- **`SENDER_EMAIL`**: Your Gmail address (e.g., `yourname@gmail.com`)
- **`SENDER_PASSWORD`**: Your Gmail App Password (see below)
- **`RECIPIENT_EMAIL`**: Email where you want to receive notifications (can be the same)

#### Getting a Gmail App Password:

1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification if not already enabled
3. Go to https://myaccount.google.com/apppasswords
4. Generate an app password for "Mail"
5. Copy the 16-character password (no spaces)
6. Use this as your `SENDER_PASSWORD` secret

**Alternative email providers:**
- If you use a different email provider, you may need to modify the SMTP settings in `scraper.py`:
  - For Outlook/Hotmail: `smtp.office365.com`, port `587` (use STARTTLS)
  - For Yahoo: `smtp.mail.yahoo.com`, port `587` (use STARTTLS)
  - For custom providers: Check their SMTP documentation

### 3. Customize Your Search

Edit `config.json` to customize what you're looking for:

```json
{
  "search_terms": [
    "vintage mantel",
    "vintage coat",
    "retro mantel",
    "70s coat",
    "80s coat",
    "vintage wollmantel"
  ],
  "search_ebay_kleinanzeigen": true,
  "search_vinted": true,
  "search_google": true,
  "location": "Berlin"
}
```

**Tips for search terms:**
- Use both English and German terms if searching in Germany
- Include decade-specific terms (60s, 70s, 80s, 90s)
- Add brand names if you're looking for specific designers
- Use material terms (wool, leather, cashmere)

### 4. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. The bot will now run automatically every day at 9 AM UTC (10 AM CET)

### 5. Test It Manually

To test before waiting for the scheduled run:

1. Go to **Actions** tab
2. Click **"Daily Vintage Coat Search"** in the left sidebar
3. Click **"Run workflow"** → **"Run workflow"** button
4. Watch it run and check your email!

## How It Works

### Search Sources

1. **eBay Kleinanzeigen**: Germany's largest classifieds platform
2. **Vinted**: Popular second-hand fashion marketplace
3. **Google Search**: Catches items from smaller shops and websites

### Smart Duplicate Detection

The bot maintains a SQLite database (`seen_items.db`) that tracks:
- Item title
- URL
- Price
- Source
- Date first seen

Each item gets a unique ID (MD5 hash), so you'll only be notified once per item.

### Email Notifications

You'll receive an HTML email with:
- Number of new items found
- Title, price, and source for each item
- Direct links to view each item
- Timestamp of the search

If no new items are found, no email is sent.

## Customization

### Changing Search Schedule

Edit `.github/workflows/daily_search.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC
```

Cron schedule examples:
- `0 9 * * *` - Daily at 9 AM UTC
- `0 */12 * * *` - Every 12 hours
- `0 9 * * 1,3,5` - Mondays, Wednesdays, Fridays at 9 AM
- `0 6,18 * * *` - Daily at 6 AM and 6 PM UTC

### Adding More Search Sources

To add a new website, edit `scraper.py` and add a method like:

```python
def search_custom_site(self):
    """Search your custom website"""
    print("Searching Custom Site...")
    
    # Your scraping logic here
    url = "https://example.com/search?q=vintage+coat"
    response = requests.get(url, headers=self.headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Parse results and add to self.results
    # ...
```

Then call it in the `run()` method.

### Price Filtering

You can add price filtering by modifying the scraper to skip items outside your budget:

```python
# In each search method, before adding to results:
if item.get('price') != 'N/A':
    price_value = float(item['price'].replace('€', '').replace(',', '.').strip())
    if price_value > 200:  # Skip items over €200
        continue
```

### Location Filtering

For eBay Kleinanzeigen, you can add location parameters:

```python
search_url = f"{base_url}?keywords={term}&locationId=YOUR_CITY_ID"
```

## Troubleshooting

### Not receiving emails?

1. Check GitHub Actions logs:
   - Go to **Actions** tab → Click on latest run
   - Look for errors in the "Run vintage coat finder" step

2. Verify your secrets are set correctly:
   - Settings → Secrets → Check all three secrets exist

3. Gmail App Password issues:
   - Make sure 2FA is enabled on your Google account
   - Generate a fresh App Password
   - Use the password without spaces

### No items found?

1. Try broader search terms in `config.json`
2. Check if websites have changed their HTML structure
3. Run manually to see console output in Actions logs

### Database not persisting?

Make sure the workflow has write permissions:
- Settings → Actions → General → Workflow permissions
- Select "Read and write permissions"

## Privacy & Ethics

- **Respectful scraping**: The bot waits between requests to avoid overloading servers
- **User-Agent**: Identifies itself properly in HTTP headers
- **Terms of Service**: Make sure automated scraping is allowed on target websites
- **Rate limiting**: Built-in delays prevent abuse

## Local Development

To test locally:

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/vintage-coat-finder.git
cd vintage-coat-finder

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="where-to-send@gmail.com"

# Run the scraper
python scraper.py
```

## Cost

**Completely free!** GitHub Actions provides 2,000 free minutes per month for public repositories. This bot uses about 2-3 minutes per run, so even daily runs stay well within the free tier.

## Future Improvements

Potential enhancements:
- [ ] Add Selenium for JavaScript-heavy sites (Vinted full results)
- [ ] Image recognition to filter by style/color
- [ ] Telegram bot notifications as alternative to email
- [ ] Size filtering
- [ ] Distance calculation from your location
- [ ] Price tracking over time
- [ ] Web dashboard to view all found items

## License

MIT License - Feel free to modify and reuse!

## Contributing

Found a bug or want to add a feature? Pull requests are welcome!

---

Happy hunting! 🧥✨
