# Finding customers — the playbook

The goal of this doc: never do spray-and-pray cold outreach. Every prospect
should come from a signal that says "this company has the problem you're
solving, right now, with budget assigned."

---

## The five signals

### Signal 1 — Job postings (strongest)
If a company has an open role for "LLM Engineer," "RAG Engineer," "AI
Engineer (evals)," or "Forward Deployed Engineer" mentioning Langfuse /
LangSmith / Braintrust / evals / golden sets — they have the problem
AND the budget.

**Where to look:**
- LinkedIn Jobs (filter by keyword, last 7 days)
- Indeed, Wellfound, YC Work at a Startup
- company careers pages directly (for series A/B startups)

**Keyword set:**
```
"LLM evaluation"
"agent evaluation"
"prompt engineering" AND "production"
"RAG" AND "evaluation"
"Forward Deployed Engineer" AND ("AI" OR "LLM")
"Langfuse" OR "LangSmith" OR "Braintrust"  (name-drops = they've felt the pain)
"golden set"
```

A company with 2+ matching roles in 30 days is an A-tier target.

### Signal 2 — Public shipping artifacts
- Changelog/blog posts mentioning "new AI feature" in last 90 days
- "Powered by GPT / Claude" in product footers
- Status pages with incidents tagged "model" or "LLM" or "AI"
- Public docs with `/ai`, `/assistant`, or `/chat` routes

### Signal 3 — Funding + stage match
Sweet spot: Series A/B SaaS that added AI to positioning in 2024-2026.
- Seed — no budget yet
- Public — 12-month procurement cycle
- Series A/B — budget + speed + pain

Crunchbase filter: Series A/B, raised 2024-2026, keywords "AI" / "agent" / "copilot".

### Signal 4 — Integration footprint
They appear in partner pages of:
- Anthropic, OpenAI (customer logos)
- LangChain, LlamaIndex (case studies)
- Pinecone, Weaviate, pgvector (customer lists)
- ElevenLabs, VAPI (voice agents)

Scrape those logos — they form your ICP list.

### Signal 5 — Pain tells
- G2 reviews mentioning "hallucination," "wrong answers," "inconsistent"
- GitHub issues on public repos mentioning "flaky," "regression," "eval"
- Engineers on X/LinkedIn complaining about eval difficulty

---

## The scoring function

```
score = (
    open_roles_count * 3 +          # strongest signal
    (3 if series_A_or_B else 0) +
    customer_logo_matches * 2 +
    recent_ai_blog_posts +
    pain_tell_count
) * recency_weight
```

A-tier (>= 12): cold email within 48 hours.
B-tier (6-11): add to nurture list.
C-tier: skip.

---

## The cold email template

Subject: `{{role_title}} — a shortcut`

> Hi {{first_name}},
>
> Saw you're hiring a {{role_title}} — the JD mentions {{specific_detail_from_post}}.
>
> I built guapo_evals specifically for that problem: a drop-in Python SDK
> that traces every LLM/tool call and runs golden-set evals on every deploy.
> Teams use it to catch agent regressions before prod.
>
> Would a 15-minute demo be useful? Happy to instrument one of your agents
> live — if it doesn't surface something useful in the first 10 minutes, I'll
> buy you coffee.
>
> — Tali
> BliqByte | bliqbyte.com

**Rules:**
- One specific detail from their JD — proves it's not a blast
- One concrete offer (live instrumentation)
- One escape hatch (coffee)
- No attachments, no calendar links in the first email
- Signature: personal name + company + URL. Nothing else.

Target: 5 sends/day, expect 15-25% reply rate with this level of specificity.

---

## The automation (build this in week 2)

A weekend-grade scraper + scorer:

```
crontab: daily at 6am
  ↓
scrape LinkedIn / Wellfound / YC for keyword set
  ↓
dedupe by company (company_name + domain)
  ↓
enrich via Clearbit / Apollo: size, funding, founders
  ↓
score each
  ↓
post top 5 A-tier to Slack #sales channel with pre-drafted email
  ↓
you paste, personalize one line, send
```

This pipeline is reusable across every future BliqByte product.
Invest the weekend; it pays for itself by the third outbound cycle.

---

## What NOT to do

- Don't cold email someone whose only signal is "their company does AI." Too broad.
- Don't lead with the product. Lead with the specific job posting.
- Don't use first-message calendar links — they kill reply rates.
- Don't follow up more than twice. Three silent contacts = remove from list.
- Don't pitch C-suite. Pitch whoever is on the hook for agent reliability:
  staff engineers, tech leads, heads of AI. Those are the people who feel
  the pain at 2am when the agent breaks.
