"""
Utility functions for LazyLauncher.

This module contains helper functions for URL Validation, file operations, etc.
"""

import re
import os
import urllib.parse
from pathlib import Path
from typing import Optional, Union

def validate_url(url: str) -> bool:
    """
    Validate if a given string is a valid URL or file path.
    
    Args:
        url: The URL or path to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not url or not url.strip():
        return False
    
    url = url.strip()
    
    # Check if it's a valid HTTP/HTTPS URL
    try:
        result = urllib.parse.urlparse(url)
        if result.scheme in ('http', 'https') and result.netloc:
            return True
    except Exception:
        pass
    
    # Check if it's a valid file:// URL
    if url.startswith('file://'):
        try:
            path = urllib.parse.urlparse(url).path
            return os.path.exists(path)
        except Exception:
            return False
    
    # Check if it's a valid absolute path
    if os.path.isabs(url):
        return os.path.exists(url)
    
    # Check for other protocols (ftp, mailto, etc.)
    try:
        result = urllib.parse.urlparse(url)
        if result.scheme and result.scheme not in ('http', 'https', 'file'):
            # Basic validation for other protocols
            if result.scheme in ('ftp', 'ftps') and result.netloc:
                return True
            elif result.scheme == 'mailto' and '@' in result.path:
                return True
            elif result.scheme in ('tel', 'sms') and result.path:
                return True
            # Add more protocol validations as needed
            return bool(result.scheme and (result.netloc or result.path))
    except Exception:
        pass
    
    return False

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a String to be Safe for use as a filename.

    Args:
        filename: The filename to Sanitize

    Returns:
        A safe filename string
    """

    if not filename:
        return "unnamed"
    
    # Remove or Replace Invalid Characters
    # Keep Alphanumeric, Hyphens, Underscores and dots
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', filename.strip())

    # Remove multiple consecutive Underscores
    sanitized = re.sub(r'_+', '_', sanitized)

    # Remove leading/trailing Underscores and dots
    sanitized = sanitized.strip('_.')

    # Ensure it's not empty
    if not sanitized:
        sanitized = "unnamed"

    # Limit length (most filesystems support at least 255 chars)
    # Preserve file extension if present
    if len(sanitized) > 100:
        if '.' in sanitized:
            name_part, ext = sanitized.rsplit('.', 1)
            max_name_len = 100 - len(ext) - 1  # -1 for the dot
            if max_name_len > 0:
                sanitized = name_part[:max_name_len] + '.' + ext
            else:
                sanitized = sanitized[:100]
        else:
            sanitized = sanitized[:100]

    return sanitized


def ensure_directory_exists(path: Union[str, Path]) -> bool:
    """
    Ensure a Directory exists, creating it if necessary.

    Args:
        path: The directory path to ensure exists

    Returns: 
        True if Directory exists or was created, False otherwise
    """

    try:
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error Creating Directory {path}: {e}")
        return False
    

def is_executable(path: Union[str, Path]) -> bool:
    """
    Check if a file is executable.

    Args:
        path: The file path to check

    Returns:
        True if file is executable, False otherwise
    """

    try:
        path = Path(path)
        return path.is_file() and os.access(path, os.X_OK)
    except Exception:
        return False
    

def find_executable(command: str) -> Optional[str]:
    """
    Find the full path to an executable command.

    Args:
        command: The Command to Find

    Returns:
        Full Path to the executable, or None if not Found
    """

    try:
        import shutil
        return shutil.which(command)
    except Exception:
        return None
    

def get_file_size_human(path: Union[str, Path]) -> str:
    """
    Get human-readable file size.
    
    Args:
        path: The file path
        
    Returns:
        Human-readable file size string
    """
    try:
        size = Path(path).stat().st_size
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        
        return f"{size:.1f} TB"
    except Exception:
        return "Unknown"
    

def extract_domain(url: str) -> Optional[str]:
    """
    Extract domain name from a URL.

    Args:
        url: The URL to extract domain from

    Returns:
        Domain name or None if extraction fails
    """

    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()

        # Remove www. prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]

        return domain if domain else None
    except Exception:
        return None
    

def format_exec_command(browser_command: str, url: str) -> str:
    """
    Format the Exec command for the .desktop file.
    
    Args:
        browser_command: The browser command/path
        url: The URL to open
        
    Returns:
        Properly formatted Exec command
    """
    # Escape special characters in URL
    escaped_url = url.replace('"', '\\"').replace("'", "\\'")
    
    if browser_command == "xdg-open":
        return f"xdg-open \"{escaped_url}\""
    else:
        # For custom browsers, add the URL as an argument
        # Handle spaces in browser path
        if ' ' in browser_command and not (browser_command.startswith('"') and browser_command.endswith('"')):
            browser_command = f'"{browser_command}"'
        return f"{browser_command} \"{escaped_url}\""
    

def validate_shortcut_name(name: str) -> tuple[bool, str]:
    """
    Validate a shortcut name and return validation result with message.

    Args:
        name: The shortcut name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """

    if not name or not name.strip():
        return False, "Shortcut name can not be Empty"
    
    name = name.strip()

    # Check Length
    if len(name) < 1:
        return False, "Shortcut Name must be at least 1 character long"
    
    if len(name) > 50:
        return False, "Shortcut name must be 50 characters or less"
    
    # Check for invalid characters (basic check)
    if any(char in name for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']):
        return False, "Shortcut name contains invalid characters"
    
    # Check if it starts/ends with Whitespace
    if name != name.strip():
        return False, "Shortcut name cannot start or end with whitespace"
    
    return True, ""


def get_common_browser() -> list[dict]:
    """
    Get a list of commonly available browser on Linux.

    Returns: 
        List of browser dictionaries with name and command
    """

    browsers = [
        {"name": "Default Browser", "command": "xdg-open"},
        {"name": "Firefox", "command": "firefox"},
        {"name": "Google Chrome", "command": "google-chrome"},
        {"name": "Chromium", "command": "chromium-browser"},
        {"name": "Microsoft Edge", "command": "microsoft-edge"},
        {"name": "Opera", "command": "opera"},
        {"name": "Brave Browser", "command": "brave-browser"},
        {"name": "Vivaldi", "command": "vivaldi"},
        {"name": "Konqueror", "command": "konqueror"},
        {"name": "Epiphany", "command": "epiphany"},
    ]

    # Filter to only available browsers
    available_browsers = []
    
    for browser in browsers:
        try:
            if browser["command"] == "xdg-open" or find_executable(browser["command"]):
                available_browsers.append(browser)
        except Exception:
            # Skip browsers that cause errors during detection
            continue

    return available_browsers


def validate_browser_command(command: str) -> bool:
    """
    Validate if a browser command is available.
    
    Args:
        command: The browser command to validate
        
    Returns:
        True if browser is available, False otherwise
    """
    if not command or not command.strip():
        return False
    
    command = command.strip()
    
    # Default system command is always valid
    if command == "xdg-open":
        return True
    
    # Check if it's an executable path
    if os.path.isabs(command):
        return is_executable(command)
    
    # Check if command is available in PATH
    return find_executable(command) is not None