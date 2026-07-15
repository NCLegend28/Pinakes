# 📲 Appointment Reminders Setup

This guide explains how to set up automated SMS appointment reminders for customers.

## Features

- **24-Hour Reminders**: Sends SMS 24 hours before appointments
- **1-Hour Reminders**: (Optional) Can be enabled for last-minute reminders
- **Smart Tracking**: Won't send duplicate reminders
- **Graceful Failures**: Booking succeeds even if SMS fails

## Prerequisites

1. **Twilio Account**: Sign up at https://www.twilio.com
2. **Phone Number**: Purchase a Twilio phone number
3. **Database Migration**: Run the reminder tracking migration

## Setup Steps

### 1. Configure Twilio

Add these environment variables to your `.env.local`:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

Get these values from your Twilio Console:
- Dashboard → Account Info → Account SID
- Dashboard → Account Info → Auth Token
- Phone Numbers → Active Numbers → Copy your number

### 2. Run Database Migration

Run this migration in your Supabase SQL Editor:

```sql
-- From: database/migrations/004_add_reminder_tracking.sql

ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS reminder_sent_at TIMESTAMP;

ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS reminder_1hr_sent_at TIMESTAMP;

CREATE INDEX IF NOT EXISTS idx_conversations_appointment_reminders
ON conversations (appointment_time, reminder_sent_at)
WHERE appointment_time IS NOT NULL AND calendar_event_id IS NOT NULL;
```

### 3. Configure Cron Job

#### Option A: Vercel Cron (Recommended)

If deploying to Vercel, cron is already configured in `vercel.json`:

```json
{
  "crons": [
    {
      "path": "/api/cron/send-reminders",
      "schedule": "0 * * * *"
    }
  ]
}
```

This runs every hour automatically. No additional setup needed!

#### Option B: External Cron Service

If not using Vercel, use a service like:
- **cron-job.org** (free)
- **EasyCron** (free tier available)
- **Your own server cron**

Configure it to call:
```
GET https://your-domain.com/api/cron/send-reminders
Headers: Authorization: Bearer YOUR_CRON_SECRET
```

Set `CRON_SECRET` in your environment:
```env
CRON_SECRET=your-random-secret-key-here
```

Schedule: Every hour (`0 * * * *`)

### 4. Test the Reminder System

#### Manual Test

Call the endpoint manually to test:

```bash
curl -X GET https://your-domain.com/api/cron/send-reminders \
  -H "Authorization: Bearer YOUR_CRON_SECRET"
```

Or if testing locally without auth:

```bash
curl http://localhost:3002/api/cron/send-reminders
```

Expected response:
```json
{
  "success": true,
  "reminders_sent": 2,
  "details": {
    "24hr_reminders": [
      {
        "conversation_id": "uuid",
        "phone": "+1234567890",
        "success": true,
        "message_id": "SMxxxxxxxxx"
      }
    ]
  },
  "timestamp": "2025-01-15T10:00:00.000Z"
}
```

#### Create Test Appointment

1. Book an appointment for exactly 24 hours from now
2. Wait for the next hour (when cron runs)
3. Check your phone for the reminder SMS
4. Check logs to verify reminder was sent

## How It Works

### Reminder Flow

1. **Cron runs every hour**
2. **Query**: Finds appointments 24-25 hours away with no reminder sent
3. **Send SMS**: For each appointment, sends reminder with details
4. **Track**: Updates `reminder_sent_at` to prevent duplicates
5. **Report**: Returns summary of reminders sent

### Reminder Message Format

```
Reminder: You have a [Service] appointment tomorrow at [Time].

[Business Name]
[Address]

See you then! Reply CANCEL if you need to cancel.
```

Example:
```
Reminder: You have a Property Viewing appointment tomorrow at 2:00 PM.

Premier Real Estate
123 Main St, Downtown

See you then! Reply CANCEL if you need to cancel.
```

### Database Schema

The `conversations` table tracks reminders:

```sql
conversations {
  ...
  appointment_time TIMESTAMP,
  calendar_event_id VARCHAR,
  reminder_sent_at TIMESTAMP,       -- 24hr reminder
  reminder_1hr_sent_at TIMESTAMP,   -- 1hr reminder (optional)
}
```

