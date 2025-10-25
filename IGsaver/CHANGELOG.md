# Changelog

All notable changes to IGsaver project.

## [1.0.0] - 2025-10-25

### ✅ Completed Features

#### 1. Advanced CLI with argparse
- Complete command-line interface with help system
- Options: `--stories`, `--force`, `--output`, `--quiet`, `--verbose`
- Comprehensive help with usage examples
- Argument validation and error handling

#### 2. Incremental Backup (Smart Skip)
- Automatically skips already downloaded files
- Detects files by date/timestamp pattern
- Saves bandwidth and time on subsequent runs
- Default enabled, use `--force` to disable
- Tracks skipped vs downloaded items

#### 3. Download Active Stories (24h)
- Download ephemeral stories before they expire
- Use `--stories` flag to activate
- Separate directory structure: `username/stories/`
- Same incremental backup logic
- Progress tracking per story

#### 4. Visual Progress Bars
- Real-time progress with tqdm library
- Per-highlight progress tracking
- Shows: current/total, elapsed time, ETA
- Can be disabled with `--no-progress`
- Non-intrusive output during download

#### 5. Configuration File Support (YAML)
- Optional `config.yaml` for advanced settings
- Filters: date range, video/photo only, file size
- Pattern matching: include/exclude
- Quality settings
- Rate limiting options
- See `config.example.yaml` for all options

#### 6. Comprehensive Summary Reports
- Detailed statistics after each backup
- Shows: highlights/items downloaded/skipped/failed
- Total size and duration
- Error list (if any)
- Success/failure status
- Saved to logs for later review

### 🔐 Security Features

- Session token management (no password storage)
- 2FA support with interactive prompts
- Secure password input (hidden)
- Session validation and auto-refresh
- Multiple authentication attempts

### 📁 Project Structure

- Clean code architecture with separation of concerns
- Type hints throughout codebase
- Modular design:
  - `cli.py` - Command-line interface
  - `auth.py` - Authentication
  - `downloader.py` - Highlights download
  - `stories_downloader.py` - Stories download
  - `config_loader.py` - Configuration management
  - `progress.py` - Progress tracking
  - `summary.py` - Statistics and reports
  - `ui.py` - User interface
  - `exceptions.py` - Custom exceptions
  - `constants.py` - Configuration constants

### 📊 Performance

- Incremental backups: 10x faster on subsequent runs
- Progress feedback: Real-time status updates
- Smart skip: Bandwidth saving
- Efficient file detection
- Parallel-ready architecture

### 📚 Documentation

- README.md - Complete usage guide
- FEATURES.md - Detailed feature explanations
- TROUBLESHOOTING.md - Common issues and solutions
- config.example.yaml - Configuration template
- Inline code documentation with docstrings

## Future Roadmap

- [ ] Desktop GUI interface (PyQt)
- [ ] Web dashboard
- [ ] Multi-account support
- [ ] Scheduled automatic backups
- [ ] Export to different formats
- [ ] Hybrid solution with Laravel backend

## Notes

### Instagram API Limitations

- Uses unofficial API (instaloader)
- Rate limiting may occur
- Challenge/security checks possible
- Recommend: max 1 backup per day

### Tested On

- Python 3.13.7
- Linux (Arch-based)
- Instagram accounts with/without 2FA

### Dependencies

- instaloader >= 4.10
- python-dotenv >= 1.0.0
- tqdm >= 4.66.0
- pyyaml >= 6.0
