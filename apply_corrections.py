import argparse
import csv
import logging
import os
import sys
import time

import models

LOG = logging.getLogger(__name__)


class GeocodedCoursePointReader(csv.DictReader):
    def __next__(self) -> models.CoursePoint:
        if self.line_num == 0:
            self.fieldnames

        row = super().__next__()
        return models.GeocodedCoursePoint.model_validate(row)


class CorrectionsReader(csv.DictReader):
    def __next__(self) -> models.CoursePoint:
        if self.line_num == 0:
            self.fieldnames

        row = super().__next__()
        return models.Correction.model_validate(row)


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-o", "--output", dest="dstfile")
    p.add_argument("-v", "--verbose", action="count", default=0)

    p.add_argument("srcfile")
    p.add_argument("corrections")

    return p.parse_args()


def main():
    args = parse_args()

    loglevel = ["WARNING", "INFO", "DEBUG"][min(3, args.verbose)]
    logging.basicConfig(level=loglevel)

    with open(args.corrections) as fd:
        reader = CorrectionsReader(fd)
        corrections = {row.name: row for row in reader}

    with (
        open(args.srcfile) as infd,
        open(args.dstfile, "w") if args.dstfile else sys.stdout as outfd,
    ):
        reader = GeocodedCoursePointReader(infd)
        writer = csv.DictWriter(outfd, [*models.GeocodedCoursePoint.model_fields])
        writer.writeheader()
        for row in reader:
            LOG.debug(f"processing {row.name} ({row.address})")

            if row.name in corrections:
                row.lat = corrections[row.name].lat
                row.lon = corrections[row.name].lon

            writer.writerow(row.model_dump())


if __name__ == "__main__":
    main()
