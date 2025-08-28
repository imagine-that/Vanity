# Vanity - TikTok Hashtag Hunter Automation

An automated system for searching TikTok hashtags on the [TikTok Hashtag Hunter](https://ubiwiz.com/tiktok-hashtag-hunter) website and capturing screenshots of the results.

## Features

- **Automated Browser Control**: Uses Playwright for reliable browser automation
- **CSV-Based Input**: Reads hashtag terms from the included CSV file
- **Smart Screenshot Capture**: Takes full-page screenshots with proper labeling
- **Batch Processing**: Process hashtags in configurable batches
- **Error Handling**: Robust error handling with detailed logging
- **Progress Tracking**: Real-time progress updates and comprehensive logs

## Quick Start

### 1. Setup

```bash
# Install dependencies and browsers
./setup.sh
```

### 2. Test Run (Recommended First)

```bash
# Test with 3 hashtags
python run_automation.py --mode test --num-tests 3
```

### 3. Batch Processing

```bash
# Process 20 hashtags starting from the beginning
python run_automation.py --mode batch --start-index 0 --batch-size 20

# Process the next 20 hashtags
python run_automation.py --mode batch --start-index 20 --batch-size 20
```

### 4. Full Processing (Use with Caution)

```bash
# Process all 290 hashtags (will take a long time!)
python run_automation.py --mode full
```

## Files Structure

```
├── main.py                    # Main automation script
├── run_automation.py          # Configuration and batch runner
├── setup.sh                   # Setup script
├── requirements.txt           # Python dependencies
├── combined above 10k.csv     # Hashtag terms (290 entries)
├── screenshots/               # Output directory for screenshots
└── automation.log             # Detailed execution logs
```

## CSV File Format

The system reads from `combined above 10k.csv` which contains:
- **Column 1**: Hashtag terms (e.g., "achievements", "acrobatics")
- **Column 2**: Usage counts (informational only)

## Output

### Screenshots
- Saved in `screenshots/` directory
- Named format: `{hashtag}_{timestamp}.png`
- Full-page screenshots for complete result capture

### Logs
- Real-time console output
- Detailed logs in `automation.log`
- Progress tracking and error reporting

## Configuration Options

### Command Line Arguments

```bash
python run_automation.py [options]

Options:
  --mode {test,full,batch}   Automation mode (default: test)
  --num-tests N             Number of hashtags for test mode (default: 3)
  --start-index N           Starting index for batch mode (default: 0)
  --batch-size N            Batch size for batch mode (default: 10)
```

### Direct Script Usage

```python
from main import TikTokHashtagAutomation

# Create automation instance
automation = TikTokHashtagAutomation()

# Run with custom parameters
automation.run_automation(
    max_searches=10,     # Limit number of searches
    start_index=50       # Start from index 50
)
```

## Technical Details

### Browser Settings
- Uses Chromium browser with Playwright
- Viewport: 1920x1080 for consistent screenshots
- Non-headless mode for transparency (configurable)
- Anti-detection measures included

### Error Handling
- Automatic retry for failed searches
- Graceful handling of network issues
- Detailed error logging for troubleshooting

### Performance Considerations
- 2-second delay between searches (respectful to server)
- Configurable batch processing for large datasets
- Memory-efficient CSV processing

## Troubleshooting

### Common Issues

1. **Browser Installation Issues**
   ```bash
   playwright install chromium
   ```

2. **Permission Errors**
   ```bash
   chmod +x setup.sh
   ```

3. **Network Issues**
   - Check internet connection
   - Verify website accessibility
   - Review logs for specific errors

### Log Analysis
Check `automation.log` for detailed execution information:
- Search success/failure rates
- Screenshot save confirmations
- Error details and stack traces

## Safety Features

- **Rate Limiting**: Built-in delays between requests
- **Batch Processing**: Avoid overwhelming the target website
- **Error Recovery**: Continue processing after individual failures
- **Resource Cleanup**: Proper browser and resource management

## Customization

### Modify Target Website
Edit the `website_url` in `main.py`:
```python
self.website_url = "https://your-target-website.com"
```

### Change Screenshot Settings
Modify screenshot parameters in the `search_and_screenshot` method:
```python
page.screenshot(
    path=str(screenshot_path), 
    full_page=True,           # Change to False for viewport only
    quality=90                # JPEG quality (if using JPEG format)
)
```

### Adjust Wait Times
Modify delays in the automation:
```python
time.sleep(2)  # Change delay between searches
timeout=30000  # Change page load timeout
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided as-is for educational and automation purposes. Please respect the target website's terms of service and rate limits.