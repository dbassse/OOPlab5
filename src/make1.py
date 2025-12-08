from task_package.zad1 import MusicCatalog, Track


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
