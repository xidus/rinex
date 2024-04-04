"""
Module for RINEX3 observation file validation.

"""

import os
import pathlib
from dataclasses import dataclass

from rinex.validate import (
    has_valid_characters,
    name_is_valid,
    receiver_is_valid,
    start_time_is_valid,
    file_period_is_valid,
    data_freq_is_valid,
    data_type_is_valid,
    format_is_valid,
    compression_is_valid,
)


class Field:
    """
    Field descriptor for string slices.

    """
    _slice = None
    def __init__(self, beg: int, end: int) -> None:
        self._slice = slice(beg, end, None)

    def __get__(self, instance, cls):
        return instance._fname[self._slice]


class ObservationFile:
    """
    Validator class for RINEX Observation file.

    Dev notes
    ---------
    Reference filename for string positions:

    ALGO00CAN_R_20121601000_15M_01S_GO.rnx.gz
    0123456789

    """

    name: Field = Field(0, 9)
    receiver: Field = Field(10, 11)
    start_time: Field = Field(12, 23)
    file_period: Field = Field(24, 27)
    data_freq: Field = Field(28, 31)
    data_type: Field = Field(32, 34)
    format_: Field = Field(35, 38)
    compression: Field = Field(39, 42)

    def __init__(self, fname: str) -> None:
        self._fname = fname

    def is_valid(self):
        return (True
            and has_valid_characters(self._fname)
            and name_is_valid(self.name)
            and receiver_is_valid(self.receiver)
            and start_time_is_valid(self.start_time)
            and file_period_is_valid(self.file_period)
            and data_freq_is_valid(self.data_freq)
            and data_type_is_valid(self.data_type)
            and format_is_valid(self.format_)
            and compression_is_valid(self.compression) # BUG!
        )
