# Multi-Intent Workflow System

## Overview

The Multi-Intent Workflow System enables the AI receptionist to handle **multiple user intentions simultaneously**. Instead of forcing users through rigid qualification steps before addressing their needs, it intelligently detects and processes multiple intents in parallel.

## Key Features

### 1. **Intent Detection**
The system detects 6 primary intent types:
- **APPOINTMENT**: User wants to schedule/book something
- **QUALIFY**: Lead qualification (budget, timeline, preferences)
- **QUESTION**: FAQ or information requests
- **SUPPORT**: General assistance needs
- **OTHER**: Off-topic conversation
- **SPAM**: Malicious/irrelevant content

### 2. **Parallel Processing**
Multiple intents can be handled simultaneously:
```
User: "I need to schedule a viewing for a 3BR house in downtown, budget is $500k"
↓
Detected: APPOINTMENT (primary) + QUALIFY (secondary)
↓
Appointment Handler: Schedules the viewing
Qualification Handler: Extracts 3BR, downtown, $500k budget
↓
Response: "I'd love to schedule a viewing for you! I have availability on..."
```

### 3. **Contextual Information Extraction**
The system automatically extracts relevant data:

**For Appointments:**
- Appointment type (viewing, consultation, meeting, callback)
- Preferred date/time
- Urgency level (immediate, soon, flexible)

**For Qualification:**
- Budget
- Timeline
- Location preferences
- Property type
- Contact information

## Implementation

### Architecture

```
┌─────────────────────────────────────────────┐
│        User Message                         │
│  "I need to see a house next Tuesday"       │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│    Intent Detection (Guard Agent)           │
│  • Classifies primary & secondary intents   │
│  • Extracts structured information          │
│  • Assesses risk & need for clarification   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         Intent Router                       │
│  Routes to appropriate handler(s)           │
└─────────┬───────────────┬───────────────────┘
          │               │
          ▼               ▼
┌──────────────────┐  ┌──────────────────────┐
│ Appointment      │  │ Qualification        │
│ Handler          │  │ Handler              │
│ • Check calendar │  │ • Extract lead data  │
│ • Suggest times  │  │ • Score lead         │
│ • Book slot      │  │ • Identify gaps      │
└──────────────────┘  └──────────────────────┘
          │               │
          └───────┬───────┘
                  ▼
┌─────────────────────────────────────────────┐
│     Combine Responses                       │
│  "Great! I can schedule you for Tuesday     │
│   at 2PM. What budget range are you         │
│   considering?"                             │
└─────────────────────────────────────────────┘
```

### File Structure

```
lib/workflow/
├── multi-intent-workflow.ts    # NEW: Multi-intent engine
├── workflow-engine.ts           # Legacy single-intent engine
├── direct-completion.ts         # LLM API wrapper
└── conversation-manager.ts      # Conversation persistence

app/api/v1/chat/message/
└── route.ts                     # Updated with feature flag
```

### Enabling Multi-Intent Mode

**Default**: Multi-intent is ENABLED by default.

To disable (use legacy single-intent workflow):
```env
# .env.local
NEXT_PUBLIC_USE_MULTI_INTENT=false
```

## Usage Examples

### Example 1: Appointment Request
```
User: "I need to schedule an appointment for next Tuesday at 2PM"

Detection:
  Primary: APPOINTMENT
  Secondary: []
  Extracted: { preferredDate: "next Tuesday", preferredTime: "2PM", urgency: "soon" }

Response:
  "I'd be happy to schedule that for you! Let me check our availability for
   Tuesday at 2 PM. I have these times available:
   1. Tuesday, Nov 14 at 2:00 PM
   2. Tuesday, Nov 14 at 3:00 PM
   Which works best for you?"
```

### Example 2: Qualified Lead with Appointment
```
User: "I'm looking for a 3BR house in Westwood, budget $800k, need to move in 2 months. Can I see some properties this week?"

Detection:
  Primary: APPOINTMENT
  Secondary: [QUALIFY]
  Extracted:
    appointment: { type: "viewing", urgency: "immediate" }
    qualification: { propertyType: "3BR", location: "Westwood", budget: 800000, timeline: "2 months" }

Handlers:
  Appointment: Schedules viewing for this week
  Qualification: Scores as HOT lead (short timeline, clear budget)

Response:
  "Excellent! You're well-qualified for what we offer. I have several 3BR homes
   in Westwood within your $800k budget. I can schedule viewings this week:
   1. Thursday at 10 AM
   2. Friday at 2 PM
   Which time works better for you?"
```

### Example 3: Question + Qualification
```
User: "What areas do you cover? I'm looking in the $500-600k range"

Detection:
  Primary: QUESTION
  Secondary: [QUALIFY]
  Extracted:
    question: "What areas do you cover?"
    qualification: { budget: 550000 }

Response:
  "We primarily serve the greater metro area including downtown, Westwood,
   and surrounding neighborhoods. With your $500-600k budget, you'll have
   great options in areas like... Are you interested in a specific neighborhood?"
```

