"""
Configuration module for LazyLauncher.

This module contains default settings and configurations for the LazyLauncher application.
"""

import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration class for LazyLauncher settings."""

    def __init__(self):
        self.app_name = "LazyLauncher"
        self.app_version = "1.0.0"

        # Default Settings
        self.default_browser = "xdg-open"
        self.default_icon = "applications-internet"
        self.default_category = "Network;WebBrowser;"

        # Paths
        self.user_applications_dir = Path.home() / ".local" / "share" / "applications"
        self.system_applications_dir = Path("/usr/share/applications")

        # GUI Settings
        self.window_size = "500x400"
        self.window_title = f"{self.app_name} - Custom KRunner Shortcuts"

        # Desktop file template
        self.desktop_template = """[Desktop Entry]
Name={name}
GenericName={description}
Exec={exec_command}
Icon={icon}
Type=Application
Comment="Open - {description}"
Categories={categories}
StartupNotify=true
""" 

        # Common Websites Icons Mapping
        self.site_icons = {
            'youtube.com': 'youtube',
            'youtu.be': 'youtube',
            'google.com': 'google',
            'github.com': 'github',
            'stackoverflow.com': 'stackoverflow',
            'reddit.com': 'reddit',
            'twitter.com': 'twitter',
            'x.com': 'twitter',
            'facebook.com': 'facebook',
            'linkedin.com': 'linkedin',
            'instagram.com': 'instagram',
            'discord.com': 'discord',
            'slack.com': 'slack',
            'teams.microsoft.com': 'teams',
            'zoom.us': 'zoom',
            'wikipedia.org': 'wikipedia',
            'amazon.com': 'amazon',
            'ebay.com': 'ebay',
            'netflix.com': 'netflix',
            'spotify.com': 'spotify',
        }
            
        # KDE System Command Preference
        self.kbuildsycoca_commands = [
            'kbuildsycoca6', # KDE 6
            'kbuildsycoca5', # KDE 5
            'kbuildsycoca'   # Fallback
        ]
        
    
    def get_application_dir(self, mode: str = "user") -> Path:
        """Get the application directory based on installation mode."""
        if mode == "system":
            return self.system_applications_dir
        else:
            return self.user_applications_dir
        

    def get_icon_for_url(self, url: str) -> str:
        """Get an appropriate icon for a given URL."""
        url_lower = url.lower()

        # Check for known Sites
        for domain, icon in self.site_icons.items():
            if domain in url_lower:
                return icon
            
        # Default Based on protocol/type
        if url_lower.startswith(('http://', 'https://')):
            return 'application-internet'
        elif url_lower.startswith('file://') or os.path.isabs(url):
            return 'folder'
        elif url_lower.startswith('ftp://'):
            return 'folder-remote'
        elif url_lower.startswith('mailto:'):
            return 'mail-send'
        else:
            return self.default_icon
        

    def get_categories_for_url(self, url: str) -> str:
        """Get appropriate Desktop File Categories for a URL"""
        url_lower = url.lower()

        # Media Sites
        if any(site in url_lower for site in ['youtube', 'netflix', 'spotify', 'twitch', 'hotstar', 'prime']):
            return "AudioVideo;Audio;Video;Player;"
        
        # Development Sites
        elif any(site in url_lower for site in ['github', 'stackoverflow', 'gitlab', 'chatgpt', 'deepseek', 'gemini']):
            return "Development;IDE;"
        
        # Social Media
        elif any(site in url_lower for site in ['twitch', 'twitter', 'x', 'facebook', 'linkedin', 'reddit', 'instagram']):
            return "Network;Chat;InstantMessaging;"
        
        # Shopping
        elif any(site in url_lower for site in ['amazon', 'flipkart', 'ebay', 'shopping']):
            return "Network;WebBrowser;"
        
        # Communication
        elif any(site in url_lower for site in ['discord', 'slack', 'teams', 'zoom']):
            return "Network;Chat;VideoConference;"
        
        # Local files
        elif url_lower.startswith('file://') or os.path.isabs(url):
            return "System;FileManager;"
        
        # Default Category
        else:
            return self.default_category
        
    

    def load_user_config(self) -> Dict[str, Any]:
        """Load user-specific configuration (for future use)."""
        # Placeholder for loading user config from file
        # Could read from ~/.config/lazylauncher/config.json
        return {}
    

    def save_user_config(self, config: Dict[str, Any]) -> bool:
        """Save user-specific configuration (for future use)."""
        # Placeholder for saving user config to file
        return True
    

    