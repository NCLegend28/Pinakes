# Google Calendar Integration Setup

This guide walks through setting up the Google Calendar integration for the AI receptionist.

## Overview

The Google Calendar integration allows the AI agent to:
- Check real calendar availability (9 AM - 5 PM, Monday-Friday)
- Present actual available time slots to HOT leads
- Automatically create calendar events with attendee details
- Update conversation records with appointment information

## Prerequisites

1. A Google Cloud project with Calendar API enabled
2. OAuth 2.0 credentials (Client ID and Client Secret)
3. Supabase database with migrations applied
4. Node.js environment with googleapis package

## Step 1: Install Dependencies

```bash
cd saas-platform
npm install googleapis
```

## Step 2: Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Navigate to **APIs & Services > Library**
   - Search for "Google Calendar API"
   - Click **Enable**

## Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth client ID**
3. Configure the OAuth consent screen:
   - User Type: **External**
   - App name: Your app name
   - User support email: Your email
   - Developer contact: Your email
   - Scopes: Add `https://www.googleapis.com/auth/calendar` and `https://www.googleapis.com/auth/calendar.events`
4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: "AI Receptionist Calendar Integration"
   - Authorized redirect URIs:
     - Development: `http://localhost:3001/api/integrations/google-calendar/callback`
     - Production: `https://yourdomain.com/api/integrations/google-calendar/callback`
5. Copy the **Client ID** and **Client Secret**

## Step 4: Configure Environment Variables

Add the following to `saas-platform/.env.local`:

```env
# Google Calendar OAuth
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:3001/api/integrations/google-calendar/callback

# Make sure these are also set
NEXT_PUBLIC_APP_URL=http://localhost:3001
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## Step 5: Run Database Migrations

Apply the integrations table schema:

```bash
cd ..
# Connect to your Supabase database using the SQL editor
# or run the migration file directly
psql $DATABASE_URL -f database/migrations/003_add_integrations.sql
```

The migration creates:
- `integrations` table for storing OAuth tokens
- `calendar_event_id` and `appointment_time` columns in `conversations` table

## Step 6: Test the Integration

1. Start the development server:
   ```bash
   cd saas-platform
   npm run dev
   ```

2. Navigate to `http://localhost:3001/dashboard/integrations`

3. Click on **Google Calendar > Connect Calendar**

4. Complete the OAuth flow:
   - Sign in with your Google account
   - Grant calendar access permissions
   - You'll be redirected back to the dashboard

5. Test the widget with a HOT lead scenario:
   - Open the widget test page
   - Provide all 5 qualifying criteria
   - Answer YES to timeline ≤ 3 months
   - Answer YES to pre-approval
   - The agent should present real available time slots from your calendar

## Architecture

### Database Schema

```sql
-- Stores OAuth tokens and integration metadata
CREATE TABLE integrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,  -- 'google_calendar'
  config JSONB NOT NULL,       -- {access_token, refresh_token, calendar_id}
  enabled BOOLEAN DEFAULT true,
  last_sync_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Track appointments in conversations
ALTER TABLE conversations
ADD COLUMN calendar_event_id VARCHAR(255),
ADD COLUMN appointment_time TIMESTAMP;
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/integrations/google-calendar/connect` | GET | Initiate OAuth flow |
| `/api/integrations/google-calendar/callback` | GET | Handle OAuth callback |
| `/api/integrations/google-calendar/status` | GET | Check connection status |
| `/api/integrations/google-calendar/availability` | GET | Get available time slots |
| `/api/integrations/google-calendar/book` | POST | Create calendar event |
| `/api/integrations/google-calendar/disconnect` | POST | Revoke access |

### Workflow Integration

The action agent (for HOT leads) automatically:
1. Checks if calendar is connected
2. Fetches available slots for the next 7 days
3. Presents 2-3 specific times to the user
4. Creates calendar event when user confirms
5. Updates conversation record with event details

## Security & Privacy

- OAuth tokens are encrypted in the database
- Only `calendar.readonly` and `calendar.events` scopes are requested
- Event details are never read - only availability and booking
- Tokens can be revoked instantly via the disconnect button
- All API calls use tenant-specific authentication

## Troubleshooting

### "Calendar not connected" error
- Verify environment variables are set correctly
- Check that the OAuth flow completed successfully
- Ensure the integrations table exists in the database

### "Failed to fetch availability"
- Confirm the Google Calendar API is enabled
- Check that the OAuth token hasn't expired (auto-refresh is implemented)
- Verify the calendar ID in the integration config

### OAuth redirect mismatch
- Ensure `GOOGLE_REDIRECT_URI` matches the authorized redirect URI in Google Cloud Console
- For production, update both the environment variable and Google Cloud settings

### Agent not showing calendar slots
- Verify `NEXT_PUBLIC_APP_URL` is set correctly
- Check browser console for API errors
- Ensure the lead is classified as HOT (all 5 criteria + timeline ≤3mo + pre-approved)

## Next Steps

1. Test with multiple tenants
2. Add calendar sync status indicator
3. Support multiple calendar sources (Outlook, iCloud)
4. Add timezone handling for international users
5. Implement calendar event updates and cancellations

## Files Modified/Created

### New Files
- `/lib/integrations/google-calendar.ts` - Core calendar operations
- `/app/api/integrations/google-calendar/connect/route.ts` - OAuth initiation
- `/app/api/integrations/google-calendar/callback/route.ts` - OAuth callback
- `/app/api/integrations/google-calendar/status/route.ts` - Connection status
- `/app/api/integrations/google-calendar/availability/route.ts` - Fetch slots
- `/app/api/integrations/google-calendar/book/route.ts` - Create events
- `/app/api/integrations/google-calendar/disconnect/route.ts` - Revoke access
- `/app/dashboard/integrations/google-calendar/page.tsx` - UI for connection
- `/database/migrations/003_add_integrations.sql` - Schema changes

### Modified Files
- `/lib/workflow/workflow-engine.ts` - Added calendar integration to action agent
- `/app/dashboard/integrations/page.tsx` - Added Google Calendar to integrations list

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the Google Calendar API documentation
- Contact the development team
