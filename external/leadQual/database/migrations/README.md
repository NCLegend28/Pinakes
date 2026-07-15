# Database Migrations

This folder contains SQL migration scripts to update your Supabase database schema.

## How to Run Migrations

1. Open your **Supabase Dashboard**
2. Navigate to **SQL Editor**
3. Open the migration file you need to run
4. Copy and paste the contents into the SQL Editor
5. Click **Run** to execute

## Migration Files

### 001_add_missing_tenant_columns.sql
**Run this if you're getting errors about missing columns in the tenants table.**

This migration safely adds the following columns if they don't exist:
- `support_email` - Support contact email
- `logo_url` - Company logo URL
- `primary_color` - Brand primary color (hex)
- `business_hours` - Operating hours (JSONB)
- `phone_number` - Support phone number
- `subdomain` - Custom subdomain
- `custom_domain` - Custom domain

The migration uses `DO $$ ... END $$` blocks to check if columns exist before adding them, so it's safe to run multiple times without errors.

## Troubleshooting

If you see errors like:
```
Could not find the 'column_name' column of 'table_name' in the schema cache
```

This means your database is missing columns. Run the appropriate migration to add them.

## Best Practices

1. **Always run migrations in order** (001, 002, 003, etc.)
2. **Test in development first** before running in production
3. **Backup your database** before running migrations
4. **Check the output** to see which columns were added
