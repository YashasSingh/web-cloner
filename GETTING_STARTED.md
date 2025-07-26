# Getting Started with Website Cloner

Welcome to Website Cloner! This guide will walk you through everything you need to know to start downloading websites safely and effectively.

## What is Website Cloner?

Website Cloner is a Python application that downloads entire websites for offline viewing. It captures HTML pages, stylesheets, JavaScript files, images, and other assets while converting links to work without an internet connection.

## Before You Begin

### System Requirements

**Minimum Requirements:**
- Python 3.7 or higher
- 2GB RAM
- 1GB free disk space
- Internet connection

**Recommended Setup:**
- Python 3.9 or higher
- 4GB RAM or more
- SSD storage for better performance
- Stable broadband internet connection

### Important Legal Notice

**You Must Have Permission**: Only clone websites you own or have explicit permission to download. Always respect:
- Copyright laws and intellectual property rights
- Website terms of service
- robots.txt files and crawling policies
- Server resources and bandwidth

## Installation

### Step 1: Verify Python Installation

Open a command prompt or terminal and check your Python version:

```bash
python --version
```

If Python is not installed or the version is below 3.7, download and install Python from [python.org](https://www.python.org/).

**Windows Users**: During installation, make sure to check "Add Python to PATH".

### Step 2: Download Website Cloner

Download all the project files to a folder on your computer, for example:
- Windows: `C:\Users\YourName\website-cloner\`
- macOS/Linux: `~/website-cloner/`

### Step 3: Install Dependencies

#### Option A: Automatic Setup (Windows)

1. Navigate to the project folder
2. Double-click `setup_cloner.bat`
3. The script will install dependencies and launch the application

#### Option B: Manual Installation

Open a command prompt/terminal in the project folder and run:

```bash
pip install -r requirements_cloner.txt
```

Or install packages individually:

```bash
pip install requests beautifulsoup4 lxml
```

### Step 4: Test Installation

Verify everything is working:

```bash
python -c "from website_cloner import WebsiteCloner; print('Installation successful!')"
```

## First Time Usage

### Starting the Application

#### Graphical Interface (Recommended for Beginners)

```bash
python website_cloner_main.py
```

This opens a user-friendly window with all options clearly labeled.

#### Command Line Interface

```bash
python website_cloner_main.py --no-gui --url https://example.com
```

### Your First Clone

Let's start with a simple, safe website:

1. **Launch the GUI**: Run `python website_cloner_main.py`
2. **Enter URL**: Type `https://example.com` in the URL field
3. **Choose Output**: Leave the default "cloned_sites" directory
4. **Set Depth**: Keep the default value of 2
5. **Select Assets**: Keep HTML, CSS, and Images checked
6. **Click "Start Cloning"**: Watch the progress in the log area

The process should complete in under a minute, creating a folder structure like:
```
cloned_sites/
└── example.com/
    ├── index.html
    └── clone_info.json
```

### Viewing Your Cloned Website

1. Navigate to the output folder
2. Open `index.html` in your web browser
3. The website should display and function offline

## Understanding the Interface

### GUI Components

**URL Input Section:**
- **URL Field**: Enter the website address to clone
- **Validation**: Automatically adds "https://" if missing

**Output Settings:**
- **Output Directory**: Where files will be saved
- **Browse Button**: Select a custom location

**Clone Settings:**
- **Maximum Depth**: How many levels of links to follow
  - 1 = Single page only
  - 2 = Page + direct links (recommended)
  - 3+ = Deeper crawling (use carefully)

**Asset Selection:**
- **HTML Pages**: The actual web pages
- **CSS Stylesheets**: Styling and layout files
- **JavaScript Files**: Interactive functionality
- **Images**: Photos, graphics, icons
- **Fonts**: Custom typography files
- **Videos**: Media content
- **Documents**: PDFs and other files

**Advanced Settings:**
- **Respect robots.txt**: Honor website crawling policies (recommended)
- **Request Delay**: Time between downloads (1 second default)

### Progress Monitoring

**Progress Bar**: Visual indicator of overall completion
**Status Label**: Current operation description
**Log Area**: Detailed download information
**Status Bar**: File count and statistics

## Common Usage Scenarios

### Scenario 1: Learning Web Development

**Goal**: Study how websites are built
**Settings**:
- Depth: 1-2
- Assets: HTML, CSS, JavaScript
- Target: Well-designed websites you admire

**Example**:
```bash
python website_cloner_main.py --no-gui --url https://developer.mozilla.org --depth 2 --assets html css js
```

### Scenario 2: Creating Documentation Backup

**Goal**: Offline access to technical documentation
**Settings**:
- Depth: 3-4
- Assets: HTML, CSS, Images
- Target: Official documentation sites

**Example**:
```bash
python website_cloner_main.py --no-gui --url https://docs.python.org --depth 3 --output python_docs
```

### Scenario 3: Website Backup

**Goal**: Backup your own website
**Settings**:
- Depth: 4-5 (or as needed)
- Assets: All types
- Target: Your own website

**Example**:
```bash
python website_cloner_main.py --no-gui --url https://mywebsite.com --depth 4 --assets html css js images fonts
```

### Scenario 4: Research and Analysis

**Goal**: Academic research on web design
**Settings**:
- Depth: 2
- Assets: HTML, CSS
- Target: Websites relevant to your research

## Best Practices

### Choosing Appropriate Targets

**Good Candidates:**
- Static websites with clear navigation
- Documentation and educational sites
- Personal blogs and portfolios
- Your own websites

**Avoid These:**
- Large e-commerce platforms
- Social media sites
- Sites requiring login
- Heavily JavaScript-dependent applications

### Setting Appropriate Depth

**Depth 1**: Perfect for single-page analysis or very focused content
**Depth 2**: Ideal for most websites, captures main content without being excessive
**Depth 3**: Use for thorough documentation or small to medium sites
**Depth 4+**: Only for comprehensive backups of your own sites

### Selecting Asset Types

**Essential Combination**: HTML + CSS + Images
- Provides complete visual experience
- Maintains layout and appearance
- Includes all graphic content

**Development Study**: HTML + CSS + JavaScript
- Shows complete functionality
- Useful for learning interactive elements
- May not work perfectly offline

**Minimal Backup**: HTML only
- Fastest download
- Text content preserved
- Basic structure maintained

### Managing Download Size

**Before Starting:**
- Estimate website size by browsing manually
- Start with depth 1 to test
- Check available disk space

**During Download:**
- Monitor progress and file counts
- Stop if downloads seem excessive
- Check log for unusual activity

**After Completion:**
- Review downloaded content
- Clean up unnecessary files
- Compress folders for storage

## Troubleshooting Guide

### Installation Issues

**"Python not found" Error:**
1. Install Python from python.org
2. Ensure "Add to PATH" was selected during installation
3. Restart command prompt/terminal
4. Try `python3` instead of `python` on macOS/Linux

**"pip not found" Error:**
1. Python installation may be incomplete
2. Try `python -m pip install` instead of `pip install`
3. Reinstall Python with all components

**"Permission denied" Error:**
1. Run command prompt as administrator (Windows)
2. Use `pip install --user` to install for current user only
3. Check antivirus software blocking installation

### Download Issues

**"robots.txt disallows" Error:**
1. Uncheck "Respect robots.txt" in GUI
2. Add `--no-robots` flag in command line
3. Ensure you have permission to clone the site

**"SSL Certificate" Error:**
1. Try HTTP instead of HTTPS if available
2. Update Python and certificates
3. Use `--ignore-ssl` flag if available

**"Connection timeout" Error:**
1. Check internet connection
2. Increase request delay
3. Try again later when server is less busy

**"403 Forbidden" or "Access Denied":**
1. Website blocks automated access
2. Try different user agent
3. Reduce request frequency
4. Check if login is required

### Performance Issues

**Very Slow Downloads:**
1. Increase delay between requests
2. Check internet connection speed
3. Server may be intentionally throttling

**Running Out of Disk Space:**
1. Choose more selective asset types
2. Reduce crawl depth
3. Use external storage drive

**Application Freezing:**
1. Reduce crawl depth
2. Close other applications
3. Restart and try smaller chunks

## Advanced Usage Tips

### Command Line Automation

Create batch scripts for repeated tasks:

**Windows batch file (clone_docs.bat):**
```batch
@echo off
python website_cloner_main.py --no-gui --url %1 --depth 2 --assets html css images --output documentation
```

**Linux/macOS script (clone_docs.sh):**
```bash
#!/bin/bash
python website_cloner_main.py --no-gui --url "$1" --depth 2 --assets html css images --output documentation
```

### Selective Content Download

**Download only images:**
```bash
python website_cloner_main.py --no-gui --url https://gallery.example.com --assets images --depth 2
```

**Download only documentation:**
```bash
python website_cloner_main.py --no-gui --url https://docs.example.com --assets html css --depth 3
```

### Integration with Other Tools

**Schedule regular backups** using system cron jobs or Task Scheduler
**Combine with version control** to track changes over time
**Use with web servers** to serve cloned content locally

## Understanding Output

### File Organization

The cloner preserves the original website structure:

**Original URL**: `https://example.com/docs/guide.html`
**Local Path**: `cloned_sites/example.com/docs/guide.html`

**Original URL**: `https://example.com/css/style.css`
**Local Path**: `cloned_sites/example.com/css/style.css`

### Link Conversion

**Before (in original HTML):**
```html
<link href="https://example.com/css/style.css" rel="stylesheet">
<img src="https://example.com/images/logo.png" alt="Logo">
```

**After (in cloned HTML):**
```html
<link href="css/style.css" rel="stylesheet">
<img src="images/logo.png" alt="Logo">
```

### Clone Information

Each clone includes a `clone_info.json` file with details:
- Original URL and domain
- Clone settings used
- Number of files downloaded
- List of failed downloads
- Timestamp of clone operation

## Next Steps

### Expanding Your Skills

1. **Experiment with Different Sites**: Try various types of websites to understand different challenges
2. **Learn Web Technologies**: Understanding HTML, CSS, and JavaScript helps interpret results
3. **Study Cloned Sites**: Compare original and cloned versions to understand the process
4. **Automate Common Tasks**: Create scripts for frequently cloned sites

### Contributing to the Project

The Website Cloner project welcomes contributions:
- Report bugs and issues
- Suggest new features
- Improve documentation
- Add support for new content types

### Staying Legal and Ethical

- Always check website terms of service
- Respect copyright and intellectual property
- Use reasonable crawling speeds
- Give credit when using cloned content for learning

## Getting Help

### Resources Available

1. **This Getting Started Guide**: Comprehensive introduction
2. **README.md**: Complete technical documentation
3. **Demo Script**: `python demo_cloner.py` for testing
4. **Example Sites**: Start with example.com for safe testing

### Self-Help Checklist

Before seeking help:
1. Read error messages carefully
2. Check system requirements
3. Verify internet connection
4. Try with a simpler website first
5. Review the troubleshooting section

---

**You're now ready to start using Website Cloner effectively and responsibly!**

Remember: The key to successful website cloning is starting small, understanding your target, and always respecting the website owner's rights and server resources.
