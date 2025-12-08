from dataclasses import dataclass, field
from typing import List


# 1. Датакласс для трека
@dataclass
class Track:
    title: str
    artist: str
    duration_sec: int  # длительность в секундах

    @property
    def duration_formatted(self) -> str:
        """Возвращает длительность в формате ММ:СС"""
        minutes = self.duration_sec // 60
        seconds = self.duration_sec % 60
        return f"{minutes}:{seconds:02d}"


# 2. Контейнер для хранения треков
@dataclass
class MusicCatalog:
    tracks: List[Track] = field(default_factory=list)

    def add_track(self, track: Track) -> None:
        """Добавление трека в каталог"""
        self.tracks.append(track)

    def get_tracks_shorter_than(self, max_minutes: int) -> List[Track]:
        """Получение треков короче указанного количества минут"""
        max_seconds = max_minutes * 60
        return [track for track in self.tracks if track.duration_sec < max_seconds]

    def get_tracks_by_artist(self, artist: str) -> List[Track]:
        """Получение треков конкретного исполнителя"""
        return [
            track for track in self.tracks if track.artist.lower() == artist.lower()
        ]


# 3. Демонстрация работы
def main() -> None:
    # Создаем каталог
    catalog = MusicCatalog()

    # Добавляем треки
    catalog.add_track(Track("Bohemian Rhapsody", "Queen", 354))
    catalog.add_track(Track("Stairway to Heaven", "Led Zeppelin", 482))
    catalog.add_track(Track("Yesterday", "The Beatles", 125))
    catalog.add_track(Track("Smells Like Teen Spirit", "Nirvana", 301))
    catalog.add_track(Track("Blinding Lights", "The Weeknd", 200))
    catalog.add_track(Track("Take Five", "Dave Brubeck", 175))

    print("Все треки в каталоге:")
    for i, track in enumerate(catalog.tracks, 1):
        print(f"{i}. {track.artist} - {track.title} ({track.duration_formatted})")

    print("\nТреки короче 3 минут (180 секунд):")
    short_tracks = catalog.get_tracks_shorter_than(3)

    if short_tracks:
        for i, track in enumerate(short_tracks, 1):
            print(f"{i}. {track.artist} - {track.title} ({track.duration_formatted})")
    else:
        print("Таких треков нет")

    # Дополнительная демонстрация: поиск по исполнителю
    print("\nТреки The Beatles:")
    beatles_tracks = catalog.get_tracks_by_artist("The Beatles")
    for track in beatles_tracks:
        print(f"- {track.title} ({track.duration_formatted})")


if __name__ == "__main__":
    main()
