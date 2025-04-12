%.gpx: %.csv csv2kml.py
	gpsbabel -i unicsv -f $< -o gpx -F $@

%.kml: %.csv
	uv run csv2kml.py $< -o $@

all: course_locations_geocoded.gpx course_locations_geocoded.kml
