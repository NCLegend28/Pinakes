# Conversation Timeout & Session Management

## Problem Solved
Previously, conversations that were abandoned or went nowhere would remain "active" indefinitely. This created a cluttered dashboard and inaccurate metrics.

## Solution Implemented

### 30-Minute Inactivity Timeout
- Conversations automatically close after **30 minutes** of inactivity
- Customers can resume within the window, start fresh after

### Key Components

#### 1. **Database Migration** 
Added `last_activity_at` column to track conversation liveliness:

```sql
ALTER TABLE conversations 
ADD COLUMN IF NOT EXISTS last_activity_at TIMESTAMP DEFAULT NOW();
```

**Location:** [database/migrations/006_add_last_activity.sql](file:///Users/mosley/projects/leadQual/saas-platform/database/migrations/006_add_last_activity.sql)

> [!IMPORTANT]
> You need to run this migration in your Supabase SQL Editor (instructions below).

#### 2. **Session Continuity** 
[chat/start/route.ts](file:///Users/mosley/projects/leadQual/saas-platform/app/api/v1/chat/start/route.ts#L41-L86)

When a visitor starts a chat:
- Check if they have an active conversation
- If < 30 minutes inactive → Resume existing conversation
- If > 30 minutes inactive → Auto-close old one, start new

#### 3. **Activity Tracking**
[conversation-manager.ts](file:///Users/mosley/projects/leadQual/saas-platform/lib/workflow/conversation-manager.ts#L109-L112)

Every message updates `last_activity_at` to keep the session alive.

#### 4. **Cleanup Cron Job**
[cron/close-stale-conversations/route.ts](file:///Users/mosley/projects/leadQual/saas-platform/app/api/cron/close-stale-conversations/route.ts)

Runs periodically to batch-close truly abandoned conversations.

## How To Deploy

### Step 1: Run Database Migration

Go to your Supabase Dashboard → SQL Editor and run:

```sql
ALTER TABLE conversations 
ADD COLUMN IF NOT EXISTS last_activity_at TIMESTAMP DEFAULT NOW();

UPDATE conversations 
SET last_activity_at = COALESCE(ended_at, created_at)
WHERE last_activity_at IS NULL();

CREATE INDEX IF NOT EXISTS idx_conversations_last_activity 
ON conversations(last_activity_at DESC);

CREATE INDEX IF NOT EXISTS idx_conversations_stale 
ON conversations(status, last_activity_at) 
WHERE status = 'active';
```

### Step 2: Set Up Cron Job (Optional but Recommended)

Add to your `vercel.json` or platform config:

```json
{
  "crons": [{
    "path": "/api/cron/close-stale-conversations",
    "schedule": "*/15 * * * *"
  }]
}
```

This runs every 15 minutes to clean up stale conversations.

### Step 3: Deploy

```bash
git add .
git commit -m "Add conversation timeout and session management"
git push
```

## Testing

### Test Session Resume
1. Start a chat as a visitor
2. Send a message
3. Wait < 30 minutes
4. Start another chat → Should resume the same conversation

### Test Timeout
1. Start a chat
2. Wait > 30 minutes (or manually set `last_activity_at` in DB)
3. Start another chat → Should create a new conversation and close the old one

### Manual Cleanup
You can manually trigger the cleanup cron:
```bash
curl http://localhost:3000/api/cron/close-stale-conversations
```

## Benefits

✅ **Cleaner Dashboard** - Only truly active conversations show as "active"  
✅ **Accurate Metrics** - Conversation counts reflect real engagement  
✅ **Better UX** - Customers get a fresh start after long delays  
✅ **Session Continuity** - Quick returns resume seamlessly
