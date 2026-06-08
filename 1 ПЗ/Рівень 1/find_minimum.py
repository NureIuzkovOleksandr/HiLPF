def find_minimum(a, b, c):
    minimum = min(a, b, c)
    print(minimum)
    return minimum

def main():
    print("=" * 50)
    print("Пошук мінімуму з трьох чисел")
    print("=" * 50)

    test_cases = [
        (10, 20, 30),
        (5, 2, 8),
        (-1, -5, -3),
        (100, 100, 100),
        (3.5, 2.1, 4.9)
    ]

    print("\nПриклади:")
    for a, b, c in test_cases:
        result = find_minimum(a, b, c)
        print(f"min({a}, {b}, {c}) = {result}")

    print("\n" + "=" * 50)
    print("Інтерактивний режим")
    print("=" * 50)
    print("Введіть 'exit' для виходу\n")

    while True:
        try:
            user_input = input("Введіть три числа через пробіл: ").strip()

            if user_input.lower() == "exit":
                print("До побачення!")
                break

            numbers = list(map(float, user_input.split()))

            if len(numbers) != 3:
                print("Помилка: введіть рівно 3 числа\n")
                continue

            a, b, c = numbers
            minimum = find_minimum(a, b, c)
            print(f"Мінімум: {minimum}\n")

        except ValueError:
            print("Помилка: введіть коректні числа\n")

if __name__ == "__main__":
    main()
