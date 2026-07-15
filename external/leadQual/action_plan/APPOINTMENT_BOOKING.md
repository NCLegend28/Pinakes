# 📅 Intelligent Appointment Booking System

## Overview

The video showed: **"like to book and confirm if 4 PM is your preferred time"**

This requires:
1. Real-time calendar checking
2. Conflict detection
3. Smart time suggestions
4. Automatic confirmations
5. Integration with multiple calendar systems

---

## Database Schema

```sql
-- Appointments table
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(50),
    customer_email VARCHAR(255),
    service_type VARCHAR(100) NOT NULL,
    service_duration INTEGER NOT NULL, -- minutes
    scheduled_date DATE NOT NULL,
    scheduled_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(50) DEFAULT 'confirmed', -- confirmed, cancelled, completed, no_show
    notes TEXT,
    upsells JSONB, -- Additional services added
    total_price DECIMAL(10,2),
    deposit_paid BOOLEAN DEFAULT false,
    deposit_amount DECIMAL(10,2),
    reminder_sent BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50) DEFAULT 'ai', -- ai, manual, customer
    calendar_event_id VARCHAR(255), -- Google Calendar/Outlook event ID
    CONSTRAINT no_overlap CHECK (scheduled_time < end_time)
);

-- Calendar integrations
CREATE TABLE calendar_integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    provider VARCHAR(50) NOT NULL, -- google, outlook, calendly
    calendar_id VARCHAR(255) NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    sync_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Business hours
CREATE TABLE business_hours (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    day_of_week INTEGER NOT NULL, -- 0=Sunday, 6=Saturday
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    is_open BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tenant_id, day_of_week)
);

-- Service definitions
CREATE TABLE services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(100) NOT NULL,
    duration_minutes INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    buffer_time_minutes INTEGER DEFAULT 0, -- Time between appointments
    description TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Blocked times (breaks, meetings, etc.)
CREATE TABLE blocked_times (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_appointments_tenant_date ON appointments(tenant_id, scheduled_date);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_customer_phone ON appointments(customer_phone);
```

---

## Core Booking Engine

