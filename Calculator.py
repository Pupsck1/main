class Calculator:
    """
        num1 (int, float): Первое число для операций
        num2 (int, float): Второе число для операций
    """

    def __init__(self, num1, num2):
        """
        Конструктор класса Calculator.

            num1 (int, float): Первое число
            num2 (int, float): Второе число
        """
        self.num1 = num1
        self.num2 = num2

    def add(self):
        """
        Выполняет операцию сложения двух чисел.

        Возвращает:
            int или float: Сумма num1 и num2
        """
        return self.num1 + self.num2

    def subtract(self):
        """
        Выполняет операцию вычитания второго числа из первого.

        Возвращает:
            int или float:
            Разность num1 и num2
        """
        return self.num1 - self.num2

    def multiply(self):
        """
        Выполняет операцию умножения двух чисел.

        Возвращает:
            int или float: Произведение num1 и num2
        """
        return self.num1 * self.num2

    def divide(self):
        """
        Выполняет операцию деления первого числа на второе.

        Возвращает:
            float: Частное от деления num1 на num2

        Исключения:
            ZeroDivisionError: Если происходит деление на ноль
        """
        if self.num2 == 0:
            raise ZeroDivisionError("Ошибка: деление на ноль невозможно")
        return self.num1 / self.num2


# Пример
if __name__ == "__main__":
    print("=== Тестирование класса Calculator ===\n")

    # Тест 1: Основной пример
    print("Тест 1: Основной пример (20 и 4)")
    calc1 = Calculator(20, 4)
    print(f"Создан калькулятор с числами: {calc1.num1} и {calc1.num2}")
    print(f"add() → {calc1.add()}")
    print(f"subtract() → {calc1.subtract()}")
    print(f"multiply() → {calc1.multiply()}")
    print(f"divide() → {calc1.divide()}")

    # Тест 2: Пример из раздела "Проверка работоспособности"
    print("\nТест 2: Проверка работоспособности (10 и 2)")
    calc2 = Calculator(10, 2)
    print(f"Создан калькулятор с числами: {calc2.num1} и {calc2.num2}")
    print(f"10 + 2 = {calc2.add()}")
    print(f"10 - 2 = {calc2.subtract()}")
    print(f"10 * 2 = {calc2.multiply()}")
    print(f"10 / 2 = {calc2.divide()}")

    # Тест 3: Работа с вещественными числами
    print("\nТест 3: Вещественные числа (7.5 и 2.5)")
    calc3 = Calculator(7.5, 2.5)
    print(f"Создан калькулятор с числами: {calc3.num1} и {calc3.num2}")
    print(f"7.5 + 2.5 = {calc3.add()}")
    print(f"7.5 - 2.5 = {calc3.subtract()}")
    print(f"7.5 * 2.5 = {calc3.multiply()}")
    print(f"7.5 / 2.5 = {calc3.divide()}")

    # Тест 4: Обработка деления на ноль (опциональное требование)
    print("\nТест 4: Проверка деления на ноль (8 и 0)")
    calc4 = Calculator(8, 0)
    print(f"Создан калькулятор с числами: {calc4.num1} и {calc4.num2}")
    print("Операции сложения, вычитания и умножения работают:")
    print(f"8 + 0 = {calc4.add()}")
    print(f"8 - 0 = {calc4.subtract()}")
    print(f"8 * 0 = {calc4.multiply()}")

    try:
        result = calc4.divide()
        print(f"8 / 0 = {result}")
    except ZeroDivisionError as e:
        print(f"При делении произошла ошибка: {e}")

    # Тест 5: Отрицательные числа
    print("\nТест 5: Отрицательные числа (-5 и 3)")
    calc5 = Calculator(-5, 3)
    print(f"Создан калькулятор с числами: {calc5.num1} и {calc5.num2}")
    print(f"-5 + 3 = {calc5.add()}")
    print(f"-5 - 3 = {calc5.subtract()}")
    print(f"-5 * 3 = {calc5.multiply()}")
    print(f"-5 / 3 = {calc5.divide():.2f}")

    print("\n=== Тестирование завершено ===")