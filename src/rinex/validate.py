"""
Module with function that can validate a filename against the RINEX3 standard.

Docstrings contain primarily text from the standard.

Delimitations
-------------

*   Only observation files are to be validated.

"""

import os
import pathlib
import string
import typing
import datetime as dt


FILENAME_CHARACTERS: set = set(string.ascii_uppercase + string.digits + '_')
# EXTENSION_CHARACTERS: set = set('.gz') | set('.bz2') | set('.zip')
EXTENSION_CHARACTERS: set = set(string.ascii_lowercase + '.')

def has_valid_characters(s: str) -> bool:
    """
    All elements of the main body of the file name
    must contain capital ASCII letters or numbers
    and all elements are fixed length and are separated by an underscore “_”.

    The file type and compression fields (extension)
    use a period “.” as a separator and
    must be ASCII characters and lower case.

    Fields must be padded with zeros to fill the field width.

    The file compression field is optional.

    Note:

    The main body of the file name should contain
    only ASCII capital letters and numbers.

    The file extension .rnx.gz should be lowercase.

    """
    fname = pathlib.Path(s).name

    # 'basename.ext1.ext2' => 'basename', 'ext1.ext2'
    basename, ext = fname.split('.', maxsplit=1)
    basename_set, ext_set = set(basename), set(ext)

    if not basename_set & FILENAME_CHARACTERS == basename_set:
        return False

    if not ext_set & EXTENSION_CHARACTERS == ext_set:
        return False

    return True


COUNTRY_CODES: list[str] = None
module_path = os.path.abspath(os.path.dirname(__file__))


def load_country_codes():
    global COUNTRY_CODES
    if COUNTRY_CODES is None:
        fname = pathlib.PurePath(module_path, 'ISO_3166-1_alpha-3.dat')
        with open(fname, encoding='utf-8') as fsock:
            COUNTRY_CODES = fsock.read().splitlines()
    return COUNTRY_CODES


def name_is_valid(s: str) -> bool:
    """
    Quotes
    ------

    9 characters - defining the site, station and country code

    Table A1:

    <SITE/STATION-MONUMENT/RECEIVER/COUNTRY/

    XXXXMRCCC
    Where:
    XXXX - existing IGS station name
    M - monument or marker number (0-9)
    R - receiver number (0-9)
    CCC - ISO Country code
    (Total 9 characters)

    Example: ALGO00CAN

    Required: Yes

    File name supports a maximum
    of 10 monuments at the same
    station and a maximum of 10
    receivers per monument.
    Country codes follow : ISO 3166-1 alpha-3

    Filename Details and Examples
    -----------------------------

    <STATION/PROJECT NAME>:

    IGS users should follow XXXXMRCCC (9 char)
    site and station naming convention described above.

    GNSS industry users could use the 9 characters to indicate the project name and/or number.

    References
    ----------
    https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3

    """
    if len(s) != 9:
        return False

    XXXX: str = s[:4]
    M: str = s[4:5]
    R: str = s[5:6]
    CCC: str = s[6:9]

    # XXXX
    # Q: Must station name be alphanumeric characters?

    # M
    try:
        int(M)
    except Exception as e:
        # raise ValueError(f'Expected `{M=}` to be a number.')
        return False

    # R
    try:
        int(R)
    except Exception as e:
        # raise ValueError(f'Expected `{R=}` to be a number.')
        return False

    # CCC
    if CCC not in load_country_codes():
        # raise ValueError(f'Expected {value!r} to be a valid three-letter country code. (See ISO 3166-1 alpha-3.)')
        return False

    return True


def receiver_is_valid(s: str) -> bool:
    """
    <DATA SOURCE>

    Data Source
    R - From Receiver data using vendor or other software
    S - From data Stream (RTCM or other)
    U - Unknown
    (1 character)

    Required: Yes

    This field is used to indicate how
    the data was collected either
    from the receiver at the station or
    from a data stream

    Filename Details and Examples
    -----------------------------

    <DATA SOURCE>:

    With real-time data
    streaming RINEX files for the same station
    can be created at many locations.

    If the RINEX file is derived from data
    collected at the receiver (official file)
    then the source is specified as R.

    On the other hand if the RINEX file is
    derived from a real-time data stream
    then the data source is marked as S
    to indicate Streamed data source.

    If the data source is unknown
    the source is marked as U.

    """
    if len(s) != 1:
        return False

    return s in ('R', 'S', 'U')


_FMT_START_TIME: str = '%Y%j%H%M'


