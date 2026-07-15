# Sequential Voice Mode

## Change Summary

The voice widget now operates in **sequential mode** - users must wait for the AI to finish speaking before they can respond.

### What Changed

**Before** (Continuous mode):
- Recording was active even during AI speech
- Attempted to detect user "interruptions"
- Could pick up AI's own voice or background noise

**After** (Sequential mode):
- Recording stops when AI starts speaking
- Recording only resumes after AI finishes
- Clear visual indicators show when user can speak

### Code Changes

#### [VoiceWidget.tsx](file:///Users/mosley/projects/leadQual/saas-platform/components/VoiceWidget.tsx)

1. **Removed interruption detection** (line 115-121)
2. **Changed TTS flow** (line 193-210):
   - Stop recording during AI speech
   - Only restart after TTS completes
3. **Updated UI indicators**:
   - "Your turn - Speak now" (green, pulsing)
   - "AI Speaking - Please wait" (blue, static)
   - Footer hint: "Wait for AI to finish before speaking"

### Benefits

✅ **No echo/feedback** - AI won't hear itself  
✅ **Cleaner conversations** - No accidental pickups during AI speech  
✅ **Simpler logic** - No complex interruption handling  
✅ **Clear UX** - Users know exactly when they can speak

### Testing

The voice widget will now:
1. Show "Your turn - Speak now" (green) when listening
2. Show "AI Speaking - Please wait" (blue) during TTS
3. Automatically resume listening after AI finishes

Try it in the running dev server at `http://localhost:3000`
