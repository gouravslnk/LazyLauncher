# LazyLauncher CLI

Command-line interface for LazyLauncher - Create, Update, Delete and Manage KRunner shortcuts from the terminal.

## Overview

The LazyLauncher CLI provides a powerful command-line alternative to the GUI interface, offering complete CRUD (Create, Read, Update, Delete) operations for managing KRunner shortcuts. Perfect for power users, automation scripts, or remote server management.

## Installation & Setup

### Prerequisites
- Python 3.6 or higher
- KDE Plasma desktop environment
- KRunner (kbuildsycoca5 or kbuildsycoca6)

### Running the CLI

Navigate to the LazyLauncher directory and run:

```bash
python scripts/lazylauncher_cli.py [command] [options]
```

Or make it executable and run directly:

```bash
chmod +x scripts/lazylauncher_cli.py
./scripts/lazylauncher_cli.py [command] [options]
```

## Commands

### 📝 `create` - Create a new shortcut

Create a new KRunner shortcut.

**Syntax:**
```bash
python scripts/lazylauncher_cli.py create <name> <url> [options]
```

**Options:**
- `-d, --description TEXT` - Description of the shortcut
- `-b, --browser TEXT` - Browser command (default: xdg-open)
- `-m, --mode {user,system}` - Installation mode (default: user)
- `-f, --force` - Force overwrite if shortcut exists

**Examples:**
```bash
# Basic shortcut
python scripts/lazylauncher_cli.py create yt https://youtube.com

# With description
python scripts/lazylauncher_cli.py create yt https://youtube.com -d "YouTube"

# With custom browser
python scripts/lazylauncher_cli.py create yt https://youtube.com -b "firefox" -d "YouTube"

# System-wide shortcut (requires sudo)
python scripts/lazylauncher_cli.py create yt https://youtube.com -m system

# Force overwrite existing
python scripts/lazylauncher_cli.py create yt https://youtube.com -f
```

---

### 🔄 `update` - Update an existing shortcut

Modify an existing shortcut's properties.

**Syntax:**
```bash
python scripts/lazylauncher_cli.py update <name> [options]
```

**Options:**
- `-u, --url TEXT` - New URL or path
- `-d, --description TEXT` - New description
- `-b, --browser TEXT` - New browser command
- `-m, --mode {user,system}` - Installation mode (default: user)

**Examples:**
```bash
# Update URL only
python scripts/lazylauncher_cli.py update yt -u https://youtube.com/feed/subscriptions

# Update description only
python scripts/lazylauncher_cli.py update yt -d "YouTube Subscriptions"

# Update multiple properties
python scripts/lazylauncher_cli.py update yt -u https://youtube.com/feed/subscriptions -d "YouTube Subs" -b firefox

# Update system shortcut
python scripts/lazylauncher_cli.py update yt -u https://youtube.com/trending -m system
```

---

### 🗑️ `remove` - Remove a shortcut

Delete an existing shortcut.

**Syntax:**
```bash
python scripts/lazylauncher_cli.py remove <name> [options]
```

**Options:**
- `-m, --mode {user,system}` - Installation mode (default: user)
- `-y, --yes` - Skip confirmation prompt

**Examples:**
```bash
# Remove with confirmation
python scripts/lazylauncher_cli.py remove yt

# Remove without confirmation
python scripts/lazylauncher_cli.py remove yt -y

# Remove system shortcut
python scripts/lazylauncher_cli.py remove yt -m system -y
```

---

### 📋 `list` - List existing shortcuts

Display all shortcuts or shortcuts from specific mode.

**Syntax:**
```bash
python scripts/lazylauncher_cli.py list [options]
```

**Options:**
- `-m, --mode {user,system,all}` - Installation mode (default: user)
- `-v, --verbose` - Show detailed information

**Examples:**
```bash
# List user shortcuts
python scripts/lazylauncher_cli.py list

# List system shortcuts
python scripts/lazylauncher_cli.py list -m system

# List all shortcuts from both modes
python scripts/lazylauncher_cli.py list -m all

# List with detailed information
python scripts/lazylauncher_cli.py list -v

# List all with details
python scripts/lazylauncher_cli.py list -m all -v
```

**Sample Output:**
```
Found 5 shortcut(s):

📁 USER mode (3 shortcuts):
  • gmail
  • github
  • youtube

📁 SYSTEM mode (2 shortcuts):
  • calculator
  • text-editor
```

---

### 🔍 `search` - Search shortcuts

Find shortcuts by name using pattern matching.

**Syntax:**
```bash
python scripts/lazylauncher_cli.py search <term> [options]
```

**Options:**
- `-m, --mode {user,system,all}` - Installation mode (default: all)
- `-v, --verbose` - Show detailed information

**Examples:**
```bash
# Search in all modes
python scripts/lazylauncher_cli.py search google

# Search in user mode only
python scripts/lazylauncher_cli.py search google -m user

# Search with detailed info
python scripts/lazylauncher_cli.py search youtube -v
```

**Sample Output:**
```
Found 2 shortcut(s) matching 'google':

📁 USER mode (2 matches):
  • google
  • google-drive
```

---

### 👁️ `show` - Show shortcut details

Display detailed information about a specific shortcut.

**Syntax:**
```bash
python scripts/lazylauncher_cli.py show <name> [options]
```

**Options:**
- `-m, --mode {user,system,all}` - Installation mode (default: all)

