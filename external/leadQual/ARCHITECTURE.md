# 🏗️ Multi-Tenant SaaS Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Customer Touchpoints                     │
├─────────────┬──────────────┬──────────────┬─────────────────┤
│ Web Widget  │ Phone Call   │ Email/SMS    │ Admin Dashboard │
└─────────────┴──────────────┴──────────────┴─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway (Next.js)                   │
│  - Authentication (tenant isolation)                         │
│  - Rate limiting                                             │
│  - Request routing                                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Conversation Engine                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tenant Config Loader                                │   │
│  │  - Load industry template                            │   │
│  │  - Apply custom instructions                         │   │
│  │  - Select AI models per agent                        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Multi-Agent Workflow (Current System)               │   │
│  │  - Guard Agent                                       │   │
│  │  - Qualifier Agent                                   │   │
│  │  - Clarifier Agent                                   │   │
│  │  - Action Agent                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ PostgreSQL   │ Redis Cache  │ S3 (Attachments)         │ │
│  │ - Tenants    │ - Sessions   │ - Call recordings        │ │
│  │ - Configs    │ - Rate limits│ - Chat transcripts       │ │
│  │ - Convos     │ - Hot data   │                          │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Integration Layer                          │
│  ┌──────────┬──────────┬──────────┬──────────┬───────────┐  │
│  │ Webhook  │ Zapier   │ CRM      │ Calendar │ Email     │  │
│  │ Events   │ Triggers │ Sync     │ Booking  │ Notify    │  │
│  └──────────┴──────────┴──────────┴──────────┴───────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### Core Tables

```sql
-- Tenants (Companies using the platform)
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,  -- acme-realty
  industry VARCHAR(50) NOT NULL,       -- real_estate, law, consulting

  -- Branding
  logo_url TEXT,
  primary_color VARCHAR(7),            -- #FF5733

  -- Business details
  business_hours JSONB,                -- {mon: "9-5", tue: "9-5", ...}
  timezone VARCHAR(50),
  phone_number VARCHAR(20),

  -- Platform
  subdomain VARCHAR(100) UNIQUE,       -- acme.virtualreceptionist.ai
  custom_domain VARCHAR(255),          -- chat.acme.com

  -- Subscription
  plan VARCHAR(50) NOT NULL,           -- starter, professional, enterprise
  plan_limits JSONB,                   -- {conversations_per_month: 500}
  stripe_customer_id VARCHAR(255),

  -- Status
  status VARCHAR(20) DEFAULT 'active', -- active, suspended, cancelled
  trial_ends_at TIMESTAMP,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Agent Configurations (AI setup per tenant)
CREATE TABLE agent_configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,

  -- Agent identity
  agent_type VARCHAR(50) NOT NULL,     -- guard, qualifier, clarifier, action
  name VARCHAR(100),                   -- "Lead Qualifier", "FAQ Bot"

  -- AI Model
  provider VARCHAR(50) NOT NULL,       -- openai, anthropic, ollama
  model VARCHAR(100) NOT NULL,         -- gpt-4o, claude-3-5-sonnet
  temperature DECIMAL(3,2) DEFAULT 0.7,
  max_tokens INTEGER DEFAULT 2000,

  -- Instructions
  system_instructions TEXT NOT NULL,   -- Custom prompt

  -- Settings
  enabled BOOLEAN DEFAULT true,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(tenant_id, agent_type)
);

-- Industry Templates (Defaults for each industry)
CREATE TABLE industry_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  industry VARCHAR(50) NOT NULL,
  agent_type VARCHAR(50) NOT NULL,

  name VARCHAR(100),
  description TEXT,

  -- Default AI configuration
  default_provider VARCHAR(50),
  default_model VARCHAR(100),
  default_temperature DECIMAL(3,2),

  -- Instructions template
  system_instructions TEXT NOT NULL,

  -- Qualification schema
  qualification_fields JSONB,          -- {name: {type: "string", required: true}}
  lead_scoring_rules JSONB,            -- {hot: {budget: ">200000"}}

  created_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(industry, agent_type)
);

-- Conversations
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,

  -- Source
  channel VARCHAR(20) NOT NULL,        -- web_chat, phone, sms, email
  source_url TEXT,                     -- Where chat started
  visitor_id VARCHAR(255),             -- Anonymous or user ID

  -- Status
  status VARCHAR(20) DEFAULT 'active', -- active, qualified, spam, closed
  lead_score VARCHAR(20),              -- hot, warm, cold, uncertain

  -- Captured data
  lead_data JSONB,                     -- {name: "John", budget: 500000, ...}
  metadata JSONB,                      -- {ip: "...", user_agent: "..."}

  -- Lifecycle
  started_at TIMESTAMP DEFAULT NOW(),
  ended_at TIMESTAMP,

  -- Cost tracking
  total_tokens INTEGER DEFAULT 0,
  total_cost DECIMAL(10,4) DEFAULT 0,

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_tenant ON conversations(tenant_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_score ON conversations(lead_score);
CREATE INDEX idx_conversations_created ON conversations(created_at DESC);

-- Messages (Conversation history)
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,

  -- Message
  role VARCHAR(20) NOT NULL,           -- user, assistant, system
  content TEXT NOT NULL,

  -- Metadata
  agent_type VARCHAR(50),              -- Which agent generated this
  model_used VARCHAR(100),             -- gpt-4o, claude-3-5-sonnet
  tokens_used INTEGER,
  cost DECIMAL(10,6),

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at DESC);

-- Integrations
CREATE TABLE integrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,

  -- Integration type
  type VARCHAR(50) NOT NULL,           -- zapier, hubspot, salesforce, google_calendar
  name VARCHAR(100),

  -- Configuration
  config JSONB NOT NULL,               -- {api_key: "...", webhook_url: "..."}

  -- Settings
  enabled BOOLEAN DEFAULT true,
  triggers JSONB,                      -- {on_qualified_lead: true, on_spam: false}

  -- Status
  last_sync_at TIMESTAMP,
  last_error TEXT,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Users (Tenant admins/staff)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,

  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  name VARCHAR(255),

  role VARCHAR(20) DEFAULT 'admin',    -- admin, member, viewer

  -- Auth
  email_verified_at TIMESTAMP,
  last_login_at TIMESTAMP,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Analytics (Aggregated metrics)
CREATE TABLE analytics_daily (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
  date DATE NOT NULL,

  -- Counts
  conversations_total INTEGER DEFAULT 0,
  conversations_qualified INTEGER DEFAULT 0,
  conversations_spam INTEGER DEFAULT 0,

  -- Lead scores
  leads_hot INTEGER DEFAULT 0,
  leads_warm INTEGER DEFAULT 0,
  leads_cold INTEGER DEFAULT 0,

  -- Costs
  total_tokens INTEGER DEFAULT 0,
  total_cost DECIMAL(10,2) DEFAULT 0,

  created_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(tenant_id, date)
);
```

