#!/usr/bin/env python3
"""
Command-line interface for LazyLauncher.

This script provides a CLI alternative to the GUI interface with full CRUD operations.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path to import lazylauncher modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from lazylauncher.creator import DesktopFileCreator
from lazylauncher.utils import validate_url, validate_shortcut_name, validate_browser_command


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="LazyLauncher CLI - Create, Update, Delete and Manage KRunner shortcuts",
        prog="lazylauncher-cli",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Create a shortcut:
    %(prog)s create yt https://youtube.com -d "YouTube"
    
  Update a shortcut:
    %(prog)s update yt -u https://youtube.com/feed/subscriptions -d "YouTube Subscriptions"
    
  List all shortcuts:
    %(prog)s list
    
  Search shortcuts:
    %(prog)s search youtube
    
  Show shortcut details:
    %(prog)s show yt
    
  Remove a shortcut:
    %(prog)s remove yt
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create shortcut command
    create_parser = subparsers.add_parser("create", help="Create a new shortcut")
    create_parser.add_argument("name", help="Shortcut name (what you type in KRunner)")
    create_parser.add_argument("url", help="URL or path to open")
    create_parser.add_argument("-d", "--description", 
                              help="Description of the shortcut", default="")
    create_parser.add_argument("-b", "--browser", 
                              help="Browser command (default: xdg-open)", 
                              default="xdg-open")
    create_parser.add_argument("-m", "--mode", 
                              choices=["user", "system"], 
                              default="user",
                              help="Installation mode (default: user)")
    create_parser.add_argument("-f", "--force", 
                              action="store_true",
                              help="Force overwrite if shortcut exists")
    
    # Update shortcut command
    update_parser = subparsers.add_parser("update", help="Update an existing shortcut")
    update_parser.add_argument("name", help="Name of shortcut to update")
    update_parser.add_argument("-u", "--url", help="New URL or path")
    update_parser.add_argument("-d", "--description", help="New description")
    update_parser.add_argument("-b", "--browser", help="New browser command")
    update_parser.add_argument("-m", "--mode", 
                              choices=["user", "system"], 
                              default="user",
                              help="Installation mode (default: user)")
    
    # Remove shortcut command
    remove_parser = subparsers.add_parser("remove", help="Remove a shortcut")
    remove_parser.add_argument("name", help="Name of shortcut to remove")
    remove_parser.add_argument("-m", "--mode", 
                              choices=["user", "system"], 
                              default="user",
                              help="Installation mode (default: user)")
    remove_parser.add_argument("-y", "--yes", 
                              action="store_true",
                              help="Skip confirmation prompt")
    
    # List shortcuts command
    list_parser = subparsers.add_parser("list", help="List existing shortcuts")
    list_parser.add_argument("-m", "--mode", 
                            choices=["user", "system", "all"], 
                            default="user",
                            help="Installation mode (default: user)")
    list_parser.add_argument("-v", "--verbose", 
                            action="store_true",
                            help="Show detailed information")
    
    # Search shortcuts command
    search_parser = subparsers.add_parser("search", help="Search shortcuts by name")
    search_parser.add_argument("term", help="Search term")
    search_parser.add_argument("-m", "--mode", 
                              choices=["user", "system", "all"], 
                              default="all",
                              help="Installation mode (default: all)")
    search_parser.add_argument("-v", "--verbose", 
                              action="store_true",
                              help="Show detailed information")
    
    # Show shortcut details command
    show_parser = subparsers.add_parser("show", help="Show detailed information about a shortcut")
    show_parser.add_argument("name", help="Name of shortcut to show")
    show_parser.add_argument("-m", "--mode", 
                            choices=["user", "system", "all"], 
                            default="all",
                            help="Installation mode (default: all)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    creator = DesktopFileCreator()
    
    if args.command == "create":
        return create_shortcut(creator, args)
    elif args.command == "update":
        return update_shortcut(creator, args)
    elif args.command == "remove":
        return remove_shortcut(creator, args)
    elif args.command == "list":
        return list_shortcuts(creator, args)
    elif args.command == "search":
        return search_shortcuts(creator, args)
    elif args.command == "show":
        return show_shortcut(creator, args)
    
    return 1


def create_shortcut(creator: DesktopFileCreator, args) -> int:
    """Create a new shortcut."""
    # Validate inputs
    is_valid, error_msg = validate_shortcut_name(args.name)
    if not is_valid:
        print(f"Error: {error_msg}", file=sys.stderr)
        return 1
    
    if not validate_url(args.url):
        print(f"Error: Invalid URL or path: {args.url}", file=sys.stderr)
        return 1
    
    # Set description if not provided
    description = args.description if args.description else args.name
    
    # Validate browser command if not default
    if args.browser != "xdg-open":
        if not validate_browser_command(args.browser):
            print(f"Error: Browser command not found or invalid: {args.browser}", file=sys.stderr)
            return 1
    
    # Check if shortcut already exists
    if not args.force:
        shortcuts = creator.list_shortcuts(args.mode)
        if args.name in shortcuts:
            print(f"Error: Shortcut '{args.name}' already exists. Use --force to overwrite.", 
                  file=sys.stderr)
            return 1
    
    # Create the shortcut
    try:
        success = creator.create_shortcut(
            name=args.name,
            description=description,
            url=args.url,
            browser_command=args.browser,
            mode=args.mode
        )
        
        if success:
            print(f"✓ Successfully created shortcut '{args.name}'")
            print(f"  You can now use Alt+SPACE and type '{args.name}' to launch it.")
            return 0
        else:
            print(f"✗ Failed to create shortcut '{args.name}'", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"✗ Error creating shortcut: {e}", file=sys.stderr)
        return 1


def update_shortcut(creator: DesktopFileCreator, args) -> int:
    """Update an existing shortcut."""
    try:
        # Check if shortcut exists
        shortcuts = creator.list_shortcuts(args.mode)
        if args.name not in shortcuts:
            print(f"Error: Shortcut '{args.name}' not found in {args.mode} mode", file=sys.stderr)
            return 1
        
        # Get current details
        current_details = creator.get_shortcut_details(args.name, args.mode)
        if not current_details:
            print(f"Error: Could not load current details for '{args.name}'", file=sys.stderr)
            return 1
        
        # Use provided values or keep current ones
        name = args.name
        url = args.url if args.url else current_details.get('url', '')
        description = args.description if args.description else current_details.get('description', '')
        browser_command = args.browser if args.browser else current_details.get('browser_command', 'xdg-open')
        
        # Validate new values
        if args.url and not validate_url(url):
            print(f"Error: Invalid URL or path: {url}", file=sys.stderr)
            return 1
            
        if args.browser and args.browser != "xdg-open":
            if not validate_browser_command(browser_command):
                print(f"Error: Browser command not found or invalid: {browser_command}", file=sys.stderr)
                return 1
        
        # Update the shortcut (create with same name overwrites)
        success = creator.create_shortcut(
            name=name,
            description=description,
            url=url,
            browser_command=browser_command,
            mode=args.mode
        )
        
        if success:
            print(f"✓ Successfully updated shortcut '{args.name}'")
            return 0
        else:
            print(f"✗ Failed to update shortcut '{args.name}'", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"✗ Error updating shortcut: {e}", file=sys.stderr)
        return 1


def remove_shortcut(creator: DesktopFileCreator, args) -> int:
    """Remove an existing shortcut."""
    try:
        # Check if shortcut exists
        shortcuts = creator.list_shortcuts(args.mode)
        if args.name not in shortcuts:
            print(f"Error: Shortcut '{args.name}' not found in {args.mode} mode", file=sys.stderr)
            return 1
        
        # Confirm deletion unless --yes is used
        if not args.yes:
            response = input(f"Are you sure you want to delete shortcut '{args.name}'? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Deletion cancelled.")
                return 0
        
        success = creator.remove_shortcut(args.name, args.mode)
        
        if success:
            print(f"✓ Successfully removed shortcut '{args.name}'")
            return 0
        else:
            print(f"✗ Shortcut '{args.name}' not found", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"✗ Error removing shortcut: {e}", file=sys.stderr)
        return 1


def list_shortcuts(creator: DesktopFileCreator, args) -> int:
    """List existing shortcuts."""
    try:
        modes_to_check = ["user", "system"] if args.mode == "all" else [args.mode]
        all_shortcuts = {}
        
        for mode in modes_to_check:
            shortcuts = creator.list_shortcuts(mode)
            if shortcuts:
                all_shortcuts[mode] = shortcuts
        
        if not all_shortcuts:
            if args.mode == "all":
                print("No shortcuts found in user or system mode")
            else:
                print(f"No shortcuts found in {args.mode} mode")
            return 0
        
        total_count = sum(len(shortcuts) for shortcuts in all_shortcuts.values())
        print(f"Found {total_count} shortcut(s):")
        print()
        
        for mode, shortcuts in all_shortcuts.items():
            print(f"📁 {mode.upper()} mode ({len(shortcuts)} shortcuts):")
            
            if args.verbose:
                for shortcut in sorted(shortcuts):
                    details = creator.get_shortcut_details(shortcut, mode)
                    print(f"  • {shortcut}")
                    if details:
                        print(f"    Description: {details.get('description', 'N/A')}")
                        print(f"    URL: {details.get('url', 'N/A')}")
                        print(f"    Browser: {details.get('browser_command', 'xdg-open')}")
                    print()
            else:
                for shortcut in sorted(shortcuts):
                    print(f"  • {shortcut}")
            print()
        
        return 0
        
    except Exception as e:
        print(f"✗ Error listing shortcuts: {e}", file=sys.stderr)
        return 1


def search_shortcuts(creator: DesktopFileCreator, args) -> int:
    """Search shortcuts by name."""
    try:
        modes_to_check = ["user", "system"] if args.mode == "all" else [args.mode]
        found_shortcuts = {}
        
        for mode in modes_to_check:
            shortcuts = creator.list_shortcuts(mode)
            matching = [s for s in shortcuts if args.term.lower() in s.lower()]
            if matching:
                found_shortcuts[mode] = matching
        
        if not found_shortcuts:
            print(f"No shortcuts found matching '{args.term}'")
            return 0
        
        total_found = sum(len(shortcuts) for shortcuts in found_shortcuts.values())
        print(f"Found {total_found} shortcut(s) matching '{args.term}':")
        print()
        
        for mode, shortcuts in found_shortcuts.items():
            print(f"📁 {mode.upper()} mode ({len(shortcuts)} matches):")
            
            if args.verbose:
                for shortcut in sorted(shortcuts):
                    details = creator.get_shortcut_details(shortcut, mode)
                    print(f"  • {shortcut}")
                    if details:
                        print(f"    Description: {details.get('description', 'N/A')}")
                        print(f"    URL: {details.get('url', 'N/A')}")
                        print(f"    Browser: {details.get('browser_command', 'xdg-open')}")
                    print()
            else:
                for shortcut in sorted(shortcuts):
                    print(f"  • {shortcut}")
            print()
        
        return 0
        
    except Exception as e:
        print(f"✗ Error searching shortcuts: {e}", file=sys.stderr)
        return 1


def show_shortcut(creator: DesktopFileCreator, args) -> int:
    """Show detailed information about a specific shortcut."""
    try:
        modes_to_check = ["user", "system"] if args.mode == "all" else [args.mode]
        
        for mode in modes_to_check:
            shortcuts = creator.list_shortcuts(mode)
            if args.name in shortcuts:
                details = creator.get_shortcut_details(args.name, mode)
                
                print(f"📋 Shortcut Details: {args.name}")
                print(f"{'='*50}")
                print(f"Mode:        {mode}")
                print(f"Name:        {details.get('name', 'N/A')}")
                print(f"Description: {details.get('description', 'N/A')}")
                print(f"URL:         {details.get('url', 'N/A')}")
                print(f"Browser:     {details.get('browser_command', 'xdg-open')}")
                
                # Show file location
                from lazylauncher.utils import sanitize_filename
                from lazylauncher.config import Config
                config = Config()
                filename = sanitize_filename(args.name) + ".desktop"
                file_path = config.get_applications_dir(mode) / filename
                print(f"File:        {file_path}")
                
                return 0
        
        print(f"✗ Shortcut '{args.name}' not found", file=sys.stderr)
        return 1
        
    except Exception as e:
        print(f"✗ Error showing shortcut details: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
