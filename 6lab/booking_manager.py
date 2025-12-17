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
        self._is_active = True

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

    def validate(self) -> bool:
        return self._is_active and self._date > datetime.now()

    def invalidate(self):
        self._is_active = False

class Booking:
    def __init__(self, user_id: str, tickets: List[Ticket]):
        self._booking_id = str(uuid.uuid4())
        self._user_id = user_id
        self._tickets = tickets
        self._date_created = datetime.now()
        self._status = "Confirmed"  # Confirmed, Cancelled

    @property
    def booking_id(self): 
        return self._booking_id
    
    @property
    def tickets(self): 
        return self._tickets
    
    @property
    def status(self): 
        return self._status

    def cancel_booking(self):
        self._status = "Cancelled"
        for t in self._tickets:
            t.invalidate()

class User:
    def __init__(self, name: str, email: str, phone: str, password: str, strategy: NotificationStrategy):
        self._user_id = str(uuid.uuid4())
        self._name = name
        self._email = email
        self._phone = phone
        self._password = password 
        self._notification_strategy = strategy
        self._bookings: List[Booking] = []

    @property
    def email(self):
        return self._email
    
    @property
    def name(self):
        return self._name
    
    @property
    def bookings(self):
        return self._bookings

    def check_password(self, pwd: str) -> bool:
        return self._password == pwd

    def add_booking(self, booking: Booking):
        self._bookings.append(booking)

    def get_all_active_tickets(self) -> List[Ticket]:
        all_tickets = []
        for booking in self._bookings:
            if booking.status == "Confirmed":
                all_tickets.extend(booking.tickets)
        return all_tickets

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
    def date(self):
        return self._date
    
    @property
    def concert_id(self):
        return self._concert_id

    def has_space(self) -> bool:
        return self._capacity > 0
    
    def reserve_spot(self):
        self._capacity -= 1

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
    def create_booking(self, user: User, concerts: List[Concert], payment_strategy: PaymentStrategy) -> bool:
        if not concerts:
            print("Кошик порожній.")
            return False

        # 1. Перевірка місць
        for concert in concerts:
            if not concert.has_space():
                print(f"Помилка: На концерт '{concert.title}' немає місць.")
                return False

        # 2. Оплата
        total_amount = sum(c.price for c in concerts)
        if not payment_strategy.pay(total_amount):
            print("Помилка оплати.")
            return False

        # 3. Резервування та створення квитків
        new_tickets = []
        for concert in concerts:
            concert.reserve_spot()
            t = Ticket(concert.id, concert.title, concert.price, concert.date)
            new_tickets.append(t)
        
        # 4. Створення об'єкта Booking
        new_booking = Booking(user.email, new_tickets) # Використав email як ID для простоти
        user.add_booking(new_booking)
        
        user.notify(f"Успішно створено замовлення {new_booking.booking_id} на {len(new_tickets)} квитків.")
        return True

    def cancel_ticket_in_booking(self, user: User, ticket_id: str, concert_manager: ConcertManager) -> bool:
        for booking in user.bookings:
            if booking.status == "Confirmed":
                for i, ticket in enumerate(booking.tickets):
                    if ticket.ticket_id == ticket_id:
                        concert = concert_manager.find_concert_by_id(ticket.concert_id)
                        if concert: 
                            concert.release_spot()
                        
                        ticket.invalidate()
                        
                        booking.tickets.pop(i) 
                        
                        if not booking.tickets: 
                            booking.cancel_booking() 
                            print(f"Замовлення {booking.booking_id} повністю скасовано.")

                        user.notify(f"Квиток на {ticket.concert_title} скасовано.")
                        return True
        return False