---

## 🔄 Workflow: How a Conversation Works

### 1. Visitor Starts Chat

```typescript
// Widget on customer's website
POST /api/v1/chat/start
{
  "tenant_slug": "acme-realty",
  "visitor_id": "anonymous-abc123",
  "source_url": "https://acme.com/contact",
  "metadata": {
    "user_agent": "...",
    "referrer": "..."
  }
}

Response:
{
  "conversation_id": "uuid",
  "session_token": "jwt-token",
  "greeting": "Hi! I'm here to help you find your dream home..."
}
```

### 2. Load Tenant Configuration

```typescript
// Server-side
async function loadTenantConfig(tenantSlug: string) {
  const tenant = await db.tenants.findBySlug(tenantSlug);

  // Load or use defaults
  const configs = await db.agentConfigs.findByTenant(tenant.id);

  if (!configs.length) {
    // First time - use industry template
    configs = await applyIndustryTemplate(tenant.id, tenant.industry);
  }

  return {
    tenant,
    agents: configs.reduce((acc, config) => {
      acc[config.agent_type] = {
        provider: config.provider,
        model: config.model,
        temperature: config.temperature,
        instructions: config.system_instructions
      };
      return acc;
    }, {})
  };
}
```

### 3. Run Workflow with Tenant Config

```typescript
// Use existing workflow.ts but with dynamic config
const { agents } = await loadTenantConfig(tenantSlug);

const guardAgent = new Agent({
  name: "Guard",
  instructions: agents.guard.instructions,  // Tenant-specific!
  model: agents.guard.model,                // Could be different per tenant
  ...
});

const result = await runWorkflow({ input_as_text: message });

// Save to database
await db.messages.create({
  conversation_id,
  role: "assistant",
  content: result.response,
  agent_type: "guard",
  model_used: agents.guard.model,
  tokens_used: result.tokens,
  cost: calculateCost(result.tokens, agents.guard.provider)
});
```

### 4. Execute Integrations

```typescript
// If lead is qualified, trigger integrations
if (result.lead_score === 'HOT') {
  const integrations = await db.integrations.findEnabled(tenantId);

  for (const integration of integrations) {
    if (integration.triggers.on_qualified_lead) {
      await executeIntegration(integration, result.lead_data);
    }
  }
}

async function executeIntegration(integration, leadData) {
  switch (integration.type) {
    case 'zapier':
      await fetch(integration.config.webhook_url, {
        method: 'POST',
        body: JSON.stringify(leadData)
      });
      break;

    case 'hubspot':
      await hubspot.contacts.create({
        email: leadData.email,
        properties: leadData
      });
      break;

    // ... etc
  }
}
```

---

## 🎨 Frontend Architecture

### Admin Dashboard (Next.js)

