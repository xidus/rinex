
from rinex.observationfile import (
    ObservationFile,
)


def test_fields_correctly_matched():
    # Examples of valid filenames from RINEX3 specification
    # Table 2: Description of Filename Parameters
    valid_filename = 'ALGO00CAN_R_20121601000_01H_01S_MO.rnx'
    obsfile = ObservationFile(valid_filename)
    test_data = (
        ('name', 'ALGO00CAN'),
        ('receiver', 'R'),
        ('start_time', '20121601000'),
        ('file_period', '01H'),
        ('data_freq', '01S'),
        ('data_type', 'MO'),
        ('format_', 'rnx'),
        ('compression', ''),
    )
    for attr, expected in test_data:
        result = getattr(obsfile, attr)
        assert result == expected, f'Expected {result!r} to be {expected!r} using {attr!r}.'


def test_is_valid_observation_file():

    # Examples of valid filenames from RINEX3 specification
    # Table 2: Description of Filename Parameters
    test_data = (
        ('ALGO00CAN_R_20121601000_01H_01S_MO.rnx', True),
        ('ALGO00CAN_R_20121601000_15M_01S_GO.rnx', True),
        ('ALGO00CAN_R_20121601000_01H_05Z_MO.rnx', True),
        ('ALGO00CAN_R_20121601000_01D_30S_GO.rnx', True),
        ('ALGO00CAN_R_20121601000_01D_30S_MO.rnx', True),
    )
    for test_input, expected in test_data:
        result = ObservationFile(test_input).is_valid()
        assert result == expected, f'Expected {result!r} to be {expected!r} using {test_input!r}.'

