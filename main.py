#!/usr/bin/env python3
"""
TikTok Hashtag Hunter Automation System

This script automates the process of searching for hashtags on the TikTok Hashtag Hunter
website and capturing screenshots of the results.

Features:
- Reads hashtag terms from CSV file
- Automates browser navigation and search
- Captures screenshots with proper labeling
- Handles errors gracefully
- Provides progress feedback
"""

import csv
import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TikTokHashtagAutomation:
    def __init__(self, csv_file_path="combined above 10k.csv", output_dir="screenshots"):
        """
        Initialize the automation system.
        
        Args:
            csv_file_path (str): Path to the CSV file containing hashtag terms
            output_dir (str): Directory to save screenshots
        """
        self.csv_file_path = csv_file_path
        self.output_dir = Path(output_dir)
        self.website_url = "https://ubiwiz.com/tiktok-hashtag-hunter"
        self.search_terms = []
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
    def load_search_terms(self):
        """Load search terms from the CSV file."""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row and len(row) > 0:
                        # Extract the hashtag term (first column)
                        hashtag = row[0].strip()
                        if hashtag:
                            self.search_terms.append(hashtag)
            
            logger.info(f"Loaded {len(self.search_terms)} search terms from {self.csv_file_path}")
            return True
            
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_file_path}")
            return False
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            return False
    
    def sanitize_filename(self, hashtag):
        """
        Create a safe filename from hashtag term.
        
        Args:
            hashtag (str): The hashtag term
            
        Returns:
            str: Safe filename
        """
        # Remove or replace problematic characters
        safe_name = hashtag.replace('#', '').replace('/', '_').replace('\\', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '-_')
        return safe_name
    
    def wait_for_search_results(self, page, timeout=10000):
        """
        Wait for search results to load on the page.
        
        Args:
            page: Playwright page object
            timeout (int): Maximum wait time in milliseconds
        """
        try:
            # Wait for any of these common elements that indicate results have loaded
            page.wait_for_function(
                """() => {
                    return document.readyState === 'complete' && 
                           (document.querySelector('[class*="result"]') || 
                            document.querySelector('[class*="data"]') || 
                            document.querySelector('table') ||
                            document.querySelector('[class*="content"]'))
                }""",
                timeout=timeout
            )
        except Exception as e:
            logger.warning(f"Timeout waiting for results, proceeding anyway: {e}")
    
    def search_and_screenshot(self, page, hashtag):
        """
        Perform search for a hashtag and take screenshot.
        
        Args:
            page: Playwright page object
            hashtag (str): Hashtag term to search for
            
        Returns:
            bool: Success status
        """
        try:
            # Clear any existing search term and input the new one
            search_selector = 'input[type="text"], input[placeholder*="hashtag"], input[placeholder*="search"]'
            
            # Try to find the search input field
            search_input = page.locator(search_selector).first
            if search_input.is_visible():
                search_input.clear()
                search_input.fill(hashtag)
                
                # Try to find and click search button or press Enter
                search_button = page.locator('button[type="submit"], button:has-text("Search"), input[type="submit"]').first
                if search_button.is_visible():
                    search_button.click()
                else:
                    # If no search button, try pressing Enter
                    search_input.press('Enter')
                
                # Wait for results to load
                self.wait_for_search_results(page)
                
                # Take screenshot
                safe_filename = self.sanitize_filename(hashtag)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = self.output_dir / f"{safe_filename}_{timestamp}.png"
                
                page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"Screenshot saved: {screenshot_path}")
                
                return True
            else:
                logger.error(f"Could not find search input field for hashtag: {hashtag}")
                return False
                
        except Exception as e:
            logger.error(f"Error searching for hashtag '{hashtag}': {e}")
            return False
    
    def run_automation(self, max_searches=None, start_index=0):
        """
        Run the complete automation process.
        
        Args:
            max_searches (int): Maximum number of searches to perform (None for all)
            start_index (int): Index to start from in the search terms list
        """
        if not self.load_search_terms():
            logger.error("Failed to load search terms. Exiting.")
            return False
        
        if start_index >= len(self.search_terms):
            logger.error(f"Start index {start_index} is beyond available terms ({len(self.search_terms)})")
            return False
        
        # Determine which terms to process
        terms_to_process = self.search_terms[start_index:]
        if max_searches:
            terms_to_process = terms_to_process[:max_searches]
        
        logger.info(f"Starting automation for {len(terms_to_process)} hashtag terms")
        logger.info(f"Target website: {self.website_url}")
        logger.info(f"Screenshots will be saved to: {self.output_dir}")
        
        with sync_playwright() as p:
            # Launch browser with appropriate settings
            browser = p.chromium.launch(
                headless=False,  # Set to True for headless mode
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            
            try:
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )
                
                page = context.new_page()
                
                # Navigate to the website
                logger.info(f"Navigating to {self.website_url}")
                page.goto(self.website_url, wait_until='domcontentloaded', timeout=30000)
                
                # Wait a bit for the page to fully load
                time.sleep(3)
                
                successful_searches = 0
                failed_searches = 0
                
                # Process each hashtag term
                for i, hashtag in enumerate(terms_to_process, start=start_index + 1):
                    logger.info(f"Processing {i}/{len(self.search_terms)}: '{hashtag}'")
                    
                    if self.search_and_screenshot(page, hashtag):
                        successful_searches += 1
                    else:
                        failed_searches += 1
                    
                    # Small delay between searches to be respectful to the server
                    time.sleep(2)
                    
                    # Progress update every 10 searches
                    if i % 10 == 0:
                        logger.info(f"Progress: {successful_searches} successful, {failed_searches} failed")
                
                logger.info(f"Automation completed!")
                logger.info(f"Total successful searches: {successful_searches}")
                logger.info(f"Total failed searches: {failed_searches}")
                
                return True
                
            except Exception as e:
                logger.error(f"Browser automation error: {e}")
                return False
            finally:
                browser.close()

def main():
    """Main function to run the automation."""
    automation = TikTokHashtagAutomation()
    
    # You can customize these parameters:
    # - max_searches: Limit number of searches (useful for testing)
    # - start_index: Start from a specific position in the CSV
    
    # For testing, start with just 5 searches
    success = automation.run_automation(max_searches=5, start_index=0)
    
    if success:
        print("Automation completed successfully!")
        print(f"Check the '{automation.output_dir}' directory for screenshots.")
        print("Check 'automation.log' for detailed logs.")
    else:
        print("Automation failed. Check 'automation.log' for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()