import pretty_midi
import numpy as np


class Melody:
    def __init__(self, note_array: list[pretty_midi.Note]) -> None:
        self.note_array = note_array

    @property
    def shortest_note_duration(self) -> float:
        shortest_note = min(self.note_array, key=lambda note: note.duration)
        return shortest_note.duration

    @property
    def ticks(self) -> int:
        last_note_in_midi_file = max(self.note_array, key=lambda note: note.end)
        return int(last_note_in_midi_file.end / self.shortest_note_duration)

    @property
    def distinct_pitches(self) -> list[int]:
        return sorted(set(note.pitch for note in self.note_array))

    def create_tracks(self) -> dict[int, list]:
        arrays: dict[int, list] = dict()
        for pitch in self.distinct_pitches:
            relevant_ticks = [
                self._get_note_start_tick(note)
                for note in self.note_array
                if note.pitch == pitch
            ]
            bump_map = self._create_track_bump_map(relevant_ticks)
            arrays[pitch] = bump_map
        return arrays

    def _get_note_start_tick(self, note: pretty_midi.Note) -> int:
        return int(note.start / self.shortest_note_duration)

    def _create_track_bump_map(self, tick_positions: list[int]) -> list[int]:
        bump_map = np.zeros(self.ticks, dtype=int)
        bump_map[tick_positions] = 1
        return bump_map.astype(int).tolist()
