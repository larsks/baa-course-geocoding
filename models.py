import pydantic


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
