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


class CorrectionsReader(csv.DictReader):
    def __next__(self) -> models.CoursePoint:
        if self.line_num == 0:
            self.fieldnames

        row = super().__next__()
        return models.Correction.model_validate(row)
