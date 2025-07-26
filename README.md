# Website Cloner

A comprehensive Python application for downloading and cloning websites with all their assets for offline viewing, learning, and backup purposes.

## Overview

Website Cloner is a powerful tool that downloads complete websites including HTML pages, CSS stylesheets, JavaScript files, images, fonts, and other assets while maintaining the original directory structure and converting links to work offline.

## Features

### Core Functionality
- **Complete Website Download**: Downloads HTML, CSS, JavaScript, images, fonts, videos, and documents
- **Intelligent Link Conversion**: Automatically converts absolute URLs to relative paths for offline viewing
- **Selective Asset Download**: Choose which types of files to download based on your needs
- **Directory Structure Preservation**: Maintains the original website's folder structure
- **Depth Control**: Configure how many levels deep to crawl through linked pages

### User Experience
- **Dual Interface**: Both graphical user interface and command-line interface
- **Real-time Progress**: Live progress tracking with detailed logging
- **Resumable Downloads**: Handles interrupted downloads gracefully
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Respectful Crawling
- **robots.txt Compliance**: Respects website crawling policies by default
- **Rate Limiting**: Configurable delays between requests to avoid server overload
- **Domain Restriction**: Only downloads content from the target domain
- **Error Handling**: Robust error handling and recovery

## Installation

### Prerequisites
- Python 3.7 or higher
- Internet connection
- Sufficient disk space for downloaded content

### Dependencies Installation

Install required Python packages:

```bash
pip install -r requirements_cloner.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4 lxml
```

### Quick Setup (Windows)

For Windows users, simply run the automated setup:

```bash
setup_cloner.bat
```

This script will:
1. Check Python installation
2. Install required dependencies
3. Launch the application

## Usage

### Graphical User Interface

Launch the GUI application:

```bash
python website_cloner_main.py
```

The GUI provides:
- URL input field with validation
- Output directory selection
- Crawl depth configuration (1-5 levels)
- Asset type selection checkboxes
- Advanced settings for delays and robots.txt
- Real-time progress bar and logging
- Start, stop, and folder opening controls

### Command Line Interface

For automated or scripted usage:

```bash
python website_cloner_main.py --no-gui --url <URL> [options]
```

#### Command Line Options

- `--url URL`: Target website URL to clone (required for CLI mode)
- `--output DIR`: Output directory (default: "cloned_sites")
- `--depth N`: Maximum crawl depth (default: 2)
- `--assets TYPES`: Space-separated list of asset types to download
- `--no-gui`: Enable command-line mode

#### Asset Types

Available asset types for selective downloading:

- `html`: HTML pages and documents
- `css`: Cascading Style Sheets
- `js`: JavaScript files
- `images`: Image files (JPG, PNG, GIF, SVG, etc.)
- `fonts`: Web fonts (WOFF, TTF, etc.)
- `videos`: Video files (MP4, WebM, etc.)
- `documents`: Document files (PDF, DOC, etc.)

#### Command Line Examples

Clone a single page with essential assets:
```bash
python website_cloner_main.py --no-gui --url https://example.com --depth 1 --assets html css images
```

Clone documentation with multiple levels:
```bash
python website_cloner_main.py --no-gui --url https://docs.example.com --depth 3 --output documentation
```

Clone only images from a website:
```bash
python website_cloner_main.py --no-gui --url https://gallery.example.com --assets images --depth 2
```

### Programmatic Usage

For integration into other Python projects:

```python
from website_cloner import WebsiteCloner

# Create cloner instance
cloner = WebsiteCloner()

# Configure progress callback (optional)
def progress_callback(progress):
    print(f"Downloaded: {progress.downloaded_files}/{progress.total_files}")
    print(f"Status: {progress.status}")

# Clone website
output_directory = cloner.clone_website(
    url="https://example.com",
    output_dir="my_clone",
    max_depth=2,
    asset_types=['html', 'css', 'js', 'images'],
    progress_callback=progress_callback
)

print(f"Website cloned to: {output_directory}")
```

## Configuration

### Crawl Depth Guidelines

- **Depth 1**: Single page only - good for landing pages or specific articles
- **Depth 2**: Page plus directly linked pages - recommended for most websites
- **Depth 3**: Two levels of linked pages - use for small to medium sites
- **Depth 4+**: Deep crawling - use with caution on large sites

### Respectful Crawling Settings

The application includes several features to ensure respectful website crawling:

- **Request Delays**: Default 1-second delay between requests (configurable)
- **robots.txt Checking**: Automatically checks and respects robots.txt files
- **Same-Domain Restriction**: Only downloads content from the target domain
- **User-Agent**: Identifies itself as an educational tool

### Advanced Configuration

```python
cloner = WebsiteCloner()

# Configure crawling behavior
cloner.respect_robots = True  # Respect robots.txt (default: True)
cloner.delay_between_requests = 1.5  # Delay in seconds (default: 1.0)
cloner.max_depth = 3  # Maximum crawl depth
cloner.enabled_assets = ['html', 'css', 'images']  # Asset types to download
```

## Output Structure

The cloner maintains the original website structure:

