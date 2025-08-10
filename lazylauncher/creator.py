"""
Desktop file creator module for EasyLauncher.

This module handles the creation and management of .desktop files for KRunner shortcuts.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional
import shutil

from .config import Config
from .utils import validate_url, sanitize_filename, validate_shortcut_name, format_exec_command


class DesktopFileCreator:
    """Class to handle creation of .desktop files for KRunner shortcuts."""
    
    def __init__(self):
        self.config = Config()
    
    def create_shortcut(self, name: str, description: str, url: str, 
                       browser_command: str = "xdg-open", mode: str = "user") -> bool:
        """
        Create a new KRunner shortcut.
        
        Args:
            name: The shortcut name (what user types in KRunner)
            description: Human-readable description
            url: URL or path to open
            browser_command: Command to open the URL (default: xdg-open)
            mode: "user" or "system" installation mode
            
        Returns:
            True if shortcut was created successfully, False otherwise
        """
        try:
            # Validate inputs
            is_valid, error_msg = validate_shortcut_name(name)
            if not is_valid:
                print(f"Error: {error_msg}")
                return False
            
            if not validate_url(url):
                print(f"Error: Invalid URL or path: {url}")
                return False
            
            # Sanitize the name for use as filename
            filename = sanitize_filename(name) + ".desktop"
            
            # Get target directory
            target_dir = self.config.get_applications_dir(mode)
            target_path = target_dir / filename
            
            # Check if file already exists
            if target_path.exists():
                # In a real GUI app, this would show a dialog
                # For now, we'll overwrite
                pass
            
            # Create the .desktop file content
            desktop_content = self._create_desktop_content(
                name=name,
                description=description,
                url=url,
                browser_command=browser_command
            )
            
            # Ensure target directory exists
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Write the .desktop file
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(desktop_content)
            
            # Make the file executable
            os.chmod(target_path, 0o755)
            
            # Update KRunner database
            self._update_krunner_database()
            
            return True
            
        except Exception as e:
            print(f"Error creating shortcut: {e}")
            return False
    
    def _create_desktop_content(self, name: str, description: str, 
                               url: str, browser_command: str) -> str:
        """Create the content for the .desktop file."""
        # Build the Exec command using utility function
        exec_command = format_exec_command(browser_command, url)
        
        # Determine appropriate icon and categories based on URL
        icon = self.config.get_icon_for_url(url)
        categories = self.config.get_categories_for_url(url)
        
        # Use config template for consistency
        content = self.config.desktop_template.format(
            name=name,
            description=description,
            exec_command=exec_command,
            icon=icon,
            categories=categories
        )
        
        return content
    
    def _update_krunner_database(self) -> bool:
        """Update KRunner's database to include the new shortcut."""
        try:
            # Try each kbuildsycoca command from config
            for command in self.config.kbuildsycoca_commands:
                try:
                    result = subprocess.run([command, '--noincremental'], 
                                          capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
            
            return False
            
        except subprocess.TimeoutExpired as e:
            print(f"Warning: Could not update KRunner database: {e}")
            print("You may need to log out and back in for the shortcut to appear.")
            return False
    
    def remove_shortcut(self, name: str, mode: str = "user") -> bool:
        """Remove an existing shortcut."""
        try:
            filename = sanitize_filename(name) + ".desktop"
            target_dir = self.config.get_applications_dir(mode)
            target_path = target_dir / filename
            
            if target_path.exists():
                target_path.unlink()
                self._update_krunner_database()
                return True
            
            return False
            
        except Exception as e:
            print(f"Error removing shortcut: {e}")
            return False
    
    def list_shortcuts(self, mode: str = "user") -> list:
        """List existing custom shortcuts."""
        try:
            target_dir = self.config.get_applications_dir(mode)
            if not target_dir.exists():
                return []
            
            shortcuts = []
            for desktop_file in target_dir.glob("*.desktop"):
                try:
                    with open(desktop_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract Name field
                        for line in content.split('\n'):
                            if line.startswith('Name='):
                                name = line.split('=', 1)[1]
                                shortcuts.append(name)
                                break
                except Exception:
                    continue
            
            return shortcuts
            
        except Exception as e:
            print(f"Error listing shortcuts: {e}")
            return []

    def get_shortcut_details(self, name: str, mode: str = "user") -> dict:
        """Get details of an existing shortcut."""
        try:
            filename = sanitize_filename(name) + ".desktop"
            target_dir = self.config.get_applications_dir(mode)
            target_path = target_dir / filename
            
            if not target_path.exists():
                return {}
            
            details = {}
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                for line in content.split('\n'):
                    if line.startswith('Name='):
                        details['name'] = line.split('=', 1)[1]
                    elif line.startswith('GenericName='):
                        details['description'] = line.split('=', 1)[1]
                    elif line.startswith('Exec='):
                        exec_line = line.split('=', 1)[1]
                        # Extract URL from exec command
                        if 'xdg-open' in exec_line:
                            # Extract URL from xdg-open command
                            parts = exec_line.split('"')
                            if len(parts) >= 2:
                                details['url'] = parts[1]
                            details['browser_command'] = 'xdg-open'
                        else:
                            # Custom browser
                            parts = exec_line.split('"')
                            if len(parts) >= 3:
                                details['browser_command'] = parts[0].strip()
                                details['url'] = parts[1]
                            elif len(parts) >= 2:
                                details['url'] = parts[1]
                                details['browser_command'] = 'custom'
                    elif line.startswith('Comment='):
                        comment = line.split('=', 1)[1]
                        if comment.startswith('Open - '):
                            details['description'] = comment[7:]
                        
            return details
            
        except Exception as e:
            print(f"Error getting shortcut details: {e}")
            return {}
