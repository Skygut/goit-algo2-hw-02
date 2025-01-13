from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    # Перевірка обмежень
    if length <= 0:
        raise ValueError("Довжина стрижня повинна бути більше 0.")
    if not prices or any(p <= 0 for p in prices):
        raise ValueError(
            "Усі ціни повинні бути більше 0, і масив цін не може бути порожнім."
        )
    if len(prices) < length:
        raise ValueError("Довжина масиву цін повинна відповідати довжині стрижня.")

    memo = {}

    def helper(n):
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = 0
        cuts = []

        for i in range(1, n + 1):
            if i <= len(prices):
                current_profit, current_cuts = helper(n - i)
                current_profit += prices[i - 1]
                if current_profit > max_profit:
                    max_profit = current_profit
                    cuts = current_cuts + [i]

        memo[n] = (max_profit, cuts)
        return memo[n]

    max_profit, cuts = helper(length)
    return {"max_profit": max_profit, "cuts": cuts, "number_of_cuts": len(cuts) - 1}


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    # Перевірка обмежень
    if length <= 0:
        raise ValueError("Довжина стрижня повинна бути більше 0.")
    if not prices or any(p <= 0 for p in prices):
        raise ValueError(
            "Усі ціни повинні бути більше 0, і масив цін не може бути порожнім."
        )
    if len(prices) < length:
        raise ValueError("Довжина масиву цін повинна відповідати довжині стрижня.")

    dp = [0] * (length + 1)
    cuts_table = [[] for _ in range(length + 1)]

    for i in range(1, length + 1):
        for j in range(1, i + 1):
            if j <= len(prices):
                if dp[i] < dp[i - j] + prices[j - 1]:
                    dp[i] = dp[i - j] + prices[j - 1]
                    cuts_table[i] = cuts_table[i - j] + [j]

    return {
        "max_profit": dp[length],
        "cuts": cuts_table[length],
        "number_of_cuts": len(cuts_table[length]) - 1,
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Базовий випадок"},
        {"length": 3, "prices": [1, 3, 8], "name": "Оптимально не різати"},
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Рівномірні розрізи"},
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(test["length"], test["prices"])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")


if __name__ == "__main__":
    run_tests()
