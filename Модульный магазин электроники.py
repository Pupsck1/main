"""
Модуль models.py
Содержит классы для представления товаров
"""


class Product:
    """Класс для представления товара в магазине"""

    def __init__(self, name: str, price: float, quantity: int):
        """
        Инициализация товара

        Args:
            name: Название товара
            price: Цена товара
            quantity: Количество на складе
        """
        self.name = name
        self.price = price
        self.quantity = quantity

    def is_available(self, requested_quantity: int = 1) -> bool:
        """
        Проверить наличие товара на складе

        Args:
            requested_quantity: Запрашиваемое количество

        Returns:
            True если товар есть в достаточном количестве, иначе False
        """
        return self.quantity >= requested_quantity

    def reduce_quantity(self, amount: int) -> bool:
        """
        Уменьшить количество товара на складе

        Args:
            amount: Количество для уменьшения

        Returns:
            True если операция успешна, иначе False
        """
        if self.is_available(amount):
            self.quantity -= amount
            return True
        return False

    def __str__(self) -> str:
        """Строковое представление товара"""
        return f"{self.name} - {self.price:.2f} руб. (в наличии: {self.quantity})"

    def __repr__(self) -> str:
        """Представление товара для отладки"""
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"

    """
    Модуль cart.py
    Содержит класс для работы с корзиной покупок
    """

    from typing import List, Tuple

    # Импортируем Product из models
    try:
        from models import Product
    except ImportError:
        # Для случая, если модуль запускается отдельно
        from .models import Product

    class ShoppingCart:
        """Класс для представления корзины покупок"""

        def __init__(self):
            """Инициализация пустой корзины"""
            self.items = []  # Список кортежей: (товар, количество)

        def add_item(self, product: Product, quantity: int = 1) -> bool:
            """
            Добавить товар в корзину

            Args:
                product: Товар для добавления
                quantity: Количество товара

            Returns:
                True если товар успешно добавлен, иначе False
            """
            if not product.is_available(quantity):
                print(f"Недостаточно товара '{product.name}' на складе. "
                      f"Запрошено: {quantity}, в наличии: {product.quantity}")
                return False

            # Проверяем, есть ли уже такой товар в корзине
            for i, (item_product, item_quantity) in enumerate(self.items):
                if item_product.name == product.name:
                    # Обновляем количество существующего товара
                    if product.is_available(item_quantity + quantity):
                        self.items[i] = (product, item_quantity + quantity)
                        return True
                    else:
                        print(f"Недостаточно товара '{product.name}' для добавления")
                        return False

            # Добавляем новый товар
            self.items.append((product, quantity))
            return True

        def remove_item(self, product_name: str, quantity: int = None) -> bool:
            """
            Удалить товар из корзины

            Args:
                product_name: Название товара для удаления
                quantity: Количество для удаления (None - удалить все)

            Returns:
                True если товар успешно удален, иначе False
            """
            for i, (product, item_quantity) in enumerate(self.items):
                if product.name == product_name:
                    if quantity is None or quantity >= item_quantity:
                        # Удаляем товар полностью
                        self.items.pop(i)
                        return True
                    else:
                        # Уменьшаем количество
                        self.items[i] = (product, item_quantity - quantity)
                        return True

            print(f"Товар '{product_name}' не найден в корзине")
            return False

        def get_total(self) -> float:
            """
            Рассчитать общую стоимость товаров в корзине

            Returns:
                Общая стоимость корзины
            """
            total = 0.0
            for product, quantity in self.items:
                total += product.price * quantity
            return total

        def clear(self) -> None:
            """Очистить корзину"""
            self.items.clear()

        def get_items(self) -> List[Tuple[Product, int]]:
            """
            Получить список товаров в корзине

            Returns:
                Список кортежей (товар, количество)
            """
            return self.items.copy()

        def is_empty(self) -> bool:
            """
            Проверить, пуста ли корзина

            Returns:
                True если корзина пуста, иначе False
            """
            return len(self.items) == 0

        def get_receipt_details(self) -> str:
            """
            Получить детализированную информацию о содержимом корзины

            Returns:
                Строка с детализацией чека
            """
            if self.is_empty():
                return "Корзина пуста"

            receipt_lines = []
            receipt_lines.append("=" * 40)
            receipt_lines.append("ЧЕК ПОКУПКИ")
            receipt_lines.append("=" * 40)

            total = 0.0
            for i, (product, quantity) in enumerate(self.items, 1):
                item_total = product.price * quantity
                total += item_total
                receipt_lines.append(f"{i}. {product.name}")
                receipt_lines.append(f"   Цена: {product.price:.2f} руб. × {quantity} = {item_total:.2f} руб.")

            receipt_lines.append("-" * 40)
            receipt_lines.append(f"ИТОГО: {total:.2f} руб.")
            receipt_lines.append("=" * 40)

            return "\n".join(receipt_lines)

        def checkout(self) -> bool:
            """
            Оформить покупку (уменьшить количество товаров на складе)

            Returns:
                True если покупка успешно оформлена, иначе False
            """
            if self.is_empty():
                print("Корзина пуста, нечего оформлять")
                return False

            # Проверяем наличие всех товаров
            for product, quantity in self.items:
                if not product.is_available(quantity):
                    print(f"Товара '{product.name}' недостаточно на складе для оформления")
                    return False

            # Уменьшаем количество товаров на складе
            for product, quantity in self.items:
                product.reduce_quantity(quantity)

            print("Покупка успешно оформлена!")
            return True

        def __str__(self) -> str:
            """Строковое представление корзины"""
            if self.is_empty():
                return "Корзина пуста"

            items_str = []
            for product, quantity in self.items:
                items_str.append(f"{product.name} - {quantity} шт.")

            return f"Корзина ({len(self.items)} товаров): {', '.join(items_str)}"