import uuid
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional

'''
Варіант 7. Клас відстеження помилок, який повинна існувати в єдиному екземплярі. Реалізовувати методи:
1) Фіксування помилки (Час, код, текст з описом помилки)
2) Очищення історії помилок.
3) Вивід інформації про всі помилки
4) Збереження історії помилок до файлу.
'''

class ErrorRecord:
    def __init__(self, code: int, text: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.time: str = datetime.now().isoformat(sep=' ', timespec='seconds')
        self.code: int = code
        self.text: str = text

    def __str__(self) -> str:
        return f"{self.time} | code={self.code} | {self.text}"

class ErrorTracker:
    _instance: ClassVar[Optional["ErrorTracker"]] = None
    _initialized: bool = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "ErrorTracker":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, filename: str = "logs.txt") -> None:
        if self._initialized:
            return
        self._history: List[ErrorRecord] = []
        self._filename: str = filename
        self._initialized = True
        print(f"[INIT] ErrorTracker ініціалізовано. Файл логів: {self._filename}")

    def log_error(self, code: int, text: str) -> None:
        record = ErrorRecord(code, text)
        self._history.append(record)
        print(f"[LOGGED] {record}")

    def show_history(self) -> None:
        if not self._history:
            print("[SHOW] Історія помилок порожня.")
            return
        for i, error in enumerate(self._history, 1):
            print(f"{i}. {error}")
    
    def clear_history(self):
        count: int = len(self._history)
        self._history.clear()
        print(f"[CLEARED] Видалено {count} записів з історії.")

    def save_to_file(self) -> None:
        with open(self._filename, 'w', encoding='utf-8') as f:
            for error in self._history:
                f.write(str(error) + "\n")
        print(f"[SAVED] Історія помилок збережена до: {self._filename}")



# test
if __name__ == "__main__":
    tracker = ErrorTracker()
    new_tracker = ErrorTracker()
    tracker.log_error(404, "Якийсь текст")
    new_tracker.log_error(500, "Якийсь текст2")
    new_tracker.show_history()
    new_tracker.save_to_file()