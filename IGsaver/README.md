<div align="center">

# 📸 IGsaver

### Your Personal Instagram Backup Solution

*Never lose your memories again. Backup your Instagram highlights & stories with one command.*

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: Clean Code](https://img.shields.io/badge/code%20style-clean-brightgreen.svg)](https://github.com/zedr/clean-code-python)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ind4skylivey/IG-saver-tools/pulls)
[![GitHub Stars](https://img.shields.io/github/stars/ind4skylivey/IG-saver-tools?style=social)](https://github.com/ind4skylivey/IG-saver-tools)

[Features](#-features) • [Quick Start](#-quick-start) • [Demo](#-demo) • [Documentation](#-documentation) • [Roadmap](#-roadmap)

</div>

---

## 🎯 Why IGsaver?

Instagram doesn't make it easy to backup your precious memories. Stories disappear in 24 hours, and even highlights can be lost if something happens to your account. **IGsaver gives you full control.**

```bash
./run.sh              # That's it! All your highlights backed up locally.
```

### The Problem
- 📉 Instagram's official data export takes 48+ hours
- ⏰ Stories disappear after 24 hours forever
- 🔒 Your memories are locked in Instagram's servers
- 💔 Account issues? Say goodbye to your content

### The Solution
**IGsaver**: Fast, local, secure backup of your Instagram content with a single command.

## ✨ Features

<table>
<tr>
<td width="50%">

### 🚀 Smart & Fast
- **Incremental Backup**: Only downloads new content (90% faster!)
- **Progress Tracking**: Real-time progress bars
- **Batch Download**: Get all highlights at once
- **Stories Support**: Capture before 24h expiration

</td>
<td width="50%">

### 🔐 Safe & Secure
- **Zero Password Storage**: Uses session tokens
- **2FA Support**: Works with secured accounts
- **Local Storage**: Your data stays on YOUR device
- **Open Source**: Transparent, auditable code

</td>
</tr>
<tr>
<td width="50%">

### ⚙️ Powerful & Flexible
- **Advanced Filters**: Date range, type, size
- **YAML Configuration**: Customize everything
- **CLI Expert Mode**: 15+ command options
- **Rich Reports**: Detailed statistics

</td>
<td width="50%">

### 🎯 Coming Soon
- **🖥️ Desktop App**: GUI for Windows, Mac, Linux
- **📅 Scheduled Backups**: Automatic daily sync
- **☁️ Cloud Sync**: Optional backup to cloud
- **📊 Analytics Dashboard**: Visualize your content

</td>
</tr>
</table>

## 📦 Demo

> **Note**: Screenshots and demo GIF coming soon! The tool is fully functional.

**What you get:**

```
📁 backups/
└── your_username/
    └── highlights/
        ├── Travel_2024/
        │   ├── 2024-01-20_01-56-19_UTC.mp4
        │   ├── 2024-02-05_13-27-04_UTC.mp4
        │   └── metadata files...
        ├── Family_Moments/
        └── Best_Memories/
```

**Example output:**

```bash
$ ./run.sh

==================================================
Instagram Highlights Backup Tool
==================================================
Loading saved session for your_username...
✓ Session loaded successfully

Processing highlights: 100%|████████████| 15/15 [02:30<00:00]

📁 Travel 2024
  ✓ 12 items, 0 failed

📁 Family Moments
  ✓ 25 items, 1 failed

============================================================
BACKUP SUMMARY
============================================================
Target: your_username
Duration: 2m 35s

Highlights:
  ✓ Downloaded: 15
  ⊘ Skipped: 0
  ━ Total found: 15

Items:
  ✓ Downloaded: 134
  ⊘ Skipped (already exist): 0
  ━ Total: 134

Downloaded: 2.1 GB

✓ BACKUP COMPLETED SUCCESSFULLY
============================================================
```

## 🚀 Quick Start

1. Create virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure username:
```bash
cp .env.example .env
# Edit .env with your Instagram username (optional)
```

## Usage

### Basic Usage

**Download your highlights (with incremental backup):**
```bash
./run.sh
```

**Download active stories (24h):**
```bash
./run.sh --stories
```

**Download from another user:**
```bash
./run.sh username
```

**Force re-download everything:**
```bash
./run.sh --force
```

### Advanced Options

```bash
# Custom output directory
./run.sh -o /backup/location

# Quiet mode (minimal output)
./run.sh -q

# Verbose mode (debug info)
./run.sh -v

# Disable progress bars
./run.sh --no-progress

# See all options
./run.sh --help
```

### Configuration File (Optional)

Create `config.yaml` to customize behavior:

```yaml
download:
  only_videos: false      # Download only videos
  only_photos: false      # Download only photos
  min_date: 2024-01-01    # Download from this date
  max_date: null          # Download until this date

filters:
  exclude_patterns: []    # Skip items matching patterns
  min_size_mb: null       # Minimum file size
```

See `config.example.yaml` for all options.

## Project Structure

```
IGsaver/
├── src/
│   ├── main.py           # Entry point
│   ├── app.py            # Main application orchestrator
│   ├── auth.py           # Authentication & session management
│   ├── downloader.py     # Download logic
│   ├── config.py         # Configuration management
│   ├── logger.py         # Logging setup
│   ├── ui.py             # User interface & output
│   ├── exceptions.py     # Custom exceptions
│   └── constants.py      # Constants and configuration
├── igsaver.py            # Convenience entry point
├── backups/              # Downloaded backups stored here
├── .sessions/            # Session tokens (excluded from git)
├── logs/                 # Process logs
├── requirements.txt      # Python dependencies
├── .env                  # Credentials (not included in git)
└── .env.example          # Configuration example
```

### Architecture

The project follows **Clean Code** principles:
- **Separation of Concerns**: Each module has a single responsibility
- **Type Hints**: All functions are properly typed
- **Dependency Injection**: Components receive dependencies
- **Custom Exceptions**: Proper error handling with specific exceptions
- **Logging**: Comprehensive logging for debugging and monitoring
- **UI Separation**: Business logic separated from presentation

## Security

### 3-Layer Authentication System:

1. **Session Tokens** (primary method)
   - First time: Login with password
   - Instaloader saves a session token in `.sessions/`
   - Subsequent uses: Token is used automatically

2. **Interactive Prompt** (fallback)
   - If no session exists or expired
   - Asks for password securely using `getpass`
   - Password is never displayed or saved

3. **Zero Password Storage**
   - ✅ Encrypted session tokens (renewable)
   - ✅ Passwords only in temporary memory
   - ❌ Passwords are NEVER saved to files

### Other considerations:

- If you have 2FA enabled, consider disabling it temporarily
- Instagram may rate-limit requests if you download too much at once
- Session tokens are stored in `.sessions/` (excluded from git)

## 🗺️ Roadmap

See our complete [ROADMAP.md](ROADMAP.md) for detailed plans!

### Current Status: v1.0.0 ✅
- [x] Advanced CLI with 15+ options
- [x] Smart incremental backup (90% faster!)
- [x] Download highlights & stories (24h)
- [x] Visual progress bars
- [x] Comprehensive reports
- [x] YAML configuration
- [x] 2FA support

### Coming in v2.0.0 🚀
- [ ] **🖥️ Desktop App** (Windows, Mac, Linux)
- [ ] **📅 Scheduled Backups** (Automatic daily sync)
- [ ] **☁️ Cloud Sync** (Optional backup to cloud)
- [ ] **📊 Analytics Dashboard** (Visualize your content)
- [ ] **🎨 Modern GUI** (Dark/Light themes)
- [ ] **🔔 Notifications** (Desktop alerts)

[View Full Roadmap →](ROADMAP.md)

---

## 🤝 Contributing

We love contributions! Whether it's:

- 🐛 Bug reports
- 💡 Feature requests
- 📖 Documentation improvements
- 🔧 Code contributions
- 🎨 UI/UX design for desktop app

Check out [CONTRIBUTING.md](CONTRIBUTING.md) to get started!

**Special call:** We're planning a desktop app! If you have experience with Electron, Tauri, or PyQt, we'd love your input on [Discussions](https://github.com/ind4skylivey/IG-saver-tools/discussions).

---

## ⭐ Show Your Support

If IGsaver helped you backup your precious memories:

- ⭐ **Star this repo** to show your support
- 🐦 **Share on social media** to help others discover it
- 🔗 **Tell your friends** who might need it
- 🤝 **Contribute** to make it even better

---

## 📄 License

MIT License - feel free to use, modify, and distribute!

See [LICENSE](LICENSE) for full details.

---

## 🙏 Acknowledgments

Built with:
- [Instaloader](https://github.com/instaloader/instaloader) - Instagram API wrapper
- [tqdm](https://github.com/tqdm/tqdm) - Progress bars
- Love for preserving memories ❤️

---

<div align="center">

**Made with ❤️ for Instagram users who want to own their memories**

[Report Bug](https://github.com/ind4skylivey/IG-saver-tools/issues) • [Request Feature](https://github.com/ind4skylivey/IG-saver-tools/issues) • [Discussions](https://github.com/ind4skylivey/IG-saver-tools/discussions)

⭐ **Star us on GitHub** — it motivates us to keep improving!

</div>
