# Fix Google OAuth "Access Blocked" Error 403

## Problem

Error message:
```
Access blocked: Qualifier has not completed the Google verification process.
The app is currently being tested, and can only be accessed by developer-approved testers.
Error 403: access_denied
```

This happens because your Google Cloud OAuth app is in **Testing** mode and your email isn't added as a test user.

## Solution: Add Test User

### Step 1: Go to Google Cloud Console

1. Open: https://console.cloud.google.com/
2. Select your project: **"Qualifier"** (or the project with client ID `146770687231-g6r6gak8elcqk41oj86avg609lsg3ahe`)

### Step 2: Navigate to OAuth Consent Screen

1. In the left sidebar, go to: **APIs & Services** → **OAuth consent screen**
2. Or direct link: https://console.cloud.google.com/apis/credentials/consent

### Step 3: Add Test Users

1. Scroll down to the **"Test users"** section
2. Click **"+ ADD USERS"**
3. Enter your email: `tali.mosley@gmail.com`
4. Click **"SAVE"**

### Step 4: Try Again

1. Go back to: `http://localhost:3002/dashboard/integrations/google-calendar`
2. Click **"Connect Google Calendar"** again
3. Should work now! ✅

---

## Alternative: Publish the App (Not Recommended for Testing)

If you want anyone to be able to use it without being a test user:

1. Go to OAuth consent screen
2. Click **"PUBLISH APP"**
3. **Warning**: This will require Google verification if you have sensitive scopes (like calendar)

**Better approach**: Keep it in Testing mode and just add test users as needed.

---

## What This Error Means

- **Publishing status**: Testing (unverified)
- **Who can access**: Only test users you explicitly add
- **Your email**: `tali.mosley@gmail.com` (needs to be added)
- **Client ID**: `146770687231-g6r6gak8elcqk41oj86avg609lsg3ahe`

---

## After Adding Test User

Once you add your email as a test user:

1. **Try connecting again** from the dashboard
2. You'll see a warning: *"Google hasn't verified this app"*
   - This is normal for testing mode
   - Click **"Continue"** (or "Advanced" → "Go to Qualifier (unsafe)")
3. Grant calendar permissions
4. You'll be redirected back to your app
5. Calendar will be connected! ✅

Then you can test the full booking flow with real calendar integration.

---

## Verification During Testing

Google will show warnings like:
- "Google hasn't verified this app"
- "This app hasn't been verified by Google"

**This is normal for testing mode**. You can safely continue as the developer.

To remove these warnings, you'd need to submit for Google verification, which:
- Takes 4-6 weeks
- Requires privacy policy, terms of service, etc.
- Only needed for production

For now, testing mode with test users is perfect.
