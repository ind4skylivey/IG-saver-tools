# IGsaver Features

## 🚀 New Features (v1.0)

### 1. Advanced CLI with argparse

Complete command-line interface with many options:

```bash
# Show help
./run.sh --help

# Download with custom output directory
./run.sh -o /custom/path username

# Force re-download (ignore existing files)
./run.sh --force

# Quiet mode (minimal output)
./run.sh -q username

# Verbose mode (debug info)
./run.sh -v username

# Disable progress bars
./run.sh --no-progress username
```

### 2. Incremental Backup (Smart Skip)

**Enabled by default!** The script automatically skips files that already exist.

**How it works:**
- Checks if file already exists before downloading
- Compares by filename (date + UTC timestamp)
- Saves bandwidth and time on subsequent runs

**Example:**
```bash
# First run: Downloads everything
./run.sh
# Downloads: 100 items

# Second run: Only downloads new content
./run.sh  
# Downloads: 5 new items, skipped 95 existing
```

**Force full re-download:**
```bash
./run.sh --force  # Re-downloads everything
```

### 3. Visual Progress Bars

Beautiful progress indicators powered by `tqdm`:

```
Processing highlights: 100%|████████████| 15/15 [02:30<00:00, 10.0s/highlight]

📁 promesse🌛🌜
  ✓ 12 items, 0 failed

📁 evol love
  ✓ 25 items, 1 failed
```

**Disable if needed:**
```bash
./run.sh --no-progress
```

### 4. Comprehensive Summary Report

After backup completes, see detailed statistics:

```
============================================================
BACKUP SUMMARY
============================================================
Target: sib.liv3y
Output: /home/il1v3y/projects/personal/IGsaver/backups
Duration: 5m 32s

Highlights:
  ✓ Downloaded: 12
  ⊘ Skipped: 3
  ━ Total found: 15

Items:
  ✓ Downloaded: 89
  ⊘ Skipped (already exist): 45
  ✗ Failed: 2
  ━ Total: 136

Downloaded: 1.2 GB

✓ BACKUP COMPLETED SUCCESSFULLY
============================================================
```

## 🎯 Common Use Cases

### Daily Backup (Incremental)
```bash
# Cron job or manual - only downloads new content
./run.sh
```

### One-time Full Backup
```bash
# First time or when you want everything fresh
./run.sh --force -o /backup/location
```

### Quick Check (Quiet Mode)
```bash
# Minimal output, perfect for scripts
./run.sh -q
```

### Debug Issues (Verbose)
```bash
# See detailed logs for troubleshooting
./run.sh -v
```

### Custom Location
```bash
# Save to external drive or specific folder
./run.sh -o /mnt/external/instagram_backup
```

## 📊 Performance Improvements

| Feature | Benefit |
|---------|---------|
| **Incremental Backup** | 10x faster subsequent runs |
| **Progress Bars** | Know exactly what's happening |
| **Skip Existing** | Save bandwidth & time |
| **Summary Report** | Track what was downloaded |

## 🔧 Technical Details

### Incremental Backup Logic

Files are identified by:
- Date/time (UTC): `2024-01-20_01-56-19_UTC`
- Extension: `.mp4` (video) or `.jpg` (photo)

If file exists with same name → skip download

### Progress Tracking

- Per-highlight progress bar
- Real-time item count
- Time elapsed/remaining
- Non-intrusive (can be disabled)

### Statistics Collection

Tracks:
- Highlights: found, downloaded, skipped, failed
- Items: downloaded, skipped, failed
- Total size downloaded
- Duration
- Errors (with messages)

## 🎓 Examples

### Example 1: First Backup
```bash
$ ./run.sh

==================================================
Instagram Highlights Backup Tool
==================================================
Instagram username: sib.liv3y
[... authentication ...]

Processing highlights: 100%|████████████| 15/15

============================================================
BACKUP SUMMARY
============================================================
Target: sib.liv3y
Duration: 8m 15s
Highlights: ✓ 15 downloaded
Items: ✓ 134 downloaded
Downloaded: 2.1 GB
✓ BACKUP COMPLETED SUCCESSFULLY
============================================================
```

### Example 2: Incremental Update (Next Day)
```bash
$ ./run.sh

==================================================
Instagram Highlights Backup Tool
==================================================
[... using saved session ...]

Processing highlights: 100%|████████████| 15/15

============================================================
BACKUP SUMMARY
============================================================
Target: sib.liv3y
Duration: 45s
Highlights: ✓ 2 downloaded, ⊘ 13 skipped
Items: ✓ 8 downloaded, ⊘ 126 skipped
Downloaded: 156 MB
✓ BACKUP COMPLETED SUCCESSFULLY
============================================================
```

### Example 3: Quiet Mode (for Automation)
```bash
$ ./run.sh -q
$ echo $?
0  # Success
```

## 🚨 Important Notes

1. **Incremental is ON by default** - Use `--force` to disable
2. **Progress bars auto-disable** in non-TTY environments
3. **Quiet mode** still logs to file for debugging
4. **Summary always generated** (saved in logs)

## ✅ Completed Features

- [x] Advanced CLI with argparse
- [x] Incremental backup (skip existing)
- [x] Visual progress bars
- [x] Comprehensive summary reports
- [x] Download active stories (24h)
- [x] Configuration file (YAML)
- [x] Filters: date range, video/photo, patterns

## 🔮 Coming Soon

- [ ] Export to different formats
- [ ] Multi-account support
- [ ] Scheduled automatic backups
- [ ] Desktop interface (PyQt)
- [ ] Web dashboard
