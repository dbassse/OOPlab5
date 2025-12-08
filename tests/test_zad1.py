import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from task_package.zad1 import MusicCatalog, Track  # noqa: E402


class TestTrack:
    """Тесты для класса Track"""

    def test_track_creation(self):
        """Проверка создания трека"""
        track = Track("Test Song", "Test Artist", 180)

        assert track.title == "Test Song"
        assert track.artist == "Test Artist"
        assert track.duration_sec == 180

    def test_duration_formatted_seconds_only(self):
        """Проверка форматирования длительности (только секунды)"""
        track = Track("Song", "Artist", 45)
        assert track.duration_formatted == "0:45"

    def test_duration_formatted_minutes_and_seconds(self):
        """Проверка форматирования длительности (минуты и секунды)"""
        track = Track("Song", "Artist", 125)
        assert track.duration_formatted == "2:05"

    def test_duration_formatted_long_track(self):
        """Проверка форматирования длительной композиции"""
        track = Track("Long Song", "Artist", 1255)
        assert track.duration_formatted == "20:55"

    @pytest.mark.parametrize(
        "seconds,expected",
        [
            (0, "0:00"),
            (59, "0:59"),
            (60, "1:00"),
            (119, "1:59"),
            (600, "10:00"),
            (3599, "59:59"),
        ],
    )
    def test_duration_formatted_parametrized(self, seconds: int, expected: str):
        """Параметризованный тест для форматирования длительности"""
        track = Track("Song", "Artist", seconds)
        assert track.duration_formatted == expected


class TestMusicCatalog:
    """Тесты для класса MusicCatalog"""

    @pytest.fixture
    def sample_catalog(self) -> MusicCatalog:
        """Фикстура с тестовым каталогом"""
        catalog = MusicCatalog()
        catalog.add_track(Track("Song 1", "Artist A", 120))  # 2:00
        catalog.add_track(Track("Song 2", "Artist B", 240))  # 4:00
        catalog.add_track(Track("Song 3", "Artist A", 90))  # 1:30
        catalog.add_track(Track("Song 4", "Artist C", 300))  # 5:00
        catalog.add_track(Track("Song 5", "Artist A", 150))  # 2:30
        return catalog

    def test_catalog_creation_empty(self):
        """Проверка создания пустого каталога"""
        catalog = MusicCatalog()
        assert len(catalog.tracks) == 0
        assert catalog.tracks == []

    def test_add_track(self, sample_catalog: MusicCatalog):
        """Проверка добавления трека в каталог"""
        initial_count = len(sample_catalog.tracks)
        new_track = Track("New Song", "New Artist", 180)

        sample_catalog.add_track(new_track)

        assert len(sample_catalog.tracks) == initial_count + 1
        assert sample_catalog.tracks[-1] == new_track

    def test_get_tracks_shorter_than_empty_catalog(self):
        """Проверка фильтрации по длительности в пустом каталоге"""
        catalog = MusicCatalog()
        result = catalog.get_tracks_shorter_than(5)
        assert result == []

    def test_get_tracks_shorter_than_boundary(self, sample_catalog: MusicCatalog):
        """Проверка фильтрации по длительности (граничное значение)"""
        # Треки короче 3 минут (180 секунд)
        result = sample_catalog.get_tracks_shorter_than(3)

        assert len(result) == 3
        # Проверяем, что все треки действительно короче 180 секунд
        for track in result:
            assert track.duration_sec < 180

        # Проверяем конкретные треки
        titles = [track.title for track in result]
        assert "Song 1" in titles  # 120 сек
        assert "Song 3" in titles  # 90 сек
        assert "Song 5" in titles  # 150 сек
        assert "Song 2" not in titles  # 240 сек > 180
        assert "Song 4" not in titles  # 300 сек > 180

    def test_get_tracks_shorter_than_zero_minutes(self, sample_catalog: MusicCatalog):
        """Проверка фильтрации с нулевой длительностью"""
        result = sample_catalog.get_tracks_shorter_than(0)
        assert result == []

    def test_get_tracks_by_artist_existing(self, sample_catalog: MusicCatalog):
        """Проверка поиска по существующему исполнителю"""
        result = sample_catalog.get_tracks_by_artist("Artist A")

        assert len(result) == 3
        for track in result:
            assert track.artist.lower() == "artist a"

        titles = [track.title for track in result]
        assert "Song 1" in titles
        assert "Song 3" in titles
        assert "Song 5" in titles

    def test_get_tracks_by_artist_case_insensitive(self, sample_catalog: MusicCatalog):
        """Проверка регистронезависимого поиска"""
        result_lower = sample_catalog.get_tracks_by_artist("artist a")
        result_upper = sample_catalog.get_tracks_by_artist("ARTIST A")
        result_mixed = sample_catalog.get_tracks_by_artist("ArTiSt A")

        assert len(result_lower) == len(result_upper) == len(result_mixed) == 3

    def test_get_tracks_by_artist_non_existing(self, sample_catalog: MusicCatalog):
        """Проверка поиска по несуществующему исполнителю"""
        result = sample_catalog.get_tracks_by_artist("Non Existing Artist")
        assert result == []

    def test_catalog_immutability(self, sample_catalog: MusicCatalog):
        """Проверка, что методы не изменяют исходный список"""
        original_tracks = sample_catalog.tracks.copy()
        original_count = len(original_tracks)

        # Вызываем методы, которые не должны изменять каталог
        sample_catalog.get_tracks_shorter_than(3)
        sample_catalog.get_tracks_by_artist("Artist A")

        # Проверяем, что каталог не изменился
        assert len(sample_catalog.tracks) == original_count
        assert sample_catalog.tracks == original_tracks
