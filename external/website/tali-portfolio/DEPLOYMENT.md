# Deployment Guide 🚀

## Quick Deploy to Vercel (Recommended)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Tali's portfolio website"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel auto-detects Vite configuration
5. Click "Deploy"
6. Done! Your site is live at `https://your-project.vercel.app`

### Step 3: Custom Domain (Optional)
1. In Vercel dashboard → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

---

## Alternative: Deploy to Netlify

### Option A: Drag & Drop
```bash
npm run build
# Drag the 'dist' folder to netlify.com/drop
```

### Option B: GitHub Integration
1. Push to GitHub
2. Go to [netlify.com](https://netlify.com)
3. Click "Add new site" → "Import an existing project"
4. Connect GitHub repository
5. Build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
6. Deploy

---

## Backend Deployment (For Chatbot)

### Option 1: Railway.app
```bash
# 1. Create railway.com account
# 2. New Project → Deploy from GitHub
# 3. Add Python backend repo
# 4. Railway auto-detects and deploys
```

### Option 2: Render.com
```bash
# 1. Create render.com account
# 2. New Web Service → Connect GitHub
# 3. Select Python backend repo
# 4. Configure:
#    - Build: pip install -r requirements.txt
#    - Start: gunicorn app:app
```

### Option 3: Fly.io
```bash
fly launch
fly deploy
```

---

## Environment Variables

### Frontend (if needed)
Create `.env` file:
```
VITE_API_URL=https://your-backend-url.com
VITE_CHATBOT_KEY=your-key-here
```

### Backend
```
OPENAI_API_KEY=your-openai-key
DATABASE_URL=your-database-url
ALLOWED_ORIGINS=https://your-frontend-url.com
```

---

## Custom Domain Setup

### Vercel
1. Purchase domain (Namecheap, Google Domains, etc.)
2. In Vercel: Settings → Domains → Add
3. Add DNS records from your domain provider:
   ```
   A Record: @ → 76.76.21.21
   CNAME: www → cname.vercel-dns.com
   ```

### Netlify
```
A Record: @ → 75.2.60.5
CNAME: www → your-site.netlify.app
```

---

## SSL Certificate
Both Vercel and Netlify provide **automatic SSL** (HTTPS) for free!

---

## Monitoring & Analytics

### Google Analytics
1. Get tracking ID from analytics.google.com
2. Add to `index.html`:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Vercel Analytics
- Enable in Vercel dashboard (free)
- Automatic tracking

---

## Performance Optimization

### Before Deploy Checklist
- [ ] Optimize images (use WebP format)
- [ ] Minimize bundle size
- [ ] Test on multiple devices
- [ ] Check Lighthouse score
- [ ] Verify all links work
- [ ] Test chatbot integration
- [ ] Add meta tags for SEO

### Build Optimization
```bash
# Analyze bundle size
npm install -D vite-bundle-visualizer
# Add to vite.config.js:
import { visualizer } from 'vite-bundle-visualizer';
plugins: [react(), visualizer()]
```

---

## SEO Setup

Add to `index.html`:
```html
<head>
  <meta name="description" content="Portfolio of Tali - Biomedical Engineer & AI/ML Developer specializing in algorithmic trading, healthcare tech, and innovative hardware solutions.">
  <meta name="keywords" content="biomedical engineer, AI ML developer, algorithmic trading, healthcare technology">
  <meta property="og:title" content="Tali - Biomedical Engineer & AI/ML Developer">
  <meta property="og:description" content="Building the future at the intersection of healthcare, AI, and finance">
  <meta property="og:image" content="https://your-site.com/og-image.jpg">
  <meta name="twitter:card" content="summary_large_image">
</head>
```

---

## Continuous Deployment

Both Vercel and Netlify automatically redeploy when you push to GitHub:
```bash
# Make changes
git add .
git commit -m "Update projects section"
git push
# Automatically deploys! ✨
```

---

## Troubleshooting

### Build Fails
```bash
# Check Node version
node --version  # Should be v16+

# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 404 on Refresh
Add `vercel.json`:
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/" }]
}
```

Or for Netlify, add `public/_redirects`:
```
/*    /index.html   200
```

---

## Backup & Version Control

```bash
# Always commit before major changes
git add .
git commit -m "Descriptive message"
git push

# Create release tags
git tag -a v1.0 -m "Initial release"
git push origin v1.0
```

---

## Cost Estimate

| Service | Cost |
|---------|------|
| Vercel (Frontend) | Free for personal projects |
| Netlify (Frontend) | Free tier available |
| Railway (Backend) | $5/month after free tier |
| Render (Backend) | Free tier available |
| Domain | $10-15/year |
| **Total** | **~$5-10/month** |

---

## Next Steps After Deployment

1. ✅ Share link on LinkedIn
2. ✅ Add to resume
3. ✅ Set up Google Analytics
4. ✅ Submit to search engines
5. ✅ Monitor performance
6. ✅ Gather feedback
7. ✅ Iterate and improve!

---

**Need help?** Check the main README or create an issue on GitHub!
