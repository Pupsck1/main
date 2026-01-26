class Employee:
    """Базовый класс для всех сотрудников"""

    def __init__(self, name: str, salary: float):
        """Инициализация сотрудника

        Args:
            name: Имя сотрудника
            salary: Базовая ставка зарплаты
        """
        self.name = name
        self._salary = salary

    def calculate_pay(self) -> float:
        """Рассчитать зарплату сотрудника

        Returns:
            Зарплата сотрудника
        """
        return self._salary

    def get_details(self) -> str:
        """Получить информацию о сотруднике

        Returns:
            Строка с информацией о сотруднике
        """
        return f"Имя: {self.name}, Должность: Сотрудник"

    def __str__(self) -> str:
        """Строковое представление сотрудника"""
        return f"{self.get_details()}, Зарплата: {self.calculate_pay()}"


class Manager(Employee):
    """Класс менеджера, наследуется от Employee"""

    def __init__(self, name: str, salary: float, bonus: float = 5000):
        """Инициализация менеджера

        Args:
            name: Имя менеджера
            salary: Базовая ставка зарплаты
            bonus: Фиксированный бонус менеджера
        """
        super().__init__(name, salary)
        self._bonus = bonus

    def calculate_pay(self) -> float:
        """Рассчитать зарплату менеджера с учетом бонуса

        Returns:
            Зарплата менеджера (базовая + бонус)
        """
        base_salary = super().calculate_pay()
        return base_salary + self._bonus

    def get_details(self) -> str:
        """Получить информацию о менеджере

        Returns:
            Строка с информацией о менеджере
        """
        return f"Имя: {self.name}, Должность: Менеджер"


class Developer(Employee):
    """Класс разработчика, наследуется от Employee"""

    def __init__(self, name: str, salary: float, language: str):
        """Инициализация разработчика

        Args:
            name: Имя разработчика
            salary: Базовая ставка зарплаты
            language: Язык программирования
        """
        super().__init__(name, salary)
        self.language = language

    def get_details(self) -> str:
        """Получить информацию о разработчике

        Returns:
            Строка с информацией о разработчике, включая язык программирования
        """
        return f"Имя: {self.name}, Должность: Разработчик, Язык: {self.language}"


def main():
    """Основная функция для демонстрации работы системы"""

    employees = [
        Employee("Иван Иванов", 40000),
        Manager("Анна Петрова", 78000, 5000),
        Developer("Сергей Сидоров", 85000, "Python"),
        Manager("Ольга Смирнова", 76000),
        Developer("Дмитрий Козлов", 100000, "Java"),
        Developer("Екатерина Волкова", 88000, "JavaScript"),
    ]

    print("=" * 50)
    print("СИСТЕМА УПРАВЛЕНИЯ СОТРУДНИКАМИ")
    print("=" * 50)


    for i, employee in enumerate(employees, 1):
        print(f"\nСотрудник #{i}:")
        print(f"  Информация: {employee.get_details()}")
        print(f"  Зарплата: {employee.calculate_pay():.2f} руб.")

    print("\n" + "=" * 50)
    print("Итоговая статистика:")
    print("=" * 50)

    # Дополнительная демонстрация полиморфизма
    total_pay = sum(emp.calculate_pay() for emp in employees)
    avg_pay = total_pay / len(employees) if employees else 0

    print(f"Всего сотрудников: {len(employees)}")
    print(f"Общая сумма зарплат: {total_pay:.2f} руб.")
    print(f"Средняя зарплата: {avg_pay:.2f} руб.")

    print("\n" + "=" * 50)
    print("Детальная информация по типам сотрудников:")
    print("=" * 50)

    employee_types = {}
    for emp in employees:
        emp_type = type(emp).__name__
        employee_types[emp_type] = employee_types.get(emp_type, 0) + 1

    for emp_type, count in employee_types.items():
        print(f"{emp_type}: {count} сотрудников")


if __name__ == "__main__":
    main()