import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Customer:
    id: int
    name: str
    contact: str


@dataclass
class Location:
    id: int
    name: str
    address: str
    zip_code: str


@dataclass
class Technician:
    id: int
    name: str
    zones: list[str]
    business_units: list[str]


@dataclass
class Appointment:
    customer_name: str
    technician_name: str
    service: str
    zip_code: str
    date: str
    time: str


class BookingSystem:
    def __init__(self, data_file: str = "data.json"):
        self.customers: dict[int, Customer] = {}
        self.locations: dict[int, Location] = {}
        self.technicians: list[Technician] = []
        self.appointments: list[Appointment] = []
        self._load_data(data_file)

    def _load_data(self, data_file: str):
        with open(data_file, "r") as f:
            data = json.load(f)

        for loc in data["Location_Profiles"]:
            zip_code = loc["address"].split()[-1]
            self.locations[loc["id"]] = Location(
                id=loc["id"],
                name=loc["name"],
                address=loc["address"],
                zip_code=zip_code,
            )

        for cust in data["Customer_Profiles"]:
            self.customers[cust["id"]] = Customer(
                id=cust["id"],
                name=cust["name"],
                contact=cust["contact"],
            )

        for tech in data["Technician_Profiles"]:
            self.technicians.append(
                Technician(
                    id=tech["id"],
                    name=tech["name"],
                    zones=tech["zones"],
                    business_units=tech["business_units"],
                )
            )

    def get_available_services(self) -> list[str]:
        services = set()
        for tech in self.technicians:
            services.update(tech.business_units)
        return sorted(services)

    def get_service_zones(self) -> list[str]:
        zones = set()
        for tech in self.technicians:
            zones.update(tech.zones)
        return sorted(zones)

    def find_technician(
        self, service: str, zip_code: str, date: str, time: str
    ) -> Optional[Technician]:
        """Find a technician that matches service, zone, and is available."""
        service = service.lower()

        for tech in self.technicians:
            # Check if technician offers this service
            if service not in tech.business_units:
                continue
            # Check if technician serves this zip code
            if zip_code not in tech.zones:
                continue
            # Check if technician is available (not already booked)
            if self._is_booked(tech, date, time):
                continue
            return tech
        return None

    def _is_booked(self, tech: Technician, date: str, time: str) -> bool:
        """Check if technician already has an appointment at this date/time."""
        for appt in self.appointments:
            if (
                appt.technician_name == tech.name
                and appt.date == date
                and appt.time == time
            ):
                return True
        return False

    def book_appointment(
        self, customer_name: str, service: str, zip_code: str, date: str, time: str
    ) -> tuple[bool, str]:
        """Attempt to book an appointment. Returns (success, message)."""
        tech = self.find_technician(service, zip_code, date, time)

        if tech is None:
            return False, (
                f"Sorry, no technician is available for {service} "
                f"in zip code {zip_code} on {date} at {time}. "
                "Please try a different time or date."
            )

        appointment = Appointment(
            customer_name=customer_name,
            technician_name=tech.name,
            service=service,
            zip_code=zip_code,
            date=date,
            time=time,
        )
        self.appointments.append(appointment)

        return True, (
            f"Appointment confirmed!\n"
            f"  Customer: {customer_name}\n"
            f"  Service: {service}\n"
            f"  Technician: {tech.name}\n"
            f"  Location: {zip_code}\n"
            f"  Date: {date}\n"
            f"  Time: {time}"
        )
