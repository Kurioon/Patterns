import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, message: str, contact_info: str):
        pass

class EmailNotification(NotificationStrategy):
    def send(self, message: str, contact_info: str):
        print(f"[EMAIL to {contact_info}]: {message}")

class SMSNotification(NotificationStrategy):
    def send(self, message: str, contact_info: str):
        print(f"[SMS to {contact_info}]: {message}")

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        print(f"Оплата {amount} грн через Credit Card успішна.")
        return True

class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        print(f"Оплата {amount} грн через PayPal успішна.")
        return True

class Ticket:
    def __init__(self, concert_id: str, concert_title: str, price: float, date: datetime):
        self._ticket_id = str(uuid.uuid4())
        self._concert_id = concert_id
        self._concert_title = concert_title
        self._price = price
        self._date = date

    @property
    def ticket_id(self):
        return self._ticket_id

    @property
    def concert_id(self):
        return self._concert_id

    @property
    def concert_title(self):
        return self._concert_title

    @property
    def price(self):
        return self._price

    @property
    def date(self):
        return self._date

class User:
    def __init__(self, name: str, email: str, phone: str, strategy: NotificationStrategy):
        self._user_id = str(uuid.uuid4())
        self._name = name
        self._email = email
        self._phone = phone
        self._notification_strategy = strategy
        self._tickets: List[Ticket] = []

    @property
    def name(self):
        return self._name

    @property
    def tickets(self):
        return self._tickets

    def add_ticket(self, ticket: Ticket):
        self._tickets.append(ticket)

    def get_ticket_by_id(self, ticket_id: str) -> Optional[Ticket]:
        for ticket in self._tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None

    def remove_ticket(self, ticket_id: str):
        for i, ticket in enumerate(self._tickets):
            if ticket.ticket_id == ticket_id:
                del self._tickets[i]
                return

    def notify(self, message: str):
        contact = self._email if isinstance(self._notification_strategy, EmailNotification) else self._phone
        self._notification_strategy.send(message, contact)

class Concert:
    def __init__(self, title: str, price: float, capacity: int, date_str: str):
        self._id = str(uuid.uuid4())
        self._title = title
        self._price = price
        self._capacity = capacity
        self._date = datetime.strptime(date_str, "%d.%m.%Y")

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def price(self):
        return self._price

    @property
    def capacity(self):
        return self._capacity
    
    @property
    def date(self):
        return self._date

    def has_space(self) -> bool:
        return self._capacity > 0

    def reserve_spot(self) -> bool:
        if self._capacity > 0:
            self._capacity -= 1
            return True
        return False

    def release_spot(self):
        self._capacity += 1

    def __str__(self):
        return f"'{self._title}' | {self._date.strftime('%d.%m.%Y')} | {self._price} грн | Місць: {self._capacity}"

class ConcertManager:
    def __init__(self):
        self._concerts: List[Concert] = []

    def add_concert(self, concert: Concert):
        self._concerts.append(concert)

    def get_all_concerts(self) -> List[Concert]:
        return self._concerts

    def find_concert_by_id(self, c_id: str) -> Optional[Concert]:
        for concert in self._concerts:
            if concert.id == c_id:
                return concert
        return None

class BookingManager:
    def process_purchase(self, user: User, concerts_to_buy: List[Concert], payment_strategy: PaymentStrategy) -> bool:
        if not concerts_to_buy:
            print("Кошик порожній.")
            return False

        for concert in concerts_to_buy:
            if not concert.has_space():
                print(f"Помилка: На концерт '{concert.title}' немає місць.")
                return False

        total_amount = sum(c.price for c in concerts_to_buy)

        if not payment_strategy.pay(total_amount):
            print("Помилка оплати.")
            return False

        for concert in concerts_to_buy:
            if concert.reserve_spot():
                new_ticket = Ticket(concert.id, concert.title, concert.price, concert.date)
                user.add_ticket(new_ticket)
                user.notify(f"Придбано квиток: {concert.title} ({concert.date.strftime('%d.%m.%Y')})")
        
        return True

    def cancel_ticket(self, user: User, ticket_id: str, concert_manager: ConcertManager) -> bool:
        ticket = user.get_ticket_by_id(ticket_id)
        if not ticket:
            return False

        concert = concert_manager.find_concert_by_id(ticket.concert_id)
        if concert:
            concert.release_spot()
        
        user.remove_ticket(ticket_id)
        user.notify(f"Квиток на {ticket.concert_title} видалено, кошти повернуто.")
        return True