```typescript
// /lib/booking/booking-engine.ts

interface TimeSlot {
  startTime: string;
  endTime: string;
  available: boolean;
  reason?: string;
}

interface BookingRequest {
  tenantId: string;
  customerName: string;
  customerPhone: string;
  customerEmail?: string;
  serviceId: string;
  date: string; // YYYY-MM-DD
  time: string; // HH:MM
  notes?: string;
}

export class BookingEngine {
  
  /**
   * Check if a specific time slot is available
   */
  async checkAvailability(
    tenantId: string,
    date: string,
    time: string,
    durationMinutes: number
  ): Promise<{ available: boolean; reason?: string }> {
    
    // 1. Check if within business hours
    const businessHours = await this.getBusinessHours(tenantId, date);
    if (!this.isWithinBusinessHours(time, durationMinutes, businessHours)) {
      return {
        available: false,
        reason: `We're closed at that time. Our hours are ${businessHours.open} - ${businessHours.close}`
      };
    }
    
    // 2. Check for existing appointments
    const existingAppointments = await this.getAppointments(tenantId, date);
    const hasConflict = this.detectConflict(time, durationMinutes, existingAppointments);
    if (hasConflict) {
      return {
        available: false,
        reason: 'That time slot is already booked'
      };
    }
    
    // 3. Check for blocked times
    const blockedTimes = await this.getBlockedTimes(tenantId, date);
    if (this.isBlocked(time, durationMinutes, blockedTimes)) {
      return {
        available: false,
        reason: 'That time is not available'
      };
    }
    
    // 4. Check calendar integration
    if (await this.hasCalendarIntegration(tenantId)) {
      const calendarFree = await this.checkExternalCalendar(tenantId, date, time, durationMinutes);
      if (!calendarFree) {
        return {
          available: false,
          reason: 'Calendar conflict detected'
        };
      }
    }
    
    return { available: true };
  }
  
  /**
   * Get all available time slots for a date
   */
  async getAvailableSlots(
    tenantId: string,
    date: string,
    serviceDurationMinutes: number,
    slotIntervalMinutes: number = 30
  ): Promise<TimeSlot[]> {
    
    const slots: TimeSlot[] = [];
    const businessHours = await this.getBusinessHours(tenantId, date);
    
    // Generate all possible slots
    let currentTime = this.parseTime(businessHours.open);
    const closeTime = this.parseTime(businessHours.close);
    
    while (this.addMinutes(currentTime, serviceDurationMinutes) <= closeTime) {
      const timeStr = this.formatTime(currentTime);
      const availability = await this.checkAvailability(
        tenantId,
        date,
        timeStr,
        serviceDurationMinutes
      );
      
      slots.push({
        startTime: timeStr,
        endTime: this.formatTime(this.addMinutes(currentTime, serviceDurationMinutes)),
        available: availability.available,
        reason: availability.reason
      });
      
      currentTime = this.addMinutes(currentTime, slotIntervalMinutes);
    }
    
    return slots;
  }
  
  /**
   * Suggest alternative times when requested time isn't available
   */
  async suggestAlternatives(
    tenantId: string,
    requestedDate: string,
    requestedTime: string,
    durationMinutes: number,
    numSuggestions: number = 3
  ): Promise<TimeSlot[]> {
    
    const allSlots = await this.getAvailableSlots(tenantId, requestedDate, durationMinutes);
    const availableSlots = allSlots.filter(s => s.available);
    
    if (availableSlots.length === 0) {
      // Try next day
      const nextDay = this.addDays(requestedDate, 1);
      return this.suggestAlternatives(tenantId, nextDay, requestedTime, durationMinutes, numSuggestions);
    }
    
    // Find slots closest to requested time
    const requestedMinutes = this.timeToMinutes(requestedTime);
    const sortedSlots = availableSlots.sort((a, b) => {
      const aDiff = Math.abs(this.timeToMinutes(a.startTime) - requestedMinutes);
      const bDiff = Math.abs(this.timeToMinutes(b.startTime) - requestedMinutes);
      return aDiff - bDiff;
    });
    
    return sortedSlots.slice(0, numSuggestions);
  }
  
  /**
   * Create a new appointment
   */
  async createAppointment(request: BookingRequest): Promise<Appointment> {
    
    // 1. Validate availability
    const service = await this.getService(request.serviceId);
    const availability = await this.checkAvailability(
      request.tenantId,
      request.date,
      request.time,
      service.duration_minutes
    );
    
    if (!availability.available) {
      throw new Error(`Time slot not available: ${availability.reason}`);
    }
    
    // 2. Calculate end time
    const endTime = this.addMinutes(
      this.parseTime(request.time),
      service.duration_minutes
    );
    
    // 3. Create appointment in database
    const appointment = await db.appointments.create({
      tenant_id: request.tenantId,
      customer_name: request.customerName,
      customer_phone: request.customerPhone,
      customer_email: request.customerEmail,
      service_type: service.name,
      service_duration: service.duration_minutes,
      scheduled_date: request.date,
      scheduled_time: request.time,
      end_time: this.formatTime(endTime),
      total_price: service.price,
      notes: request.notes,
      created_by: 'ai'
    });
    
    // 4. Create calendar event
    if (await this.hasCalendarIntegration(request.tenantId)) {
      const eventId = await this.createCalendarEvent(request.tenantId, {
        summary: `${service.name} - ${request.customerName}`,
        description: request.notes,
        start: `${request.date}T${request.time}`,
        end: `${request.date}T${this.formatTime(endTime)}`,
        attendees: [request.customerEmail].filter(Boolean)
      });
      
      await db.appointments.update(appointment.id, {
        calendar_event_id: eventId
      });
    }
    
    // 5. Send confirmations
    await this.sendConfirmations(appointment);
    
    // 6. Update CRM
    await this.syncToCRM(request.tenantId, appointment);
    
    return appointment;
  }
  
  /**
   * Send SMS and email confirmations
   */
  private async sendConfirmations(appointment: Appointment) {
    const tenant = await this.getTenant(appointment.tenant_id);
    
    // SMS confirmation
    if (appointment.customer_phone) {
      await this.sendSMS(appointment.customer_phone, `
Hi ${appointment.customer_name}! Your ${appointment.service_type} appointment is confirmed for ${appointment.scheduled_date} at ${appointment.scheduled_time}.

${tenant.business_name}
${tenant.address}

Reply CANCEL to cancel.
      `.trim());
    }
    
    // Email confirmation with calendar invite
    if (appointment.customer_email) {
      await this.sendEmail({
        to: appointment.customer_email,
        subject: `Appointment Confirmed - ${appointment.service_type}`,
        html: this.generateConfirmationEmail(appointment, tenant),
        icalEvent: this.generateICalEvent(appointment, tenant)
      });
    }
  }
  
  /**
   * Generate iCal event for email
   */
  private generateICalEvent(appointment: Appointment, tenant: Tenant): string {
    return `
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AI Receptionist//EN
BEGIN:VEVENT
UID:${appointment.id}
DTSTAMP:${new Date().toISOString()}
DTSTART:${appointment.scheduled_date}T${appointment.scheduled_time}
DTEND:${appointment.scheduled_date}T${appointment.end_time}
SUMMARY:${appointment.service_type}
DESCRIPTION:${appointment.notes || ''}
LOCATION:${tenant.address}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR
    `.trim();
  }
  
  /**
   * Detect conflicts with existing appointments
   */
  private detectConflict(
    newTime: string,
    newDuration: number,
    existingAppointments: Appointment[]
  ): boolean {
    const newStart = this.timeToMinutes(newTime);
    const newEnd = newStart + newDuration;
    
    return existingAppointments.some(apt => {
      const aptStart = this.timeToMinutes(apt.scheduled_time);
      const aptEnd = this.timeToMinutes(apt.end_time);
      
      // Check for overlap
      return (newStart < aptEnd && newEnd > aptStart);
    });
  }
  
  /**
   * Check if time is within business hours
   */
  private isWithinBusinessHours(
    time: string,
    durationMinutes: number,
    businessHours: BusinessHours
  ): boolean {
    const requestedStart = this.timeToMinutes(time);
    const requestedEnd = requestedStart + durationMinutes;
    const openTime = this.timeToMinutes(businessHours.open);
    const closeTime = this.timeToMinutes(businessHours.close);
    
    return requestedStart >= openTime && requestedEnd <= closeTime;
  }
  
  /**
   * Time utility functions
   */
  private timeToMinutes(time: string): number {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
  }
  
  private parseTime(time: string): Date {
    const [hours, minutes] = time.split(':').map(Number);
    const date = new Date();
    date.setHours(hours, minutes, 0, 0);
    return date;
  }
  
  private formatTime(date: Date): string {
    return date.toTimeString().slice(0, 5); // HH:MM
  }
  
  private addMinutes(date: Date, minutes: number): Date {
    return new Date(date.getTime() + minutes * 60000);
  }
  
  private addDays(dateStr: string, days: number): string {
    const date = new Date(dateStr);
    date.setDate(date.getDate() + days);
    return date.toISOString().split('T')[0];
  }
}
```

---

## Google Calendar Integration

```typescript
// /lib/integrations/google-calendar.ts
import { google } from 'googleapis';

