import pydantic
from enum import StrEnum
from typing import Self


class BaseModel(pydantic.BaseModel):
    pass


class Point(BaseModel):
    lat: float
    lng: float


class Geometry(BaseModel):
    bounds: dict[str, Point] | None = None
    location: Point
    location_type: str


class GeocodeResponse(BaseModel):
    formatted_address: str
    geometry: Geometry
    place_id: str
    types: list[str]


class GeocodeResponseList(pydantic.RootModel):
    root: list[GeocodeResponse]

    def __getitem__(self, i):
        return self.root[i]


class LocationKind(StrEnum):
    MED = "Medical"
    HYD = "Hydration"
    TRN = "Transit"

    @classmethod
    def from_tacid(cls, v):
        return {
            "H": cls.HYD,
            "M": cls.MED,
            "P": cls.TRN,
        }[v[0]]


class Side(StrEnum):
    RIGHT = "R"
    LEFT = "L"
    UNKNOWN = ""


class MedDiv(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class CoursePoint(BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    name: str = pydantic.Field(validation_alias="Tac ID")
    primary_channel: str = pydantic.Field(validation_alias="Pri Chan")
    secondary_channel: str = pydantic.Field(validation_alias="Sec Chan")
    med_channel: str = pydantic.Field(validation_alias="Med Chan")
    med_div: MedDiv = pydantic.Field(validation_alias="Med Div")
    mile: float = pydantic.Field(validation_alias="Mile")
    side: Side = pydantic.Field(validation_alias="Side")
    address: str = pydantic.Field(validation_alias="Address (ArcGIS Geocodable)")
    desc: str = pydantic.Field(validation_alias="Cross Street or Landmark")
    bus_stop: str = pydantic.Field(validation_alias="Approximate Bus Stop Location")
    bus_side: Side = pydantic.Field(validation_alias="Bus Side")


class GeocodedCoursePoint(CoursePoint):
    kind: LocationKind | None = None
    formatted_address: str
    lat: float
    lon: float

    @pydantic.model_validator(mode="after")
    def validate_kind(self) -> Self:
        if self.kind is None:
            self.kind = LocationKind.from_tacid(self.name)

        return self
