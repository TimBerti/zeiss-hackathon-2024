from dataclasses import dataclass
from enum import Enum
import time

RESERVATION_MAX_AGE_SECONDS = 5 * 60


class NoSuchDeskException(LookupError):
    pass

class DeskUnavailableException(Exception):
    pass

class Status(Enum):
    Free = 0
    Occupied = 1
    Reserved = 2


@dataclass
class Record:
    status: Status = Status.Free
    timestamp: float = 0


db: list[Record] = [Record() for _ in range(6)]


def get_record(desk_id: int) -> Record:
    if desk_id < 0 or desk_id >= len(db):
        raise NoSuchDeskException(desk_id)
    return db[desk_id]


def drop_expired_reservation(record: Record):
    timestamp_expiry = time.time() + RESERVATION_MAX_AGE_SECONDS
    if record.status == Status.Reserved and record.timestamp < timestamp_expiry:
        record.status = Status.Free


def drop_expired_reservations():
    for record in db:
        drop_expired_reservation(record)


def make_reservation(desk_id: int):
    record = get_record(desk_id)
    drop_expired_reservation(record)
    if record.status != Status.Free:
        raise DeskUnavailableException(desk_id)
    record.status = Status.Reserved


def get_status_mask() -> list[int]:
    drop_expired_reservations()
    return [record.status.value for record in db]


def set_status(desk_id: int, status: Status) -> bool:
    assert isinstance(status, Status)
    record = get_record(desk_id)
    drop_expired_reservation(record)
    if status == Status.Free and record.status == Status.Reserved:
        return False
    record.status = status
    return True


def set_status_mask(mask: list[int]):
    for desk_id, status_int in enumerate(mask):
        set_status(desk_id, status_int)
