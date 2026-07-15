# 🏢 Multi-Tenant SaaS: Who Uses What?

## The Big Picture

You are building a **platform** that you will sell to multiple **companies**. Each company is called a **tenant**.

```
┌─────────────────────────────────────────────────────────┐
│  YOU (Platform Owner)                                   │
│  - Manage infrastructure                                │
│  - Handle billing/subscriptions                         │
│  - Monitor system health                                │
│  - Provide support                                      │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ TENANT 1     │  │ TENANT 2     │  │ TENANT 3     │
│ (Customer)   │  │ (Customer)   │  │ (Customer)   │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Real-World Example

### Tenant 1: ACME Real Estate
- **Website:** acmerealestate.com
- **Dashboard Login:** admin@acmerealestate.com
- **What they see in dashboard:**
  - Their 150 conversations this month
  - Their qualified leads
  - Their AI configuration (Real Estate template)
  - Their branding (red logo, #DC2626 color)
  - Their contact info (555-123-4567)
- **Widget on their site:** Red bubble, ACME logo, real estate AI

### Tenant 2: Johnson Law Firm
- **Website:** johnsonlaw.com
- **Dashboard Login:** sarah@johnsonlaw.com
- **What they see in dashboard:**
  - Their 89 conversations this month
  - Their qualified leads
  - Their AI configuration (Legal template)
  - Their branding (blue logo, #1E40AF color)
  - Their contact info (555-987-6543)
- **Widget on their site:** Blue bubble, Johnson Law logo, legal AI

### Tenant 3: Smith Consulting
- **Website:** smithconsulting.com
- **Dashboard Login:** info@smithconsulting.com
- **What they see in dashboard:**
  - Their 203 conversations this month
  - Their qualified leads
  - Their AI configuration (Consulting template)
  - Their branding (green logo, #059669 color)
  - Their contact info (555-456-7890)
- **Widget on their site:** Green bubble, Smith logo, consulting AI

## 🔒 Data Isolation (Critical!)

Each tenant's data is completely isolated:

```sql
-- ACME Real Estate can ONLY see their data
SELECT * FROM conversations WHERE tenant_id = 'acme-real-estate-id';

-- Johnson Law can ONLY see their data
SELECT * FROM conversations WHERE tenant_id = 'johnson-law-id';

-- They NEVER see each other's conversations, leads, or settings
```

This is enforced at:
1. **Database level:** Row-Level Security (RLS) policies
2. **API level:** All requests include tenant_id from session
3. **UI level:** User sessions are tenant-scoped

## 📊 The Dashboard

### What Each Tenant Sees:
- **Overview:** Their analytics (conversations, leads, revenue)
- **Conversations:** Their customer chats
- **Settings:**
  - General: Their company name, branding, contact info
  - AI Config: Their agent settings (models, temperatures)
  - Widget: Embed code for their website
- **Integrations:** Their CRM/calendar connections
- **Billing:** Their plan, usage, invoices

### What They DON'T See:
- ❌ Other tenants' data
- ❌ Other tenants' customers
- ❌ Platform infrastructure details
- ❌ Your admin controls

## 💰 Business Model

You charge each tenant monthly:

| Plan        | Price/Month | Conversations | Tenants      |
|-------------|-------------|---------------|--------------|
| Starter     | $99         | 500/month     | Small biz    |
| Professional| $129        | 2,000/month   | Growing biz  |
| Enterprise  | Custom      | Unlimited     | Large corps  |

**Example Revenue:**
- 10 tenants × $99 = $990/month
- 5 tenants × $129 = $645/month
- **Total: $1,635/month recurring revenue**

## 🛠️ Your Role (Platform Owner)

### What You DO:
1. **Onboard new tenants** (signup flow creates new tenant)
2. **Monitor system health** (server uptime, API performance)
3. **Handle billing** (Stripe integration)
4. **Provide support** (help tenants configure their AI)
5. **Deploy updates** (new features benefit all tenants)

### What You DON'T Do:
- ❌ Manually configure each tenant's AI (they do it themselves)
- ❌ Respond to their customers (the AI does that)
- ❌ Manage their conversations (they see them in dashboard)

## 🚀 Future: Super Admin Dashboard

Eventually you'll build a **super admin dashboard** (just for you) where you can:
- See all tenants (high-level view)
- Monitor platform-wide metrics
- Manage subscriptions
- Troubleshoot issues
- View system health

But right now, the dashboard is **for your customers** (tenants), not for you.

## 📝 How Tenants Sign Up

1. **They visit your landing page:** virtualreceptionist.ai
2. **They click "Start Free Trial"**
3. **Signup form:**
   - Company name → becomes tenant
   - Email/password → their login
   - Industry → applies AI template
4. **They get:**
   - Dashboard access at /dashboard
   - Their own tenant_id in database
   - Widget embed code for their site
5. **They configure:**
   - Branding (logo, colors)
   - Contact info (phone, email)
   - AI agents (models, prompts)
6. **They embed widget** on their website
7. **Their customers chat** via the widget
8. **They view conversations** in the dashboard

## 🔑 Key Takeaway

Think of your platform like **Shopify for AI receptionists**:
- Shopify = ecommerce platform
- You = AI receptionist platform
- Shopify merchants = your tenants
- Merchant's customers = tenant's website visitors

Each merchant (tenant) gets their own store (dashboard + widget) with their own branding and data, but you (platform owner) provide the infrastructure.

---

**You are building the infrastructure. Your customers (tenants) are the ones using it to serve their customers.**