## Advanced Configuration

### Enable 1-Hour Reminders

Uncomment the 1-hour reminder code in `/app/api/cron/send-reminders/route.ts`:

```typescript
// Find appointments that need 1-hour reminders
const { data: appointments1hr } = await supabase
  .from('conversations')
  .select(...)
  .gte('appointment_time', in1Hour.toISOString())
  .lt('appointment_time', in2Hours.toISOString())
  .is('reminder_1hr_sent_at', null);

// Send 1-hour reminders
for (const apt of appointments1hr) {
  // ... similar logic to 24hr reminders
  // Update reminder_1hr_sent_at instead
}
```

### Customize Reminder Time Windows

Edit the time calculations in `route.ts`:

```typescript
// For 48-hour reminders instead:
const in48Hours = new Date(now.getTime() + 48 * 60 * 60 * 1000);
const in49Hours = new Date(now.getTime() + 49 * 60 * 60 * 1000);
```

### Custom Message Templates

Edit the message format in `/lib/notifications/sms.ts`:

```typescript
function formatReminderMessage(details: AppointmentDetails): string {
  return `Hey ${details.customerName}! Just a heads up...`;
}
```

## Monitoring

### Check Logs

**Vercel Logs**:
- Dashboard → Your Project → Logs
- Filter by `/api/cron/send-reminders`

**Look for**:
```
🔔 Checking for appointments to remind...
   Found 3 appointments needing 24hr reminders
   ✅ Sent 24hr reminder for conversation abc-123
   ✅ Sent 24hr reminder for conversation def-456
```

### Twilio Logs

Check SMS delivery in Twilio Console:
- Monitor → Logs → Messaging Logs
- Filter by date/time
- Check delivery status

### Database Queries

Check which appointments have reminders sent:

```sql
SELECT
  id,
  appointment_time,
  reminder_sent_at,
  lead_profile->>'name' as customer_name,
  lead_profile->>'phone' as phone
FROM conversations
WHERE appointment_time IS NOT NULL
  AND reminder_sent_at IS NOT NULL
ORDER BY appointment_time DESC;
```

Find appointments needing reminders:

```sql
SELECT
  id,
  appointment_time,
  lead_profile->>'name' as customer_name
FROM conversations
WHERE appointment_time BETWEEN NOW() + INTERVAL '24 hours'
                           AND NOW() + INTERVAL '25 hours'
  AND reminder_sent_at IS NULL
  AND calendar_event_id IS NOT NULL;
```

## Troubleshooting

### No reminders being sent

**Check**:
1. Is Twilio configured? Check env vars are set
2. Are there appointments 24 hours away? Check database
3. Is cron running? Check Vercel logs or external cron service
4. Are reminders already sent? Check `reminder_sent_at` column

### SMS not received

**Check**:
1. Phone number format: Must be E.164 format (+1234567890)
2. Twilio account status: Is it verified/active?
3. Twilio balance: Do you have credits?
4. Phone number capability: Can it send SMS?
5. Recipient phone: Is it valid? Carrier issues?

### Duplicate reminders

**Check**:
- `reminder_sent_at` is being updated after sending
- Cron isn't running too frequently
- Query filters include `reminder_sent_at IS NULL`

## Cost Estimation

Twilio SMS pricing (USA):
- **Outbound SMS**: ~$0.0079 per message
- **For 1000 appointments/month**: ~$8/month
- **Plus phone number**: $1.15/month

Budget-friendly!

## Best Practices

1. **Always update reminder_sent_at**: Prevents duplicate sends
2. **Don't fail bookings on SMS errors**: SMS is supplementary
3. **Log everything**: Makes debugging much easier
4. **Monitor Twilio spend**: Set up usage alerts
5. **Test with your own number first**: Before going live

## Next Steps

After setting up reminders:

1. ✅ **Email Confirmations**: Add email with iCal attachments
2. ✅ **SMS Reply Handling**: Handle CANCEL replies from customers
3. ✅ **Dashboard Analytics**: Show reminder delivery stats
4. ✅ **Reminder Preferences**: Let customers opt in/out

---

**Questions?** Check the main documentation or Twilio docs at https://www.twilio.com/docs/sms
