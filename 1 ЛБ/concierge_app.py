
from datetime import datetime
from typing import List, Dict, Optional

class ConciergeLog:

    def __init__(self):

        self.entries: List[Dict] = []
        self.resident_id_counter = 1

    def log_entry(self, name: str, action: str) -> bool:
        if action.lower() not in ['вхід', 'вихід']:
            return False

        entry = {
            'name': name,
            'action': action,
            'timestamp': datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        }

        self.entries.append(entry)
        return True

    def get_current_residents(self) -> List[str]:
        residents = set()

        for entry in self.entries:
            if entry['action'].lower() == 'вхід':
                residents.add(entry['name'])
            else:
                residents.discard(entry['name'])

        return sorted(list(residents))

    def get_all_history(self) -> List[Dict]:
        return self.entries.copy()

    def get_resident_history(self, name: str) -> List[Dict]:
        return [e for e in self.entries if e['name'].lower() == name.lower()]

    def print_status(self) -> None:
        residents = self.get_current_residents()
        print("\n" + "=" * 50)
        print("ПОТОЧНИЙ СТАТУС БУДИНКУ")
        print("=" * 50)

        if residents:
            print(f"У будинку {len(residents)} людей:")
            for i, name in enumerate(residents, 1):
                print(f"  {i}. {name}")
        else:
            print("Будинок порожній")
        print()

    def print_history(self, limit: int = 10) -> None:
        print("\n" + "=" * 50)
        print("ІСТОРІЯ ВХОДІВ-ВИХОДІВ")
        print("=" * 50)

        if not self.entries:
            print("Історія порожня\n")
            return


        recent = self.entries[-limit:]

        for entry in reversed(recent):
            emoji = "" if entry['action'].lower() == 'вхід' else ""
            print(f"{emoji} {entry['name']:<20} | {entry['action']:<10} | {entry['timestamp']}")
        print()

def main():
    log = ConciergeLog()

    print("=" * 50)
    print("ДОДАТОК КОНСЬЄРЖА")
    print("=" * 50)

    while True:
        print("\nМЕНЮ:")
        print("1. Зареєструвати вхід")
        print("2. Зареєструвати вихід")
        print("3. Подивитися, хто у будинку")
        print("4. Подивитися історію")
        print("5. Пошук по людині")
        print("0. Вихід")

        choice = input("\nОберіть опцію (0-5): ").strip()

        if choice == "0":
            print("До побачення!")
            break

        elif choice == "1":

            name = input("Введіть ім'я людини: ").strip()
            if name:
                if log.log_entry(name, "вхід"):
                    print(f"{name} зареєстрований вхід")
                    log.print_status()
                else:
                    print("Помилка реєстрації")

        elif choice == "2":

            name = input("Введіть ім'я людини: ").strip()
            if name:
                if log.log_entry(name, "вихід"):
                    print(f"{name} зареєстрований вихід")
                    log.print_status()
                else:
                    print("Помилка реєстрації")

        elif choice == "3":

            log.print_status()

        elif choice == "4":

            try:
                limit = int(input("Скільки останніх записів показати? (за замовчуванням 10): ") or "10")
                log.print_history(limit)
            except ValueError:
                log.print_history()

        elif choice == "5":

            name = input("Введіть ім'я для пошуку: ").strip()
            if name:
                history = log.get_resident_history(name)
                if history:
                    print(f"\nІсторія для {name}:")
                    for entry in history:
                        emoji = "" if entry['action'].lower() == 'вхід' else ""
                        print(f"{emoji} {entry['action']:<10} | {entry['timestamp']}")
                    print()
                else:
                    print(f"Немає записів для {name}\n")

        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
