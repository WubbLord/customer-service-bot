from booking import BookingSystem
from faq import FAQHandler


def get_input(prompt: str) -> str:
    """Get user input with a prompt."""
    return input(f"{prompt}: ").strip()


def handle_booking(booking_system: BookingSystem):
    """Handle the appointment booking flow."""
    print("\n--- Book an Appointment ---")

    customer_name = get_input("Your name")
    if not customer_name:
        print("Name is required.")
        return

    services = booking_system.get_available_services()
    print(f"Available services: {', '.join(s.title() for s in services)}")
    service = get_input("Service needed (e.g., plumbing, electrical, hvac)").lower()
    if service not in services:
        print(f"Sorry, '{service}' is not a valid service.")
        return

    zones = booking_system.get_service_zones()
    print(f"We serve zip codes: {', '.join(zones)}")
    zip_code = get_input("Your zip code")
    if zip_code not in zones:
        print(f"Sorry, we don't serve zip code '{zip_code}'.")
        return

    # Get and validate date with reprompting
    while True:
        date_input = get_input("Preferred date (e.g., 2025-02-15)")
        if not date_input:
            print("Date is required.")
            continue
        date = booking_system.parse_date(date_input)
        if date is None:
            print(f"Could not parse '{date_input}'. Please use a format like '12/2/2026', '2026-12-02', or 'December 2, 2026'.")
            continue
        break

    # Get and validate time with reprompting
    while True:
        time_input = get_input("Preferred time (e.g., 10:00 AM)")
        if not time_input:
            print("Time is required.")
            continue
        time = booking_system.parse_time(time_input)
        if time is None:
            print(f"Could not parse '{time_input}'. Please use a format like '10AM', '10:30 AM', or '14:30'.")
            continue
        break

    message = booking_system.book_appointment(
        customer_name=customer_name,
        service=service,
        zip_code=zip_code,
        date=date,
        time=time,
    )
    print(f"\n{message}")


def parse_intent(user_input: str) -> str:
    """Parse user input to determine intent."""
    text = user_input.lower()

    if any(word in text for word in ["book", "appointment", "schedule"]):
        return "book"

    if any(word in text for word in ["location", "where", "area", "zip", "zone"]):
        return "locations"

    if any(word in text for word in ["service", "offer", "what do you", "help with"]):
        return "services"

    if any(word in text for word in ["quit", "exit", "bye", "goodbye"]):
        return "exit"

    if any(word in text for word in ["help"]):
        return "help"

    return "unknown"


def print_help():
    """Print help message."""
    print(
        """
How can I help you today?

  - Type "book" to schedule a two-hour appointment
  - Type "services" to see what services we offer
  - Type "locations" to see which areas we serve
  - Type "quit" to exit

You can also ask questions like:
  - "I need to book an appointment"
  - "What services do you offer?"
  - "Where are you located?"
"""
    )


def main():
    print("=" * 50)
    print("  Welcome to the Customer Service Chat Bot!")
    print("=" * 50)

    booking_system = BookingSystem()
    faq_handler = FAQHandler(booking_system)

    print_help()

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue

        intent = parse_intent(user_input)

        if intent == "exit":
            print("Thank you for using our service. Goodbye!")
            break
        elif intent == "book":
            handle_booking(booking_system)
        elif intent == "locations":
            print(faq_handler.get_locations_response())
        elif intent == "services":
            print(faq_handler.get_services_response())
        elif intent == "help":
            print_help()
        else:
            print(
                "I'm not sure I understand. Type 'help' to see what I can do, "
                "or 'book' to schedule an appointment."
            )


if __name__ == "__main__":
    main()