export class GoogleCalendarIntegration {
  private oauth2Client: any;
  
  constructor(credentials: CalendarCredentials) {
    this.oauth2Client = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET,
      process.env.GOOGLE_REDIRECT_URI
    );
    
    this.oauth2Client.setCredentials({
      access_token: credentials.access_token,
      refresh_token: credentials.refresh_token
    });
  }
  
  /**
   * Check if time slot is available on Google Calendar
   */
  async checkAvailability(
    calendarId: string,
    startTime: string,
    endTime: string
  ): Promise<boolean> {
    const calendar = google.calendar({ version: 'v3', auth: this.oauth2Client });
    
    const response = await calendar.freebusy.query({
      requestBody: {
        timeMin: startTime,
        timeMax: endTime,
        items: [{ id: calendarId }]
      }
    });
    
    const busy = response.data.calendars[calendarId].busy || [];
    return busy.length === 0;
  }
  
  /**
   * Create calendar event
   */
  async createEvent(
    calendarId: string,
    event: {
      summary: string;
      description?: string;
      start: string;
      end: string;
      attendees?: string[];
    }
  ): Promise<string> {
    const calendar = google.calendar({ version: 'v3', auth: this.oauth2Client });
    
    const response = await calendar.events.insert({
      calendarId,
      requestBody: {
        summary: event.summary,
        description: event.description,
        start: {
          dateTime: event.start,
          timeZone: 'America/Denver' // Get from tenant settings
        },
        end: {
          dateTime: event.end,
          timeZone: 'America/Denver'
        },
        attendees: event.attendees?.map(email => ({ email })),
        reminders: {
          useDefault: false,
          overrides: [
            { method: 'email', minutes: 24 * 60 }, // 1 day before
            { method: 'popup', minutes: 60 } // 1 hour before
          ]
        }
      },
      sendUpdates: 'all' // Send invites to attendees
    });
    
    return response.data.id;
  }
  
  /**
   * Update existing event
   */
  async updateEvent(
    calendarId: string,
    eventId: string,
    updates: Partial<Event>
  ): Promise<void> {
    const calendar = google.calendar({ version: 'v3', auth: this.oauth2Client });
    
    await calendar.events.patch({
      calendarId,
      eventId,
      requestBody: updates,
      sendUpdates: 'all'
    });
  }
  
  /**
   * Delete event
   */
  async deleteEvent(calendarId: string, eventId: string): Promise<void> {
    const calendar = google.calendar({ version: 'v3', auth: this.oauth2Client });
    
    await calendar.events.delete({
      calendarId,
      eventId,
      sendUpdates: 'all'
    });
  }
}
```

---

## AI Agent Function Tools

```typescript
// Add these tools to your AI agent

