# Testing Instructions

## How to Test IGsaver

Since the application requires interactive input (username and password), you need to run it from your terminal directly.

### Step 1: Navigate to Project Directory

```bash
cd /home/il1v3y/projects/personal/IGsaver
```

### Step 2: Run the Application

You can run it in two ways:

**Option A: Using the virtual environment directly (recommended)**
```bash
venv/bin/python igsaver.py
```

**Option B: Activate virtual environment first**
```bash
source venv/bin/activate
python igsaver.py
```

### What to Expect:

1. **First prompt**: Enter your Instagram username
   ```
   Instagram username: your_username_here
   ```

2. **Security notice**: You'll see this message
   ```
   ==================================================
   AUTHENTICATION REQUIRED
   ==================================================
   Your password will NOT be saved to any file.
   Only a temporary session token will be stored.
   ==================================================
   ```

3. **Password prompt**: Enter your password (won't be visible)
   ```
   Password for your_username_here: 
   ```

4. **Login process**: The system will authenticate
   ```
   Logging in as your_username_here...
   ✓ Session started and saved successfully
   ✓ Future runs won't require password entry
   ```

5. **Download process**: Your highlights will be downloaded
   ```
   Fetching profile for your_username_here...
   Downloading highlights from your_username_here...
   
   [1] Downloading: Highlight Name
     ✓ Item 1 downloaded
     ✓ Item 2 downloaded
     Total: 2 items in 'Highlight Name'
   
   ✓ Completed: X highlights downloaded
   Location: /home/il1v3y/projects/personal/IGsaver/backups/your_username_here
   ```

6. **Completion**:
   ```
   ==================================================
   Backup completed
   ==================================================
   ```

### Next Runs

On subsequent runs, you won't need to enter your password:

```bash
python igsaver.py
```

The system will automatically use your saved session token.

### Download Another User's Public Highlights

```bash
python igsaver.py another_username
```

### Check Your Backups

```bash
ls -la backups/
ls -la backups/your_username_here/highlights/
```

### Check Logs

```bash
ls -la logs/
cat logs/igsaver_*.log
```

### Troubleshooting

**If you get "2FA required" error:**
- Temporarily disable Two-Factor Authentication on Instagram
- Or use an app-specific password if Instagram provides one

**If you get "Invalid credentials":**
- Double-check your username and password
- Make sure your account is not locked or restricted

**If you get "Private profile" error:**
- You can only download highlights from accounts you follow
- Or your own account

**If session expires:**
- Simply run the script again, it will prompt for password
- A new session token will be created

### Session Files Location

Session tokens are stored in:
```
.sessions/session-your_username_here
```

These files are encrypted and excluded from git.

## Alternative: Configure Username in .env

To avoid typing your username each time:

1. Edit `.env` file:
   ```bash
   nano .env
   ```

2. Add your username:
   ```
   IG_USERNAME=your_username_here
   ```

3. Save and run:
   ```bash
   python igsaver.py
   ```

Now it will only ask for password on first run.