**Examples:**
```bash
# Show shortcut details (searches all modes)
python scripts/lazylauncher_cli.py show youtube

# Show from specific mode
python scripts/lazylauncher_cli.py show youtube -m user
```

**Sample Output:**
```
📋 Shortcut Details: youtube
==================================================
Mode:        user
Name:        youtube
Description: YouTube
URL:         https://youtube.com
Browser:     xdg-open
File:        /home/user/.local/share/applications/youtube.desktop
```

## Common Use Cases

### Quick Setup
```bash
# Create common shortcuts
python scripts/lazylauncher_cli.py create yt https://youtube.com -d "YouTube"
python scripts/lazylauncher_cli.py create gh https://github.com -d "GitHub"
python scripts/lazylauncher_cli.py create gmail https://mail.google.com -d "Gmail"
```

### Bulk Operations
```bash
# List all shortcuts and save to file
python scripts/lazylauncher_cli.py list -m all -v > my_shortcuts.txt

# Search and remove test shortcuts
python scripts/lazylauncher_cli.py search test
python scripts/lazylauncher_cli.py remove test-shortcut -y
```

### System Administration
```bash
# Create system-wide shortcuts (requires sudo privileges)
sudo python scripts/lazylauncher_cli.py create office https://office.com -m system -d "Office 365"

# List system shortcuts
python scripts/lazylauncher_cli.py list -m system
```

### Custom Browser Configuration
```bash
# Create shortcuts with specific browsers
python scripts/lazylauncher_cli.py create fb https://facebook.com -b "google-chrome" -d "Facebook"
python scripts/lazylauncher_cli.py create twitter https://twitter.com -b "firefox" -d "Twitter"
```

## Error Handling

The CLI provides comprehensive error handling and validation:

- **Invalid URLs**: Validates URLs and file paths
- **Missing shortcuts**: Checks if shortcuts exist before operations
- **Permission issues**: Handles system mode permission requirements
- **Browser validation**: Verifies custom browser commands exist

**Example Error Messages:**
```bash
# Invalid shortcut name
✗ Error: Shortcut name contains invalid characters

# Shortcut not found
✗ Error: Shortcut 'nonexistent' not found in user mode

# Invalid browser
✗ Error: Browser command not found or invalid: /path/to/invalid/browser
```

## Tips & Best Practices

### 1. **Use Descriptive Names**
```bash
# Good
python scripts/lazylauncher_cli.py create youtube-music https://music.youtube.com -d "YouTube Music"

# Less clear
python scripts/lazylauncher_cli.py create ym https://music.youtube.com
```

### 2. **Organize with Consistent Naming**
```bash
# Group related shortcuts
python scripts/lazylauncher_cli.py create google-search https://google.com -d "Google Search"
python scripts/lazylauncher_cli.py create google-drive https://drive.google.com -d "Google Drive"
python scripts/lazylauncher_cli.py create google-docs https://docs.google.com -d "Google Docs"
```

### 3. **Use Force Flag for Updates**
```bash
# Update by recreating with force flag
python scripts/lazylauncher_cli.py create yt https://youtube.com/new-url -f -d "Updated YouTube"
```

### 4. **Backup Your Shortcuts**
```bash
# Export shortcuts for backup
python scripts/lazylauncher_cli.py list -m all -v > shortcuts_backup.txt
```

### 5. **Test Before System Installation**
```bash
# Test in user mode first
python scripts/lazylauncher_cli.py create test-shortcut https://example.com
# Test it works in KRunner
# Then create system version
sudo python scripts/lazylauncher_cli.py create test-shortcut https://example.com -m system
```

## Integration with Scripts

The CLI can be easily integrated into shell scripts for automation:

```bash
#!/bin/bash
# setup_shortcuts.sh - Setup common development shortcuts

echo "Setting up development shortcuts..."

python scripts/lazylauncher_cli.py create gh https://github.com -d "GitHub" -f
python scripts/lazylauncher_cli.py create so https://stackoverflow.com -d "Stack Overflow" -f
python scripts/lazylauncher_cli.py create docs https://devdocs.io -d "DevDocs" -f

echo "Development shortcuts created!"
python scripts/lazylauncher_cli.py list
```

## Troubleshooting

### Common Issues:

1. **Permission Denied (System Mode)**
   ```bash
   # Solution: Use sudo for system mode
   sudo python scripts/lazylauncher_cli.py create shortcut https://example.com -m system
   ```

2. **Shortcut Not Appearing in KRunner**
   ```bash
   # Solution: Refresh KRunner database manually
   kbuildsycoca6 --noincremental
   # or
   kbuildsycoca5 --noincremental
   ```

3. **Custom Browser Not Working**
   ```bash
   # Check if browser exists
   which firefox
   # Use full path if needed
   python scripts/lazylauncher_cli.py create shortcut https://example.com -b "/usr/bin/firefox"
   ```

## Exit Codes

- `0`: Success
- `1`: Error (validation, file operations, etc.)

This makes the CLI suitable for use in automated scripts with proper error handling.

## Related Files

- `../lazylauncher/gui.py` - GUI version with same functionality
- `../lazylauncher/creator.py` - Core shortcut creation logic
- `../lazylauncher/config.py` - Configuration and defaults
- `../lazylauncher/utils.py` - Utility functions

## Support

For issues or questions, please refer to the main project README or create an issue in the project repository.
