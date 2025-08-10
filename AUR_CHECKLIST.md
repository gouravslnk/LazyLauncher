# ✅ AUR Publication Checklist

Follow this checklist to publish LazyLauncher to AUR:

## 🚀 Pre-Publication Checklist

### Prerequisites
- [ ] Running Arch Linux (or Arch-based distro)
- [ ] Have `base-devel` installed: `sudo pacman -S base-devel`
- [ ] SSH key generated: `ssh-keygen -t ed25519 -C "your-email@example.com"`
- [ ] Git configured with name and email

### Test PKGBUILD
- [ ] Run `makepkg -si` in LazyLauncher directory
- [ ] LazyLauncher installs without errors
- [ ] `lazylauncher` command works
- [ ] `lazylauncher-cli --help` works
- [ ] Clean up: `rm -f *.pkg.tar.*`

## 🏷️ Create GitHub Release

- [ ] Go to: https://github.com/gouravslnk/LazyLauncher/releases
- [ ] Click "Create a new release"
- [ ] Set tag: `v1.0.0`
- [ ] Set title: `LazyLauncher v1.0.0 - GUI Tool for KRunner Shortcuts`
- [ ] Add release description (see AUR_GUIDE.md for template)
- [ ] Click "Publish release"

### Update PKGBUILD Checksum
- [ ] Download: `wget https://github.com/gouravslnk/LazyLauncher/archive/v1.0.0.tar.gz`
- [ ] Get checksum: `sha256sum v1.0.0.tar.gz`
- [ ] Update PKGBUILD: replace `'SKIP'` with actual checksum
- [ ] Test again: `makepkg -si`

## 👤 Setup AUR Account

- [ ] Register at: https://aur.archlinux.org/register/
- [ ] Verify email and activate account
- [ ] Copy SSH public key: `cat ~/.ssh/id_ed25519.pub`
- [ ] Add SSH key to AUR account: https://aur.archlinux.org/account/
- [ ] Test SSH: `ssh aur@aur.archlinux.org help`

## 📦 Publish to AUR

- [ ] Clone AUR repo: `git clone ssh://aur@aur.archlinux.org/lazylauncher.git`
- [ ] Enter directory: `cd lazylauncher`
- [ ] Copy PKGBUILD: `cp ../LazyLauncher/PKGBUILD .`
- [ ] Generate .SRCINFO: `makepkg --printsrcinfo > .SRCINFO`
- [ ] Test build: `makepkg -si`
- [ ] Add files: `git add PKGBUILD .SRCINFO`
- [ ] Commit: `git commit -m "Initial upload: LazyLauncher v1.0.0"`
- [ ] Push: `git push origin master`

## ✅ Verify Success

- [ ] Check AUR page: https://aur.archlinux.org/packages/lazylauncher
- [ ] Package information appears correctly
- [ ] Install from AUR: `yay -S lazylauncher`
- [ ] Test installed package works

## 📢 Announce (Optional)

- [ ] Update GitHub README with AUR installation instructions
- [ ] Post on r/archlinux
- [ ] Post on r/kde
- [ ] Share with friends!

---

🎉 **Congratulations! LazyLauncher is now available to millions of Arch Linux users!**

For detailed instructions, see **AUR_GUIDE.md**
