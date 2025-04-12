import sys
import argparse
import csv
import jinja2

import models


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-o", "--output", dest="dstfile")

    p.add_argument("srcfile")

    return p.parse_args()


def main():
    args = parse_args()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

    with (
        open(args.srcfile) as infd,
        open(args.dstfile, "w") if args.dstfile else sys.stdout as outfd,
    ):
        reader = csv.DictReader(infd)
        locations = [models.CoursePoint(**row) for row in reader]

        tmpl = env.get_template("locations.kml")
        outfd.write(tmpl.render(locations=locations))


if __name__ == "__main__":
    main()
