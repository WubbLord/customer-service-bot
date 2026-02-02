# CSR Chat Bot

A command-line Customer Service Representative chatbot that can book appointments and answer FAQs.

## How to Run

```bash
python main.py
```

## Features

1. **Book Appointments** - Schedule service appointments with available technicians
2. **FAQ - Services** - View available services (plumbing, electrical, hvac)
3. **FAQ - Locations** - View zip codes we serve

## Example Session

```
==================================================
  Welcome to the Customer Service Chat Bot!
==================================================

How can I help you today?

  - Type "book" to schedule an appointment
  - Type "services" to see what services we offer
  - Type "locations" to see which areas we serve
  - Type "quit" to exit

You: What services do you offer?
We offer the following services:
  Electrical, Hvac, Plumbing

You: Where are you located?
We serve the following zip codes in San Francisco:
  94101, 94106, 94107, 94111, 94113, 94115, 94117, 94118, 94119, 94120, 94133

You: book
--- Book an Appointment ---
Your name: Justin Long
Available services: Electrical, Hvac, Plumbing
Service needed (e.g., plumbing, electrical, hvac): plumbing
We serve zip codes: 94101, 94106, 94107, 94111, 94113, 94115, 94117, 94118, 94119, 94120, 94133
Your zip code: 94115
Preferred date (e.g., 2025-02-15): 2025-02-15
Preferred time (e.g., 10:00 AM): 10:00 AM

Appointment confirmed!
  Customer: Justin Long
  Service: plumbing
  Technician: Michael Page
  Location: 94115
  Date: 2025-02-15
  Time: 10:00 AM

You: quit
Thank you for using our service. Goodbye!
```

## Project Structure

```
customer-service-bot/
├── data.json      # Customer, location, and technician data
├── main.py        # CLI entry point and chat loop
├── booking.py     # Data classes and booking logic
├── faq.py         # FAQ response handlers
└── README.md
```

## Technician Matching Logic

When booking an appointment, the system finds a technician who:
1. Offers the requested service (plumbing, electrical, or hvac)
2. Serves the customer's zip code
3. Is available at the requested date/time (not already booked)
