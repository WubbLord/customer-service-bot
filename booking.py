import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

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
        self.technicians: list[Technician] = []
        self.appointments: list[Appointment] = []
        self._load_data(data_file)

    def _load_data(self, data_file: str):
        with open(data_file, "r") as f:
            data = json.load(f)

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
            if service not in tech.business_units:
                continue
            if zip_code not in tech.zones:
                continue
            if self._is_booked(tech, date, time):
                continue
            return tech
        return None

    def _is_booked(self, tech: Technician, date: str, time: str) -> bool:
        """Check if technician has a conflicting appointment (within 2 hours)."""
        for appt in self.appointments:
            if appt.technician_name != tech.name:
                continue
            if appt.date != date:
                continue
            try:
                appt_time = datetime.strptime(appt.time, "%I:%M %p")
                new_time = datetime.strptime(time, "%I:%M %p")
                diff_minutes = abs((new_time - appt_time).total_seconds() / 60)
                if diff_minutes < 120:
                    return True
            except ValueError:
                if appt.time == time:
                    return True
        return False

    def book_appointment(
        self, customer_name: str, service: str, zip_code: str, date: str, time: str
    ) -> str:
        """Attempt to book an appointment. Returns message."""
        tech = self.find_technician(service, zip_code, date, time)

        if tech is None:
            return f"""Sorry, no technician is available for {service} in zip code {zip_code} on {date} at {time}.\nPlease try a different time or date."""

        appointment = Appointment(
            customer_name=customer_name,
            technician_name=tech.name,
            service=service,
            zip_code=zip_code,
            date=date,
            time=time,
        )
        self.appointments.append(appointment)

        return f"""Appointment confirmed!
  Customer: {customer_name}
  Service: {service}
  Technician: {tech.name}
  Location: {zip_code}
  Date: {date}
  Time: {time}
"""