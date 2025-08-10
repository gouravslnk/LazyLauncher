"""
Desktop file creator module for LazyLauncher.

This module handles the creation and management of .desktop files for KRunner shortcuts.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional
import shutil

from .config import Config
from .utils import validate_url, sanitize_filename

class DesktopFileCreator:
    """
    Class to handle creation of .desktop files for KRunner Shortcuts.
    """

    def __init__(self):
        self.config = Config()

    def create_shortcut(self, name: str, description: str, url: str, browser_command: str = "xdg-open", mode: str = "user") -> bool:

        """
        Create a new KRunner Shortcut.
        
        Args:
            name: The Shortcut Name (what user types in KRunner)
            description: Human-Readable Deacription 
            url: URL or Path to Open
            browser_command: Command to open the URL (default: xdg-open)
            mode: "user" or "system" installation mode

        Returns:
            True if shortcut was created successfully, False otherwise
        """

        try:
            # Sanitize the name for use as filename
            filename = sanitize_filename(name) + ".desktop"

            # Get Target Directory
            target_dir = self._get_applications_dir(mode)
            target_path = target_dir / filename

            # Check if file already exixts
            if target_path.exists():
                # In a real GUI app, this would show a dialog
                pass

            # Create the .desktop file content
            desktop_content = self._create_desktop_content(
                name=name,
                description=description,
                url=url,
                browser_command=browser_command
            )

            # Ensure Target Directory Exists
            target_dir.mkdir(parents=True, exist_ok=True)

            # Write the .desktop file
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(desktop_content)

            # Make the file executable
            os.chmod(target_path, 0o755)

            # Update KRunner Database
            self._update_krunner_datebase()

            return True
        
        except Exception as e:
            print(f"Error Creating Shortcut: {e}")
            return False
        
    
    def _get_applications_dir(self, mode: str) -> Path:
        """
        Get the appropriate applications directory based on mode.
        """

        if mode == "system":
            return Path("/usr/share/appliations")
        else:
            # User Mode
            home = Path.home()
            return home / ".local" / "share" / "applications"
        
    
    def _create_desktop_content(self, name: str, description: str, url: str, browser_command: str,) -> str:
        """
        Create the context for the .desktop file.
        """
        # Build the Exec Command
        if browser_command == "xdg-open":
            exec_command = f"xdg-open {url}"
        else:
            exec_command = f"{browser_command} {url}"

        # Determine appropriate icon based on URL
        icon = self._get_appropriate_icon(url)

        # Create .desktop file content
        content = f"""[Desktop Entry]
Name={name}
GenericName={description}
Exec={exec_command}
Icon={icon}
Type=Application
Comment={description}
Categories=Network;WebBrowser;
StartupNotify=true
"""
        return content
    

    def _get_appropriate_icon(self, url: str) -> str:
        """Get an appropriate icon based on the URL."""
        url_lower = url.lower()

        
