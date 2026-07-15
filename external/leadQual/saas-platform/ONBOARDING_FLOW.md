# Onboarding Flow Documentation

## Overview

Smooth 4-step onboarding that gets new users from signup to first conversation in under 2 minutes.

---

## Flow Diagram

```
Signup → Onboarding → Dashboard
  |          |
  |      Step 1: Welcome
  |      Step 2: Customize
  |      Step 3: Test
  |      Step 4: Install
  |          |
  |      Skip anytime → Dashboard
```

---

## Step-by-Step

### Step 1: Welcome 👋
**Goal**: Orient and excite the user

**Content**:
- Celebration message
- Overview of what they'll do
- 3-card preview of steps ahead
- CTA: "Let's get started"

**Time**: 10 seconds

---

### Step 2: Customize 🎨
**Goal**: Personalize without overwhelming

**Content**:
- Industry-specific AI already configured
- Optional greeting message field
- List of what AI can do out-of-the-box
- CTA: "Save & continue" or "Skip for now"

**Time**: 30-60 seconds (or skip)

**What's editable**:
- Greeting message (optional)
- Everything else pre-configured based on industry

---

### Step 3: Test 🚀
**Goal**: Let them experience the product immediately

**Content**:
- Embedded voice widget
- Suggestions for what to ask
- Pro tips on testing
- CTA: "Looks good, continue"

**Time**: 1-2 minutes

**Why this matters**:
- Instant gratification
- Builds confidence
- Discovers any issues immediately

---

### Step 4: Install 📦
**Goal**: Get them live on their website

**Content**:
- Copy-paste widget code
- Platform-specific instructions (WordPress, Squarespace, etc.)
- Success message
- CTA: "Go to Dashboard"

**Time**: 2-5 minutes

---

## Design Principles

### 1. Progress Transparency
- Visual progress bar at top
- Step indicators with icons
- Completed steps show green checkmark

### 2. Low Friction
- "Skip to dashboard" always visible
- Optional fields clearly marked
- Each step has skip option

### 3. Immediate Value
- Industry template pre-configured
- Can skip customization
- Test widget works immediately

### 4. Clear Next Actions
- One primary CTA per step
- Secondary "Skip" option
- No dead ends

---

## User Psychology

### Hook (Step 1)
- Celebrate their decision
- Show clear path forward
- Build excitement

### Investment (Step 2)
- Small customization = ownership
- But entirely optional
- Pre-filled defaults = safety net

### Aha Moment (Step 3)
- They see it work
- Experience the magic
- Product sells itself

### Commitment (Step 4)
- They install on site
- Now invested
- Likely to explore dashboard

---

## Technical Implementation

### Files
```
app/onboarding/page.tsx          - Main onboarding flow
app/auth/signup/page.tsx         - Redirects to onboarding
app/api/dashboard/tenant/route.ts - Fetch tenant data
```

### State Management
- Local state for step progression
- Session for auth check
- API calls for tenant data

### Skip Logic
```typescript
// User can skip at any time
const handleSkip = () => {
  router.push('/dashboard');
};
```

---

## Conversion Metrics to Track

1. **Completion Rate**: % who complete all 4 steps
2. **Step Drop-off**: Where users abandon
3. **Skip Rate**: Which steps get skipped most
4. **Time to Complete**: Average duration
5. **Widget Installation**: % who actually install

**Targets**:
- 80%+ reach Step 3 (Test)
- 60%+ complete Step 4 (Install)
- <2 minutes average time

---

## Future Enhancements

### Quick Wins
- [ ] Add video tutorial in Step 1
- [ ] Live chat support button
- [ ] Email with instructions after each step

### Advanced
- [ ] Conditional steps based on industry
- [ ] AI-powered greeting suggestions
- [ ] Live demo call with sample customer
- [ ] Integration wizards (CRM, calendar)
- [ ] Team invites in onboarding

### Personalization
- [ ] Industry-specific examples in Test step
- [ ] Custom widget preview with their branding
- [ ] Smart defaults based on sign up source

---

## Edge Cases Handled

1. **User refreshes page**: State preserved via session
2. **User closes browser**: Can resume on return
3. **Multiple tabs**: All sync to same step
4. **Direct dashboard access**: Can skip onboarding entirely
5. **Return users**: Don't show onboarding again

---

## A/B Test Ideas

### Test 1: Step Order
- **A**: Current (Welcome → Customize → Test → Install)
- **B**: Test first (Welcome → Test → Customize → Install)
- **Hypothesis**: Trying first increases completion

### Test 2: Skip Visibility
- **A**: Skip button always visible (current)
- **B**: Hide skip until step 2
- **Hypothesis**: Less skipping = better retention

### Test 3: Greeting Field
- **A**: Optional greeting field (current)
- **B**: AI-generated suggestions
- **Hypothesis**: Suggestions increase customization

---

## Mobile Experience

All steps fully responsive:
- Progress bar scales down
- Step indicators stack on small screens
- Widget code gets horizontal scroll
- Touch-friendly buttons

---

## Success Criteria

**User completes onboarding successfully when**:
1. They understand what the product does
2. They've tested it (had conversation)
3. They have widget code copied
4. They reach dashboard feeling confident

**Business success when**:
- >70% complete onboarding
- >50% install widget within 24 hours
- <5% contact support during onboarding
- First conversation happens within 1 hour

---

## Status

✅ **Built**: Core 4-step flow with skip options
🚧 **TODO**: Connect to real tenant data
🚧 **TODO**: Integrate live voice widget in Step 3
🚧 **TODO**: Track analytics events

**Ready for**: User testing and feedback

---

## Feedback Questions

1. Does the flow feel too long or too short?
2. Is any step confusing?
3. Do you feel confident after completing?
4. Would you actually install the widget?
5. What would make this smoother?
