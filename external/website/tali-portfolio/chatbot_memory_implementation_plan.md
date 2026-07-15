# ChatBot Memory & Context Implementation Plan
**Project:** tali-portfolio — ChatBot.jsx  
**Goal:** Make the chatbot context-aware so it never repeats itself or loses track of conversation history

---

## Problem Summary
The chatbot currently sends each message independently with no memory of prior exchanges. Every request is stateless — like starting a brand new conversation each time. The fix requires maintaining a conversation history array and passing it with every API call.

---

## Architecture Overview

```
User Input
    ↓
ChatBot.jsx (manages conversationHistory state)
    ↓
POST /api/chat  { messages: [...history, newMessage] }
    ↓
Backend (server.js or separate API route)
    ↓
AI Provider (Claude / OpenAI)  ← receives full history
    ↓
Response appended to history
    ↓
UI updated
```

---

## Phase 1 — Frontend: ChatBot.jsx

### 1.1 Add Conversation History State
```javascript
const [conversationHistory, setConversationHistory] = useState([
  {
    role: 'system',
    ci's portfolio assistant. You know about his projects 
    (Financio, Apollo Gloves, AI Receptionist SaaS), his background in biomedical 
    engineering from UT Austin, and his skills in Python, ML, and full-stack development.
    Never repeat information you've already shared in this conversation.
    Be concise, conversational, and helpful.`
  }
]);
```

### 1.2 Update the Send Message Function
```javascript
const sendMessage = async (userInput) => {
  // Build updated history with new user message
  const updatedHistory = [
    ...conversationHistory,
    { role: 'user', content: userInput }
  ];

  // Optimistically update UI
  setConversationHistory(updatedHistory);

  // Send full history to backend
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages: updatedHistory })
  });

  const data = await response.json();

  // Append assistant response to history
  setConversationHistory([
    ...updatedHistory,
    { role: 'assistant', content: data.reply }
  ]);
};
```

### 1.3 Display Logic
- Only render messages where `role !== 'system'` so the system prompt stays hidden
- User messages render right-aligned (already done)
- Assistant messages render left-aligned (already done)
- Add a "Clear conversation" button that resets history to just the system prompt

---

## Phase 2 — Backend: API Route

### 2.1 Add `/api/chat` endpoint to server.js
```javascript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

app.post('/api/chat', async (req, res) => {
  const { messages } = req.body;

  // Separate sysm prompt from conversation
  const systemPrompt = messages.find(m => m.role === 'system')?.content;
  const conversation = messages.filter(m => m.role !== 'system');

  const response = await anthropic.messages.create({
    model: 'claude-opus-4-6',
    max_tokens: 1024,
    system: systemPrompt,
    messages: conversation
  });

  res.json({ reply: response.content[0].text });
});
```

### 2.2 Install Anthropic SDK on server
```bash
source /home/aferrone/nodevenv/public_html/tali-portfolio/24/bin/activate
npm install @anthropic-ai/sdk
```

### 2.3 Set API Key as Environment Variable
In cPanel → Node.js App → Environment Variables, add:
```
ANTHROPIC_API_KEY = your_key_here
```
Never hardcode the key in source files.

---

## Phase 3 — Context & Persona

### 3.1 Enrich the System Prompt
Give the assistant deep knowledge about Tali so answers are accurate and personal:

```
You are an AI assistant embedded in Tali  portfolio website.

About Tali:
- Biomedical engineer from UT Austin with compual specialization
- Currently building an AI Receptionist SaaS platform with voice integration
- Creator of Financio, an algorithmic trading system with sub-5% MAPE
- Built Apollo Gloves — EMG-based gesture recognition hardware
- Skills: Python, React, ML/AI, full-stack development
- Philosophy: "Carpe Diem" and "As you climb, you must lift"

Rules:
- Never repeat information already covered in the conversation
- Keep responses concise (2-4 sentences unless detail is requested)
- If asked something you don't know, say so honestly
- Direct recruiters/visitors to relevant projects based on their interests
```

### 3.2 Suggested Quick-Reply Buttons
Pre-defined prompts that inject into the conversation naturally:
- "Tell me about your AI projects"
- "What's your background?"
- "Let's hear about Financio"
- "What are you looking for?"

---

## Phase 4 — Quality of Life

### 4.1 Token/Length Management
Conversation history can grow large and hit API token limits. Add a sliding window:
```javascript
const MAX_ORY = 20; // keep last 20 messages

const trimmedHistory = [
  conversationHistory[0], // always keep system prompt
  ...conversationHistory.slice(1).slice(-MAX_HISTORY)
];
```

### 4.2 Error Handling
```javascript
try {
  const response = await fetch('/api/chat', { ... });
  if (!response.ok) throw new Error('API error');
  // handle response
} catch (err) {
  // Show friendly error message in chat UI
  appendMessage('assistant', 'Sorry, something went wrong. Please try again.');
}
```

### 4.3 Loading State
Show a typing indicator while waiting for response:
```javascript
const [isTyping, setIsTyping] = useState(false);
// Set true before fetch, false after
```

---

## Implementation Order for Agent

1. **ChatBot.jsx** — add `conversationHistory` state, update send function, fix display filter
2. **server.js** — add `/api/chat` POST route with Anthropic SDK
3. **Environment** — add `ANTHROPIC_API_KEY` to cPanel env vars, run `npm install @anthropic-ai/sdk`
4. **System prompt** — write detailed pentext prompt
5. **Deploy** — `npm run build` locally → SCP `dist/` → restart Passenger
6. **Test** — verify history persists across multiple turns, no repeated answers

---

## Files to Modify
| File | Change |
|------|--------|
| `src/components/ChatBot.jsx` | Add history state, update fetch logic, fix display |
| `server.js` | Add `/api/chat` endpoint |
| `.env` or cPanel env vars | Add `ANTHROPIC_API_KEY` |
| `package.json` | Add `@anthropic-ai/sdk` dependency |
