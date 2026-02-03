import json
import re
from datetime import datetime
from dataclasses import dataclass
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

    def parse_date(self, date_str: str) -> Optional[str]:
        """Parse various date formats and return standardized format, or None if invalid."""
        date_str = date_str.strip()

        date_formats = [
            "%Y-%m-%d",           # 2026-12-02
            "%m/%d/%Y",            # 12/2/2026, 12/02/2026
            "%m-%d-%Y",            # 12-2-2026
            "%d/%m/%Y",            # 2/12/2026 (European)
            "%d-%m-%Y",            # 2-12-2026
            "%B %d, %Y",           # December 2, 2026
            "%b %d, %Y",           # Dec 2, 2026
            "%d %B %Y",            # 2 December 2026
            "%d %b %Y",            # 2 Dec 2026
            "%Y/%m/%d",            # 2026/12/02
            "%m/%d/%y",            # 12/2/26
            "%d/%m/%y",            # 2/12/26
        ]

        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%B %d, %Y")
            except ValueError:
                continue

        return None

    def parse_time(self, time_str: str) -> Optional[str]:
        """Parse various time formats and return standardized format, or None if invalid."""
        time_str = time_str.strip().upper()

        hour_match = re.match(r'^(\d{1,2})\s*(AM|PM)?$', time_str)
        if hour_match:
            hour = int(hour_match.group(1))
            am_pm = hour_match.group(2) or ""

            if hour < 1 or hour > 12:
                return None

            if not am_pm:
                am_pm = "AM"

            time_str = f"{hour:02d}:00 {am_pm}"
            try:
                dt = datetime.strptime(time_str, "%I:%M %p")
                return dt.strftime("%I:%M %p")
            except ValueError:
                pass

        am_pm_formats = [
            "%I:%M %p",            # 10:30 AM
            "%I:%M%p",             # 10:30AM
            "%I %p",               # 10 AM
            "%I%p",                # 10AM
            "%I:%M:%S %p",         # 10:30:45 AM
            "%I:%M:%S%p",          # 10:30:45AM
        ]

        for fmt in am_pm_formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                return dt.strftime("%I:%M %p")
            except ValueError:
                continue

        hour_minute_formats = [
            "%H:%M",               # 14:30
            "%H:%M:%S",            # 14:30:45
            "%H",                  # 14
        ]

        for fmt in hour_minute_formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                return dt.strftime("%I:%M %p")
            except ValueError:
                continue

        return None

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