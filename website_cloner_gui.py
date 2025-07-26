#!/usr/bin/env python3
"""
Website Cloner GUI

Provides a user-friendly graphical interface for cloning websites.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import webbrowser
from website_cloner import WebsiteCloner, CloneProgress

class WebsiteClonerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Cloner")
        self.root.geometry("800x600")
        
        self.cloner = WebsiteCloner()
        self.current_thread = None
        self.is_cloning = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # URL input frame
        url_frame = ttk.LabelFrame(main_frame, text="Website to Clone")
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        # URL input
        ttk.Label(url_frame, text="URL:").pack(anchor=tk.W, padx=5, pady=5)
        self.url_var = tk.StringVar(value="https://")
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=('Arial', 10))
        self.url_entry.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Output directory frame
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Output directory
        dir_frame = ttk.Frame(output_frame)
        dir_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(dir_frame, text="Output Directory:").pack(anchor=tk.W)
        
        dir_input_frame = ttk.Frame(dir_frame)
        dir_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.output_var = tk.StringVar(value="cloned_sites")
        self.output_entry = ttk.Entry(dir_input_frame, textvariable=self.output_var)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(dir_input_frame, text="Browse", command=self.browse_output_dir).pack(side=tk.RIGHT)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Clone Settings")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Depth setting
        depth_frame = ttk.Frame(settings_frame)
        depth_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(depth_frame, text="Maximum Depth:").pack(side=tk.LEFT)
        self.depth_var = tk.IntVar(value=2)
        depth_spin = ttk.Spinbox(depth_frame, from_=1, to=5, textvariable=self.depth_var, width=5)
        depth_spin.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Label(depth_frame, text="(1=single page, 2=one level deep, etc.)").pack(side=tk.LEFT, padx=(10, 0))
        
        # Asset types
        assets_frame = ttk.LabelFrame(settings_frame, text="Assets to Download")
        assets_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.asset_vars = {}
        asset_types = [
            ('html', 'HTML Pages', True),
            ('css', 'CSS Stylesheets', True),
            ('js', 'JavaScript Files', True),
            ('images', 'Images', True),
            ('fonts', 'Fonts', False),
            ('videos', 'Videos', False),
            ('documents', 'Documents', False)
        ]
        
        assets_grid = ttk.Frame(assets_frame)
        assets_grid.pack(padx=5, pady=5)
        
        for i, (key, label, default) in enumerate(asset_types):
            var = tk.BooleanVar(value=default)
            self.asset_vars[key] = var
            cb = ttk.Checkbutton(assets_grid, text=label, variable=var)
            cb.grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)
        
        # Advanced settings
        advanced_frame = ttk.LabelFrame(settings_frame, text="Advanced Settings")
        advanced_frame.pack(fill=tk.X, padx=5, pady=5)
        
        adv_grid = ttk.Frame(advanced_frame)
        adv_grid.pack(padx=5, pady=5)
        
        # Respect robots.txt
        self.robots_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(adv_grid, text="Respect robots.txt", variable=self.robots_var).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        # Delay setting
        ttk.Label(adv_grid, text="Delay between requests (seconds):").grid(row=0, column=1, sticky=tk.W, padx=(20, 5))
        self.delay_var = tk.DoubleVar(value=1.0)
        delay_spin = ttk.Spinbox(adv_grid, from_=0.1, to=5.0, increment=0.1, textvariable=self.delay_var, width=8)
        delay_spin.grid(row=0, column=2, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="Start Cloning", command=self.start_cloning)
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_cloning, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.open_button = ttk.Button(button_frame, text="Open Output Folder", command=self.open_output_folder, state=tk.DISABLED)
        self.open_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_button = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_button.pack(side=tk.RIGHT)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress")
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to clone")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.pack(pady=(0, 5))
        
        # Log text area
        log_frame = ttk.Frame(progress_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_var.set(directory)
    
    def start_cloning(self):
        """Start the cloning process"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL to clone")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_var.set(url)
        
        # Get selected asset types
        selected_assets = [key for key, var in self.asset_vars.items() if var.get()]
        if not selected_assets:
            messagebox.showerror("Error", "Please select at least one asset type to download")
            return
        
        # Update cloner settings
        self.cloner.respect_robots = self.robots_var.get()
        self.cloner.delay_between_requests = self.delay_var.get()
        
        # Clear log and reset progress
        self.clear_log()
        self.progress_var.set(0)
        self.status_var.set("Starting...")
        
        # Update button states
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.open_button.config(state=tk.DISABLED)
        self.is_cloning = True
        
        # Start cloning in separate thread
        self.current_thread = threading.Thread(
            target=self._clone_worker,
            args=(url, self.output_var.get(), self.depth_var.get(), selected_assets),
            daemon=True
        )
        self.current_thread.start()
    
    def stop_cloning(self):
        """Stop the cloning process"""
        self.is_cloning = False
        self.log_message("Stopping clone operation...")
        self.status_var.set("Stopping...")
        
        # Reset button states
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def _clone_worker(self, url, output_dir, max_depth, asset_types):
        """Worker thread for cloning"""
        try:
            result_dir = self.cloner.clone_website(
                url=url,
                output_dir=output_dir,
                max_depth=max_depth,
                asset_types=asset_types,
                progress_callback=self._progress_callback
            )
            
            if self.is_cloning:  # Only show success if not stopped
                self.root.after(0, lambda: self._clone_completed(result_dir))
                
        except Exception as e:
            if self.is_cloning:  # Only show error if not stopped
                self.root.after(0, lambda: self._clone_failed(str(e)))
    
    def _progress_callback(self, progress: CloneProgress):
        """Handle progress updates from cloner"""
        if not self.is_cloning:
            return
        
        # Update progress bar
        if progress.total_files > 0:
            percent = (progress.downloaded_files / progress.total_files) * 100
            self.root.after(0, lambda: self.progress_var.set(percent))
        
        # Update status
        self.root.after(0, lambda: self.status_var.set(progress.status))
        
        # Log current file
        if progress.current_file:
            filename = os.path.basename(progress.current_file) or progress.current_file
            self.root.after(0, lambda: self.log_message(f"Downloading: {filename}"))
        
        # Update status bar
        status_text = f"Downloaded: {progress.downloaded_files}, Failed: {progress.failed_files}"
        self.root.after(0, lambda: self.status_bar.config(text=status_text))
    
    def _clone_completed(self, result_dir):
        """Handle successful completion"""
        self.is_cloning = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.open_button.config(state=tk.NORMAL)
        
        self.progress_var.set(100)
        self.status_var.set("Clone completed successfully!")
        self.log_message(f"Clone completed! Files saved to: {result_dir}")
        self.log_message("You can now open the output folder to view the cloned website.")
        
        # Ask if user wants to open the folder
        if messagebox.askyesno("Clone Complete", 
                              f"Website cloned successfully to:\n{result_dir}\n\nOpen the folder now?"):
            self.open_output_folder()
    
    def _clone_failed(self, error_message):
        """Handle clone failure"""
        self.is_cloning = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        self.status_var.set("Clone failed")
        self.log_message(f"Clone failed: {error_message}")
        messagebox.showerror("Clone Failed", f"Failed to clone website:\n{error_message}")
    
    def open_output_folder(self):
        """Open the output folder in file explorer"""
        output_path = self.output_var.get()
        if os.path.exists(output_path):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(output_path)
                elif os.name == 'posix':  # macOS and Linux
                    os.system(f'open "{output_path}"' if sys.platform == 'darwin' else f'xdg-open "{output_path}"')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open folder: {e}")
        else:
            messagebox.showwarning("Warning", "Output folder does not exist yet")
    
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.delete(1.0, tk.END)
    
    def log_message(self, message):
        """Add a message to the log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = WebsiteClonerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
