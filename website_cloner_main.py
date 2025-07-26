#!/usr/bin/env python3
"""
Website Cloner

A Python application that helps clone websites by downloading HTML, CSS, JavaScript,
images, and other assets while maintaining the directory structure and converting
links to work locally.

Features:
- Download complete websites with all assets
- Maintain original directory structure
- Convert absolute URLs to relative paths
- Selective downloading (choose specific file types)
- Respect robots.txt and rate limiting
- GUI and command-line interfaces
- Resume interrupted downloads

Usage:
    python main.py

"""

import tkinter as tk
from website_cloner_gui import WebsiteClonerGUI
import sys
import argparse
from website_cloner import WebsiteCloner

def main():
    """Main entry point for the Website Cloner"""
    parser = argparse.ArgumentParser(description='Clone websites for offline viewing')
    parser.add_argument('--url', help='URL to clone')
    parser.add_argument('--output', help='Output directory')
    parser.add_argument('--depth', type=int, default=2, help='Maximum crawl depth (default: 2)')
    parser.add_argument('--no-gui', action='store_true', help='Run in command-line mode')
    parser.add_argument('--assets', nargs='+', default=['html', 'css', 'js', 'images'], 
                       help='Asset types to download (html, css, js, images, fonts, videos)')
    
    args = parser.parse_args()
    
    if args.no_gui and args.url:
        # Command-line mode
        print("Website Cloner - Command Line Mode")
        print("=" * 40)
        
        cloner = WebsiteCloner()
        cloner.clone_website(
            url=args.url,
            output_dir=args.output or 'cloned_sites',
            max_depth=args.depth,
            asset_types=args.assets
        )
    else:
        # GUI mode
        try:
            root = tk.Tk()
            app = WebsiteClonerGUI(root)
            
            print("Website Cloner Started")
            print("=" * 30)
            print("Enter a URL and click 'Start Cloning' to begin")
            print("The application will download the website and all its assets")
            print()
            
            root.mainloop()
            
        except Exception as e:
            print(f"Error starting GUI: {e}")
            print("Try running with --no-gui flag for command-line mode")
            sys.exit(1)

if __name__ == "__main__":
    main()
