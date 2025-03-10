from dataclasses import dataclass
from pathlib import Path
import pretty_midi
import numpy as np
from scad import SCADTrack, SCADHeader, SCADFile, SCADTracks


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

DEFAULT_TICK_LENGTH__SEC = 0.5


class TickNote:
    def __init__(self, note: pretty_midi.Note, start_tick: int) -> None:
        self.pitch = note.pitch
        self.start_tick = start_tick

    def __repr__(self) -> str:
        return f"{self.pitch} ({self.start_tick})"

    @classmethod
    def from_note(
        cls, note: pretty_midi.Note, tick_length__sec: float = DEFAULT_TICK_LENGTH__SEC
    ) -> "TickNote":
        tick = int(note.start / tick_length__sec)
        return TickNote(note, start_tick=tick)


class Melody:
    def __init__(self, note_array: list[TickNote], ticks: int) -> None:
        self.note_array = note_array
        self.ticks = ticks
        self.distinct_pitches = self.get_distinct_pitches()

    def get_distinct_pitches(self) -> list[int]:
        return sorted(set(note.pitch for note in self.note_array))

    def create_tracks(self) -> dict[int, list]:
        arrays: dict[int, list] = dict()
        for pitch in self.get_distinct_pitches():
            relevant_ticks = [
                note.start_tick for note in self.note_array if note.pitch == pitch
            ]
            arr = np.zeros(ticks, dtype=int)
            for tick in relevant_ticks:
                arr[tick] = 1
            arrays[pitch] = arr.tolist()
        return arrays


ticks = int(length__sec / DEFAULT_TICK_LENGTH__SEC)

tick_notes = [TickNote.from_note(note) for note in notes]
mel = Melody(tick_notes, ticks)
arrs = mel.create_tracks()

track_names: list[str] = list()
tracks: list[SCADTrack] = list()

for pitch, content in arrs.items():
    track_name = f"t{pitch}"
    track_names.append(track_name)
    tracks.append(SCADTrack(track_name=track_name, track_content=content))

scad_tracks = SCADTracks(tracks)

header = SCADHeader(
    number_of_tracks=len(tracks),
    number_of_notes_in_track=ticks,
    cylinder_radius__mm=25,
    cylinder_height__mm=40,
    distance_between_tracks__mm=2,
    offset_of_tracks_from_edge__mm=2,
    bump_radius__mm=1,
    bump_height__mm=1,
)

SCADFile(header, scad_tracks).to_file("output2.scad")
