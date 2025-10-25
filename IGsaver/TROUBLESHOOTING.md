# Troubleshooting Guide

## Error: "challenge_required" 

### Problem
```
400 Bad Request - "fail" status, message "challenge_required"
```

This happens when Instagram detects unusual activity and requires you to verify your identity.

### Solution

**Step 1: Complete the challenge in Instagram**
1. Open Instagram app on your phone OR go to instagram.com
2. Log in if needed
3. You should see a security check/challenge (might be):
   - "We detected unusual activity"
   - CAPTCHA verification
   - Email/SMS verification code
   - "Is this you?" photo verification
4. Complete whatever challenge Instagram shows you

**Step 2: Wait a bit**
- Wait 5-10 minutes after completing the challenge
- Instagram needs time to clear the flag

**Step 3: Delete the session and try again**
```bash
cd /home/il1v3y/projects/personal/IGsaver
rm .sessions/session-sib.liv3y
./run.sh
```

### Alternative: Use a different approach

If the challenge persists, try:

**Option A: Wait 24-48 hours**
- Instagram might have temporarily flagged your account
- Try again after a day or two

**Option B: Reduce activity**
- Don't run the script multiple times in a row
- Space out your backup attempts (once per day max)

**Option C: Use from a trusted location**
- Run the script from the same device/IP you normally use Instagram from
- Don't use VPN while running the backup

### Prevention

To avoid this error in the future:
1. ✅ Use the script only once per day (or less frequently)
2. ✅ Complete any Instagram notifications/challenges immediately
3. ✅ Run from the same device consistently
4. ✅ Don't run immediately after logging in from a new device
5. ✅ Keep 2FA enabled (more trusted by Instagram)

## Error: Session expired

If you see "Session has expired":
```bash
# Just run again, it will ask for password
./run.sh
```

## Error: Rate limit

If downloads are slow or failing:
- Instagram is rate-limiting you
- Wait a few hours and try again
- The script will continue from where it left off

## Error: Permission denied

If you see permission errors:
- Make sure you're running from the project directory
- Check file permissions: `ls -la backups/`

## Need more help?

Check the logs:
```bash
tail -100 logs/igsaver_*.log
```