def start_time_is_valid(s: str) -> bool:
    """
    <START TIME>

    YYYYDDDHHMM

    YYYY - Gregorian year 4 digits,
    DDD - day of Year,
    HHMM - hours and minutes of day

    (11 characters)

    Required: yes

    For GPS files use : GPS Year, day of year, hour of day, minute
    of day (see text below for details)

    Start time should be the nominal

    start time of the first observation.

    GLONASS, Galileo, BeiDou etc use respective time system.

    Filename Details and Examples
    -----------------------------

    <START TIME>:

    The start time is the file start time
    which should coincide with the first
    observation in the file.

    GPS file start time is specified in GPS Time.

    Mixed observation file start times are defined
    in the same time system as the file observation
    time system specified in the header.

    Files containing only:

      GLONASS,
      Galileo,
      QZSS,
      BDS or
      SBAS

    observations are all based on their respective time system.

    """
    if len(s) != 11:
        return False

    try:
        dt.datetime.strptime(s, _FMT_START_TIME)
    except Exception as e:
        return False
    return True


FILE_PERIOD_UNITS_ALLOWED: tuple[str] = ('M', 'H', 'D', 'Y', 'U')


def file_period_is_valid(s: str) -> bool:
    """
    <FILE PERIOD>

    DDU
    DD - file period
    U - units of file period.

    File period is used to specify intended
    collection period of the file.

    (3 characters)

    Required: yes

    File Period
    15M-15 Minutes
    01H-1 Hour
    01D-1 Day
    01Y-1 Year
    00U-Unspecified

    Filename Details and Examples
    -----------------------------

    <FILE PERIOD>:

    Is used to specify the data collection period of the file.

    GNSS observation file name - file period examples:

        //15 min, GPS Obs. 1 sec.
        ALGO00CAN_R_20121601000_15M_01S_GO.rnx.gz

        //1 hour, Obs Mixed and 5Hz
        ALGO00CAN_R_20121601000_01H_05Z_MO.rnx.gz

        //1 day, Obs GPS and 30 sec
        ALGO00CAN_R_20121601000_01D_30S_GO.rnx.gz

        //1 day, Obs. Mixed, 30 sec
        ALGO00CAN_R_20121601000_01D_30S_MO.rnx.gz


    GNSS navigation file name - file period examples:

        // 15 minute GPS only
        ALGO00CAN_R_20121600000_15M_GN.rnx.gz

        // 1 hour GPS only
        ALGO00CAN_R_20121600000_01H_GN.rnx.gz

        // 1 day mixed
        ALGO00CAN_R_20121600000_01D_MN.rnx.gz


    """
    if len(s) != 3:
        return False

    DD: str = s[:2]
    U: str = s[-1:]

    try:
        [int(d) for d in DD]
    except Exception as e:
        return False

    return U in FILE_PERIOD_UNITS_ALLOWED


DATA_FREQ_UNITS_ALLOWED: tuple[str] = ('C', 'Z', 'S', 'M', 'H', 'D', 'U')


def data_freq_is_valid(s: str) -> bool:
    """
    <DATA FREQ>

    DDU
    DD - data frequency
    U - units of data rate

    (3 characters

    Example: 05Z

    Required: Mandatory for RINEX Obs. Data.
    NOT required for Navigation Files.

    XXC - 100 Hertz
    XXZ - HertZ,
    XXS - Seconds,
    XXM - Minutes,
    XXH - Hours,
    XXD - Days
    XXU - Unspecified

    Filename Details and Examples
    -----------------------------

    <DATA FREQ>:

    Used to distinguish between observation files
    that cover the same period but contain data
    at a different sampling rate.

    GNSS data file - observation frequency examples:

        //100 Hz data rate
        ALGO00CAN_R_20121601000_01D_01C_GO.rnx.gz

        //5 Hz data rate
        ALGO00CAN_R_20121601000_01D_05Z_RO.rnx.gz

        //1 second data rate
        ALGO00CAN_R_20121601000_01D_01S_EO.rnx.gz

        //5 minute data rate
        ALGO00CAN_R_20121601000_01D_05M_JO.rnx.gz

        //1 hour data rate
        ALGO00CAN_R_20121601000_01D_01H_CO.rnx.gz

        //1 day data rate
        ALGO00CAN_R_20121601000_01D_01D_SO.rnx.gz

        //Unspecified
        ALGO00CAN_R_20121601000_01D_00U_MO.rnx.gz

    Note : Data frequency field not required for RINEX Navigation files.

    """
    if len(s) != 3:
        return False

    DD: str = s[:2]
    U: str = s[-1:]

    try:
        [int(d) for d in DD]
    except Exception as e:
        return False

    return U in DATA_FREQ_UNITS_ALLOWED


