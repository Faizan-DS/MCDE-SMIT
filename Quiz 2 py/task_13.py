from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Booking:
    booking_id: str
    room: str
    start: datetime
    end: datetime


@dataclass
class BookingResult:
    accepted: bool
    reason: str
    conflicts: list = field(default_factory=list)


class Scheduler:
    def __init__(self):
        self._rooms = {}
        self._used_ids = set()

    def book(self, booking_id, room, start, end):
        if not isinstance(room, str) or room.strip() == "":
            raise ValueError("Room name cannot be empty")
        if not isinstance(start, datetime) or not isinstance(end, datetime):
            raise TypeError("start and end must be datetime objects")
        if (start.tzinfo is None) != (end.tzinfo is None):
            raise ValueError("start and end must both be naive or both timezone-aware")

        if end <= start:
            return BookingResult(False, "end time must be after start time")
        if booking_id in self._used_ids:
            return BookingResult(False, "booking ID already used")

        existing = self._rooms.setdefault(room, [])
        conflicts = [other for other in existing if start < other.end and other.start < end]
        if conflicts:
            return BookingResult(False, "overlaps with an existing booking", conflicts)

        existing.append(Booking(booking_id, room, start, end))
        existing.sort(key=lambda booking: booking.start)
        self._used_ids.add(booking_id)
        return BookingResult(True, "booked")

    def bookings_for(self, room):
        return tuple(self._rooms.get(room, []))


def show_result(label, result):
    if result.accepted:
        print(label + ": accepted")
    else:
        print(label + ": rejected (" + result.reason + ")")
        for other in result.conflicts:
            print("    conflicts with", other.booking_id, other.start.strftime("%H:%M"), "-", other.end.strftime("%H:%M"))


if __name__ == "__main__":
    def at(hour, minute=0):
        return datetime(2026, 11, 9, hour, minute)

    scheduler = Scheduler()

    show_result("B1 Room A 09:00-10:00", scheduler.book("B1", "Room A", at(9), at(10)))
    show_result("B2 Room A 10:00-11:00", scheduler.book("B2", "Room A", at(10), at(11)))
    show_result("B3 Room A 09:30-10:30", scheduler.book("B3", "Room A", at(9, 30), at(10, 30)))
    show_result("B4 Room B 09:30-10:30", scheduler.book("B4", "Room B", at(9, 30), at(10, 30)))
    show_result("B5 Room A 08:00-09:00", scheduler.book("B5", "Room A", at(8), at(9)))
    show_result("B6 Room A 09:15-09:45", scheduler.book("B6", "Room A", at(9, 15), at(9, 45)))
    show_result("B7 Room A 11:30-11:00", scheduler.book("B7", "Room A", at(11, 30), at(11)))
    show_result("B8 Room A 12:00-12:00", scheduler.book("B8", "Room A", at(12), at(12)))
    show_result("B1 again Room A 13:00-14:00", scheduler.book("B1", "Room A", at(13), at(14)))
    show_result("B3 retry Room A 11:00-12:00", scheduler.book("B3", "Room A", at(11), at(12)))
    show_result("B9 Room A 07:00-12:30", scheduler.book("B9", "Room A", at(7), at(12, 30)))

    print()
    for room in ("Room A", "Room B"):
        print(room + " schedule:")
        for booking in scheduler.bookings_for(room):
            print("  ", booking.booking_id, booking.start.strftime("%H:%M"), "-", booking.end.strftime("%H:%M"))

    print()
    try:
        scheduler.book("X1", "Room A", "09:00", "10:00")
    except TypeError as error:
        print("text instead of datetime:", error)
