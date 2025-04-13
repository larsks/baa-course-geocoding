%.gpx: %.csv
	gpsbabel -i unicsv -f $< -o gpx -F $@

%.kml: %.csv csv2kml.py templates/locations.kml
	uv run csv2kml.py $< -o $@

all: course_locations_geocoded.gpx course_locations_geocoded.kml

clean:
	rm -f course_locations_geocoded.gpx course_locations_geocoded.kml
