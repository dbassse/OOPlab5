from dataclasses import dataclass

from task_package.zad2 import RingBuffer


def main() -> None:
    # Демонстрация работы кольцевого буфера
    def demonstrate_ring_buffer() -> None:
        print("=== Демонстрация работы кольцевого буфера ===")

        # Создаем кольцевой буфер целых чисел с емкостью 5
        buffer: RingBuffer[int] = RingBuffer[int](capacity=5)
        print(f"Создан буфер: {buffer}")
        print(f"Пустой? {buffer.is_empty()}")
        print(f"Полный? {buffer.is_full()}")

        # Добавляем элементы
        print("\n--- Добавляем 7 элементов в буфер емкостью 5 ---")
        for i in range(1, 8):
            buffer.push(i)
            print(f"Добавили {i}: {buffer}")
            print(f"Самый старый элемент: {buffer.peek()}")
            print(f"Полный? {buffer.is_full()}")

        # Извлекаем элементы
        print("\n--- Извлекаем 3 элемента ---")
        for _ in range(3):
            item = buffer.pop()
            print(f"Извлекли: {item}, Осталось: {buffer}")

        # Добавляем еще элементы
        print("\n--- Добавляем еще 3 элемента ---")
        for i in range(8, 11):
            buffer.push(i)
            print(f"Добавили {i}: {buffer}")

        # Проверяем оператор in
        print("\nПроверка наличия элементов:")
        print(f"Содержит 5? {5 in buffer}")
        print(f"Содержит 1? {1 in buffer}")  # 1 был вытеснен при переполнении

        # Получаем все элементы
        print(f"\nВсе элементы в буфере: {buffer.get_all()}")

        # Очищаем буфер
        print("\n--- Очистка буфера ---")
        buffer.clear()
        print(f"После очистки: {buffer}")
        print(f"Пустой? {buffer.is_empty()}")

    # Пример использования с разными типами данных
    def demonstrate_generics() -> None:
        print("\n\n=== Демонстрация работы с разными типами данных ===")

        # Строки
        print("\n1. Буфер строк:")
        string_buffer: RingBuffer[str] = RingBuffer[str](capacity=3)
        string_buffer.push("apple")
        string_buffer.push("banana")
        string_buffer.push("cherry")
        string_buffer.push("date")  # Вытеснит "apple"
        print(string_buffer)

        # Числа с плавающей точкой
        print("\n2. Буфер чисел с плавающей точкой:")
        float_buffer: RingBuffer[float] = RingBuffer[float](capacity=4)
        for value in [1.1, 2.2, 3.3, 4.4, 5.5]:
            float_buffer.push(value)
        print(float_buffer)

        # Собственный класс
        print("\n3. Буфер пользовательских объектов:")

        @dataclass
        class Point:
            x: float
            y: float

        point_buffer: RingBuffer[Point] = RingBuffer[Point](capacity=2)
        point_buffer.push(Point(1.0, 2.0))
        point_buffer.push(Point(3.0, 4.0))
        point_buffer.push(Point(5.0, 6.0))  # Вытеснит первую точку
        print(point_buffer)

    # Демонстрация работы с переполнением
    def demonstrate_overflow() -> None:
        print("\n\n=== Демонстрация поведения при переполнении ===")

        buffer: RingBuffer[int] = RingBuffer[int](capacity=3)

        print("Изначальный буфер (пустой):")
        print(buffer)

        print("\nДобавляем элементы 1, 2, 3:")
        for i in [1, 2, 3]:
            buffer.push(i)
            print(f"После добавления {i}: {buffer}")

        print("\nБуфер заполнен. Добавляем элемент 4:")
        buffer.push(4)
        print(f"После добавления 4: {buffer}")
        print("Элемент 1 был заменен (самый старый)")

        print("\nДобавляем элемент 5:")
        buffer.push(5)
        print(f"После добавления 5: {buffer}")
        print("Элемент 2 был заменен (самый старый)")

        print("\nДобавляем элемент 6:")
        buffer.push(6)
        print(f"После добавления 6: {buffer}")
        print("Элемент 3 был заменен (самый старый)")

    # Вызов функций
    demonstrate_ring_buffer()
    demonstrate_generics()
    demonstrate_overflow()


if __name__ == "__main__":
    main()
