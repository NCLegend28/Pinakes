# Lead Qualification Service - QA Testing Checklist

## 🎯 Testing Principles
- **Smoothness**: No lag, stuttering, or awkward pauses
- **Seamless Integration**: Components work together naturally
- **Accuracy**: Data flows correctly, calculations are precise
- **Precision**: Timestamps, scores, and costs are exact

---

## 1️⃣ Chat Widget (Web)

### Initial Load
- [ ] Widget loads within 2 seconds
- [ ] Greeting message displays correctly
- [ ] Widget respects position setting (bottom-right/left)
- [ ] Brand colors apply correctly
- [ ] No console errors on load

### Conversation Flow
- [ ] User can type and send messages smoothly
- [ ] AI responses appear within 5 seconds
- [ ] No duplicate messages
- [ ] Messages display in correct order
- [ ] Scroll behavior works (auto-scroll to latest)
- [ ] Long messages wrap properly

### Session Management
- [ ] New visitor creates new conversation
- [ ] Returning visitor (< 30 min) resumes conversation
- [ ] Returning visitor (> 30 min) starts fresh conversation
- [ ] Conversation ID persists through page refresh
- [ ] Old conversation marked as "closed" after timeout

---

## 2️⃣ Voice Widget (Phone)

### Call Initiation
- [ ] Phone button clickable and responsive
- [ ] Microphone permission request appears
- [ ] Call starts after permission granted
- [ ] Greeting plays clearly without distortion
- [ ] Visual indicator shows "listening" state

### Voice Interaction
- [ ] User speech captured accurately (STT)
- [ ] AI waits to finish speaking before listening
- [ ] State indicator changes: "Your turn" → "Processing" → "AI Speaking"
- [ ] No echo or feedback loop
- [ ] Background noise doesn't trigger false captures
- [ ] Silent pauses auto-send message (1 second delay)

### Call Quality
- [ ] TTS voice is clear and natural
- [ ] No audio clipping or distortion
- [ ] Volume level appropriate (not too loud/quiet)
- [ ] Latency < 3 seconds end-to-end
- [ ] Call can be ended cleanly at any time
- [ ] Mute button works correctly

---

## 3️⃣ AI Workflow & Qualification

### Guard Agent
- [ ] Detects SPAM correctly (blocks malicious/abusive)
- [ ] Detects QUALIFY intent (buying signals)
- [ ] Detects QUESTION intent (FAQ)
- [ ] Detects OTHER intent (off-topic, gibberish)
- [ ] Risk assessment accurate (LOW/MEDIUM/HIGH)
- [ ] Conversations route to correct agent

### Qualifier Agent
- [ ] Extracts name, email, phone correctly
- [ ] Captures budget as number
- [ ] Captures timeline in months
- [ ] Detects pre-approval status (true/false)
- [ ] Identifies preferred locations
- [ ] Scores leads accurately:
  - **HOT**: Budget ≥ $200k, timeline ≤ 3mo, pre-approved
  - **WARM**: Budget ≥ $200k, timeline 3-6mo, exploring
  - **COLD**: Budget < $200k, timeline > 6mo, browsing
  - **UNCERTAIN**: Missing critical info

### Multi-Intent Detection
- [ ] Handles appointment + qualify simultaneously
- [ ] Handles question + qualify simultaneously
- [ ] Prioritizes primary intent correctly
- [ ] Secondary intents processed

---

## 4️⃣ Dashboard - Conversations Page

### Metrics Display
- [ ] Total Conversations count accurate
- [ ] Qualified count matches status filter
- [ ] Spam Detected count accurate
- [ ] Hot Leads count matches score filter
- [ ] Numbers update in real-time

### Conversation List
- [ ] All conversations visible
- [ ] Pagination works (20 per page)
- [ ] Status badges colored correctly:
  - Active = Blue
  - Qualified = Green
  - Spam = Red
  - Closed = Gray
- [ ] Score badges colored correctly:
  - HOT = Red dot
  - WARM = Amber dot
  - COLD = Blue dot
  - None = "—"
- [ ] Dates show correct local time (Central Time)
- [ ] Cost/Token calculation accurate
- [ ] Channel displays correctly (Web Chat, Voice)

### Filters
- [ ] Status filter works (All, Active, Qualified, Spam, Closed)
- [ ] Score filter works (All, Hot, Warm, Cold, Uncertain)
- [ ] Filters can combine
- [ ] URL updates with filter params
- [ ] Filters persist on page refresh

