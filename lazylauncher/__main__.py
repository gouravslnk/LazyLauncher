#!/usr/bin/env python3

"""Main entry point for the Lazy Launcher application.

This allows running the application with: python -m lazylauncher
"""

def main():
    """Main entry point that imports and runs the GUI."""
    from .gui import main as gui_main
    gui_main()

if __name__ == "__main__":
    main()
# This allows the script to be run directly.