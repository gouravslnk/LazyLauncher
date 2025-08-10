# 🚀 Complete AUR Guide: Publish LazyLauncher to Arch Linux Repository

## 📋 What is AUR?

**AUR (Arch User Repository)** is where Arch Linux users get software. When you publish LazyLauncher here, **millions of users** can install it with:

```bash
yay -S lazylauncher
```

This puts your app alongside **Discord, Spotify, VS Code, and other major applications!**

---

## 🎯 Step-by-Step AUR Publication Process

### **Prerequisites**
- ✅ Arch Linux system (or Arch-based like Manjaro, EndeavourOS)
- ✅ `base-devel` package group installed
- ✅ SSH key generated
- ✅ Git configured

Let's check these:

```bash
# Install base-devel if missing
sudo pacman -S base-devel

# Generate SSH key if missing
ssh-keygen -t ed25519 -C "your-email@example.com"

# Configure git if missing
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

---

## **Step 1: Test PKGBUILD Locally (5 minutes)**

This ensures everything works before publishing:

```bash
# In your LazyLauncher directory
cd /path/to/LazyLauncher

# Test build
makepkg -si

# If successful, test the installed package
lazylauncher
lazylauncher-cli --help

# Clean up test files
rm -f *.pkg.tar.xz *.pkg.tar.zst
```

**✅ Expected Result:** LazyLauncher installs and runs without errors.

**❌ If errors occur:**
- Check PKGBUILD syntax
- Ensure all dependencies are correct
- Fix issues before proceeding

---

## **Step 2: Create GitHub Release (10 minutes)**

AUR needs a source tarball. Create a GitHub release:

### **2.1 Create Release on GitHub:**

1. **Go to your repository:**
   ```
   https://github.com/gouravslnk/LazyLauncher/releases
   ```

2. **Click "Create a new release"**

3. **Fill the form:**
   - **Tag version:** `v1.0.0`
   - **Release title:** `LazyLauncher v1.0.0 - GUI Tool for KRunner Shortcuts`
   - **Description:**
     ```markdown
     # LazyLauncher v1.0.0
     
     🎉 First stable release of LazyLauncher!
     
     ## What's New
     - Complete GUI interface with tabbed layout
     - Full CLI with 6 commands (create, update, remove, list, search, show)
     - Search functionality for managing shortcuts
     - Professional styling and user experience
     
     ## Installation
     
     ### Arch Linux (AUR)
     ```bash
     yay -S lazylauncher
     ```
     
     ### Manual Installation
     1. Download and extract the source code
     2. Run: `python3 -m lazylauncher`
     
     ## Usage
     - **GUI Mode:** `lazylauncher`
     - **CLI Mode:** `lazylauncher-cli --help`
     
     Enjoy creating custom KRunner shortcuts! 🚀
     ```

4. **Click "Publish release"**

### **2.2 Update PKGBUILD with Checksum:**

```bash
# Download the release tarball
wget https://github.com/gouravslnk/LazyLauncher/archive/v1.0.0.tar.gz

# Calculate SHA256 checksum
sha256sum v1.0.0.tar.gz

# Copy the checksum and update PKGBUILD
# Replace 'SKIP' with the actual checksum
```

Edit your `PKGBUILD` and replace:
```bash
sha256sums=('SKIP')
```

With:
```bash
sha256sums=('your-actual-checksum-here')
```

### **2.3 Test with Real Tarball:**

```bash
# Test with the GitHub release
makepkg -si
```

---

## **Step 3: Create AUR Account (5 minutes)**

### **3.1 Register Account:**

1. **Go to AUR registration:**
   ```
   https://aur.archlinux.org/register/
   ```

2. **Fill the form:**
   - Username (e.g., `gouravslnk`)
   - Email address
   - Real name
   - Password

3. **Verify email** and **activate account**

### **3.2 Add SSH Key:**

1. **Copy your public SSH key:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. **Add to AUR account:**
   - Go to: https://aur.archlinux.org/account/
   - Click "My Account"
   - Paste your public key in "SSH Public Key" field
   - Save

### **3.3 Test SSH Connection:**

```bash
ssh aur@aur.archlinux.org help
```

**✅ Expected:** You see AUR help message
**❌ If error:** Check SSH key setup

---

## **Step 4: Publish to AUR (10 minutes)**

### **4.1 Clone AUR Repository:**

```bash
# Clone your AUR package repository
git clone ssh://aur@aur.archlinux.org/lazylauncher.git

