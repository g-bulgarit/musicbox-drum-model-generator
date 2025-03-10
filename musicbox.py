from dataclasses import dataclass
from pathlib import Path
import pretty_midi


midi_file = Path("assets/test.mid")
midi_content = pretty_midi.PrettyMIDI(str(midi_file))
instrument = midi_content.instruments[0]

notes = midi_content.instruments[0].notes


@dataclass
class NoteRange:
    min_pitch: int
    max_pitch: int

    def in_semitones(self) -> int:
        return self.max_pitch - self.min_pitch


def get_midi_file_length__sec(notes: list[pretty_midi.Note]) -> float:
    return notes[-1].end


def get_string_representation_from_notes(notes: list[pretty_midi.Note]) -> list[str]:
    return [pretty_midi.utilities.note_number_to_name(note.pitch) for note in notes]


def get_note_range(notes: list[pretty_midi.Note]) -> NoteRange:
    min_pitch = min(notes, key=lambda note: note.pitch).pitch
    max_pitch = max(notes, key=lambda note: note.pitch).pitch
    return NoteRange(min_pitch, max_pitch)


length__sec = get_midi_file_length__sec(notes)
print(length__sec)
notes_list = get_string_representation_from_notes(notes)
print(notes_list)

print(get_note_range(notes).in_semitones())


@dataclass
class SCADHeader:
    number_of_tracks: int
    number_of_notes_in_track: int

    cylinder_radius__mm: float
    cylinder_height__mm: float
    distance_between_tracks__mm: float
    offset_of_tracks_from_edge__mm: float

    bump_radius__mm: float
    bump_height__mm: float

    def __str__(self) -> str:
        return f"""
        TRACK_LENGTH = {self.number_of_notes_in_track};
        NUM_TRACKS = {self.number_of_tracks};
        CYLINDER_RADIUS = {self.cylinder_radius__mm};
        CYLINDER_HEIGHT = {self.cylinder_height__mm};
        PROTRUSION_RADIUS = {self.bump_radius__mm};
        PROTRUSION_HEIGHT = {self.bump_height__mm};
        TRACK_TO_TRACK_DISTANCE = {self.distance_between_tracks__mm};
        EDGE_OFFSET = {self.offset_of_tracks_from_edge__mm};
        """
