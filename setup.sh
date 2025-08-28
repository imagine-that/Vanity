#!/bin/bash
"""
Setup script for TikTok Hashtag Hunter Automation

This script installs all necessary dependencies for the automation system.
"""

echo "Setting up TikTok Hashtag Hunter Automation..."

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

echo "Setup complete!"
echo ""
echo "Usage examples:"
echo "  python main.py                    # Run test with 5 hashtags"
echo "  python run_automation.py --mode test --num-tests 3    # Test with 3 hashtags"
echo "  python run_automation.py --mode batch --start-index 0 --batch-size 20    # Process 20 hashtags starting from index 0"
echo "  python run_automation.py --mode full    # Process all hashtags (use with caution)"
echo ""
echo "Screenshots will be saved in the 'screenshots/' directory"
echo "Logs will be saved in 'automation.log'"