```
app/
├── (auth)/
│   ├── login/
│   ├── signup/
│   └── forgot-password/
│
├── (dashboard)/
│   ├── overview/              # Analytics, metrics
│   ├── conversations/         # List/view all conversations
│   │   └── [id]/             # Individual conversation
│   ├── settings/
│   │   ├── ai-config/        # Configure agents
│   │   ├── branding/         # Logo, colors
│   │   ├── integrations/     # Connect CRM, calendar
│   │   └── billing/          # Subscription management
│   └── widget/               # Embed code, customization
│
├── api/
│   ├── v1/
│   │   ├── chat/             # Conversation API
│   │   ├── tenants/          # Tenant management
│   │   ├── integrations/     # Integration webhooks
│   │   └── analytics/        # Metrics API
│   └── webhooks/             # External webhooks
│
└── widget/
    └── embed.js              # Embeddable chat widget
```

### Embeddable Widget (Vanilla JS)

```html
<!-- Customer adds this to their website -->
<script>
  window.VirtualReceptionist = {
    tenantSlug: 'acme-realty',
    position: 'bottom-right',
    primaryColor: '#FF5733'
  };
</script>
<script src="https://cdn.virtualreceptionist.ai/widget.js"></script>
```

---

## 🚀 Deployment Architecture

### Recommended Stack (Cost-Effective)

```yaml
Frontend (Dashboard + Widget):
  Platform: Vercel
  Cost: $20/month (Pro plan)
  CDN: Included

Backend (API):
  Platform: Railway / Render
  Cost: $20-50/month
  Auto-scaling: Yes

Database:
  Platform: Supabase / Neon
  Cost: $25/month (with backups)
  Type: PostgreSQL

Cache:
  Platform: Upstash Redis
  Cost: $10/month

AI Providers:
  Mix: OpenAI + Anthropic + Groq
  Cost: Variable (~$0.02-0.05 per conversation)

Storage:
  Platform: AWS S3 or Cloudflare R2
  Cost: ~$5/month

Monitoring:
  Platform: Sentry + Vercel Analytics
  Cost: Free tier initially

Total Fixed Costs: ~$100-150/month
Variable Costs: ~$0.05 per conversation
```

### Scalability Plan

| Stage | Traffic | Infrastructure | Monthly Cost |
|-------|---------|----------------|--------------|
| **MVP** | 10 tenants, 5K convos/mo | Single server, managed DB | $150 |
| **Growth** | 50 tenants, 50K convos/mo | Load balanced, Redis cache | $500 |
| **Scale** | 200 tenants, 500K convos/mo | Auto-scaling, CDN, dedicated DB | $2,000 |

---

## 🔐 Security & Compliance

### Tenant Isolation

```typescript
// Every query must be tenant-scoped
async function getConversations(userId: string) {
  const user = await db.users.findById(userId);

  // ✅ ALWAYS filter by tenant_id
  return db.conversations.findMany({
    where: { tenant_id: user.tenant_id }
  });
}

// ❌ NEVER allow cross-tenant access
async function badExample(conversationId: string) {
  return db.conversations.findById(conversationId);  // Dangerous!
}
```

### Data Privacy

- Encrypt conversation data at rest
- Mask PII in logs
- GDPR compliance (data export, deletion)
- SOC 2 Type II (for enterprise plan)

### Rate Limiting

```typescript
// Per tenant rate limits
const limits = {
  starter: { requests: 100, per: '1m' },
  professional: { requests: 500, per: '1m' },
  enterprise: { requests: 'unlimited' }
};
```

---

## 📊 Migration from Current Codebase

### Phase 1: Add Multi-Tenancy

1. **Add tenant context to workflow**
```typescript
// workflow.ts - Add tenant parameter
export const runWorkflow = async (
  workflow: WorkflowInput,
  tenantConfig: TenantConfig  // NEW
) => {
  // Load tenant-specific agent configs
  const guard = createGuardAgent(tenantConfig.guard);
  // ...
}
```

2. **Create configuration loader**
```typescript
// lib/tenant-config.ts
export async function loadTenantConfig(tenantId: string) {
  // Load from database
  // Fall back to industry template
  // Return agent configurations
}
```

### Phase 2: Add Persistence

1. **Add database layer**
```typescript
// lib/database.ts
export const db = {
  conversations: {
    create, find, update
  },
  messages: {
    create, findByConversation
  },
  // ...
}
```

2. **Save conversations**
```typescript
// After each workflow run
await db.messages.create({
  conversation_id,
  role: 'assistant',
  content: result.response
});
```

### Phase 3: Add Dashboard & Widget

Build Next.js frontend with:
- Admin dashboard
- Embeddable widget
- API routes

---

## 🎯 Next Implementation Steps

1. **Set up database** (Supabase/Neon)
2. **Create tenant seeding** (industry templates)
3. **Add tenant context to workflow**
4. **Build simple dashboard** (view conversations)
5. **Create embeddable widget**
6. **Deploy MVP** (single tenant initially)
7. **Test with beta customers**

Ready to start building? 🚀