```
cloned_sites/
└── example.com/
    ├── index.html
    ├── about/
    │   └── index.html
    ├── css/
    │   ├── style.css
    │   └── theme.css
    ├── js/
    │   ├── main.js
    │   └── utils.js
    ├── images/
    │   ├── logo.png
    │   ├── banner.jpg
    │   └── icons/
    │       └── favicon.ico
    ├── fonts/
    │   └── custom.woff2
    └── clone_info.json
```

### Clone Information File

Each clone includes a `clone_info.json` file with metadata:

```json
{
  "base_url": "https://example.com",
  "base_domain": "example.com",
  "max_depth": 2,
  "enabled_assets": ["html", "css", "js", "images"],
  "downloaded_files": 45,
  "failed_files": 2,
  "clone_date": "2025-07-26 10:30:00"
}
```

## How It Works

### 1. URL Processing
- Validates and normalizes the input URL
- Extracts domain information for restriction purposes
- Checks robots.txt if compliance is enabled

### 2. Content Discovery
- Downloads HTML pages and parses with BeautifulSoup
- Extracts links to other pages for deeper crawling
- Identifies asset URLs (CSS, JavaScript, images, etc.)
- Maintains a queue of discovered URLs

### 3. Asset Downloading
- Downloads each asset type based on user selection
- Preserves the original directory structure
- Handles different content types appropriately
- Implements configurable delays between requests

### 4. Link Processing
- Converts absolute URLs to relative paths in HTML files
- Updates references to downloaded assets
- Ensures proper linking between pages and resources
- Maintains functionality for offline viewing

### 5. Progress Management
- Tracks download progress in real-time
- Logs successful downloads and failures
- Provides detailed status information
- Saves comprehensive clone metadata

## Legal and Ethical Considerations

### Responsible Usage

**Always Ensure Legal Compliance:**
- Only clone websites you have explicit permission to download
- Respect copyright laws and intellectual property rights
- Check and comply with website terms of service
- Honor robots.txt files and crawling policies

**Appropriate Use Cases:**
- Educational research and learning web development
- Creating backups of your own websites
- Academic research with proper permissions
- Offline access to publicly available documentation

**Inappropriate Use Cases:**
- Downloading copyrighted content without permission
- Commercial use of cloned content without proper rights
- Ignoring website terms of service
- Overloading servers with aggressive crawling

### Technical Considerations

**Server Impact Minimization:**
- Use appropriate delays between requests
- Respect robots.txt and crawling guidelines
- Limit crawl depth on large websites
- Monitor and respond to server errors

## Troubleshooting

### Common Issues and Solutions

**Permission Denied or 403 Forbidden Errors**
- The website may block automated access
- Check if robots.txt allows crawling
- Some sites require specific headers or authentication
- Try increasing delays between requests

**SSL Certificate Errors**
- Update Python and certificate stores
- Some websites may have invalid or expired certificates
- Try HTTP instead of HTTPS if the site supports it

**Slow Download Speeds**
- Increase delays between requests if the server is limiting speed
- Check your internet connection stability
- Some servers intentionally throttle automated downloads

**Missing Content or Assets**
- JavaScript-generated content may not be captured
- Some assets may require authentication
- Dynamic content loaded after page load may be missed
- Try including JavaScript files and increase crawl depth

**Memory or Disk Space Issues**
- Large websites can consume significant resources
- Limit asset types to essential files only
- Use smaller crawl depths for very large sites
- Ensure sufficient disk space before starting

### Performance Optimization

**For Large Websites:**
- Start with depth 1 to estimate size
- Selectively choose only necessary asset types
- Use command-line interface for better performance
- Consider running during off-peak hours

**For Better Speed:**
- Reduce delays for websites that allow faster crawling
- Disable unnecessary asset types
- Use SSD storage for better I/O performance
- Close other network-intensive applications

## Testing and Validation

### Demo Script

Test the cloner functionality with the included demo:

```bash
python demo_cloner.py
```

This script provides guided testing with safe, small websites.

### Validation Steps

1. **Test with Simple Sites**: Start with basic websites like example.com
2. **Verify Output**: Check that downloaded files open correctly in a browser
3. **Test Offline Functionality**: Disconnect from internet and browse cloned site
4. **Check Link Conversion**: Ensure internal links work properly offline

## Contributing

Contributions to improve the Website Cloner are welcome. Areas for enhancement include:

- Support for JavaScript-rendered content
- Better handling of dynamic websites
- Advanced filtering and selection options
- Performance optimizations for large sites
- Additional output formats and options
- Enhanced error recovery mechanisms

## License

This software is provided for educational and legitimate backup purposes. Users are responsible for ensuring their usage complies with applicable laws, website terms of service, and ethical guidelines.

## Disclaimer

The Website Cloner is intended for educational, research, and legitimate backup purposes only. The authors assume no responsibility for misuse of this software. Users must ensure compliance with all applicable laws, regulations, and website terms of service.

## Support

For technical issues or questions:

1. Review this documentation thoroughly
2. Check the GETTING_STARTED.md file for additional guidance
3. Test with the included demo script
4. Ensure all dependencies are properly installed

---

**Website Cloner** - Ethical website downloading for learning and backup purposes
