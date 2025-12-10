from __future__ import annotations  # Дозволяє використовувати типи класів до їх повного оголошення
from abc import ABC, abstractmethod
from typing import List

"""
11.У інформаційній системі ветеринарної клініки є дані обліку різних тварини:
Собака, Кіт, Папуга. Об’єкти тварин містять лише базову інформацію (кличка,
вік, номер власника) і змінювати їх логіку не можна. Необхідно реалізувати

систему розсилання повідомлення із запрошенням для проведення різних
процедур. Об’єкти даних про тварин не можуть містити методу надсилання
повідомлення. Передбачити такі види процедур (операцій):
a. Медичний огляд: для собаки — слухають серце та перевіряють лапи, для
кота — перевіряють вуха та рефлекси, для папуги —оглядають дзьоб та
крила.
b. Грумінг: собаку стрижуть машинкою, кота вичісують, а для папуги ця
операція неможлива (тому повідомлення надсилати не потрібно)
Надіслати всім власникам тварин по 2 окремі запрошення на медичний
огляд і грумнг
"""

# Для вирішення цієї задачі я вирішив використати шаблон Візитер (Visitor).

# Інтерфейс Візитера
class VeterinaryVisitor(ABC):
    @abstractmethod
    def visit_dog(self, dog: Dog) -> None:
        pass

    @abstractmethod
    def visit_cat(self, cat: Cat) -> None:
        pass

    @abstractmethod
    def visit_parrot(self, parrot: Parrot) -> None:
        pass

# Елементи (Animals)
class Animal(ABC):
    def __init__(self, name: str, age: int, owner_phone: str) -> None:
        self.name = name
        self.age = age
        self.owner_phone = owner_phone

    @abstractmethod
    def accept(self, visitor: VeterinaryVisitor) -> None:
        pass

class Dog(Animal):
    def accept(self, visitor: VeterinaryVisitor) -> None:
        visitor.visit_dog(self)

class Cat(Animal):
    def accept(self, visitor: VeterinaryVisitor) -> None:
        visitor.visit_cat(self)

class Parrot(Animal):
    def accept(self, visitor: VeterinaryVisitor) -> None:
        visitor.visit_parrot(self)

# Конкретні Візитери 
class MedicalExamVisitor(VeterinaryVisitor):
    # Відвідувач для Медичного огляду
    def visit_dog(self, dog: Dog) -> None:
        msg = (f"SMS to {dog.owner_phone}: Шановний власнику собаки {dog.name}! "
               f"Запрошуємо на огляд: слухаємо серце та перевіряємо лапи.")
        print(msg)

    def visit_cat(self, cat: Cat) -> None:
        msg = (f"SMS to {cat.owner_phone}: Шановний власнику кота {cat.name}! "
               f"Запрошуємо на огляд: перевіряємо вуха та рефлекси.")
        print(msg)

    def visit_parrot(self, parrot: Parrot) -> None:
        msg = (f"SMS to {parrot.owner_phone}: Шановний власнику папуги {parrot.name}! "
               f"Запрошуємо на огляд: оглядаємо дзьоб та крила.")
        print(msg)

class GroomingVisitor(VeterinaryVisitor):
    # Візитер для Грумінгу
    def visit_dog(self, dog: Dog) -> None:
        msg = (f"SMS to {dog.owner_phone}: Шановний власнику собаки {dog.name}! "
               f"Запрошуємо на грумінг: стрижка машинкою.")
        print(msg)

    def visit_cat(self, cat: Cat) -> None:
        msg = (f"SMS to {cat.owner_phone}: Шановний власнику кота {cat.name}! "
               f"Запрошуємо на грумінг: вичісування.")
        print(msg)

    def visit_parrot(self, parrot: Parrot) -> None:
        pass



if __name__ == "__main__":
    clinic_pets: List[Animal] = [
        Dog("Рекс", 5, "+380501111111"),
        Cat("Барсик", 3, "+380502222222"),
        Parrot("Кеша", 2, "+380503333333"),
        Dog("Арчі", 7, "+380504444444")
    ]

    print("Розсилання запрошень на МЕДИЧНИЙ ОГЛЯД")
    med_visitor = MedicalExamVisitor()
    for pet in clinic_pets:
        pet.accept(med_visitor)

    print("\nРозсилання запрошень на ГРУМІНГ")
    grooming_visitor = GroomingVisitor()
    for pet in clinic_pets:
        pet.accept(grooming_visitor)