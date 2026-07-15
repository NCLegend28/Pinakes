# Virtual Receptionist AI - SaaS Platform

Multi-tenant SaaS platform for AI-powered virtual receptionists with industry-specific lead qualification.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Supabase account (for database)
- AI Provider API keys (OpenAI, Anthropic, etc.)

### 1. Database Setup

See `../database/SUPABASE_SETUP.md` for detailed Supabase setup instructions.

Quick summary:
1. Create Supabase project
2. Run `../database/schema.sql` in SQL Editor
3. Run `../database/seeds/001_industry_templates.sql`
4. Get API credentials from Settings → API

### 2. Environment Setup

```bash
# Copy example environment file
cp .env.local.example .env.local

# Edit .env.local with your Supabase credentials and AI API keys
```

### 3. Install and Run

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
saas-platform/
├── app/                    # Next.js App Router
│   ├── api/v1/chat/       # Chat API endpoints
│   ├── dashboard/         # Dashboard (TODO)
│   └── page.tsx           # Landing page
├── lib/                   # Core libraries
│   ├── supabase/          # Database clients
│   ├── tenant/            # Tenant configuration
│   └── workflow/          # AI workflow engine
├── types/                 # TypeScript types
└── components/            # React components
```

## 🔑 API Endpoints

### POST /api/v1/chat/start
Start a new conversation

### POST /api/v1/chat/message
Send a message and get AI response

### GET /api/v1/chat/history/[id]
Get conversation history

See full API documentation in the README.

## 🏗️ Architecture

- **Multi-tenant**: Each customer has isolated data with custom AI configs
- **Industry templates**: Pre-configured for Real Estate, Law, Consulting, Healthcare
- **AI Workflow**: Guard Agent → Qualifier Agent → Lead Scoring
- **Persistence**: All conversations and messages saved to Supabase

## 📖 Documentation

- [START_HERE.md](../START_HERE.md) - Business plan
- [MVP_ROADMAP.md](../MVP_ROADMAP.md) - 10-week plan
- [ARCHITECTURE.md](../ARCHITECTURE.md) - Technical details
- [SUPABASE_SETUP.md](../database/SUPABASE_SETUP.md) - Database setup

## 🚧 Current Status: Week 1 Complete ✅

**Completed:**
- ✅ Database schema created
- ✅ Industry templates seeded
- ✅ Next.js project set up
- ✅ Core libraries (Supabase, tenant config, workflow engine)
- ✅ Chat API endpoints
- ✅ Landing page

**Next (Week 2):**
- [ ] Authentication system
- [ ] Dashboard UI
- [ ] Tenant onboarding

See `MVP_ROADMAP.md` for full 10-week plan.
