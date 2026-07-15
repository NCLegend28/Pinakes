# 🌱 Database Seeding Instructions

## Quick Fix for "Overlap" Error

If you're getting a unique constraint error when running the industry templates seed, use one of these methods:

### Method 1: Clear and Re-seed (Recommended)

**Step 1:** Run this to clear existing templates:
```sql
TRUNCATE TABLE industry_templates CASCADE;
```

**Step 2:** Then run the full seed file:
- Copy all of `database/seeds/001_industry_templates.sql`
- Paste into Supabase SQL Editor
- Click Run

### Method 2: Use INSERT ON CONFLICT (Skip Duplicates)

Run this instead of the original seed file:

```sql
-- Real Estate Templates
INSERT INTO industry_templates (
  industry, agent_type, name, description,
  default_provider, default_model, default_temperature,
  system_instructions, qualification_fields, lead_scoring_rules
) VALUES (
  'real_estate', 'guard', 'Lead Screener', 'Screens incoming real estate leads',
  'openai', 'gpt-4o-mini', 0.3,
  'You are a lead screening assistant...',
  '{"name": {"type": "string", "required": true}}'::jsonb,
  '{"hot": {"budget": {"min": 200000}}}'::jsonb
)
ON CONFLICT (industry, agent_type) DO NOTHING;

-- Repeat for all other templates...
```

### Method 3: Check What's Already There

Before seeding, check if data exists:

```sql
-- Check if templates already exist
SELECT industry, agent_type, name
FROM industry_templates
ORDER BY industry, agent_type;
```

If you see 8 rows (4 industries × 2 agent types), **templates are already loaded!** ✅

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

## Complete Seeding Process

### Fresh Database (First Time)

1. **Run schema** (creates tables):
   ```sql
   -- Paste entire contents of database/schema.sql
   ```

2. **Run seed** (adds industry templates):
   ```sql
   -- Paste entire contents of database/seeds/001_industry_templates.sql
   ```

3. **Verify**:
   ```sql
   SELECT COUNT(*) FROM industry_templates;
   -- Should return: 8
   ```

### Already Ran Seed Once

Just verify templates exist:
```sql
SELECT industry, agent_type FROM industry_templates;
```

If you see 8 rows, you're good! ✅ No need to run seed again.

## Troubleshooting

### Error: "duplicate key value violates unique constraint"

**Cause:** Templates already exist in database
**Solution:** Use Method 1 above to clear and re-seed, or just skip seeding (data already there)

### Error: "relation 'industry_templates' does not exist"

**Cause:** Schema wasn't run first
**Solution:** Run `database/schema.sql` before running seed

### Want to Update Template Instructions?

If you need to modify the AI instructions for an existing template:

```sql
UPDATE industry_templates
SET system_instructions = 'Your new instructions here...'
WHERE industry = 'real_estate' AND agent_type = 'guard';
```

## Next Steps After Seeding

Once templates are loaded:

1. ✅ Try signup at `http://localhost:3000/auth/signup`
2. ✅ Choose an industry (e.g., Real Estate)
3. ✅ Complete signup
4. ✅ Check database:
   ```sql
   -- Should see your new tenant
   SELECT * FROM tenants ORDER BY created_at DESC LIMIT 1;

   -- Should see agent configs auto-created from template
   SELECT * FROM agent_configs
   WHERE tenant_id = (SELECT id FROM tenants ORDER BY created_at DESC LIMIT 1);
   ```

You should see 2 agent configs (guard + qualifier) automatically created! 🎉
