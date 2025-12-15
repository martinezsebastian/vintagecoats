#!/bin/bash

echo "============================================"
echo "Vintage Coat Finder - Setup Helper"
echo "============================================"
echo ""

echo "This script will help you set up the vintage coat finder."
echo ""

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo "Step 1: Initialize Git Repository"
    echo "-----------------------------------"
    read -p "Initialize git repo? (y/n): " init_git
    if [ "$init_git" = "y" ]; then
        git init
        git add .
        git commit -m "Initial commit: Vintage coat finder bot"
        echo "✓ Git repository initialized"
    fi
    echo ""
fi

echo "Step 2: Test Configuration"
echo "-----------------------------------"
echo "Your current search terms from config.json:"
grep "search_terms" config.json -A 10
echo ""

read -p "Do you want to customize search terms? (y/n): " customize
if [ "$customize" = "y" ]; then
    echo "Edit config.json to update your search terms"
    echo "Press enter when done..."
    read
fi
echo ""

echo "Step 3: Email Setup"
echo "-----------------------------------"
echo "For GitHub Actions, you'll need to set up secrets:"
echo ""
echo "Required secrets:"
echo "  1. SENDER_EMAIL - Your Gmail address"
echo "  2. SENDER_PASSWORD - Your Gmail App Password"
echo "  3. RECIPIENT_EMAIL - Where to receive notifications"
echo ""
echo "Getting Gmail App Password:"
echo "  1. Go to https://myaccount.google.com/security"
echo "  2. Enable 2-Step Verification"
echo "  3. Go to https://myaccount.google.com/apppasswords"
echo "  4. Create app password for 'Mail'"
echo "  5. Copy the 16-character password"
echo ""

read -p "Have you set up your Gmail App Password? (y/n): " has_password
if [ "$has_password" = "n" ]; then
    echo "⚠ Don't forget to set this up before deploying to GitHub!"
fi
echo ""

echo "Step 4: Test Locally (Optional)"
echo "-----------------------------------"
read -p "Do you want to test the scraper locally? (y/n): " test_local
if [ "$test_local" = "y" ]; then
    echo ""
    echo "Setting up local test environment..."
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        echo "✗ Python 3 is not installed. Please install it first."
        exit 1
    fi
    
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    
    echo ""
    echo "To test with email notifications, set environment variables:"
    echo "  export SENDER_EMAIL='your@gmail.com'"
    echo "  export SENDER_PASSWORD='your-app-password'"
    echo "  export RECIPIENT_EMAIL='recipient@email.com'"
    echo ""
    
    read -p "Run test suite? (y/n): " run_test
    if [ "$run_test" = "y" ]; then
        python3 test_scraper.py
    fi
fi
echo ""

echo "Step 5: Deploy to GitHub"
echo "-----------------------------------"
echo "To deploy to GitHub:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Push your code:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/vintage-coat-finder.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Set up GitHub Secrets:"
echo "   - Go to Settings → Secrets and variables → Actions"
echo "   - Add SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL"
echo ""
echo "4. Enable GitHub Actions:"
echo "   - Go to Actions tab"
echo "   - Click 'I understand my workflows, go ahead and enable them'"
echo ""
echo "5. Test the workflow:"
echo "   - Actions → Daily Vintage Coat Search → Run workflow"
echo ""

echo "============================================"
echo "Setup complete! 🎉"
echo "============================================"
echo ""
echo "Next steps:"
echo "  • Customize config.json with your search terms"
echo "  • Set up GitHub repository and secrets"
echo "  • Enable GitHub Actions"
echo "  • Wait for your first daily report (or trigger manually)!"
echo ""
echo "Need help? Check README.md for detailed instructions."
