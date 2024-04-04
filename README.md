# [rinex](https://github.com/xidus/rinex)

-- by [Joachim](https://github.com/xidus)


Package made for job-application case.

**Task**

Write a program that checks the following:

*   ŔINEX filenames are named correctly according to the RINEX3 standard.
*   The files are placed in the correct directory.

Program output is a report that identifies files named incorrectly or placed incorrectly.


**My solution**


This package and the following script that works on a given directory of files
for the case (not included).

```python
import os
import pathlib

import pandas as pd

from rinex.observationfile import ObservationFile


def location_expected(fname: str) -> tuple[str]:
    rfn = ObservationFile(pathlib.Path(fname).name)
    yyyydddhhmm = rfn.start_time
    yyyy = yyyydddhhmm[:4]
    ddd = yyyydddhhmm[4:7]
    return (yyyy, ddd)


def main() -> None:
    ipath = pathlib.Path('GNSS')
    fnames = [
        pathlib.PurePath(path, fname)
        for (path, _subdirs, fnames) in os.walk(ipath)
        for fname in fnames
    ]
    data = [
        (
            fname,
            ObservationFile(fname.name).is_valid(),
            fname.parts[-3:-1] == location_expected(fname.name),
        )
        for fname in fnames
    ]

    columns = [
        'fname',
        'valid_rinex3',
        'correct_path',
    ]
    df = pd.DataFrame(data=data, columns=columns)

    okw = dict(sep=';', index=False)
    df[df.valid_rinex3 == False].to_csv('invalid_rinex3.csv', **okw)
    df[df.correct_path == False].to_csv('incorrect_path.csv', **okw)


if __name__ == '__main__':
    main()
```