DATA_TYPE_VALID_OBSERVATION_CODES: tuple[str] = (
    'GO',
    'RO',
    'EO',
    'JO',
    'CO',
    'IO',
    'SO',
    'MO',
)


def data_type_is_valid(s: str) -> bool:
    """
    <DATA TYPE >

    DD
    DD - Data type
    (2 characters)

    Example: MO

    Required: Yes

    Two characters represent the data type:
    GO - GPS Obs.,
    RO - GLONASS Obs.,
    EO - Galileo Obs.
    JO - QZSS Obs.
    CO - BDS Obs.
    IO - IRNSS Obs.
    SO - SBAS Obs.
    MO Mixed Obs.

    GN - Nav. GPS,
    RN- GLONASS Nav.,
    EN- Galileo Nav.,
    JN- QZSS Nav.,
    CN- BDS Nav.
    IN - IRNSS Nav.
    SN- SBAS Nav.
    MN- Nav. All GNSS
    Constellations)
    MM-Meteorological Observation
    Etc

    Filename Details and Examples
    -----------------------------

    < DATA TYPE/ FORMAT/>:

    The data type describes the content of the file.

    The first character indicates constellation and
    the second indicates whether the files contains
    observations or navigation data.

    The next three characters indicate the data file format.


    GNSS observation filename - format/data type examples:

        //RINEX obs. GPS
        ALGO00CAN_R_20121601000_15M_01S_GO.rnx.gz

        //RINEX obs. GLONASS
        ALGO00CAN_R_20121601000_15M_01S_RO.rnx.gz

        //RINEX obs. Galileo
        ALGO00CAN_R_20121601000_15M_01S_EO.rnx.gz

        //RINEX obs. QZSS
        ALGO00CAN_R_20121601000_15M_01S_JO.rnx.gz

        //RINEX obs. BDS
        ALGO00CAN_R_20121601000_15M_01S_CO.rnx.gz

        //RINEX obs. SBAS
        ALGO00CAN_R_20121601000_15M_01S_SO.rnx.gz

        //RINEX obs. mixed
        ALGO00CAN_R_20121601000_15M_01S_MO.rnx.gz

    GNSS navigation filename examples:

        //RINEX nav. GPS
        ALGO00CAN_R_20121600000_01H_GN.rnx.gz

        //RINEX nav. GLONASS
        ALGO00CAN_R_20121600000_01H_RN.rnx.gz

        //RINEX nav. Galileo
        ALGO00CAN_R_20121600000_01H_EN.rnx.gz

        //RINEX nav. QZSS
        ALGO00CAN_R_20121600000_01H_JN.rnx.gz

        //RINEX nav. BDS
        ALGO00CAN_R_20121600000_01H_CN.rnx.gz

        //RINEX nav. SBAS
        ALGO00CAN_R_20121600000_01H_SN.rnx.gz

        //RINEX nav. mixed
        ALGO00CAN_R_20121600000_01H_MN.rnx.gz


    Meteorological filename example:

        //RINEX Met.
        ALGO00CAN_R_20121600000_01D_30M_MM.rnx.gz

    Notes
    -----
    Is 'MM' part of the options for observations files?

    """
    if len(s) != 2:
        return False

    return s in DATA_TYPE_VALID_OBSERVATION_CODES


def format_is_valid(s: str) -> bool:
    """
    <FORMAT>

    FFF
    FFF - File format
    (3 characters)

    Example: rnx

    Required: yes

    Three character indicating the data format :
    RINEX - rnx,
    Hatanaka Compressed RINEX -crx,
    ETC

    Filename Details and Examples
    -----------------------------

    Notes
    -----
    The `ETC` above indicates, that the file
    extension is not constricted to the two examples
    given, but could be any three-character combination.

    I guess this means that anything goes.

    Assumptions
    -----------
    Input is already validated as ASCII-characters (upper-case letters).

    """
    return len(s) == 3


COMPRESSION_EXTENSIONS_ALLOWED: tuple[str] = ('gz', 'bz2', 'zip')


def compression_is_valid(s: str) -> bool:
    """
    <COMPRESSION>

    (2-3 Characters)

    Example: gz

    Required: No

    gz

    Filename Details and Examples
    -----------------------------

    Valid compression methods include:

    gzip - “.gz”,
    bzip2 - “.bz2” and
    “.zip”.

    Note: The main body of the file name should
    contain only ASCII capital letters and numbers.

    The file extension .rnx.gz should be lowercase.

    """
    if not len(s):
        # Allowed, since not required.
        return True

    # if not (2 <= len(s) <= 3):
    #     return False

    return s in COMPRESSION_EXTENSIONS_ALLOWED