class ConcertSystem:
    def __init__(self):
        self._concert_manager = ConcertManager()
        self._booking_manager = BookingManager()
        self._users: List[User] = []

    def register_user(self, name: str, email: str, phone: str, strategy_type: str) -> User:
        if strategy_type == "sms":
            strategy = SMSNotification()
        else:
            strategy = EmailNotification()
            
        new_user = User(name, email, phone, strategy)
        self._users.append(new_user)
        new_user.notify("Реєстрація успішна.")
        return new_user

    def get_concerts(self):
        return self._concert_manager.get_all_concerts()

    def purchase_tickets(self, user: User, cart: List[Concert], payment_strategy: PaymentStrategy):
        return self._booking_manager.process_purchase(user, cart, payment_strategy)

    def cancel_booking(self, user: User, ticket_id: str):
        return self._booking_manager.cancel_ticket(user, ticket_id, self._concert_manager)

def print_separator():
    print("-" * 50)

def register_scenario(system: ConcertSystem) -> User:
    print_separator()
    print("РЕЄСТРАЦІЯ")
    name = input("Введіть ім'я: ")
    email = input("Введіть email: ")
    phone = input("Введіть телефон: ")
    
    print("Спосіб сповіщень: 1. Email, 2. SMS")
    choice = input("Вибір: ")
    strategy_type = "sms" if choice == "2" else "email"
    
    user = system.register_user(name, email, phone, strategy_type)
    return user

def booking_scenario(system: ConcertSystem, user: User):
    cart = []
    concerts = system.get_concerts()
    
    while True:
        print_separator()
        print("АФІША:")
        for idx, c in enumerate(concerts):
            print(f"{idx + 1}. {c}")
        
        choice = input("\nВведіть номер (або 'pay' / 'b'): ")
        
        if choice == 'b': return
        if choice == 'pay': break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(concerts):
                concert = concerts[idx]
                if input(f"Додати '{concert.title}'? (y/n): ") == 'y':
                    cart.append(concert)
                    print("Додано.")
            else:
                print("Невірний номер.")
        except ValueError:
            print("Введіть число.")

    if cart:
        total = sum(c.price for c in cart)
        print(f"До сплати: {total}")
        
        print("Оберіть метод оплати:")
        print("1. Кредитна карта")
        print("2. PayPal")
        pay_choice = input("Вибір: ")

        payment_strategy = PayPalPayment() if pay_choice == "2" else CreditCardPayment()

        if system.purchase_tickets(user, cart, payment_strategy):
            print("Операція успішна.")

def history_scenario(system: ConcertSystem, user: User):
    print_separator()
    print("ВАШІ КВИТКИ:")
    if not user.tickets:
        print("Пусто.")
        return

    for t in user.tickets:
        print(f"ID: {t.ticket_id} | {t.concert_title} | {t.date.strftime('%d.%m.%Y')}")

def cancel_scenario(system: ConcertSystem, user: User):
    history_scenario(system, user)
    if not user.tickets: return
    
    t_id = input("\nВведіть ID квитка для видалення: ")
    if system.cancel_booking(user, t_id):
        print("Видалено.")
    else:
        print("Помилка видалення.")

def main():
    sys = ConcertSystem()
    sys._concert_manager.add_concert(Concert("Океан Ельзи", 1500.0, 100, "12.10.2025"))
    sys._concert_manager.add_concert(Concert("Imagine Dragons", 3500.0, 5, "01.06.2025"))
    sys._concert_manager.add_concert(Concert("Hans Zimmer", 4000.0, 50, "15.11.2025"))

    user = None

    while True:
        print_separator()
        print("1. Реєстрація")
        print("2. Купити квитки")
        print("3. Мої квитки")
        print("4. Скасувати квиток")
        print("5. Вихід")
        
        cmd = input("Вибір: ")

        if cmd == '1':
            user = register_scenario(sys)
        elif cmd == '2':
            if user:
                booking_scenario(sys, user)
            else:
                print("Спочатку зареєструйтесь.")
        elif cmd == '3':
            if user:
                history_scenario(sys, user)
            else:
                print("Спочатку зареєструйтесь.")
        elif cmd == '4':
            if user:
                cancel_scenario(sys, user)
            else:
                print("Спочатку зареєструйтесь.")
        elif cmd == '5':
            break

if __name__ == "__main__":
    main()