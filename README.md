# LazyLauncher - GUI Tool to Create Custom KRunner Shortcuts

> Why click twice when you can click once?

LazyLauncher is a simple GUI and CLI tool for KDE Plasma users to easily create custom KRunner shortcuts without manually editing `.desktop` files.

## What is LazyLauncher?

Create custom shortcuts for KDE's KRunner (Alt+F2 or ALT+SPACE) with ease:
- `yt` → Opens YouTube
- `gh` → Opens GitHub  
- `g` → Opens Google Search
- `docs` → Opens your Documents folder

##  Features

###  GUI Interface
- **Tabbed interface** with Create and Manage tabs
- **Complete CRUD operations**: Create, Update, Delete shortcuts
- **Search functionality** to quickly find existing shortcuts
- **Professional styling** with modern colors
- **Custom browser selection** (default or manual path)
- **Instant KRunner integration**

###  CLI Interface
- **Full command-line interface** with comprehensive options
- **Six main commands**: create, update, remove, list, search, show
- **Verbose modes** and **regex search**
- **Interactive confirmation** for destructive operations

##  Requirements

- **Python 3.6+** (with tkinter)
- **KDE Plasma** desktop environment
- **kbuildsycoca5/6** (for KRunner integration)

##  Installation

### Arch Linux (Recommended)
```bash
yay -S lazylauncher
# OR
paru -S lazylauncher
```

### Manual Installation
```bash
git clone https://github.com/gouravslnk/LazyLauncher.git
cd LazyLauncher

# GUI Mode
python3 -m lazylauncher

# CLI Mode
python3 scripts/lazylauncher_cli.py --help
```

##  Quick Examples

### GUI Usage:
1. Run: `lazylauncher` (if installed via AUR) or `python3 -m lazylauncher`
2. **Create Tab**: Fill form to create new shortcuts
3. **Manage Tab**: Search, update, or delete existing shortcuts
4. Test: Press `Alt+F2` and type your shortcut name

### CLI Usage:
```bash
# If installed via AUR:
lazylauncher-cli create yt "https://youtube.com" -d "YouTube"
lazylauncher-cli list
lazylauncher-cli search youtube

# If running from source:
python3 scripts/lazylauncher_cli.py create yt "https://youtube.com" -d "YouTube"
python3 scripts/lazylauncher_cli.py list
python3 scripts/lazylauncher_cli.py search youtube
```

## 📁 Project Structure

```
LazyLauncher/
├── lazylauncher/           # Main package
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # Entry point for module execution
│   ├── gui.py              # Tkinter GUI interface
│   ├── creator.py          # Desktop file creation logic
│   ├── config.py           # Configuration and defaults
│   └── utils.py            # Utility functions
├── scripts/                # Additional utilities
│   ├── lazylauncher_cli.py # Command-line interface
│   └── README.md           # CLI documentation
├── assets/                 # Icons and resources
│   ├── site_icons.json     # Icon mappings
│   └── README.md           # Assets documentation
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── LICENSE                # MIT License
```

##  How It Works

1. **User Input**: Collects shortcut details through GUI or CLI
2. **File Generation**: Creates a `.desktop` file with proper format
3. **File Placement**: Saves to `~/.local/share/applications/` (user mode)
4. **Database Update**: Runs `kbuildsycoca5/6` to refresh KRunner's cache
5. **Ready to Use**: Shortcut immediately available in KRunner

##  Troubleshooting

- **Tkinter import error**: Install `python3-tk` package
- **KRunner not updating**: Ensure `kbuildsycoca5/6` is installed
- **Shortcuts not appearing**: Try logging out and back in

##  Contributing

Contributions welcome! Please feel free to submit:
-  Bug reports
-  Feature requests  
-  Pull requests

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



