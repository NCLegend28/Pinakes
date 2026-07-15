# 🕐 Timezone Fix - Complete

## Problem

The calendar was creating events in the wrong timezone. When you said "Monday at 10 AM", it created the event for 11 AM instead. This happened because the system was treating all times as UTC without considering your local timezone.

## Solution

Implemented full timezone awareness throughout the calendar system:

### 1. **Timezone-Aware Slot Generation** ✅
- Available slots (9 AM - 5 PM) are now generated in **your timezone**
- When the AI says "Monday at 10:00 AM", it means 10 AM in **your timezone**
- Slots are stored as UTC internally but displayed in your timezone

### 2. **Timezone-Aware Event Creation** ✅
- Calendar events are created with the correct timezone
- Google Calendar properly shows the event in your local time
- No more 1-hour offset issues

### 3. **Timezone Configuration** ✅
- Each tenant can have their own timezone
- Added `timezone` column to tenants table
- Default: `America/Chicago` (Central Time)

## Setup

### Step 1: Run Database Migration

Copy and run this in your Supabase SQL Editor:

```sql
-- Add timezone column
ALTER TABLE tenants
ADD COLUMN IF NOT EXISTS timezone VARCHAR(100) DEFAULT 'America/Chicago';

-- Update existing tenants
UPDATE tenants
SET timezone = 'America/Chicago'
WHERE timezone IS NULL;
```

### Step 2: Set Your Timezone

Run this command with your timezone:

```bash
npx tsx scripts/set-tenant-timezone.ts test-company America/Chicago
```

**Common US Timezones:**
- `America/New_York` - Eastern Time (ET)
- `America/Chicago` - Central Time (CT)
- `America/Denver` - Mountain Time (MT)
- `America/Los_Angeles` - Pacific Time (PT)
- `America/Phoenix` - Arizona (no DST)
- `America/Anchorage` - Alaska Time (AKT)
- `Pacific/Honolulu` - Hawaii Time (HT)

### Step 3: Test It!

1. Start a new conversation in the chat widget
2. Qualify as a HOT lead (budget, location, timeline, pre-approved, email)
3. When AI shows available times, they should be in YOUR timezone
4. Select a time (e.g., "Monday at 10 AM")
5. Check your Google Calendar - event should be at 10 AM (not 11 AM!)

## Technical Details

### Files Changed

1. **`lib/integrations/google-calendar.ts`**
   - Added `date-fns-tz` for timezone handling
   - `getAvailableSlots()` generates slots in tenant's timezone
   - `createCalendarEvent()` creates events with proper timezone
   - Both functions now fetch tenant timezone from database

2. **`lib/integrations/timezone-utils.ts`** (NEW)
   - `getTenantTimezone()` - Fetches timezone from database
   - `US_TIMEZONES` - Common timezone mappings
   - `getBrowserTimezone()` - Client-side timezone detection

3. **`database/migrations/005_add_tenant_timezone.sql`** (NEW)
   - Adds `timezone` column to tenants table
   - Sets default to `America/Chicago`

4. **`scripts/set-tenant-timezone.ts`** (NEW)
   - Helper script to set tenant timezone
   - Lists common timezones
   - Updates database

### How It Works

**Before (Broken):**
```
User: "Monday at 10 AM"
System generates slot: 10:00 UTC → Shows as 4 AM CST
System creates event: 10:00 UTC → Shows as 4 AM in calendar
```

**After (Fixed):**
```
User: "Monday at 10 AM" in CST
System generates slot: 10:00 CST → Stores as 16:00 UTC
System creates event: 10:00 CST → Calendar shows 10 AM
```

### Example Flow

1. **Tenant timezone**: `America/Chicago` (CST = UTC-6)

2. **Generate slots**:
   - Start with current time in Chicago (e.g., 2:00 PM CST)
   - Generate 9 AM CST → Convert to 15:00 UTC → Store as ISO
   - Generate 10 AM CST → Convert to 16:00 UTC → Store as ISO
   - etc.

3. **Show to user**:
   - AI sees slot: "2025-11-10T16:00:00.000Z" (UTC)
   - Workflow converts: 16:00 UTC → 10:00 AM CST
   - AI says: "Monday at 10:00 AM"

4. **User selects**:
   - User: "Monday at 10 AM"
   - AI returns: `selected_slot_index: 1`
   - Workflow uses: "2025-11-10T16:00:00.000Z"

5. **Create event**:
   - Start: "2025-11-10T16:00:00.000Z"
   - End: "2025-11-10T17:00:00.000Z"
   - Timezone: "America/Chicago"
   - Google Calendar shows: Monday 10:00 AM - 11:00 AM CST ✅

## Benefits

✅ **Accurate Times**: Events created at the exact time users expect
✅ **Multi-Timezone Support**: Each tenant can have different timezones
✅ **Daylight Saving Time**: Automatic DST handling
✅ **International Ready**: Works with any IANA timezone
✅ **Consistent UX**: Times displayed in user's local timezone

## Testing Checklist

- [ ] Run database migration
- [ ] Set tenant timezone
- [ ] Restart Next.js server
- [ ] Start new conversation
- [ ] Qualify as HOT lead
- [ ] Note the times AI suggests (should be in your timezone)
- [ ] Select a time
- [ ] Check Google Calendar (should match selected time)
- [ ] Verify no 1-hour offset

## Next Steps

### For Production

1. **Add timezone to onboarding**:
   - Ask new tenants for their timezone during signup
   - Auto-detect from browser: `Intl.DateTimeFormat().resolvedOptions().timeZone`

2. **Add timezone to dashboard**:
   - Allow tenants to change timezone in settings
   - Show current timezone on integrations page

3. **Multi-location support**:
   - For businesses with multiple locations
   - Each location can have its own timezone
   - Calendar shows availability for selected location

### For International

Add more timezone options:
- Europe: `Europe/London`, `Europe/Paris`, etc.
- Asia: `Asia/Tokyo`, `Asia/Singapore`, etc.
- Australia: `Australia/Sydney`, `Australia/Melbourne`, etc.

All IANA timezone identifiers are supported: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

---

**Status**: Timezone system is fully implemented and ready to test! 🎉
