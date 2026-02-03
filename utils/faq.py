from .booking import BookingSystem


class FAQHandler:
    def __init__(self, booking_system: BookingSystem):
        self.booking_system = booking_system

    def get_locations_response(self) -> str:
        zones = self.booking_system.get_service_zones()
        return (
            "We serve the following zip codes in San Francisco:\n"
            f"  {', '.join(zones)}"
        )

    def get_services_response(self) -> str:
        services = self.booking_system.get_available_services()
        return (
            "We offer the following services:\n"
            f"  {', '.join(s.title() for s in services)}"
        )
