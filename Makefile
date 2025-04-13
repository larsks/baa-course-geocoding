all: course_locations_geocoded.gpx course_locations_geocoded.kml

course_locations_geocoded.corrected.csv: course_locations_geocoded.csv corrections.csv
	uv run apply_corrections.py -o $@ $< corrections.csv

course_locations_geocoded.gpx: course_locations_geocoded.corrected.csv
	gpsbabel -i unicsv -f $< -o gpx -F $@

course_locations_geocoded.kml: course_locations_geocoded.corrected.csv csv2kml.py templates/locations.kml
	uv run csv2kml.py $< -o $@

clean:
	rm -f course_locations_geocoded.gpx course_locations_geocoded.kml course_locations_geocoded.corrected.csv
