import os
import sys
from typing import List, Optional

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from task_package.zad2 import RingBuffer  # noqa: E402


class TestRingBuffer:
    """Тесты для класса RingBuffer"""

    # Основные тесты для целых чисел
    def test_buffer_creation_default_capacity(self) -> None:
        """Проверка создания буфера с емкостью по умолчанию"""
        buffer: RingBuffer[int] = RingBuffer[int]()
        assert buffer.capacity == 10
        assert len(buffer) == 0
        assert buffer.is_empty() is True
        assert buffer.is_full() is False

    def test_buffer_creation_custom_capacity(self) -> None:
        """Проверка создания буфера с заданной емкостью"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=5)
        assert buffer.capacity == 5
        assert len(buffer) == 0
        assert buffer.is_empty() is True
        assert buffer.is_full() is False

    def test_buffer_creation_invalid_capacity(self) -> None:
        """Проверка создания буфера с некорректной емкостью"""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            RingBuffer[int](capacity=0)

        with pytest.raises(ValueError, match="Capacity must be positive"):
            RingBuffer[int](capacity=-1)

    def test_push_and_len(self) -> None:
        """Проверка добавления элементов и определения длины"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)

        buffer.push(1)
        assert len(buffer) == 1
        assert buffer.is_empty() is False

        buffer.push(2)
        assert len(buffer) == 2

        buffer.push(3)
        assert len(buffer) == 3
        assert buffer.is_full() is True

    def test_push_overflow(self) -> None:
        """Проверка переполнения буфера (замены старых элементов)"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)

        buffer.push(1)
        buffer.push(2)
        buffer.push(3)
        assert buffer.get_all() == [1, 2, 3]

        # Добавляем четвертый элемент - должен заменить первый
        buffer.push(4)
        assert buffer.get_all() == [2, 3, 4]
        assert buffer.is_full() is True

        # Добавляем пятый элемент - должен заменить второй
        buffer.push(5)
        assert buffer.get_all() == [3, 4, 5]

    def test_pop_empty(self) -> None:
        """Проверка извлечения из пустого буфера"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)
        assert buffer.pop() is None

    def test_pop_normal(self) -> None:
        """Проверка извлечения элементов в правильном порядке"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)

        buffer.push(1)
        buffer.push(2)
        buffer.push(3)

        assert buffer.pop() == 1
        assert len(buffer) == 2
        assert buffer.get_all() == [2, 3]

        assert buffer.pop() == 2
        assert len(buffer) == 1
        assert buffer.get_all() == [3]

        assert buffer.pop() == 3
        assert len(buffer) == 0
        assert buffer.is_empty() is True
        assert buffer.pop() is None

    def test_pop_after_overflow(self) -> None:
        """Проверка извлечения после переполнения"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)

        buffer.push(1)
        buffer.push(2)
        buffer.push(3)
        buffer.push(4)  # Вытесняет 1
        buffer.push(5)  # Вытесняет 2

        assert buffer.pop() == 3  # Самый старый из оставшихся
        assert buffer.pop() == 4
        assert buffer.pop() == 5
        assert buffer.pop() is None

    def test_peek(self) -> None:
        """Проверка просмотра элемента без извлечения"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)

        assert buffer.peek() is None

        buffer.push(10)
        assert buffer.peek() == 10
        assert len(buffer) == 1  # Длина не изменилась

        buffer.push(20)
        assert buffer.peek() == 10  # Все еще первый элемент

        buffer.pop()
        assert buffer.peek() == 20

    def test_is_full(self) -> None:
        """Проверка определения заполненности буфера"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=2)

        assert buffer.is_full() is False

        buffer.push(1)
        assert buffer.is_full() is False

        buffer.push(2)
        assert buffer.is_full() is True

        buffer.pop()
        assert buffer.is_full() is False

        buffer.push(3)
        assert buffer.is_full() is True

    def test_clear(self) -> None:
        """Проверка очистки буфера"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=5)

        buffer.push(1)
        buffer.push(2)
        buffer.push(3)
        assert len(buffer) == 3

        buffer.clear()
        assert len(buffer) == 0
        assert buffer.is_empty() is True
        assert buffer.get_all() == []
        assert buffer.pop() is None
        assert buffer.peek() is None

    def test_get_all(self) -> None:
        """Проверка получения всех элементов"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=4)

        assert buffer.get_all() == []

        buffer.push(10)
        buffer.push(20)
        buffer.push(30)
        assert buffer.get_all() == [10, 20, 30]

        buffer.push(40)
        buffer.push(50)  # Вытесняет 10
        assert buffer.get_all() == [20, 30, 40, 50]

    def test_contains_operator(self) -> None:
        """Проверка оператора in"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)

        buffer.push(1)
        buffer.push(2)
        buffer.push(3)

        assert 1 in buffer
        assert 2 in buffer
        assert 3 in buffer
        assert 4 not in buffer

        buffer.push(4)  # Вытесняет 1
        assert 1 not in buffer
        assert 4 in buffer

    def test_str_representation(self) -> None:
        """Проверка строкового представления"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)

        assert str(buffer) == "RingBuffer(capacity=3, size=0, items=[])"

        buffer.push(100)
        assert str(buffer) == "RingBuffer(capacity=3, size=1, items=[100])"

        buffer.push(200)
        buffer.push(300)
        assert str(buffer) == "RingBuffer(capacity=3, size=3, items=[100, 200, 300])"

    # Параметризованные тесты
    @pytest.mark.parametrize(
        "capacity,items_to_push",
        [
            (1, [1]),
            (2, [1, 2]),
            (5, list(range(10))),  # 10 элементов в буфер емкостью 5
            (10, list(range(100))),  # 100 элементов в буфер емкостью 10
        ],
    )
    def test_buffer_capacity_parametrized(
        self, capacity: int, items_to_push: List[int]
    ) -> None:
        """Параметризованный тест для разных емкостей"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=capacity)

        for item in items_to_push:
            buffer.push(item)

        # После всех добавлений буфер должен быть полным
        assert buffer.is_full() is True
        assert len(buffer) == capacity

        # Последние capacity элементов должны быть в буфере
        expected_items = items_to_push[-capacity:]
        assert buffer.get_all() == expected_items


class TestRingBufferGenerics:
    """Тесты для проверки работы с разными типами данных"""

    def test_string_buffer(self) -> None:
        """Проверка буфера строк"""
        buffer: RingBuffer[str] = RingBuffer[str](capacity=2)

        buffer.push("hello")
        buffer.push("world")
        assert buffer.get_all() == ["hello", "world"]

        buffer.push("test")  # Вытесняет "hello"
        assert buffer.get_all() == ["world", "test"]
        assert "hello" not in buffer
        assert "world" in buffer

    def test_float_buffer(self) -> None:
        """Проверка буфера чисел с плавающей точкой"""
        buffer: RingBuffer[float] = RingBuffer[float](capacity=3)

        buffer.push(1.5)
        buffer.push(2.7)
        buffer.push(3.9)

        assert buffer.pop() == pytest.approx(1.5)
        assert buffer.peek() == pytest.approx(2.7)

    def test_none_values(self) -> None:
        """Проверка буфера с None значениями"""
        buffer: RingBuffer[Optional[int]] = RingBuffer[Optional[int]](capacity=3)

        buffer.push(1)
        buffer.push(None)
        buffer.push(3)

        assert buffer.get_all() == [1, None, 3]
        assert None in buffer
        assert buffer.pop() == 1
        assert buffer.pop() is None
        assert buffer.pop() == 3


class TestRingBufferEdgeCases:
    """Тесты для граничных случаев"""

    def test_single_element_buffer(self) -> None:
        """Проверка буфера емкостью 1"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=1)

        assert buffer.is_empty() is True
        assert buffer.is_full() is False

        buffer.push(100)
        assert buffer.is_empty() is False
        assert buffer.is_full() is True
        assert buffer.get_all() == [100]

        buffer.push(200)  # Вытесняет 100
        assert buffer.get_all() == [200]

        assert buffer.pop() == 200
        assert buffer.is_empty() is True

    def test_large_capacity(self) -> None:
        """Проверка буфера с большой емкостью"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=1000)

        for i in range(1500):
            buffer.push(i)

        # Последние 1000 элементов
        expected = list(range(500, 1500))
        assert buffer.get_all() == expected
        assert buffer.is_full() is True

    def test_clear_and_reuse(self) -> None:
        """Проверка очистки и повторного использования буфера"""
        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)

        # Первое использование
        buffer.push(1)
        buffer.push(2)
        buffer.push(3)
        assert buffer.is_full() is True

        # Очистка
        buffer.clear()
        assert buffer.is_empty() is True

        # Повторное использование
        buffer.push(10)
        buffer.push(20)
        assert buffer.get_all() == [10, 20]
        assert buffer.is_full() is False


# Интеграционные тесты
def test_integration_scenario() -> None:
    """Интеграционный тест полного сценария использования"""
    buffer: RingBuffer[str] = RingBuffer[str](capacity=4)

    # Этап 1: Наполнение
    for word in ["first", "second", "third", "fourth"]:
        buffer.push(word)

    assert buffer.is_full() is True
    assert buffer.get_all() == ["first", "second", "third", "fourth"]

    # Этап 2: Переполнение с заменой
    buffer.push("fifth")
    assert buffer.get_all() == ["second", "third", "fourth", "fifth"]
    assert "first" not in buffer
    assert "fifth" in buffer

    # Этап 3: Извлечение
    assert buffer.pop() == "second"
    assert buffer.peek() == "third"
    assert len(buffer) == 3

    # Этап 4: Добавление после извлечения
    buffer.push("sixth")
    buffer.push("seventh")
    assert buffer.get_all() == ["fourth", "fifth", "sixth", "seventh"]

    # Этап 5: Очистка
    buffer.clear()
    assert buffer.is_empty() is True
    assert buffer.pop() is None

    # Этап 6: Начинаем заново
    buffer.push("new")
    assert buffer.get_all() == ["new"]
