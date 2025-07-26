#!/usr/bin/env python3
"""
Website Cloner Core Module

Handles the actual downloading and processing of websites and their assets.
"""

import requests
import os
import urllib.parse
from urllib.robotparser import RobotFileParser
import time
import re
from bs4 import BeautifulSoup
from pathlib import Path
import mimetypes
from typing import Set, List, Dict, Optional
import threading
from dataclasses import dataclass
import json

@dataclass
class CloneProgress:
    """Represents the progress of a cloning operation"""
    total_files: int = 0
    downloaded_files: int = 0
    failed_files: int = 0
    current_file: str = ""
    status: str = "Starting..."

class WebsiteCloner:
    """Main class for cloning websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Website-Cloner/1.0 (Educational Purpose)'
        })
        
        self.downloaded_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.url_queue: List[str] = []
        self.progress = CloneProgress()
        self.base_domain = ""
        self.base_url = ""
        self.output_dir = ""
        self.max_depth = 2
        self.current_depth = 0
        self.respect_robots = True
        self.delay_between_requests = 1.0  # seconds
        self.progress_callback = None
        
        # File type mappings
        self.asset_extensions = {
            'html': ['.html', '.htm', '.php', '.asp', '.aspx', '.jsp'],
            'css': ['.css'],
            'js': ['.js'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
            'fonts': ['.woff', '.woff2', '.ttf', '.eot', '.otf'],
            'videos': ['.mp4', '.webm', '.ogg', '.avi', '.mov'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf']
        }
        
        self.enabled_assets = ['html', 'css', 'js', 'images']
    
    def clone_website(self, url: str, output_dir: str = "cloned_sites", 
                     max_depth: int = 2, asset_types: List[str] = None,
                     progress_callback=None):
        """Main method to clone a website"""
        
        self.progress_callback = progress_callback
        self.max_depth = max_depth
        self.enabled_assets = asset_types or ['html', 'css', 'js', 'images']
        
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        self.base_url = url
        parsed_url = urllib.parse.urlparse(url)
        self.base_domain = parsed_url.netloc
        
        # Create output directory
        safe_domain = re.sub(r'[^\w\-_.]', '_', self.base_domain)
        self.output_dir = os.path.join(output_dir, safe_domain)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Check robots.txt if enabled
        if self.respect_robots and not self._check_robots_txt(url):
            raise ValueError(f"robots.txt disallows crawling of {url}")
        
        # Initialize progress
        self.progress.status = "Starting clone..."
        self._update_progress()
        
        # Start cloning
        self._clone_recursive(url, 0)
        
        # Convert links in HTML files
        self._convert_links_to_relative()
        
        # Save clone information
        self._save_clone_info()
        
        self.progress.status = "Clone completed!"
        self._update_progress()
        
        return self.output_dir
    
    def _clone_recursive(self, url: str, depth: int):
        """Recursively clone website pages and assets"""
        
        if depth > self.max_depth or url in self.downloaded_urls:
            return
        
        if not self._is_same_domain(url):
            return
        
        try:
            self.progress.current_file = url
            self.progress.status = f"Downloading: {os.path.basename(url) or 'index'}"
            self._update_progress()
            
            # Download the page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Save the file
            local_path = self._url_to_local_path(url)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            content_type = response.headers.get('content-type', '').lower()
            
            if 'text/html' in content_type:
                # Process HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract and download assets
                assets = self._extract_assets(soup, url)
                self._download_assets(assets)
                
                # Extract links for further crawling
                if depth < self.max_depth:
                    links = self._extract_links(soup, url)
                    for link in links:
                        if link not in self.downloaded_urls:
                            time.sleep(self.delay_between_requests)
                            self._clone_recursive(link, depth + 1)
                
                # Save processed HTML
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
            else:
                # Save binary content as-is
                with open(local_path, 'wb') as f:
                    f.write(response.content)
            
            self.downloaded_urls.add(url)
            self.progress.downloaded_files += 1
            self._update_progress()
            
            # Rate limiting
            time.sleep(self.delay_between_requests)
            
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            self.failed_urls.add(url)
            self.progress.failed_files += 1
            self._update_progress()
    
    def _extract_assets(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract asset URLs from HTML"""
        assets = []
        
        # CSS files
        if 'css' in self.enabled_assets:
            for link in soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                if href:
                    assets.append(urllib.parse.urljoin(base_url, href))
        
        # JavaScript files
        if 'js' in self.enabled_assets:
            for script in soup.find_all('script', src=True):
                src = script.get('src')
                if src:
                    assets.append(urllib.parse.urljoin(base_url, src))
        
        # Images
        if 'images' in self.enabled_assets:
            for img in soup.find_all('img', src=True):
                src = img.get('src')
                if src:
                    assets.append(urllib.parse.urljoin(base_url, src))
            
            # Background images in style attributes
            for element in soup.find_all(style=True):
                style = element.get('style')
                bg_matches = re.findall(r'background-image:\s*url\(["\']?([^)"\']+)["\']?\)', style)
                for match in bg_matches:
                    assets.append(urllib.parse.urljoin(base_url, match))
        
        # Fonts
        if 'fonts' in self.enabled_assets:
            for link in soup.find_all('link'):
                href = link.get('href', '')
                if any(ext in href.lower() for ext in self.asset_extensions['fonts']):
                    assets.append(urllib.parse.urljoin(base_url, href))
        
        return assets
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract page links for further crawling"""
        links = []
        
        if 'html' in self.enabled_assets:
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and not href.startswith('#'):
                    full_url = urllib.parse.urljoin(base_url, href)
                    if self._is_same_domain(full_url) and self._is_html_page(full_url):
                        links.append(full_url)
        
        return links
    
    def _download_assets(self, asset_urls: List[str]):
        """Download asset files"""
        for asset_url in asset_urls:
            if asset_url in self.downloaded_urls:
                continue
            
            try:
                if not self._should_download_asset(asset_url):
                    continue
                
                self.progress.current_file = asset_url
                self.progress.status = f"Downloading asset: {os.path.basename(asset_url)}"
                self._update_progress()
                
                response = self.session.get(asset_url, timeout=30)
                response.raise_for_status()
                
                local_path = self._url_to_local_path(asset_url)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                self.downloaded_urls.add(asset_url)
                self.progress.downloaded_files += 1
                self._update_progress()
                
                time.sleep(self.delay_between_requests / 2)  # Shorter delay for assets
                
            except Exception as e:
                print(f"Failed to download asset {asset_url}: {e}")
                self.failed_urls.add(asset_url)
                self.progress.failed_files += 1
                self._update_progress()
    
    def _should_download_asset(self, url: str) -> bool:
        """Check if an asset should be downloaded based on file type"""
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path.lower()
        
        for asset_type in self.enabled_assets:
            if any(path.endswith(ext) for ext in self.asset_extensions[asset_type]):
                return True
        
        return False
    
    def _is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain"""
        parsed_url = urllib.parse.urlparse(url)
        return parsed_url.netloc == self.base_domain or parsed_url.netloc == ''
    
    def _is_html_page(self, url: str) -> bool:
        """Check if URL points to an HTML page"""
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path.lower()
        
        # If no extension, assume HTML
        if not os.path.splitext(path)[1]:
            return True
        
        return any(path.endswith(ext) for ext in self.asset_extensions['html'])
    
    def _url_to_local_path(self, url: str) -> str:
        """Convert URL to local file path"""
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path
        
        # Remove leading slash
        if path.startswith('/'):
            path = path[1:]
        
        # If path is empty or ends with /, use index.html
        if not path or path.endswith('/'):
            path = os.path.join(path, 'index.html')
        
        # If no extension, add .html for HTML pages
        if not os.path.splitext(path)[1] and self._is_html_page(url):
            path += '.html'
        
        # Create safe filename
        path = re.sub(r'[<>:"|?*]', '_', path)
        
        return os.path.join(self.output_dir, path)
    
    def _convert_links_to_relative(self):
        """Convert absolute URLs to relative paths in HTML files"""
        self.progress.status = "Converting links to relative paths..."
        self._update_progress()
        
        for root, dirs, files in os.walk(self.output_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    self._convert_file_links(file_path)
    
    def _convert_file_links(self, file_path: str):
        """Convert links in a single HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Convert links
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and href.startswith(('http://', 'https://')):
                    local_path = self._convert_url_to_relative(href, file_path)
                    if local_path:
                        link['href'] = local_path
            
            # Convert asset references
            for element in soup.find_all(['img', 'script', 'link'], src=True):
                src = element.get('src') or element.get('href')
                if src and src.startswith(('http://', 'https://')):
                    local_path = self._convert_url_to_relative(src, file_path)
                    if local_path:
                        if element.name == 'link':
                            element['href'] = local_path
                        else:
                            element['src'] = local_path
            
            # Save modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
        except Exception as e:
            print(f"Failed to convert links in {file_path}: {e}")
    
    def _convert_url_to_relative(self, url: str, current_file: str) -> Optional[str]:
        """Convert absolute URL to relative path"""
        if url in self.downloaded_urls:
            target_path = self._url_to_local_path(url)
            if os.path.exists(target_path):
                return os.path.relpath(target_path, os.path.dirname(current_file))
        return None
    
    def _check_robots_txt(self, url: str) -> bool:
        """Check robots.txt for crawling permissions"""
        try:
            robots_url = urllib.parse.urljoin(url, '/robots.txt')
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch('*', url)
        except:
            return True  # If can't read robots.txt, assume allowed
    
    def _save_clone_info(self):
        """Save information about the clone operation"""
        info = {
            'base_url': self.base_url,
            'base_domain': self.base_domain,
            'max_depth': self.max_depth,
            'enabled_assets': self.enabled_assets,
            'downloaded_files': len(self.downloaded_urls),
            'failed_files': len(self.failed_urls),
            'downloaded_urls': list(self.downloaded_urls),
            'failed_urls': list(self.failed_urls),
            'clone_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        info_path = os.path.join(self.output_dir, 'clone_info.json')
        with open(info_path, 'w') as f:
            json.dump(info, f, indent=2)
    
    def _update_progress(self):
        """Update progress information"""
        self.progress.total_files = len(self.downloaded_urls) + len(self.failed_urls) + len(self.url_queue)
        
        if self.progress_callback:
            self.progress_callback(self.progress)

# Example usage
if __name__ == "__main__":
    cloner = WebsiteCloner()
    
    def progress_callback(progress):
        print(f"Progress: {progress.downloaded_files}/{progress.total_files} - {progress.status}")
    
    try:
        output_dir = cloner.clone_website(
            url="https://example.com",
            output_dir="test_clone",
            max_depth=1,
            asset_types=['html', 'css', 'images'],
            progress_callback=progress_callback
        )
        print(f"Website cloned to: {output_dir}")
    except Exception as e:
        print(f"Error: {e}")
