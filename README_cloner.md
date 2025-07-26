# Website Cloner

A powerful Python application for cloning websites and downloading all their assets for offline viewing, learning, or backup purposes.

## Features

- **Complete Website Download**: Downloads HTML, CSS, JavaScript, images, fonts, and other assets
- **Intelligent Link Conversion**: Converts absolute URLs to relative paths for offline viewing
- **Selective Asset Download**: Choose which types of files to download (HTML, CSS, JS, images, etc.)
- **Depth Control**: Set how deep to crawl through linked pages
- **Respectful Crawling**: Respects robots.txt and includes configurable delays
- **Progress Tracking**: Real-time progress updates with detailed logging
- **GUI and CLI**: Both graphical and command-line interfaces
- **Resume Capability**: Handles interrupted downloads gracefully
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

1. **Download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements_cloner.txt
   ```

### Required Dependencies

- `requests` - HTTP library for downloading content
- `beautifulsoup4` - HTML parsing and manipulation
- `lxml` - Fast XML and HTML parsing
- `urllib3` - URL handling utilities

## Usage

### GUI Mode (Recommended)

```bash
python website_cloner_main.py
```

The GUI provides an easy-to-use interface with:
- URL input field
- Output directory selection
- Crawl depth settings
- Asset type selection (HTML, CSS, JS, images, fonts, videos, documents)
- Advanced settings (robots.txt respect, request delays)
- Real-time progress tracking
- Detailed logging

### Command Line Mode

```bash
python website_cloner_main.py --no-gui --url https://example.com --output my_clone --depth 2
```

#### Command Line Options

- `--url URL`: Website URL to clone
- `--output DIR`: Output directory (default: cloned_sites)
- `--depth N`: Maximum crawl depth (default: 2)
- `--assets TYPES`: Asset types to download (default: html css js images)
- `--no-gui`: Run in command-line mode

#### Examples

```bash
# Clone a single page with all assets
python website_cloner_main.py --no-gui --url https://example.com --depth 1

# Clone with specific asset types
python website_cloner_main.py --no-gui --url https://example.com --assets html css images

# Clone to specific directory
python website_cloner_main.py --no-gui --url https://example.com --output ./my_websites/example
```

### Programmatic Usage

```python
from website_cloner import WebsiteCloner

cloner = WebsiteCloner()

def progress_callback(progress):
    print(f"Downloaded: {progress.downloaded_files}, Status: {progress.status}")

# Clone a website
output_dir = cloner.clone_website(
    url="https://example.com",
    output_dir="cloned_sites",
    max_depth=2,
    asset_types=['html', 'css', 'js', 'images'],
    progress_callback=progress_callback
)

print(f"Website cloned to: {output_dir}")
```

## How It Works

### 1. URL Analysis
- Parses the input URL and extracts domain information
- Checks robots.txt if respect_robots is enabled
- Validates the URL and prepares for crawling

### 2. Content Discovery
- Downloads HTML pages and parses them with BeautifulSoup
- Extracts links to other pages (for deeper crawling)
- Identifies asset URLs (CSS, JS, images, etc.)
- Maintains a queue of URLs to process

### 3. Asset Download
- Downloads each asset type based on user selection
- Preserves original directory structure
- Handles different content types appropriately
- Implements respectful delays between requests

### 4. Link Conversion
- Converts absolute URLs to relative paths
- Updates HTML files to work offline
- Maintains proper linking between pages and assets
- Ensures all downloaded content is accessible

### 5. Progress Tracking
- Provides real-time updates on download progress
- Logs successful downloads and failures
- Saves clone information for future reference

## Asset Types

The cloner can download various types of web assets:

### Supported Asset Types

- **HTML**: Web pages (.html, .htm, .php, .asp, .aspx, .jsp)
- **CSS**: Stylesheets (.css)
- **JavaScript**: Scripts (.js)
- **Images**: Graphics (.jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico)
- **Fonts**: Web fonts (.woff, .woff2, .ttf, .eot, .otf)
- **Videos**: Media files (.mp4, .webm, .ogg, .avi, .mov)
- **Documents**: Files (.pdf, .doc, .docx, .txt, .rtf)

## Configuration Options

### Crawl Depth
- **1**: Single page only
- **2**: Page + directly linked pages
- **3+**: Deeper crawling (use with caution)

### Respectful Crawling
- **robots.txt**: Respects website crawling policies
- **Delays**: Configurable delays between requests (default: 1 second)
- **Domain Restriction**: Only downloads from the same domain

### Output Structure
```
cloned_sites/
└── example.com/
    ├── index.html
    ├── about.html
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    ├── images/
    │   ├── logo.png
    │   └── banner.jpg
    └── clone_info.json
```

## Legal and Ethical Considerations

### Always Respect:
- **Copyright Laws**: Only clone content you have permission to download
- **robots.txt**: The tool respects robots.txt by default
- **Terms of Service**: Check website terms before cloning
- **Server Load**: Use appropriate delays to avoid overwhelming servers

### Appropriate Use Cases:
- **Learning**: Studying web development techniques
- **Backup**: Creating backups of your own websites
- **Research**: Academic research with proper permissions
- **Development**: Creating offline development environments

### Inappropriate Use Cases:
- **Copyright Infringement**: Copying protected content without permission
- **Commercial Use**: Using cloned content for commercial purposes without rights
- **Overloading Servers**: Aggressive crawling that impacts website performance

## Troubleshooting

### Common Issues

**"Permission Denied" or "Access Forbidden"**
- Website blocks automated access
- Try enabling robots.txt respect
- Some sites require specific headers or authentication

**"SSL Certificate Error"**
- Update your Python certificates
- Try HTTP instead of HTTPS if appropriate
- Check if the website has valid SSL

**"Downloads are Slow"**
- Increase delay between requests
- Check your internet connection
- Some servers limit download speed

**"Missing Assets"**
- Some assets may be loaded dynamically with JavaScript
- Try including JavaScript files in download
- Some content may only be available to authenticated users

### Performance Tips

- Use smaller crawl depths for large websites
- Disable unnecessary asset types to speed up cloning
- Close other network-heavy applications
- Use SSD storage for better I/O performance

## Demo

Try the demo script to see the cloner in action:

```bash
python demo_cloner.py
```

This will guide you through cloning a test website and demonstrate the main features.

## Contributing

Contributions are welcome! Areas for improvement:

- Support for JavaScript-rendered content
- Better handling of dynamic websites
- Advanced filtering options
- Performance optimizations
- Additional output formats

## License

This project is for educational and legitimate backup purposes. Please respect copyright laws and website terms of service.

## Disclaimer

This tool is provided for educational and legitimate backup purposes only. Users are responsible for ensuring their use complies with applicable laws, website terms of service, and ethical guidelines. The authors are not responsible for any misuse of this software.

---

**Website Cloner** - Your tool for ethical website downloading and learning!