## Comparison: Legacy vs Multi-Intent

### Legacy Single-Intent Workflow

**User**: "I need to schedule an appointment for next Tuesday"

**System**:
1. Guard: Classifies as QUALIFY (tries to force qualification)
2. Extractor: Finds 0/5 criteria (budget, timeline, location, pre-approval, contact)
3. Clarifier: "That sounds great! What areas are you most interested in?" ❌
   - **Ignores the appointment request**
   - **Forces unnecessary qualification**

### Multi-Intent Workflow

**User**: "I need to schedule an appointment for next Tuesday"

**System**:
1. Intent Detection: Primary=APPOINTMENT, extracts "next Tuesday"
2. Appointment Handler: Checks calendar, suggests specific times ✅
3. Response: "I'd be happy to schedule that! I have these times available..." ✅
   - **Directly addresses the request**
   - **Natural conversation flow**

## Benefits

### 1. **Better User Experience**
- Users get direct answers to their questions
- No forced qualification when they just want information
- Natural, helpful conversation

### 2. **Higher Conversion Rates**
- Reduces friction in booking appointments
- Captures partial qualification data opportunistically
- Maintains engagement throughout conversation

### 3. **Flexible Conversations**
- Handles mixed intents: "Can I see a house? My budget is $500k"
- Adapts to user's communication style
- Works for both chatbots and voice interfaces

### 4. **Efficient Lead Capture**
- Extracts qualification data without rigid forms
- Scores leads based on available information
- Continues conversation naturally

## Calendar Integration

The system integrates with Google Calendar for appointment booking:

**When calendar is connected:**
- Fetches real availability
- Suggests specific date/time slots
- Books appointments automatically
- Sends confirmation emails

**When calendar is NOT connected:**
- Asks for preferred time
- Confirms request will be coordinated
- Saves appointment request for manual follow-up

## API Response Format

### Multi-Intent Response
```typescript
{
  message: string;              // AI response to user
  intents: {
    primaryIntent: IntentType;
    secondaryIntents: IntentType[];
    confidence: number;
    needsClarification: boolean;
    risk: 'LOW' | 'MEDIUM' | 'HIGH';
  };
  appointment?: {
    scheduled: boolean;
    appointmentTime?: string;
    appointmentType?: string;
    response: string;
    nextStep?: string;
  };
  qualification?: {
    leadScore?: 'hot' | 'warm' | 'cold' | 'uncertain';
    profile?: Record<string, unknown>;
    needsMoreInfo: boolean;
    response: string;
  };
  should_end: boolean;
}
```

## Future Enhancements

- [ ] Question/FAQ handler with knowledge base integration
- [ ] Support handler for escalation to human agents
- [ ] Multi-language intent detection
- [ ] Custom intent types per tenant/industry
- [ ] Intent confidence scoring and fallback logic
- [ ] A/B testing framework for comparing workflows

## Migration Guide

### Switching from Legacy to Multi-Intent

1. **No code changes required** - Multi-intent is enabled by default
2. **Test your use cases** - Try appointment booking, questions, qualification
3. **Monitor logs** - Check intent detection accuracy in server logs
4. **Adjust agent prompts** - Fine-tune guard/appointment/qualification agents if needed
5. **Rollback if needed** - Set `NEXT_PUBLIC_USE_MULTI_INTENT=false`

### Customizing Intent Detection

Edit the Guard Agent instructions in the database to adjust intent classification:

```sql
UPDATE agent_configs
SET system_instructions = '... your custom instructions ...'
WHERE agent_type = 'guard' AND tenant_id = 'your-tenant-id';
```

## Troubleshooting

### Intent Misclassification

**Problem**: System classifies appointment as qualification

**Solution**: Check Guard Agent instructions, increase context about appointment keywords ("schedule", "book", "viewing", "consultation")

### Missing Data Extraction

**Problem**: Budget mentioned but not extracted

**Solution**: Review Intent Detection schema, ensure extraction prompt explicitly asks for budget/price mentions

### Calendar Not Working

**Problem**: Appointment handler doesn't show available times

**Solution**:
1. Check `/api/integrations/google-calendar/availability` returns slots
2. Verify `NEXT_PUBLIC_APP_URL` is set correctly
3. Check tenant has connected Google Calendar integration

## Reference

- **Multi-Intent Workflow**: `lib/workflow/multi-intent-workflow.ts`
- **API Route**: `app/api/v1/chat/message/route.ts`
- **Voice Widget**: `components/VoiceWidget.tsx`
- **Voice Fixes**: `.claude/commands/fix-voice.md`
