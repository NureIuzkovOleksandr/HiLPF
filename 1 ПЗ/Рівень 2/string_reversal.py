def reverse_string(text):
    return text[::-1]

def main():
    test_cases = [
        "hello",
        "world",
        "Python",
        "12345",
        "привіт",
        ""
    ]

    print("=" * 50)
    print("Функція для обернення рядка")
    print("=" * 50)

    for test in test_cases:
        result = reverse_string(test)
        print(f"Вхід: '{test}'")
        print(f"Вихід: '{result}'")
        print("-" * 50)

    print("\nІнтерактивний режим:")

    while True:
        user_input = input("Введіть рядок для обернення: ")
        if user_input.lower() == "exit":
            print("До побачення!")
            break
        result = reverse_string(user_input)
        print(f"Результат: {result}\n")

if __name__ == "__main__":
    main()