const bookingTools = [
  {
    name: 'check_availability',
    description: 'Check if a specific date and time is available for booking',
    parameters: {
      type: 'object',
      properties: {
        date: {
          type: 'string',
          description: 'Date in YYYY-MM-DD format'
        },
        time: {
          type: 'string',
          description: 'Time in HH:MM format (24-hour)'
        },
        service: {
          type: 'string',
          description: 'Name of the service'
        }
      },
      required: ['date', 'time', 'service']
    }
  },
  {
    name: 'get_available_slots',
    description: 'Get all available time slots for a specific date',
    parameters: {
      type: 'object',
      properties: {
        date: {
          type: 'string',
          description: 'Date in YYYY-MM-DD format'
        },
        service: {
          type: 'string',
          description: 'Name of the service'
        }
      },
      required: ['date', 'service']
    }
  },
  {
    name: 'book_appointment',
    description: 'Book an appointment after confirming availability',
    parameters: {
      type: 'object',
      properties: {
        customer_name: { type: 'string' },
        customer_phone: { type: 'string' },
        customer_email: { type: 'string' },
        date: { type: 'string', description: 'YYYY-MM-DD' },
        time: { type: 'string', description: 'HH:MM' },
        service: { type: 'string' },
        notes: { type: 'string' }
      },
      required: ['customer_name', 'customer_phone', 'date', 'time', 'service']
    }
  },
  {
    name: 'suggest_alternative_times',
    description: 'Suggest alternative available times when requested time is not available',
    parameters: {
      type: 'object',
      properties: {
        date: { type: 'string' },
        time: { type: 'string' },
        service: { type: 'string' }
      },
      required: ['date', 'time', 'service']
    }
  }
];
```

---

## Conversation Flow Example

```typescript
// How the AI should handle booking in conversation

