import time


class Timer:
    """Упрощенный класс-секундомер для задания"""

    def __enter__(self):
        """Запоминаем время старта"""
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Вычисляем и выводим время выполнения"""
        self.end_time = time.perf_counter()
        elapsed = self.end_time - self.start_time
        print(f"Цикл/блок кода выполнялся {elapsed:.4f} секунд")


# Проверка работы таймера
if __name__ == "__main__":
    print("Запуск тяжелого цикла для демонстрации работы таймера...")

    with Timer():
        for _ in range(10 ** 7):
            pass

    print("Таймер успешно сработал!")