# If repository doesn't exist, it will be empty (that's normal)
cd lazylauncher
```

### **4.2 Prepare Files:**

```bash
# Copy PKGBUILD from your LazyLauncher directory
cp ../LazyLauncher/PKGBUILD .

# Verify PKGBUILD
cat PKGBUILD

# Test one more time to be sure
makepkg -si
```

### **4.3 Create .SRCINFO:**

```bash
# Generate .SRCINFO (required by AUR)
makepkg --printsrcinfo > .SRCINFO

# Verify it looks correct
cat .SRCINFO
```

### **4.4 Commit and Push:**

```bash
# Add files
git add PKGBUILD .SRCINFO

# Commit
git commit -m "Initial upload: LazyLauncher v1.0.0

LazyLauncher is a GUI tool for creating custom KRunner shortcuts in KDE Plasma.

Features:
- Tabbed GUI interface (Create/Manage tabs)
- Complete CRUD operations for shortcuts
- Full CLI with 6 commands
- Search functionality
- Professional design
- Instant KRunner integration"

# Push to AUR
git push origin master
```

---

## **Step 5: Verify Publication (2 minutes)**

### **5.1 Check AUR Page:**

1. **Go to your package page:**
   ```
   https://aur.archlinux.org/packages/lazylauncher
   ```

2. **Verify information:**
   - ✅ Package name: `lazylauncher`
   - ✅ Description appears correctly
   - ✅ Dependencies listed
   - ✅ Source URL points to your GitHub
   - ✅ Maintainer shows your name

### **5.2 Test Installation:**

```bash
# Remove your local version first
sudo pacman -R lazylauncher

# Install from AUR
yay -S lazylauncher

# Test it works
lazylauncher
lazylauncher-cli --help
```

**🎉 SUCCESS!** Your package is now live on AUR!

---

## **Step 6: Share with Community (Optional)**

### **6.1 Update Your GitHub README:**

Add AUR installation instructions:

```markdown
## Installation

### Arch Linux (AUR)
```bash
yay -S lazylauncher
# OR
paru -S lazylauncher
```

### Other Distributions
Download from [GitHub Releases](https://github.com/gouravslnk/LazyLauncher/releases)
```

### **6.2 Announce on Reddit:**

- r/archlinux
- r/kde
- r/linux

Example post:
```
[NEW AUR PACKAGE] LazyLauncher - GUI tool for KRunner shortcuts

I've published LazyLauncher to AUR! It's a simple GUI/CLI tool for creating 
custom KRunner shortcuts in KDE Plasma.

Install: yay -S lazylauncher

Features:
- Tabbed GUI interface
- Complete shortcut management
- CLI with 6 commands
- Search functionality

GitHub: https://github.com/gouravslnk/LazyLauncher
AUR: https://aur.archlinux.org/packages/lazylauncher
```

---

## **📊 Maintenance & Updates**

### **When You Release v1.1.0:**

1. **Create GitHub release** (as before)
2. **Update PKGBUILD:**
   ```bash
   pkgver=1.1.0
   pkgrel=1  # Reset to 1 for new version
   # Update sha256sum
   ```
3. **Update AUR:**
   ```bash
   makepkg --printsrcinfo > .SRCINFO
   git add PKGBUILD .SRCINFO
   git commit -m "Update to v1.1.0"
   git push
   ```

### **If Users Report Issues:**

- Monitor AUR comments
- Fix issues in your GitHub repo
- Update AUR package accordingly

---

## **🎉 Success Metrics**

After publication, you can track:

- **AUR votes:** Users vote for good packages
- **Popularity:** How many users install it
- **Comments:** User feedback and suggestions
- **Flagged:** Community reports if package needs attention

**Your LazyLauncher is now available to millions of Arch Linux users!**

---

## **🆘 Troubleshooting**

### **makepkg fails:**
```bash
# Check dependencies
pacman -S base-devel
# Check PKGBUILD syntax
```

### **SSH key issues:**
```bash
# Regenerate key
ssh-keygen -t ed25519 -C "your-email@example.com"
# Add to AUR account
```

### **Git push fails:**
```bash
# Check remote
git remote -v
# Should show: ssh://aur@aur.archlinux.org/lazylauncher.git
```

### **Package not found after upload:**
- Wait 5-10 minutes for AUR to refresh
- Check AUR page for errors
- Verify .SRCINFO was generated correctly

---

**🚀 You're now an AUR package maintainer! Welcome to the community!**
