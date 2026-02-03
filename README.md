# CSR Chat Bot

A command-line Customer Service chatbot for booking service appointments.

## Run

**CLI:**
```bash
python main.py
```

**Web app:**
```bash
pip install flask
python app.py
```
Then open http://127.0.0.1:5000 to view the web app.

## Features

- **Book appointments** for services
- **2-hour appointment slots** with automatic conflict detection
- **FAQ** for service areas and available services

## Example Session

```
==================================================
  Welcome to the Customer Service Chat Bot!
==================================================

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
Preferred date (e.g., 2025-02-15): 02/15/2025
Preferred time (e.g., 10:00 AM): 10am

Appointment confirmed!
  Customer: Justin Long
  Service: plumbing
  Technician: Michael Page
  Location: 94115
  Date: February 15, 2025
  Time: 10:00 AM

You: quit
Thank you for using our service. Goodbye!
```

## Files

| File | Purpose |
|------|---------|
| `main.py` | CLI interface |
| `app.py` | Web interface (Flask) |
| `booking.py` | Booking logic and data models |
| `faq.py` | FAQ response handlers |
| `data.json` | Technician and service data |
