"""
1. Используя данные и аннотацию из второй лабораторной работы, сформировать DataFrame,
который будет содержать 2 колонки - абсолютный и относительный пути к файлу.
2. Произвести именование колонок сформированного DataFrame. Названия колонок должны отражать содержимое данных.
3. Добавить новую колонку согласно варианту.
4. Реализовать функцию сортировки по добавленной колонке.
5. Реализовать функцию фильтрации по добавленной колонке.
6. Отобразить график по добавленной колонке с помощью matplotlib
для всех отсортированных данных (графики и оси должны иметь соответствующие подписи).
7. Сохранить датафрейм и график в файлы.

Вар 7: Добавить колонку со значениями для гистограммы распределения яркости по всем каналам изображения.

Варианты с гистограммой: колонка содержит диапазоны значений (в любом формате), под которые подходит конкретный файл,
например "1-100", "101-200", "201-300" и т.д. Значения диапазонов и их количество выбирать самостоятельно
в зависимости от ваших данных. На графике отображать гистограмму, где ось x - значение диапазона,
ось y - количество файлов, подходящих под этот диапазон.
"""





import matplotlib.pyplot as plt

import argparse

from classIm import (
    ImageBrightnessAnalyzer
)

def parse_arguments() -> argparse.Namespace:
    """
    Передача аргументов через командную строку
    """

    parser = argparse.ArgumentParser(
        description="Гистограмма"
    )
    parser.add_argument('-a', '--annotation', type=str, default='annotation.csv',
                       help='Файл для аннотации (CSV)')
    parser.add_argument('-p', '--processed_annotation', type=str, default='processed_annotation.csv',
                       help='Файл для новой аннотации (CSV)')
    parser.add_argument('-b', '--brightness_histogram', type=str, default='brightness_histogram.png',
                       help='Файл для гистограммы (PNG)')
    parser.add_argument('-f', '--filtered_brightness_histogram', type=str, default='filtered_brightness_histogram.png',
                       help='Файл для отфильтрованной гистограммы (PNG)')
    parser.add_argument('-bd', '--base_dir', type=str, default='',
                       help='Базовая дирриктория')
    return parser.parse_args()


def main():
    try:
        args = parse_arguments()
        analyzer = ImageBrightnessAnalyzer(csv_path=args.annotation, base_dir=args.base_dir)
        analyzer.load_data()
        analyzer.compute_brightness_ranges()
        analyzer.plot_brightness_histogram(save_path=args.brightness_histogram)
        analyzer.save_dataframe(save_path=args.processed_annotation)

        # Пример сортировки
        sorted_df = analyzer.sort_by_brightness_range(ascending=True)

        # Пример фильтрации (например, диапазон от 101 до 200)
        filtered_df = analyzer.filter_by_brightness_range(min_range=101, max_range=200)

        # Построение графика по отфильтрованным данным
        plt.figure(figsize=(10, 6))
        counts_filtered = (
            filtered_df["brightness_range"]
            .value_counts()
            .sort_index(key=lambda x: x.map(lambda r: int(r.split("-")[0])))
        )
        counts_filtered.plot(kind="bar")
        plt.xlabel("Диапазон яркости (отфильтрованные)")
        plt.ylabel("Количество файлов")
        plt.title("Распределение яркости после фильтрации")
        plt.tight_layout()
        plt.savefig(args.filtered_brightness_histogram)
        plt.close()

        print("Обработка завершена успешно.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
