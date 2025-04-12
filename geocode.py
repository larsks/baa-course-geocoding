import sys
import time
import argparse
import os
import googlemaps
import csv

import models

field_map = {
    "Tac ID": "name",
    "Pri Chan": "primary_channel",
    "Sec Chan": "secondary_channel",
    "Med Chan": "med_channel",
    "Med Div": "med_div",
    "Mile": "mile",
    "Side": "side",
    "Column 08": "",
    "Address (ArcGIS Geocodable)": "address",
    "Cross Street or Landmark": "cross_street",
    "Approximate Bus Stop Location": "bus_stop",
    "Bus Side": "bus_side",
}

geocode_fields = ["desc", "lat", "lon"]


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-o", "--output", dest="dstfile")

    p.add_argument("srcfile")

    return p.parse_args()


def main():
    gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

    args = parse_args()

    with (
        open(args.srcfile) as infd,
        open(args.dstfile, "w") if args.dstfile else sys.stdout as outfd,
    ):
        reader = csv.DictReader(infd)
        writer = csv.DictWriter(outfd, [*models.CoursePoint.model_fields])
        writer.writeheader()
        for row in reader:
            newrow = models.CoursePoint.model_validate(row)
            print(f"location: {newrow.name}")

            try:
                res = gmaps.geocode(newrow.address)
                loc = models.GeocodeResponseList.model_validate(res)[0]
            except Exception as err:
                breakpoint()
                pass
            newrow.desc = loc.formatted_address
            newrow.lat = loc.geometry.location.lat
            newrow.lon = loc.geometry.location.lng

            writer.writerow(newrow.model_dump())
            time.sleep(0.1)


if __name__ == "__main__":
    main()
