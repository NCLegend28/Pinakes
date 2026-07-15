# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides calendar scheduling capabilities for AI agents. It integrates with both Google Calendar and Microsoft Outlook Calendar via OAuth 2.0, allowing agents to schedule consultations with leads and automatically send calendar invitations.

## Architecture

### Core Components

1. **Express Server** (`server.js`): Main entry point that serves multiple purposes:
   - OAuth flow endpoints for Google and Microsoft authentication
   - MCP HTTP transport endpoint (`/mcp`) for tool invocations
   - Health check endpoint (`/healthz`)

2. **MCP Tool**: `schedule_consultation` - Creates calendar events on agent calendars and invites leads with optional video conferencing links (Google Meet or Microsoft Teams)

3. **Calendar Provider Integration**:
   - **Google**: Uses `googleapis` library with OAuth 2.0 and automatic token refresh
   - **Microsoft**: Uses `@azure/msal-node` for auth and `@microsoft/microsoft-graph-client` for Graph API calls

4. **Database**: Supabase PostgreSQL with two key tables:
   - `calendar_accounts`: Stores OAuth tokens per agent_id and provider
   - `scheduled_events`: Records all created calendar events with metadata

### OAuth Flow Pattern

Both providers follow the same pattern:
1. `/oauth/{provider}/start?agent_id=UUID` - Initiates OAuth with agent_id in state parameter
2. `/oauth/{provider}/callback` - Handles callback, exchanges code for tokens, fetches user email, upserts to `calendar_accounts`

### Token Management

Each provider has a dedicated function (`googleCalendarForAgent`, `msGraphForAgent`) that:
- Fetches tokens from Supabase by agent_id and provider
- Checks token expiry (with 60-second buffer)
- Automatically refreshes expired tokens and updates DB
- Returns authenticated API client

### ESM/CommonJS Hybrid

The server uses CommonJS (`require`) but dynamically imports the ESM-only `@modelcontextprotocol/sdk` at runtime in the `start()` function. This is necessary because the MCP SDK is pure ESM while the rest of the codebase uses CommonJS.

## Development Commands

```bash
# Install dependencies
npm install

# Start the server (requires env vars to be set)
npm start
# or
node server.js

# Server runs on PORT (default 3334)
```

## Environment Variables Required

```
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE=your-service-role-key

# Google Calendar OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:3334/oauth/google/callback

# Microsoft Calendar OAuth
MS_CLIENT_ID=
MS_CLIENT_SECRET=
MS_TENANT_ID=common
MS_REDIRECT_URI=http://localhost:3334/oauth/microsoft/callback

# MCP Authentication
MCP_ACCESS_TOKEN=your-secret-token

# Server
PORT=3334
```

Create a `.env` file with these values before running.

## Database Schema

Required Supabase tables:

```sql
-- calendar_accounts table
-- Stores OAuth tokens per agent and provider
-- Primary key: (agent_id, provider)
-- Columns: id, agent_id, provider, email, access_token, refresh_token, expires_at, scope

-- scheduled_events table
-- Records all created calendar events
-- Columns: id, agent_id, provider, provider_event_id, html_link, start_at, end_at, contact_method, created_at
```

## MCP Tool Schema

`schedule_consultation` tool parameters:
- `agent_id` (required): UUID of the agent whose calendar to use
- `provider` (required): "google" or "microsoft"
- `date_iso` (required): ISO 8601 start time with timezone
- `duration_minutes`: Default 30
- `contact_method` (required): "phone", "zoom", or "in_person"
- `lead_email` (required): Attendee email
- `lead_name` (required): Attendee name
- `calendar_id`: Optional, defaults to "primary"
- `location`: Physical location for in-person meetings
- `notes`: Additional notes for the event description
- `time_zone`: Default "America/Chicago" (used by Outlook)
- `generate_meet`: Default true (creates Google Meet/Teams links)

## Testing OAuth Flows

1. Start server: `npm start`
2. Navigate to `http://localhost:3334/oauth/google/start?agent_id=test-agent-uuid`
3. Complete OAuth and verify tokens stored in `calendar_accounts` table
4. Repeat for Microsoft: `http://localhost:3334/oauth/microsoft/start?agent_id=test-agent-uuid`

## MCP Integration

The MCP endpoint (`/mcp`) is protected by Bearer token authentication. All requests must include:
```
Authorization: Bearer <MCP_ACCESS_TOKEN>
```

The server implements HTTP transport for MCP, not stdio transport.

## Key Implementation Details

- **Token Refresh**: Both providers auto-refresh tokens with 60-second expiry buffer
- **Event Tracking**: All created events are logged to `scheduled_events` with provider-specific event IDs
- **Video Conferencing**: Google events can generate Meet links; Microsoft events automatically create Teams meetings when `isOnlineMeeting: true`
- **Email Invitations**: Both providers automatically send calendar invites to attendees via `sendUpdates: 'all'` (Google) or default behavior (Microsoft)
- **Error Handling**: Tool returns `{status: 'error', message: '...'}` on failures; errors logged to console
