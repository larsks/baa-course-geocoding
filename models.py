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


class CoursePoint(BaseModel):
    name: str = pydantic.Field(validation_alias="Tac ID")
    primary_channel: str = pydantic.Field(validation_alias="Pri Chan")
    secondary_channel: str = pydantic.Field(validation_alias="Sec Chan")
    med_channel: str = pydantic.Field(validation_alias="Med Chan")
    med_div: str = pydantic.Field(validation_alias="Med Div")
    mile: str = pydantic.Field(validation_alias="Mile")
    side: str = pydantic.Field(validation_alias="Side")
    address: str = pydantic.Field(validation_alias="Address (ArcGIS Geocodable)")
    cross_street: str = pydantic.Field(validation_alias="Cross Street or Landmark")
    bus_stop: str = pydantic.Field(validation_alias="Approximate Bus Stop Location")
    bus_side: str = pydantic.Field(validation_alias="Bus Side")
    kind: LocationKind | None = None
    desc: str | None = None
    lat: float | None = None
    lon: float | None = None

    @pydantic.model_validator(mode="after")
    def validate_kind(self) -> Self:
        if self.kind is None:
            self.kind = LocationKind.from_tacid(self.name)

        return self
