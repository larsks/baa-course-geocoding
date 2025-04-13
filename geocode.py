import argparse
import csv
import logging
import os
import sys
import time

import googlemaps

import models
from readers import CoursePointReader

LOG = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-o", "--output", dest="dstfile")
    p.add_argument("-v", "--verbose", action="count", default=0)

    p.add_argument("srcfile")

    return p.parse_args()


def main():
    args = parse_args()

    loglevel = ["WARNING", "INFO", "DEBUG"][min(3, args.verbose)]
    logging.basicConfig(level=loglevel)
    gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

    with (
        open(args.srcfile) as infd,
        open(args.dstfile, "w") if args.dstfile else sys.stdout as outfd,
    ):
        reader = CoursePointReader(infd)
        writer = csv.DictWriter(outfd, [*models.GeocodedCoursePoint.model_fields] + [*models.GeocodedCoursePoint.model_computed_fields])
        writer.writeheader()
        for row in reader:
            LOG.debug(f"processing {row.name} ({row.address})")

            try:
                res = gmaps.geocode(row.address)
                loc = models.GeocodeResponseList.model_validate(res)[0]
            except Exception as err:
                LOG.warning(f'failed to decode "{row.address}": {err}')
                continue

            newrow = models.GeocodedCoursePoint(
                **row.model_dump(),
                formatted_address=loc.formatted_address,
                lat=loc.geometry.location.lat,
                lon=loc.geometry.location.lng,
            )

            writer.writerow(newrow.model_dump())
            time.sleep(0.1)


if __name__ == "__main__":
    main()
