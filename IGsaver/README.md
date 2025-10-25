# IGsaver - Instagram Highlights Backup Tool

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: Clean Code](https://img.shields.io/badge/code%20style-clean-brightgreen.svg)](https://github.com/zedr/clean-code-python)

CLI tool in Python to backup your Instagram highlights and active stories with smart incremental backup, progress tracking, and comprehensive reporting.

## Features

- ✅ Download all your Instagram highlights
- ✅ Download active stories (24h expiration)
- ✅ Smart incremental backup (skip existing files)
- ✅ Visual progress bars with real-time tracking
- ✅ Comprehensive summary reports
- ✅ Advanced CLI with many options
- ✅ Configuration file support (YAML)
- ✅ Filters: date range, video/photo only, patterns
- ✅ Save videos, photos and metadata
- ✅ Automatic folder organization
- ✅ Secure credentials management (session tokens + 2FA)

## Installation

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

## Roadmap

- [x] Advanced CLI options (argparse) ✅
- [x] Incremental backup (only new content) ✅
- [x] Download active stories (24h) ✅
- [x] Visual progress bars ✅
- [x] Comprehensive summary reports ✅
- [x] Configuration file support ✅
- [ ] Desktop interface (PyQt)
- [ ] Hybrid solution with Laravel backend
- [ ] Multi-account support
- [ ] Scheduled automatic backups
