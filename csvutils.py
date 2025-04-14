import csv
import models


class CoursePointReader(csv.DictReader):
    def __next__(self) -> models.CoursePoint:
        if self.line_num == 0:
            self.fieldnames

        row = super().__next__()
        return models.CoursePoint.model_validate(row)


class GeocodedCoursePointReader(csv.DictReader):
    def __next__(self) -> models.CoursePoint:
        if self.line_num == 0:
            self.fieldnames

        row = super().__next__()
        return models.GeocodedCoursePoint.model_validate(row)


class GeocodedCoursePointWriter(csv.DictWriter):
    def __init__(
        self,
        fd,
    ):
        fieldnames = [*models.GeocodedCoursePoint.model_fields] + [*models.GeocodedCoursePoint.model_computed_fields]
        super().__init__(fd, fieldnames)

    def writerow(self, row):
        if isinstance(row, dict):
            super().writerow(row)
        else:
            super().writerow(row.model_dump())

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class CorrectionsReader(csv.DictReader):
    def __next__(self) -> models.CoursePoint:
        if self.line_num == 0:
            self.fieldnames

        row = super().__next__()
        return models.Correction.model_validate(row)
