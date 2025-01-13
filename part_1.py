from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(
    print_jobs: List[PrintJob], constraints: PrinterConstraints
) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    max_volume = constraints.max_volume
    max_items = constraints.max_items

    # Сортуємо завдання за пріоритетом (1 найвищий, 3 найнижчий)
    print_jobs.sort(key=lambda x: (x.priority, x.print_time))

    grouped_jobs = []
    total_time = 0

    while print_jobs:
        current_group = []
        current_volume = 0
        for job in print_jobs[:]:
            if (
                current_volume + job.volume <= max_volume
                and len(current_group) < max_items
            ):
                current_group.append(job)
                current_volume += job.volume
                print_jobs.remove(job)

        if current_group:
            max_print_time = max(job.print_time for job in current_group)
            total_time += max_print_time
            grouped_jobs.extend(current_group)
        else:
            break

    return {"print_order": [job.id for job in grouped_jobs], "total_time": total_time}


# Тестування


def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        PrintJob(id="M1", volume=100, priority=1, print_time=120),
        PrintJob(id="M2", volume=150, priority=1, print_time=90),
        PrintJob(id="M3", volume=120, priority=1, print_time=150),
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        PrintJob(id="M1", volume=100, priority=2, print_time=120),  # лабораторна
        PrintJob(id="M2", volume=150, priority=1, print_time=90),  # дипломна
        PrintJob(id="M3", volume=120, priority=3, print_time=150),  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        PrintJob(id="M1", volume=250, priority=1, print_time=180),
        PrintJob(id="M2", volume=200, priority=1, print_time=150),
        PrintJob(id="M3", volume=180, priority=2, print_time=120),
    ]

    constraints_test1 = PrinterConstraints(max_volume=300, max_items=2)
    constraints_test2 = PrinterConstraints(max_volume=300, max_items=2)
    constraints_test3 = PrinterConstraints(max_volume=300, max_items=2)

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints_test1)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints_test2)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints_test3)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