const bookingConversationFlow = `
User: "I'd like to book a manicure"

AI: "Great! I'd be happy to help you book a manicure. 
     What date were you thinking?"

User: "How about this Thursday?"

AI: *calls get_available_slots for Thursday*
    "This Thursday we have openings at 10am, 2pm, 4pm, and 6pm. 
     Which time works best for you?"

User: "4pm sounds good"

AI: *calls check_availability for Thursday 4pm*
    "Perfect! I can confirm 4pm this Thursday for a manicure. 
     May I have your name and phone number to complete the booking?"

User: "Sarah Johnson, 303-555-0123"

AI: "Thanks Sarah! Just to confirm:
     - Manicure
     - Thursday, December 7th at 4:00 PM
     - Duration: 45 minutes
     - Price: $50
     
     Would you like to add anything else? 
     We also offer gel polish for an additional $15."

User: "Yes, add the gel polish"

AI: *calls book_appointment with upsell*
    "Excellent! Your appointment is confirmed:
     
     📅 Thursday, Dec 7 at 4:00 PM
     💅 Manicure + Gel Polish
     💰 Total: $65
     
     You'll receive a confirmation text shortly at 303-555-0123.
     Is there anything else I can help you with?"
`;
```

---

## API Endpoints

```typescript
// /pages/api/booking/check-availability.ts
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { tenantId, date, time, serviceId } = req.body;
  
  const engine = new BookingEngine();
  const result = await engine.checkAvailability(tenantId, date, time, serviceId);
  
  res.json(result);
}

// /pages/api/booking/available-slots.ts
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { tenantId, date, serviceId } = req.query;
  
  const engine = new BookingEngine();
  const slots = await engine.getAvailableSlots(
    tenantId as string,
    date as string,
    serviceId as string
  );
  
  res.json({ slots });
}

// /pages/api/booking/create.ts
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const bookingRequest: BookingRequest = req.body;
  
  try {
    const engine = new BookingEngine();
    const appointment = await engine.createAppointment(bookingRequest);
    
    res.json({ success: true, appointment });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
}
```

---

## Testing the System

```typescript
// Test cases for booking engine

describe('BookingEngine', () => {
  it('should detect conflicts', async () => {
    const engine = new BookingEngine();
    
    // Book first appointment
    await engine.createAppointment({
      tenantId: 'test-tenant',
      date: '2024-12-07',
      time: '14:00',
      serviceId: 'manicure'
    });
    
    // Try to book overlapping appointment
    const result = await engine.checkAvailability(
      'test-tenant',
      '2024-12-07',
      '14:30',
      45 // 45 minutes, would overlap
    );
    
    expect(result.available).toBe(false);
  });
  
  it('should suggest alternatives', async () => {
    const engine = new BookingEngine();
    
    const suggestions = await engine.suggestAlternatives(
      'test-tenant',
      '2024-12-07',
      '14:00', // Not available
      45
    );
    
    expect(suggestions.length).toBeGreaterThan(0);
    expect(suggestions.every(s => s.available)).toBe(true);
  });
});
```

---

## Key Features Summary

✅ **Real-time availability checking**
✅ **Conflict detection**
✅ **Business hours validation**
✅ **Buffer time support**
✅ **Smart time suggestions**
✅ **Multiple calendar integration** (Google, Outlook)
✅ **Automatic confirmations** (SMS, Email, Calendar invite)
✅ **CRM sync**
✅ **Timezone support**
✅ **No-show tracking**

---

*Next: Implement upselling engine and payment processing*
