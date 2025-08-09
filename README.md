# LazyLauncher - GUI Tool to Create Custom KRunner Shortcuts

> Why click twice when you can click once?

LazyLauncher is a simple GUI application built with Python and Tkinter that allows KDE Plasma users to easily create custom KRunner shortcuts without manually editing `.desktop` files.

## Problem Statement

KRunner in KDE Plasma allows launching applications and executing commands quickly, but it lacks a simple GUI for creating **custom shortcuts** (e.g., typing `yt Spiderman` to search YouTube). Currently, users must manually create `.desktop` files in `~/.local/share/applications/` and run `kbuildsycoca5` to refresh KRunner's database — a process that is tedious for users.

## Features

- **Form-based shortcut creation** with intuitive GUI
- **Custom browser selection** (default or manual path)
- **Automatic file placement** in appropriate directories
- **Instant KRunner update** using `kbuildsycoca5/kbuildsycoca6`
- **Smart icon detection** based on URL
- **Overwrite confirmation** for existing shortcuts
- **Both GUI and CLI interfaces**

## Installation

### Prerequisites

- Python 3.6 or higher
- KDE Plasma desktop environment
- Tkinter (usually included with Python)

### Quick Start

1. Clone or download the repository:
   ```bash
   git clone <repository-url>
   cd LazyLauncher
   ```

2. Run the GUI application:
   ```bash
   python -m lazylauncher
   ```

   Or run directly:
   ```bash
   python lazylauncher/gui.py
   ```

### CLI Usage

You can also use the command-line interface:

```bash
# Create a shortcut
python scripts/lazylauncher_cli.py create yt "https://youtube.com" -d "YouTube"

# List shortcuts
python scripts/lazylauncher_cli.py list

# Remove a shortcut
python scripts/lazylauncher_cli.py remove yt
```

## Usage

### GUI Interface

1. **Launch the application**: Run `python -m lazylauncher`
2. **Fill in the form**:
   - **Shortcut Name**: What you'll type in KRunner (e.g., `yt`)
   - **Description**: Human-readable description (e.g., `YouTube`)
   - **URL or Path**: The URL or file path to open
   - **Browser**: Choose default browser or specify custom path
   - **Installation Mode**: User mode (recommended) or system-wide

3. **Create the shortcut**: Click "Create Shortcut"
4. **Test it**: Press `Alt+F2` or `Alt+Space` and type your shortcut name

### Examples

- **YouTube**: Name: `yt`, URL: `https://youtube.com`
- **Google**: Name: `g`, URL: `https://google.com`
- **GitHub**: Name: `gh`, URL: `https://github.com`
- **Local folder**: Name: `docs`, URL: `/home/user/Documents`

## File Structure

```
LazyLauncher/
├── lazylauncher/           # Main package
│   ├── __init__.py         # Package initialization
│   ├── gui.py              # Tkinter GUI interface
│   ├── creator.py          # Desktop file creation logic
│   ├── config.py           # Configuration and defaults
│   ├── utils.py            # Utility functions
│   └── __main__.py         # Entry point for module execution
├── assets/                 # Icons and resources
├── tests/                  # Unit tests
│   ├── __init__.py
│   └── test_creator.py     # Tests for core functionality
├── scripts/                # Additional utilities
│   └── easylauncher_cli.py # Command-line interface
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── LICENSE                # License information
```

## How It Works

1. **User Input**: Collects shortcut details through GUI or CLI
2. **File Generation**: Creates a `.desktop` file with proper format:
   ```ini
   [Desktop Entry]
   Name=yt
   GenericName=YouTube
   Exec=xdg-open https://www.youtube.com
   Icon=youtube
   Type=Application
   Comment=YouTube
   Categories=Network;WebBrowser;
   StartupNotify=true
   ```
3. **File Placement**: Saves to `~/.local/share/applications/` (user mode) or `/usr/share/applications/` (system mode)
4. **Database Update**: Runs `kbuildsycoca5/kbuildsycoca6` to refresh KRunner's cache
5. **Ready to Use**: Shortcut immediately available in KRunner

## Technical Details

### Dependencies

- **Python 3.6+**: Core language
- **Tkinter**: GUI framework (built-in with Python)
- **Standard Library**: `os`, `pathlib`, `subprocess`, `urllib`

### Supported Platforms

- **Primary**: KDE Plasma on Linux
- **Secondary**: Any Linux desktop with KRunner support

### Icon Detection

LazyLauncher automatically selects appropriate icons based on the URL:
- YouTube, Google, GitHub, etc. → Site-specific icons
- HTTP/HTTPS URLs → Web browser icon
- File paths → Folder icon
- Other protocols → Generic application icon

## Development

### Running Tests

```bash
python -m unittest tests/test_creator.py -v
```

### Code Structure

- `gui.py`: Tkinter-based user interface
- `creator.py`: Core logic for `.desktop` file creation
- `config.py`: Configuration management and defaults
- `utils.py`: Helper functions for validation and file operations
- `__main__.py`: Entry point for `python -m lazylauncher`

## Troubleshooting

### Common Issues

1. **Shortcut doesn't appear in KRunner**:
   - Make sure `kbuildsycoca5` or `kbuildsycoca6` is installed
   - Try logging out and back in
   - Check if the `.desktop` file was created correctly

2. **Permission denied (system mode)**:
   - System mode requires sudo privileges
   - Use user mode instead (recommended)

3. **Custom browser not working**:
   - Verify the browser executable path is correct
   - Make sure the file is executable

### Debug Information

Check created `.desktop` files in:
- User mode: `~/.local/share/applications/`
- System mode: `/usr/share/applications/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- **PyQt/PySide GUI**: More modern interface
- **Icon fetching**: Automatic favicon download
- **Shortcut management**: Edit/organize existing shortcuts
- **Categories**: Better desktop file categorization
- **Templates**: Pre-defined shortcut templates
- **Import/Export**: Backup and share shortcuts

## Acknowledgments

- KDE Plasma team for the excellent desktop environment
- Python community for the great development tools
