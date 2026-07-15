# Supabase Storage Setup for Company Logos

This guide explains how to configure your Supabase Storage bucket for logo uploads.

## 📦 Bucket Configuration

### 1. Create the Bucket

You've already done this! Your bucket should be named:
```
company-logos
```

### 2. Make Bucket Public

The bucket needs to be **public** so logo URLs work on your website.

**Steps:**
1. Go to **Supabase Dashboard** → **Storage**
2. Find your `company-logos` bucket
3. Click the **settings icon** (⚙️) next to the bucket name
4. Toggle **"Public bucket"** to **ON**
5. Click **Save**

### 3. Set Up Storage Policies

Your bucket needs policies to control who can upload/delete files.

**Go to:** Storage → company-logos → Policies

#### Policy 1: Allow Authenticated Users to Upload

This allows logged-in users to upload their company logos.

**Create Policy:**
```sql
CREATE POLICY "Allow authenticated users to upload logos"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'company-logos'
  AND auth.uid() IS NOT NULL
);
```

**In Supabase UI:**
1. Click **"New Policy"**
2. Choose **"For full customization"** or **"Custom"**
3. **Policy Name:** `Allow authenticated users to upload logos`
4. **Policy Command:** `INSERT`
5. **Target Roles:** `authenticated`
6. **WITH CHECK expression:**
   ```sql
   bucket_id = 'company-logos' AND auth.uid() IS NOT NULL
   ```
7. Click **Save**

#### Policy 2: Allow Public Read Access

This allows anyone to view/download logos (needed for your website visitors).

**Create Policy:**
```sql
CREATE POLICY "Allow public read access to logos"
ON storage.objects
FOR SELECT
TO public
USING (bucket_id = 'company-logos');
```

**In Supabase UI:**
1. Click **"New Policy"**
2. Choose **"For full customization"** or **"Custom"**
3. **Policy Name:** `Allow public read access to logos`
4. **Policy Command:** `SELECT`
5. **Target Roles:** `public`
6. **USING expression:**
   ```sql
   bucket_id = 'company-logos'
   ```
7. Click **Save**

#### Policy 3: Allow Authenticated Users to Update/Delete

This allows users to replace or remove their logos.

**Create Policy:**
```sql
CREATE POLICY "Allow authenticated users to update/delete logos"
ON storage.objects
FOR DELETE
TO authenticated
USING (
  bucket_id = 'company-logos'
  AND auth.uid() IS NOT NULL
);
```

**In Supabase UI:**
1. Click **"New Policy"**
2. Choose **"For full customization"** or **"Custom"**
3. **Policy Name:** `Allow authenticated users to update/delete logos`
4. **Policy Command:** `DELETE`
5. **Target Roles:** `authenticated`
6. **USING expression:**
   ```sql
   bucket_id = 'company-logos' AND auth.uid() IS NOT NULL
   ```
7. Click **Save**

---

## ✅ Verify Setup

After configuring the bucket and policies, verify everything works:

### Test Upload:
1. Run your dev server: `npm run dev`
2. Go to `/dashboard/settings`
3. Click **"Upload logo"**
4. Select an image file
5. **Check the terminal** for logs:
   ```
   [POST /api/dashboard/settings/upload-logo] Uploading to Supabase Storage: logos/...
   [POST /api/dashboard/settings/upload-logo] Upload successful
   [POST /api/dashboard/settings/upload-logo] Public URL: https://...
   ```

### Check Supabase Storage:
1. Go to **Supabase Dashboard** → **Storage** → **company-logos**
2. Open the **logos** folder
3. You should see your uploaded file!

### Check Public URL:
1. Copy the public URL from the logs
2. Paste it in your browser
3. You should see your logo image!

---

## 🔧 Troubleshooting

### Error: "Failed to upload to storage: new row violates row-level security policy"

**Problem:** Missing upload policy

**Solution:** Create Policy 1 (Allow authenticated users to upload)

### Error: "Failed to upload to storage: Bucket not found"

**Problem:** Bucket name mismatch

**Solution:** Make sure your bucket is named exactly `company-logos` (no spaces, lowercase)

### Error: Logo uploads but URL doesn't work

**Problem:** Bucket is not public

**Solution:** Go to bucket settings and toggle "Public bucket" to ON

### Error: "Failed to upload to storage: permission denied"

**Problem:** Missing RLS policies

**Solution:** Create all 3 policies listed above

---

## 📁 Folder Structure

Uploaded logos are stored in this structure:
```
company-logos/
└── logos/
    ├── acme-real-estate-1734567890123-logo.png
    ├── johnson-law-1734567891234-logo.png
    └── smith-consulting-1734567892345-logo.png
```

Each file is prefixed with:
- Tenant slug (for organization)
- Timestamp (for uniqueness)
- Original filename (sanitized)

---

## 🔐 Security Notes

✅ **What's secure:**
- Only authenticated users can upload
- Files are prefixed with tenant slug
- Public read access is required for website display
- Automatic image optimization prevents huge files

⚠️ **Future enhancements:**
- Add tenant-specific folder paths
- Implement file size quotas per tenant
- Add automatic cleanup of old logos
- Implement CDN caching

---

## 🎯 How It Works

```
User uploads logo
      ↓
API validates file (type, size)
      ↓
Sharp resizes to 400x400 max
      ↓
Upload to Supabase Storage
      ↓
Get public URL
      ↓
Save URL to database
      ↓
Logo appears in widget!
```

---

## 🔗 Configuration

Your code is configured to use the bucket name: **`company-logos`**

If you named your bucket differently, update this file:
```
app/api/dashboard/settings/upload-logo/route.ts
Line 94: .from('company-logos')
```

Change `'company-logos'` to your bucket name.

---

**✅ Once you've completed these steps, your logo upload system will be fully functional with Supabase Storage!**
