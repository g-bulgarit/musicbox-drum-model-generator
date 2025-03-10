import pretty_midi
import numpy as np

DEFAULT_TICK_LENGTH__SEC = 0.5


class TickNote:
    def __init__(self, note: pretty_midi.Note, start_tick: int) -> None:
        self.pitch = note.pitch
        self.start_tick = start_tick
        self.note = note

    def __repr__(self) -> str:
        return f"{self.pitch} ({self.start_tick})"

    @classmethod
    def from_note(
        cls, note: pretty_midi.Note, tick_length__sec: float = DEFAULT_TICK_LENGTH__SEC
    ) -> "TickNote":
        tick = int(note.start / tick_length__sec)
        return TickNote(note, start_tick=tick)


class Melody:
    def __init__(self, note_array: list[TickNote]) -> None:
        self.note_array = note_array

    @property
    def ticks(self) -> int:
        last_end_time = max(self.note_array, key=lambda e: e.note.end).note.end
        return int(last_end_time / DEFAULT_TICK_LENGTH__SEC)

    @property
    def distinct_pitches(self) -> list[int]:
        return sorted(set(note.pitch for note in self.note_array))

    def create_tracks(self) -> dict[int, list]:
        arrays: dict[int, list] = dict()
        for pitch in self.distinct_pitches:
            relevant_ticks = [
                note.start_tick for note in self.note_array if note.pitch == pitch
            ]
            arr = np.zeros(self.ticks, dtype=int)
            for tick in relevant_ticks:
                arr[tick] = 1
            arrays[pitch] = arr.tolist()
        return arrays
