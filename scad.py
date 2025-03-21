from dataclasses import dataclass, field
from pathlib import Path

SCAD_FILE_CONTENT = Path("music_box.scad").read_text()


@dataclass
class SCADHeader:
    number_of_tracks: int
    number_of_notes_in_track: int

    cylinder_radius__mm: float
    inner_cylinder_radius__mm: float
    cylinder_height__mm: float = field(init=False)
    inner_cylinder_height__mm: float = field(init=False)
    distance_between_tracks__mm: float
    offset_of_tracks_from_edge__mm: float

    bump_radius__mm: float
    bump_height__mm: float

    number_of_drawing_fragments: int = 128

    def __post_init__(self) -> None:
        self.cylinder_height__mm = self.number_of_tracks * (
            self.distance_between_tracks__mm + (self.bump_radius__mm * 2)
        ) + (self.offset_of_tracks_from_edge__mm * 2)
        self.inner_cylinder_height__mm = self.cylinder_height__mm * 2

    def __str__(self) -> str:
        return f"""
$fn={self.number_of_drawing_fragments};
TRACK_LENGTH = {self.number_of_notes_in_track};
NUM_TRACKS = {self.number_of_tracks};
CYLINDER_RADIUS = {self.cylinder_radius__mm};
INNER_CYLINDER_RADIUS = {self.inner_cylinder_radius__mm};
CYLINDER_HEIGHT = {self.cylinder_height__mm};
INNER_CYLINDER_HEIGHT = {self.inner_cylinder_height__mm};
PROTRUSION_RADIUS = {self.bump_radius__mm};
PROTRUSION_HEIGHT = {self.bump_height__mm};
TRACK_TO_TRACK_DISTANCE = {self.distance_between_tracks__mm};
EDGE_OFFSET = {self.offset_of_tracks_from_edge__mm};\n
"""


@dataclass
class SCADTrack:
    track_name: str
    track_content: list[int]

    def __str__(self) -> str:
        return f"{self.track_name} = {self.track_content};\n"


@dataclass
class SCADTracks:
    tracks: list[SCADTrack]

    def __str__(self) -> str:
        output: str = ""
        for track in self.tracks:
            output += str(track)

        output += (
            f"TRACKS = [{', '.join([track.track_name for track in self.tracks])}];\n"
        )
        return output


@dataclass
class SCADFile:
    header: SCADHeader
    tracks: SCADTracks
    content: str = SCAD_FILE_CONTENT

    def to_file(self, filepath: Path | str):
        with Path(filepath).open("w+") as output_file:
            output_file.write(str(self.header))
            output_file.write(str(self.tracks))
            output_file.write(self.content)
