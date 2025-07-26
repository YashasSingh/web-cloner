#!/usr/bin/env python3
"""
Website Cloner Demo

Demonstrates how to use the website cloner programmatically.
"""

from website_cloner import WebsiteCloner
import sys

def demo_clone():
    """Demonstrate website cloning"""
    print("Website Cloner Demo")
    print("=" * 30)
    
    # Create cloner instance
    cloner = WebsiteCloner()
    
    # Progress callback
    def progress_callback(progress):
        print(f"[{progress.downloaded_files}/{progress.total_files}] {progress.status}")
        if progress.current_file:
            print(f"  Current: {progress.current_file}")
    
    # Demo URLs (safe, small sites for testing)
    test_urls = [
        "https://httpbin.org/html",
        "https://example.com"
    ]
    
    print("Available test URLs:")
    for i, url in enumerate(test_urls):
        print(f"  {i+1}. {url}")
    
    print("\nOr enter your own URL:")
    
    try:
        choice = input("Enter choice (1-{}) or URL: ".format(len(test_urls)))
        
        if choice.isdigit() and 1 <= int(choice) <= len(test_urls):
            url = test_urls[int(choice) - 1]
        else:
            url = choice
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"\nCloning: {url}")
        print("Settings:")
        print("  - Max depth: 1")
        print("  - Assets: HTML, CSS, Images")
        print("  - Output: demo_clone/")
        print()
        
        # Clone the website
        output_dir = cloner.clone_website(
            url=url,
            output_dir="demo_clone",
            max_depth=1,
            asset_types=['html', 'css', 'images'],
            progress_callback=progress_callback
        )
        
        print(f"\nClone completed successfully!")
        print(f"Files saved to: {output_dir}")
        print(f"Downloaded: {len(cloner.downloaded_urls)} files")
        print(f"Failed: {len(cloner.failed_urls)} files")
        
        if cloner.failed_urls:
            print("\nFailed URLs:")
            for url in list(cloner.failed_urls)[:5]:  # Show first 5
                print(f"  - {url}")
            if len(cloner.failed_urls) > 5:
                print(f"  ... and {len(cloner.failed_urls) - 5} more")
        
    except KeyboardInterrupt:
        print("\nClone interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
    
    print("\nDemo completed!")

if __name__ == "__main__":
    demo_clone()