### Individual Conversation View
- [ ] Click conversation → opens detail page
- [ ] Full transcript displayed
- [ ] Messages in chronological order
- [ ] User vs Assistant clearly distinguished
- [ ] Lead data extracted and displayed
- [ ] Timestamps accurate
- [ ] Cost breakdown visible

---

## 5️⃣ Data Integrity

### Timestamps
- [ ] `started_at` matches conversation start time (local timezone)
- [ ] `created_at` accurate
- [ ] `ended_at` populated when closed
- [ ] `last_activity_at` updates with each message
- [ ] All times in correct timezone (UTC stored, local displayed)

### Lead Scores
- [ ] Score only assigned when conversation qualified
- [ ] Score matches qualification criteria
- [ ] Score visible in dashboard immediately
- [ ] Score affects conversation routing

### Cost Calculation
- [ ] Token count accurate per message
- [ ] Cost calculated based on model pricing
- [ ] Total cost = sum of all messages
- [ ] Cost displays as `$X.XX / Y,YYY tokens`
- [ ] Zero cost never shows for conversations with tokens

### Session Continuity
- [ ] Visitor returns < 30 min → same conversation ID
- [ ] Visitor returns > 30 min → new conversation ID
- [ ] Old conversation auto-closed correctly
- [ ] No orphaned "active" conversations

---

## 6️⃣ Knowledge Base Integration

### FAQ Responses
- [ ] Questions routed to knowledge base
- [ ] Answers use company-specific info
- [ ] Responses concise and accurate
- [ ] Prices, hours, services quoted correctly
- [ ] No generic "contact us" responses when info available
- [ ] Follow-up questions suggested

---

## 7️⃣ Calendar Integration (Optional)

### Appointment Booking
- [ ] Calendar availability detected
- [ ] Available slots displayed (top 3-5)
- [ ] User can select slot
- [ ] Confirmation message clear
- [ ] Event created in Google Calendar
- [ ] No double-bookings

---

## 8️⃣ Performance & Reliability

### Speed
- [ ] Dashboard loads < 2 seconds
- [ ] Chat widget loads < 2 seconds
- [ ] AI response time < 5 seconds average
- [ ] TTS generation < 2 seconds
- [ ] No UI blocking during API calls

### Error Handling
- [ ] Network errors show user-friendly message
- [ ] API failures don't crash widget
- [ ] Conversation recoverable after error
- [ ] Console logs useful for debugging
- [ ] No infinite loops or retry storms

### Scalability
- [ ] Dashboard performs with 100+ conversations
- [ ] Pagination prevents slow queries
- [ ] Filters indexed for fast lookup
- [ ] No memory leaks in long sessions

---

## 9️⃣ Security & Privacy

### Data Protection
- [ ] Conversation data tenant-isolated (RLS)
- [ ] No cross-tenant data leakage
- [ ] API endpoints require authentication
- [ ] Sensitive data not logged to console
- [ ] Visitor IDs properly anonymized

### Input Validation
- [ ] XSS prevented (user input sanitized)
- [ ] SQL injection prevented (parameterized queries)
- [ ] File upload restrictions (if applicable)
- [ ] Rate limiting on API endpoints

---

## 🔟 Edge Cases & Stress Tests

### Unusual Inputs
- [ ] Empty messages ignored
- [ ] Very long messages (500+ words) handled
- [ ] Special characters don't break parsing
- [ ] Emoji handled correctly
- [ ] Multiple languages supported (if applicable)

### Concurrent Users
- [ ] Multiple conversations simultaneously
- [ ] No race conditions on database writes
- [ ] Conversation IDs unique
- [ ] No message cross-contamination

### Network Issues
- [ ] Slow connections don't timeout prematurely
- [ ] Offline detection and graceful handling
- [ ] Reconnection resumes conversation
- [ ] Pending messages queued and sent

---

## ✅ Pre-Production Checklist

- [ ] All above tests passed
- [ ] No critical console errors
- [ ] Database migrations applied
- [ ] Environment variables configured
- [ ] Cron jobs scheduled (stale conversation cleanup)
- [ ] Monitoring/logging set up
- [ ] Backup strategy in place
- [ ] Documentation updated

---

## 📊 Success Metrics

After testing, verify:
- **Accuracy**: > 95% of leads scored correctly
- **Speed**: < 3 sec average response time
- **Reliability**: < 1% error rate
- **User Experience**: No awkward pauses or confusion
- **Data Quality**: 100% of conversations have timestamps, costs
