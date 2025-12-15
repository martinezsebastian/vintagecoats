#!/usr/bin/env python3
"""
Test script for vintage coat finder
Run this locally to verify everything works before deploying to GitHub Actions
"""

import os
import sys
from scraper import VintageCoatFinder

def test_database():
    """Test database creation and operations"""
    print("Testing database...")
    finder = VintageCoatFinder()
    
    # Test item
    test_item = {
        'id': 'test123',
        'title': 'Test Vintage Coat',
        'url': 'https://example.com/test',
        'price': '€50',
        'source': 'Test'
    }
    
    # Test marking as seen
    finder.mark_item_seen(test_item)
    assert finder.is_item_seen('test123'), "Failed to mark item as seen"
    
    print("✓ Database tests passed")

def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    finder = VintageCoatFinder()
    
    assert 'search_terms' in finder.config, "Missing search_terms in config"
    assert len(finder.config['search_terms']) > 0, "No search terms configured"
    
    print(f"✓ Config loaded successfully")
    print(f"  Search terms: {finder.config['search_terms']}")

def test_email_config():
    """Test email configuration"""
    print("Testing email configuration...")
    
    sender = os.environ.get('SENDER_EMAIL')
    password = os.environ.get('SENDER_PASSWORD')
    recipient = os.environ.get('RECIPIENT_EMAIL')
    
    if not all([sender, password, recipient]):
        print("⚠ Warning: Email not configured")
        print("  Set these environment variables to test email:")
        print("  - SENDER_EMAIL")
        print("  - SENDER_PASSWORD")
        print("  - RECIPIENT_EMAIL")
        return False
    
    print("✓ Email configuration found")
    print(f"  Sender: {sender}")
    print(f"  Recipient: {recipient}")
    return True

def test_search_dry_run():
    """Test search without actually making requests"""
    print("Testing search structure...")
    finder = VintageCoatFinder()
    
    # Check methods exist
    assert hasattr(finder, 'search_ebay_kleinanzeigen'), "Missing eBay Kleinanzeigen search"
    assert hasattr(finder, 'search_vinted'), "Missing Vinted search"
    assert hasattr(finder, 'search_google'), "Missing Google search"
    
    print("✓ All search methods present")

def main():
    """Run all tests"""
    print("=" * 50)
    print("Vintage Coat Finder - Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_config()
        print()
        
        test_database()
        print()
        
        test_search_dry_run()
        print()
        
        email_configured = test_email_config()
        print()
        
        print("=" * 50)
        print("All basic tests passed! ✓")
        print("=" * 50)
        print()
        
        if email_configured:
            response = input("Email is configured. Run actual search? (y/n): ")
            if response.lower() == 'y':
                print("\nRunning actual search...")
                finder = VintageCoatFinder()
                finder.run()
        else:
            print("Skipping actual search (email not configured)")
            print("\nTo test with email:")
            print("1. Set environment variables:")
            print("   export SENDER_EMAIL='your@gmail.com'")
            print("   export SENDER_PASSWORD='your-app-password'")
            print("   export RECIPIENT_EMAIL='recipient@email.com'")
            print("2. Run: python test_scraper.py")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
