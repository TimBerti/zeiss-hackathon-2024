from dataclasses import dataclass
from enum import Enum
import time

RESERVATION_MAX_AGE_SECONDS = 30


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
    _status: Status = Status.Free
    timestamp: float = 0

    @property
    def status(self) -> Status:
        self._drop_expired_reservation()
        return self._status

    @status.setter
    def status(self, status: Status | int):
        self._status = Status(status)
        self.timestamp = time.time()

    def _drop_expired_reservation(self):
        timestamp_expiry = time.time() - RESERVATION_MAX_AGE_SECONDS
        if self._status == Status.Reserved and self.timestamp < timestamp_expiry:
            self.status = Status.Free


db: list[Record] = [Record() for i in range(8)]


def get_record(desk_id: int) -> Record:
    if desk_id < 0 or desk_id >= len(db):
        raise NoSuchDeskException(desk_id)
    return db[desk_id]


def make_reservation(desk_id: int):
    record = get_record(desk_id)
    if record.status != Status.Free:
        raise DeskUnavailableException(desk_id)
    record.status = Status.Reserved


def get_status_mask() -> list[int]:
    return [record.status.value for record in db]


def set_status(desk_id: int, status: Status) -> bool:
    assert isinstance(status, Status)
    record = get_record(desk_id)
    if status == Status.Free and record.status == Status.Reserved:
        return False
    record.status = status
    return True


def set_status_mask(mask: list[int]):
    for desk_id, status_int in enumerate(mask):
        set_status(desk_id, Status(status_int))
