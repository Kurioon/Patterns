from typing import List, Protocol

""" 
Варіант  7. Користувач здійснює планування своїх покупок. Для цього він може додавати 
певну кількість Товару (Назва, виробник, ціна) до кошика та вилучати його. 
Забезпечити можливість відміни декількох останніх  дій користувача з кошиком.  
"""

class Product:

    def __init__(self, name: str, manufacturer: str, price: float) -> None:
        self.name = name
        self.manufacturer = manufacturer
        self.price = price

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', manufacturer='{self.manufacturer}', price={self.price})"
    
class ShoppingCart:

    def __init__(self) -> None:
        self._items: List[Product] = []

    def add_item(self, product: Product) -> None:
        self._items.append(product)
        print(f"[Кошик] Додано: {product.name} ({product.manufacturer})")

    def remove_item(self, product: Product) -> None:
        try: 
            self._items.remove(product)
            print(f"[Кошик] Вилучено: {product.name} ({product.manufacturer})")
        except ValueError:
            print(f"[Кошик] Помилка: {product.name} не знайдено для вилучення.")
    def __str__(self) -> str:
        if not self._items:
            return "Кошик порожній."
        
        item_names = '\n -'.join([f"{prod.name} ({prod.manufacturer}) - {prod.price:.2f} грн" for prod in self._items])
        total_price = sum(prod.price for prod in self._items)
        return f"У кошику:\n  - {item_names}\n\nЗагальна сума: {total_price:.2f} грн"
    
class Command(Protocol):

    def execute(self) -> None: ...

    def undo(self) -> None: ...

class AddCommand:

    def __init__(self, cart: ShoppingCart, product: Product) -> None:
        self._cart: ShoppingCart = cart
        self._product: Product = product

    def execute(self) -> None:
        self._cart.add_item(self._product)

    def undo(self) -> None:
        self._cart.remove_item(self._product)

class RemoveCommand:

    def __init__(self, cart: ShoppingCart, product: Product) -> None:
        self._cart: ShoppingCart = cart
        self._product: Product = product

    def execute(self) -> None:
        self._cart.remove_item(self._product)

    def undo(self) -> None:
        self._cart.add_item(self._product)

class CartManager:

    def __init__(self, cart: ShoppingCart) -> None:
        self._cart: ShoppingCart = cart
        self._history: List[Command] = []

    def execute(self, command: Command) -> None:
        print(f"--- Виконання: {command.__class__.__name__} ---")
        command.execute()
        self._history.append(command)

    def undo(self) -> None:
        if not self._history:
            print("--- Немає дій для скасування ---")
            return

        command = self._history.pop()
        print(f"--- Скасування: {command.__class__.__name__} ---")
        command.undo()

if __name__ == "__main__":
    milk = Product(name="Молоко", manufacturer="Ферма", price=45.50)
    bread = Product(name="Хліб", manufacturer="Пекарня", price=25.00)
    eggs = Product(name="Яйця", manufacturer="Курка", price=70.10)

    cart = ShoppingCart()
    manager = CartManager(cart)

    print(cart)
   
    manager.execute(AddCommand(cart, milk))
    print(cart)

    manager.execute(AddCommand(cart, bread))
    print(cart)

    manager.execute(AddCommand(cart, eggs))
    print(cart)

    manager.execute(RemoveCommand(cart, bread))
    print(cart)

    manager.undo()
    print(cart)

    manager.undo()
    print(cart)
    
    manager.undo()
    print(cart)

    manager.undo() 
    manager.undo() 