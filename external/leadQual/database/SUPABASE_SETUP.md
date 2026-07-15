# Supabase Setup Guide

This guide walks you through setting up the Supabase database for the Virtual Receptionist AI platform.

## 1. Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign in or create an account
3. Click "New Project"
4. Fill in details:
   - **Name**: `virtual-receptionist` (or your preferred name)
   - **Database Password**: Generate a strong password (save this!)
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free tier is fine for development

## 2. Get Database Credentials

Once your project is created, get your connection details:

1. Go to **Settings** → **Database**
2. Copy the following:
   - **Connection String** (URI format)
   - **Connection Pooler** (recommended for production)
   - **Direct Connection** (for migrations)

3. Go to **Settings** → **API**
4. Copy:
   - **Project URL**: `https://xxx.supabase.co`
   - **anon public** key: For client-side queries
   - **service_role** key: For server-side admin queries ⚠️ Keep secret!

## 3. Set Up Environment Variables

Create a `.env.local` file in your Next.js project:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database (for migrations)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
DIRECT_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
```

## 4. Run Database Schema

### Option A: Using Supabase SQL Editor (Easiest)

1. Go to **SQL Editor** in Supabase dashboard
2. Click **New Query**
3. Copy the contents of `database/schema.sql`
4. Paste into the editor
5. Click **Run**

### Option B: Using psql CLI

```bash
# Connect to your Supabase database
psql "postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres"

# Run the schema
\i database/schema.sql
```

### Option C: Using Supabase CLI (Recommended for production)

```bash
# Install Supabase CLI
brew install supabase/tap/supabase

# Login
supabase login

# Link to your project
supabase link --project-ref xxx

# Run migrations
supabase db push
```

## 5. Seed Industry Templates

After running the schema, seed the industry templates:

### Using SQL Editor:

1. Go to **SQL Editor**
2. Copy contents of `database/seeds/001_industry_templates.sql`
3. Paste and **Run**

### Using psql:

```bash
psql "your-connection-string" -f database/seeds/001_industry_templates.sql
```

## 6. Verify Installation

Run these queries in the SQL Editor to verify:

```sql
-- Check tables were created
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

-- Check industry templates were seeded
SELECT industry, agent_type, name
FROM industry_templates
ORDER BY industry, agent_type;

-- Should return 8 rows (4 industries × 2 agent types each)
```

Expected output:
```
consulting   | guard     | Project Screener
consulting   | qualifier | Project Discovery Specialist
healthcare   | guard     | Patient Screener
healthcare   | qualifier | Patient Intake Coordinator
law_firm     | guard     | Case Screener
law_firm     | qualifier | Case Intake Specialist
real_estate  | guard     | Lead Screener
real_estate  | qualifier | Property Needs Qualifier
```

## 7. Set Up Row Level Security (Optional but Recommended)

Enable RLS policies for tenant isolation:

```sql
-- Enable RLS on tenant-scoped tables (already done in schema)
-- Now create policies for authenticated users

-- Example: Users can only access their tenant's data
CREATE POLICY tenant_isolation_policy ON conversations
  FOR ALL
  TO authenticated
  USING (
    tenant_id IN (
      SELECT tenant_id FROM users WHERE id = auth.uid()
    )
  );

-- Repeat for other tables: messages, agent_configs, integrations, analytics_daily
```

## 8. Test Connection

Test the connection from your Next.js app:

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Test query
const { data, error } = await supabase
  .from('industry_templates')
  .select('*')
  .limit(1)

if (error) {
  console.error('Connection failed:', error)
} else {
  console.log('✅ Supabase connected:', data)
}
```

## 9. Create Sample Tenant (for testing)

```sql
-- Create a test tenant
INSERT INTO tenants (name, slug, industry, plan, status)
VALUES (
  'Acme Real Estate',
  'acme-realty',
  'real_estate',
  'professional',
  'active'
);

-- Get the tenant ID
SELECT id, name, slug FROM tenants WHERE slug = 'acme-realty';

-- Apply real estate template to this tenant
INSERT INTO agent_configs (tenant_id, agent_type, name, provider, model, temperature, max_tokens, system_instructions)
SELECT
  (SELECT id FROM tenants WHERE slug = 'acme-realty'),
  agent_type,
  name,
  default_provider,
  default_model,
  default_temperature,
  2000,
  system_instructions
FROM industry_templates
WHERE industry = 'real_estate';

-- Verify agent configs were created
SELECT
  t.name as tenant_name,
  ac.agent_type,
  ac.name as agent_name,
  ac.provider,
  ac.model
FROM agent_configs ac
JOIN tenants t ON t.id = ac.tenant_id
WHERE t.slug = 'acme-realty';
```

## 10. Backup and Monitoring

### Enable Backups

1. Go to **Settings** → **Database** → **Backups**
2. Daily backups are automatic on Pro plan
3. Free tier: Manual backups via SQL dump

### Enable Monitoring

1. Go to **Reports** to view:
   - Database size
   - API requests
   - Active connections
   - Query performance

## Troubleshooting

### Connection Refused

- Check your IP is allowed (Supabase Settings → Database → Connection Pooling)
- Verify password is correct
- Use connection pooler URL for external connections

### Table Already Exists

```sql
-- Drop all tables and start over (CAUTION: Deletes all data!)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- Then re-run schema.sql
```

### RLS Blocking Queries

```sql
-- Temporarily disable RLS for testing (don't do this in production!)
ALTER TABLE conversations DISABLE ROW LEVEL SECURITY;

-- Or grant bypass to service role
GRANT USAGE ON SCHEMA public TO service_role;
```

## Next Steps

✅ Database is set up!

Now proceed to:
1. Set up Next.js project
2. Create Supabase client library
3. Implement authentication
4. Build tenant configuration loader
5. Integrate with existing AI workflow

---

## Quick Reference

### Useful SQL Queries

```sql
-- Count conversations by tenant
SELECT
  t.name,
  COUNT(c.id) as total_conversations
FROM tenants t
LEFT JOIN conversations c ON c.tenant_id = t.id
GROUP BY t.name;

-- View recent conversations
SELECT * FROM recent_conversations LIMIT 10;

-- Tenant overview
SELECT * FROM tenant_overview;

-- Check token usage and costs
SELECT
  t.name,
  SUM(c.total_tokens) as tokens_used,
  SUM(c.total_cost) as total_cost
FROM conversations c
JOIN tenants t ON t.id = c.tenant_id
GROUP BY t.name;
```

### Reset Data (Keep Schema)

```sql
TRUNCATE TABLE
  conversations,
  messages,
  agent_configs,
  integrations,
  analytics_daily,
  users,
  tenants
CASCADE;
```
