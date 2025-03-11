from pathlib import Path
import pretty_midi

from musical_containers import Melody
from scad import SCADTrack, SCADHeader, SCADTracks, SCADFile


class MusicBoxBuilder:
    @classmethod
    def from_midi(cls, midi_filepath: Path | str) -> "MusicBoxBuilder":
        midi_content = pretty_midi.PrettyMIDI(str(midi_filepath))
        instrument = midi_content.instruments[0]
        return MusicBoxBuilder(notes=instrument.notes)

    def __init__(self, notes: list[pretty_midi.Note]) -> None:
        self.melody = Melody(notes)
        self.tracks = self.melody.create_tracks()

    def _compile_scad_tracks(self) -> SCADTracks:
        track_names: list[str] = list()
        tracks: list[SCADTrack] = list()

        for pitch, content in self.tracks.items():
            track_name = f"t{pitch}"
            track_names.append(track_name)
            tracks.append(SCADTrack(track_name=track_name, track_content=content))

        return SCADTracks(tracks)

    def build(self) -> SCADFile:
        header = SCADHeader(
            number_of_tracks=len(self.tracks),
            number_of_notes_in_track=self.melody.ticks,
            cylinder_radius__mm=25,
            distance_between_tracks__mm=2,
            offset_of_tracks_from_edge__mm=2,
            bump_radius__mm=1,
            bump_height__mm=1,
        )
        tracks = self._compile_scad_tracks()
        return SCADFile(header, tracks)


if __name__ == "__main__":
    drum = MusicBoxBuilder.from_midi(Path("assets/entertainer.mid"))
    scad_code = drum.build()
    scad_code.to_file("test.scad")
