import random
from typing import Protocol

"""
Варіант 7. Нехай існує кілька стратегій торгів на криптобіржі. Кожна стратегія -це об'єкт, що приймає історію (список) цін криптовалюти і визначає ціну купівлі та ціну продажу.
Існує кілька стратегій: "Жадібна" - ціна купівлі рівна мінімальній із цін в історії, а ціна продажу - максимальні та "Стратегія середньої ціни" для якої ціна купівлі та ціна продажу рівні середньому арифметичному цін історії.  
Також нехай існує кілька Криптобірж (Binance, Coinbase, тощо) і Клас, що має методи для отримання історії торгів та поточного курсу (для простоти можна історію вважати константою, а поточний курс - випадковим числом)
Необхідно створити Підсистему торгового бота,  яка за певною стратегією торгів та поточним значенням курсу приймає рішення продавати (якщо поточна ціна вища за ціну продажу), купувати (
якщо поточна ціна нижча за ціну купівлі) чи тримати. Передбачити, що в майбутньому може бути більше стратегій та криптобірж.
"""

class TradingStrategy(Protocol):
    def calculate_prices(self, history: list[float]) -> tuple[float, float]:
        pass

class GreedyStrategy:
    def calculate_prices(self, history: list[float]) -> tuple[float, float]:
        if not history:
            return 0, 0
        buy_price = min(history)
        sell_price = max(history)
        print(f"--- [Жадібна стратегія]: Ціна купівлі = {buy_price:.2f}, Ціна продажу = {sell_price:.2f} ---")
        return buy_price, sell_price
    
class AveragePriceStrategy:
    def calculate_prices(self, history: list[float]) -> tuple[float, float]:
        if not history:
            return 0, 0
        average_price = sum(history) / len(history)
        print(f"--- [Стратегія середньої ціни]: Ціна купівлі/продажу = {average_price:.2f} ---")
        return average_price, average_price

class CryptoExchange:
    def __init__(self, strategy: TradingStrategy):
        self._strategy = strategy
        self._history = []
    
    def get_current_price(self) -> int:
        return random.randint(1, 50000)
    
    def get_price_history(self) -> list[float]:
        raise NotImplementedError
    
    def name(self) -> str:
        raise NotImplementedError
    
    def make_decision(self):
        current_price = self.get_current_price()
        history = self.get_price_history()

        print(f"\nБіржа: {self.name()}. Поточний курс: {current_price:.2f}")

        buy_price, sell_price = self._strategy.calculate_prices(history)

        if current_price > sell_price:
            print(">>> РІШЕННЯ: ПРОДАВАТИ")
        elif current_price < buy_price:
            print(">>> РІШЕННЯ: КУПУВАТИ")
        else:
            print(">>> РІШЕННЯ: ТРИМАТИ")

class Binance(CryptoExchange):
    def __init__(self, strategy):
        super().__init__(strategy)
        self._price_history = [29800.50, 30100.75, 30550.25, 29900.00, 31000.10, 31200.90, 30800.30]

    def get_price_history(self) -> list[float]:
        return self._price_history
    
    def name(self) -> str:
        return "Binance"
    
class Coinbase(CryptoExchange):
    def __init__(self, strategy):
        super().__init__(strategy)
        self._price_history = [30000.15, 30200.80, 30150.50, 30300.20, 30550.90, 30400.00, 30600.45]

    def get_price_history(self) -> list[float]:
        return self._price_history
    
    def name(self) -> str:
        return "Coinbase"



if __name__ == "__main__":

    greedy_strategy = GreedyStrategy()
    average_strategy = AveragePriceStrategy()

    print("Демонстрація роботи торгових ботів")

    binance_bot_greedy = Binance(strategy=greedy_strategy)
    binance_bot_greedy.make_decision()

    coinbase_bot_greedy = Coinbase(strategy=greedy_strategy)
    coinbase_bot_greedy.make_decision()

    binance_bot_average = Binance(strategy=average_strategy)
    binance_bot_average.make_decision()

    coinbase_bot_average = Coinbase(strategy=average_strategy)
    coinbase_bot_average.make_decision()