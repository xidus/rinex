
import string

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


def test_has_valid_characters():
    test_data = (
        ('ALGO00CAN_R_20121601000_01H_01S_MO.rnx', True),
        ('ALGO00CAN_R_20121601000_15M_01S_GO.rnx', True),
        ('ALGO00CAN_R_20121601000_01H_05Z_MO.rnx', True),
        ('ALGO00CAN_R_20121601000_01D_30S_GO.rnx', True),
        ('ALGO00CAN_R_20121601000_01D_30S_MO.rnx', True),
        # (, ),
    )
    for test_input, expected in test_data:
        result = has_valid_characters(test_input)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'


def test_name_is_valid():
    test_data = (
        # From the specification
        ('ALGO00CAN', True),
        # (, ),
    )
    for test_input, expected in test_data:
        result = name_is_valid(test_input)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'


def test_receiver_is_valid():
    allowed = {'S', 'R', 'U'}
    test_data = \
        tuple((c, True) for c in allowed) \
        + tuple((c, False) for c in set(string.ascii_uppercase) - allowed)
    for test_input, expected in test_data:
        result = receiver_is_valid(test_input)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'


def test_start_time_is_valid():
    test_data = (
        # From the specification
        ('20121501200', True),
    )
    for test_input, expected in test_data:
        result = start_time_is_valid(test_input)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'


def test_file_period_is_valid():
    test_data = (
        # From the specification
        ('15M', True),
        ('15M', True),
        ('01H', True),
        ('01D', True),
        ('01Y', True),
        ('00U', True),

        # Added
        ('.0M', False),
        ('0.H', False),
        ('-1M', False),
        ('-0H', False),
        # (, ),
        # (, ),
    )
    for test_input, expected in test_data:
        result = file_period_is_valid(test_input)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'


def test_data_freq_is_valid():
    test_data = (
        # From the specification
        ('05Z', True),

        # Added
        ('001C', False),
        # (, ),
        # (, ),
    )
    for test_input, expected in test_data:
        result = data_freq_is_valid(test_input)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'


def test_data_type_is_valid():
    test_data = (
        # From the specification
        ('MO', True),

        # Added
        ('', False),
        # (, ),
        # (, ),
    )
    for test_input, expected in test_data:
        result = data_type_is_valid(test_input)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'


def test_format_is_valid():
    test_data = (
        # From the specification
        ('rnx', True),
        ('crx', True),
    )
    for test_input, expected in test_data:
        result = format_is_valid(test_input)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'


def test_compression_is_valid():
    test_data = (
        # From the specification
        ('gz', True),
        ('bz2', True),
        ('zip', True),

        # Added
        ('.gz', False),
        # (, ),
        # (, ),
    )
    for test_input, expected in test_data:
        result = compression_is_valid(test_input)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'
