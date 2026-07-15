# Stripe Billing Setup Guide

## Overview

Stripe integration for subscription billing with 14-day free trial and automatic payment handling.

---

## 1. Create Stripe Account

1. Go to [stripe.com](https://stripe.com)
2. Sign up for an account
3. Verify your business details
4. Enable test mode for development

---

## 2. Create Products & Prices

### In Stripe Dashboard → Products:

#### Starter Plan
- **Name**: Starter
- **Description**: Perfect for small businesses
- **Price**: $49/month
- **Billing**: Recurring monthly
- Copy the **Price ID** (starts with `price_`)

#### Pro Plan
- **Name**: Pro
- **Description**: For growing businesses
- **Price**: $99/month
- **Billing**: Recurring monthly
- **Metadata**: Add `recommended: true`
- Copy the **Price ID**

#### Enterprise Plan
- **Name**: Enterprise
- **Description**: Custom solutions
- **Price**: $299/month
- **Billing**: Recurring monthly
- Copy the **Price ID**

---

## 3. Get API Keys

### Test Keys (Development)

1. Go to Developers → API Keys
2. Copy **Publishable key** (starts with `pk_test_`)
3. Copy **Secret key** (starts with `sk_test_`)

### Webhook Secret

1. Go to Developers → Webhooks
2. Click "+ Add endpoint"
3. **Endpoint URL**: `https://your-domain.com/api/billing/webhook`
4. **Events to send**:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
5. Copy the **Signing secret** (starts with `whsec_`)

---

## 4. Configure Environment Variables

Add to `.env.local`:

```env
# Stripe API Keys
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx

# Stripe Price IDs
STRIPE_STARTER_PRICE_ID=price_xxxxx
STRIPE_PRO_PRICE_ID=price_xxxxx
STRIPE_ENTERPRISE_PRICE_ID=price_xxxxx
```

---

## 5. Enable Customer Portal

1. Go to Settings → Billing → Customer portal
2. Click "Activate test link"
3. Configure:
   - ✅ Allow customers to update payment method
   - ✅ Allow customers to view invoices
   - ✅ Allow customers to cancel subscriptions
   - Set cancellation behavior: "Cancel at end of billing period"

---

## 6. Apply Database Migration

Run the subscription tables migration:

```bash
psql $DATABASE_URL -f database/migrations/001_add_subscriptions.sql
```

This creates:
- `subscriptions` table
- `usage_records` table

---

## 7. Test Checkout Flow

### Local Testing with Stripe CLI

1. Install Stripe CLI:
   ```bash
   brew install stripe/stripe-brew/stripe
   ```

2. Login to Stripe:
   ```bash
   stripe login
   ```

3. Forward webhooks to local:
   ```bash
   stripe listen --forward-to localhost:3002/api/billing/webhook
   ```

4. Use test card:
   - **Card number**: 4242 4242 4242 4242
   - **Expiry**: Any future date
   - **CVC**: Any 3 digits

---

## 8. API Routes

### Create Checkout Session
```typescript
POST /api/billing/create-checkout
{
  "planId": "starter",
  "tenantId": "uuid",
  "email": "user@example.com"
}
```

### Manage Subscription
```typescript
POST /api/billing/manage-subscription
{
  "action": "cancel",  // or "reactivate", "update"
  "subscriptionId": "sub_xxxxx"
}
```

### Customer Portal
```typescript
POST /api/billing/portal
{
  "customerId": "cus_xxxxx"
}
```

### Webhooks
```
POST /api/billing/webhook
```

---

## 9. Production Checklist

Before going live:

- [ ] Switch to live API keys (not test keys)
- [ ] Create production products/prices in Stripe
- [ ] Update environment variables with live keys
- [ ] Set up production webhook endpoint
- [ ] Test full payment flow with real card
- [ ] Enable tax collection (if required)
- [ ] Set up billing alerts for failed payments
- [ ] Configure email notifications
- [ ] Review security settings
- [ ] Enable fraud detection

---

## 10. Usage Flow

### New Customer Signup

1. User selects plan on pricing page
2. Redirects to Stripe Checkout
3. Enters payment details
4. Checkout completes → webhook fires
5. `checkout.session.completed` event:
   - Create subscription record
   - Update tenant with `stripe_customer_id`
   - Set trial end date
6. User redirected to dashboard

### Subscription Management

**Cancel**:
```typescript
const response = await fetch('/api/billing/manage-subscription', {
  method: 'POST',
  body: JSON.stringify({
    action: 'cancel',
    subscriptionId: 'sub_xxxxx'
  })
});
```

**Update Plan**:
```typescript
const response = await fetch('/api/billing/manage-subscription', {
  method: 'POST',
  body: JSON.stringify({
    action: 'update',
    subscriptionId: 'sub_xxxxx',
    newPlanId: 'pro'
  })
});
```

**Portal Access**:
```typescript
const response = await fetch('/api/billing/portal', {
  method: 'POST',
  body: JSON.stringify({
    customerId: 'cus_xxxxx'
  })
});
window.location.href = response.url;
```

---

## 11. Webhook Events

### checkout.session.completed
- Create subscription record in database
- Update tenant with Stripe customer ID
- Send welcome email

### customer.subscription.updated
- Update subscription status
- Handle plan changes
- Update billing period

### customer.subscription.deleted
- Mark subscription as canceled
- Update tenant status
- Send cancellation email

### invoice.payment_succeeded
- Reset usage counters for new period
- Send payment receipt

### invoice.payment_failed
- Send payment failure notification
- Attempt retry
- Suspend access if continues to fail

---

## 12. Testing Scenarios

### Successful Subscription
1. Go to `/pricing`
2. Click "Start free trial"
3. Complete checkout with `4242 4242 4242 4242`
4. Verify subscription created in database
5. Verify 14-day trial set

### Failed Payment
1. Use card: `4000 0000 0000 0341`
2. Payment will be declined
3. Verify error handling

### Cancel Subscription
1. Call manage-subscription API with `action: 'cancel'`
2. Verify `cancel_at_period_end = true`
3. Verify user retains access until period end

---

## 13. Cost Analysis

### Platform Fees (Stripe)
- **2.9% + $0.30** per successful charge
- No setup fees
- No monthly fees
- No hidden fees

### Example Revenue
At $99/month plan:
- Gross: $99.00
- Stripe fee: $3.17
- **Net: $95.83** (96.8% margin)

At 100 customers:
- Monthly revenue: $9,900
- Stripe fees: $317
- **Net revenue: $9,583**

---

## 14. Troubleshooting

### Webhook Not Receiving Events
- Check webhook URL is publicly accessible (use ngrok for local)
- Verify webhook secret is correct
- Check Stripe dashboard → Webhooks → Recent deliveries

### Checkout Session Not Creating
- Verify price IDs match environment variables
- Check API key permissions
- Review server logs for errors

### Customer Portal Not Loading
- Ensure portal is activated in Stripe dashboard
- Verify customer ID is valid
- Check return URL is set

---

## 15. Next Steps

- [ ] Set up usage-based billing for overage
- [ ] Add dunning management for failed payments
- [ ] Implement revenue analytics dashboard
- [ ] Set up automated tax calculation
- [ ] Add invoice customization (logo, colors)
- [ ] Implement referral/coupon system

---

## Resources

- [Stripe Documentation](https://stripe.com/docs)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Testing Cards](https://stripe.com/docs/testing)
- [Webhooks Guide](https://stripe.com/docs/webhooks)

---

**Status**: ✅ Ready for testing
**Next**: Configure environment variables and test checkout flow
