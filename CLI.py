import datetime
from typing import Optional

class Task:
    """Модель задачи."""
    PRIORITIES = ("low", "medium", "high")
    STATUSES = ("active", "completed")

    def __init__(
        self,
        task_id: int,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium",
        status: str = "active",
        created_at: Optional[datetime.datetime] = None,
    ):
        self.id = task_id
        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.priority = priority.lower()
        self.status = status.lower()
        self.created_at = created_at or datetime.datetime.now()

    def to_dict(self) -> dict:
        """Преобразует задачу в словарь для сериализации."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Создаёт задачу из словаря (десериализация)."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            status=data.get("status", "active"),
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
        )

    def mark_completed(self) -> None:
        """Помечает задачу как выполненную."""
        self.status = "completed"

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', status={self.status}, priority={self.priority})"

    from typing import List, Optional, Callable
    import datetime
    from models import Task

    class TaskManager:
        """Управление коллекцией задач."""

        def __init__(self):
            self.tasks: List[Task] = []
            self._next_id = 1

        def _update_next_id(self) -> None:
            """Обновляет значение следующего свободного ID на основе текущих задач."""
            if self.tasks:
                self._next_id = max(task.id for task in self.tasks) + 1
            else:
                self._next_id = 1

        def load_tasks(self, tasks: List[Task]) -> None:
            """Загружает задачи (например, из файла) и пересчитывает ID."""
            self.tasks = tasks
            self._update_next_id()

        def add_task(self, title: str, description: Optional[str] = None, priority: str = "medium") -> Task:
            """Добавляет новую задачу и возвращает её."""
            if not title or not title.strip():
                raise ValueError("Название задачи не может быть пустым.")
            if priority not in Task.PRIORITIES:
                raise ValueError(f"Приоритет должен быть одним из: {', '.join(Task.PRIORITIES)}")

            task = Task(
                task_id=self._next_id,
                title=title,
                description=description,
                priority=priority,
            )
            self.tasks.append(task)
            self._next_id += 1
            return task

        def mark_task_completed(self, task_id: int) -> bool:
            """Помечает задачу с указанным ID как выполненную.
            Возвращает True, если задача найдена и помечена, иначе False.
            """
            for task in self.tasks:
                if task.id == task_id:
                    if task.status == "active":
                        task.mark_completed()
                        return True
                    else:
                        return False  # уже выполнена
            return False

        def get_tasks(
                self,
                status: Optional[str] = None,
                priority: Optional[str] = None,
                sort_by: str = "created_at",  # 'created_at' или 'priority'
                reverse: bool = False,
        ) -> List[Task]:
            """Возвращает отфильтрованный и отсортированный список задач."""
            result = self.tasks[:]

            # Фильтрация по статусу
            if status and status in Task.STATUSES:
                result = [t for t in result if t.status == status]

            # Фильтрация по приоритету
            if priority and priority in Task.PRIORITIES:
                result = [t for t in result if t.priority == priority]

            # Сортировка
            if sort_by == "created_at":
                result.sort(key=lambda t: t.created_at, reverse=reverse)
            elif sort_by == "priority":
                priority_order = {"low": 0, "medium": 1, "high": 2}
                result.sort(key=lambda t: priority_order[t.priority], reverse=reverse)
            else:
                raise ValueError("sort_by должен быть 'created_at' или 'priority'")

            return result

        def clear_all(self) -> None:
            """Удаляет все задачи (используется с осторожностью)."""
            self.tasks.clear()
            self._next_id = 1
            import sys
            from core import TaskManager
            import storage

            class CLI:
                """Интерактивная консольная оболочка."""

                def __init__(self):
                    self.manager = TaskManager()
                    self.running = True

                def run(self):
                    """Запускает главный цикл CLI."""
                    # Загружаем задачи при старте
                    tasks = storage.load_tasks(storage.DEFAULT_FILE)
                    self.manager.load_tasks(tasks)

                    print("=== Менеджер задач === (введите help для списка команд)")

                    while self.running:
                        try:
                            user_input = input("\n> ").strip().lower()
                            if not user_input:
                                continue
                            self._execute_command(user_input)
                        except KeyboardInterrupt:
                            print("\nВыход...")
                            self._save_and_exit()
                            break
                        except Exception as e:
                            print(f"Ошибка: {e}")

                def _execute_command(self, cmd: str):
                    """Разбирает и выполняет команду."""
                    parts = cmd.split()
                    command = parts[0]

                    if command == "help":
                        self._show_help()
                    elif command == "add":
                        self._add_task(parts[1:])
                    elif command == "list":
                        self._list_tasks(parts[1:])
                    elif command == "done":
                        self._mark_done(parts[1:])
                    elif command == "export":
                        self._export_tasks(parts[1:])
                    elif command == "import":
                        self._import_tasks(parts[1:])
                    elif command == "exit" or command == "quit":
                        self._save_and_exit()
                        self.running = False
                    else:
                        print("Неизвестная команда. Введите 'help'.")

                def _show_help(self):
                    """Выводит справку."""
                    help_text = """
            Доступные команды:
              add <название> [--description <текст>] [--priority low|medium|high]
                  Добавить новую задачу. Название обязательно.
                  Пример: add Купить молоко --priority high
                         add Прочитать книгу --description "фантастика"

              list [--status active|completed] [--priority low|medium|high] [--sort created_at|priority] [--reverse]
                  Показать список задач. По умолчанию все активные, сортировка по дате.
                  Пример: list --status completed --sort priority

              done <id>
                  Отметить задачу с указанным ID как выполненную.

              export <json|csv> <filename>
                  Экспортировать все задачи в файл (JSON или CSV).
                  Пример: export json backup.json

              import <json|csv> <filename>
                  Импортировать задачи из файла и добавить в текущий список.
                  Пример: import csv tasks.csv

              exit / quit
                  Выйти из программы (задачи автоматически сохраняются).

            Примечания:
              - Приоритет: low (низкий), medium (средний), high (высокий).
              - Статус: active (активная) / completed (выполненная).
              - Сохранение происходит автоматически после каждого изменения.
            """
                    print(help_text)

                def _add_task(self, args):
                    """Обрабатывает команду add."""
                    if not args:
                        print("Укажите название задачи.")
                        return

                    title = args[0]
                    description = None
                    priority = "medium"

                    # Разбор опциональных параметров
                    i = 1
                    while i < len(args):
                        if args[i] == "--description" and i + 1 < len(args):
                            description = args[i + 1]
                            i += 2
                        elif args[i] == "--priority" and i + 1 < len(args):
                            priority = args[i + 1].lower()
                            if priority not in Task.PRIORITIES:
                                print(f"Неверный приоритет. Допустимые: {', '.join(Task.PRIORITIES)}")
                                return
                            i += 2
                        else:
                            print(f"Неизвестный параметр: {args[i]}")
                            return

                    try:
                        task = self.manager.add_task(title, description, priority)
                        print(f"Задача добавлена (ID {task.id}): {task.title}")
                        self._auto_save()
                    except ValueError as e:
                        print(f"Ошибка: {e}")

                def _list_tasks(self, args):
                    """Обрабатывает команду list с фильтрами и сортировкой."""
                    status = None
                    priority = None
                    sort_by = "created_at"
                    reverse = False

                    i = 0
                    while i < len(args):
                        if args[i] == "--status" and i + 1 < len(args):
                            status = args[i + 1].lower()
                            if status not in Task.STATUSES:
                                print(f"Неверный статус. Допустимые: {', '.join(Task.STATUSES)}")
                                return
                            i += 2
                        elif args[i] == "--priority" and i + 1 < len(args):
                            priority = args[i + 1].lower()
                            if priority not in Task.PRIORITIES:
                                print(f"Неверный приоритет. Допустимые: {', '.join(Task.PRIORITIES)}")
                                return
                            i += 2
                        elif args[i] == "--sort" and i + 1 < len(args):
                            sort_by = args[i + 1].lower()
                            if sort_by not in ("created_at", "priority"):
                                print("Сортировка может быть только 'created_at' или 'priority'.")
                                return
                            i += 2
                        elif args[i] == "--reverse":
                            reverse = True
                            i += 1
                        else:
                            print(f"Неизвестный параметр: {args[i]}")
                            return

                    tasks = self.manager.get_tasks(status=status, priority=priority, sort_by=sort_by, reverse=reverse)

                    if not tasks:
                        print("Задачи не найдены.")
                        return

                    # Вывод в табличном стиле
                    print("\n" + "-" * 80)
                    print(f"{'ID':<4} {'Статус':<10} {'Приоритет':<8} {'Название':<30} {'Дата создания'}")
                    print("-" * 80)
                    for task in tasks:
                        status_icon = "✓" if task.status == "completed" else "○"
                        priority_label = {
                            "low": "Низкий",
                            "medium": "Средний",
                            "high": "Высокий"
                        }.get(task.priority, task.priority)
                        date_str = task.created_at.strftime("%Y-%m-%d %H:%M")
                        print(f"{task.id:<4} {status_icon} {task.status:<8} {priority_label:<8} "
                              f"{task.title[:28]:<30} {date_str}")
                        if task.description:
                            print(f"     Описание: {task.description[:60]}")
                    print("-" * 80)

                def _mark_done(self, args):
                    """Обрабатывает команду done."""
                    if not args:
                        print("Укажите ID задачи.")
                        return
                    try:
                        task_id = int(args[0])
                    except ValueError:
                        print("ID должен быть числом.")
                        return

                    if self.manager.mark_task_completed(task_id):
                        print(f"Задача {task_id} помечена как выполненная.")
                        self._auto_save()
                    else:
                        print(f"Задача с ID {task_id} не найдена или уже выполнена.")

                def _export_tasks(self, args):
                    """Обрабатывает команду export."""
                    if len(args) < 2:
                        print("Использование: export <json|csv> <filename>")
                        return
                    fmt = args[0].lower()
                    filename = args[1]

                    try:
                        if fmt == "json":
                            storage.export_to_json(filename, self.manager.tasks)
                        elif fmt == "csv":
                            storage.export_to_csv(filename, self.manager.tasks)
                        else:
                            print("Формат должен быть json или csv.")
                            return
                        print(f"Задачи экспортированы в {filename}")
                    except Exception as e:
                        print(f"Ошибка экспорта: {e}")

                def _import_tasks(self, args):
                    """Обрабатывает команду import."""
                    if len(args) < 2:
                        print("Использование: import <json|csv> <filename>")
                        return
                    fmt = args[0].lower()
                    filename = args[1]

                    try:
                        if fmt == "json":
                            storage.import_from_json(filename, self.manager)
                        elif fmt == "csv":
                            storage.import_from_csv(filename, self.manager)
                        else:
                            print("Формат должен быть json или csv.")
                            return
                        print(f"Задачи импортированы из {filename}")
                        self._auto_save()
                    except Exception as e:
                        print(f"Ошибка импорта: {e}")

                def _auto_save(self):
                    """Автоматическое сохранение после каждого изменения."""
                    storage.save_tasks(storage.DEFAULT_FILE, self.manager.tasks)

                def _save_and_exit(self):
                    """Сохраняет перед выходом."""
                    storage.save_tasks(storage.DEFAULT_FILE, self.manager.tasks)
                    print("Задачи сохранены. До свидания!")
