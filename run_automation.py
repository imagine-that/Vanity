#!/usr/bin/env python3
"""
Configuration and utility script for TikTok Hashtag Hunter Automation

This script provides easy ways to run the automation with different settings.
"""

import argparse
import sys
from main import TikTokHashtagAutomation

def run_full_automation():
    """Run automation for all hashtags in the CSV."""
    automation = TikTokHashtagAutomation()
    return automation.run_automation()

def run_test_automation(num_tests=3):
    """Run automation for a small number of hashtags for testing."""
    automation = TikTokHashtagAutomation()
    return automation.run_automation(max_searches=num_tests, start_index=0)

def run_batch_automation(start_index, batch_size):
    """Run automation for a specific batch of hashtags."""
    automation = TikTokHashtagAutomation()
    return automation.run_automation(max_searches=batch_size, start_index=start_index)

def main():
    parser = argparse.ArgumentParser(description='TikTok Hashtag Hunter Automation')
    parser.add_argument('--mode', choices=['test', 'full', 'batch'], default='test',
                        help='Automation mode (default: test)')
    parser.add_argument('--num-tests', type=int, default=3,
                        help='Number of hashtags to test (test mode only)')
    parser.add_argument('--start-index', type=int, default=0,
                        help='Starting index for batch mode')
    parser.add_argument('--batch-size', type=int, default=10,
                        help='Batch size for batch mode')
    
    args = parser.parse_args()
    
    print(f"Running automation in {args.mode} mode...")
    
    if args.mode == 'test':
        success = run_test_automation(args.num_tests)
    elif args.mode == 'full':
        success = run_full_automation()
    elif args.mode == 'batch':
        success = run_batch_automation(args.start_index, args.batch_size)
    
    if success:
        print("Automation completed successfully!")
    else:
        print("Automation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()