class ConcertSystem:
    def __init__(self):
        self._concert_manager = ConcertManager()
        self._booking_manager = BookingManager()
        self._users: List[User] = []
        self._current_user: Optional[User] = None
        self._cart: List[Concert] = [] 

    def register(self, name, email, phone, password, strategy_type):
        strategy = SMSNotification() if strategy_type == "sms" else EmailNotification()
        new_user = User(name, email, phone, password, strategy)
        self._users.append(new_user)
        self._current_user = new_user
        print(f"Користувач {name} зареєстрований і авторизований.")

    def login(self, email, password):
        for u in self._users:
            if u.email == email and u.check_password(password):
                self._current_user = u
                print(f"Вітаємо, {u.name}!")
                return True
        print("Невірний логін або пароль.")
        return False

    def add_to_cart(self, concert: Concert):
        self._cart.append(concert)
    
    def get_cart_total(self):
        return sum(c.price for c in self._cart)

    def checkout(self, payment_method: str):
        if not self._current_user:
            print("Для оплати потрібно увійти в систему!")
            return False
        
        strategy = PayPalPayment() if payment_method == "2" else CreditCardPayment()
        result = self._booking_manager.create_booking(self._current_user, self._cart, strategy)
        if result:
            self._cart = [] # Очистити кошик після успіху
        return result
    
    def cancel_ticket(self, ticket_id: str):
        if not self._current_user:
            print("Помилка: Необхідна авторизація.")
            return False
        
        result = self._booking_manager.cancel_ticket_in_booking(
            self._current_user, 
            ticket_id, 
            self._concert_manager
        )
        
        if result:
            print("Операція успішна: Квиток скасовано.")
        else:
            print("Помилка: Квиток не знайдено або він вже неактивний.")
        return result
    

def print_separator():
    print("-" * 50)

def main_menu():
    sys = ConcertSystem()
    sys._concert_manager.add_concert(Concert("Океан Ельзи", 1500.0, 100, "12.10.2026"))
    sys._concert_manager.add_concert(Concert("Imagine Dragons", 3500.0, 1000, "01.06.2026"))
    sys._concert_manager.add_concert(Concert("Red Hot Chili Peppers", 4500.0, 40000, "20.07.2026"))
    sys._concert_manager.add_concert(Concert("Arctic Monkeys", 3800.0, 30000, "15.08.2026"))
    
    while True:
        print_separator()
        user_label = sys._current_user.name if sys._current_user else "Гість"
        print(f"СТАТУС: {user_label} | У кошику: {len(sys._cart)} концертів")
        print("1. Афіша (Обрати концерти)")
        print("2. Реєстрація")
        print("3. Вхід (Login)")
        print("4. Оплатити кошик")
        print("5. Мої квитки (Історія)")
        print("6. Скасувати квиток")
        print("7. Вихід")

        choice = input("Ваш вибір: ")

        match choice:
            case '1':
                concerts = sys._concert_manager.get_all_concerts()
                for idx, c in enumerate(concerts):
                    print(f"{idx+1}. {c}")
                try:
                    inp = input("Номер концерту для додавання в кошик (0 - назад): ")
                    if inp == '0':
                        continue
                    num = int(inp)
                    if 0 < num <= len(concerts):
                        sys.add_to_cart(concerts[num-1])
                        print("Додано!")
                except ValueError: pass

            case '2':
                name = input("Ім'я: ")
                email = input("Email: ")
                phone = input("Телефон: ")
                pwd = input("Пароль: ")
                notif = input("sms/email? ")
                sys.register(name, email, phone, pwd, notif)

            case '3':
                email = input("Email: ")
                pwd = input("Пароль: ")
                sys.login(email, pwd)

            case '4':
                if not sys._cart:
                    print("Кошик порожній.")
                    continue
                if not sys._current_user:
                    print("Спочатку увійдіть або зареєструйтесь!")
                    continue
                print(f"До сплати: {sys.get_cart_total()} грн")
                method = input("1. Карта, 2. PayPal: ")
                sys.checkout(method)

            case '5':
                if sys._current_user:
                    tickets = sys._current_user.get_all_active_tickets()
                    if not tickets: print("Квитків немає.")
                    for t in tickets:
                        print(f"ID: {t.ticket_id} | {t.concert_title}") 
                else:
                    print("Потрібна авторизація.")

            case '6': 
                if not sys._current_user:
                    print("Спочатку увійдіть у систему!")
                    continue
                
                # Спочатку покажемо квитки, щоб юзер бачив ID
                tickets = sys._current_user.get_all_active_tickets()
                if not tickets:
                    print("У вас немає активних квитків для скасування.")
                    continue
                
                for t in tickets:
                    print(f"ID: {t.ticket_id} | {t.concert_title}")
                    
                t_id = input("\nВведіть ID квитка, який треба скасувати: ")
                sys.cancel_ticket(t_id)

            case '7':
                print("До побачення.")
                break

if __name__ == "__main__":
    main_menu()