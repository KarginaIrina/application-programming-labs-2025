from typing import Optional, Tuple, List


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
import cv2


class ImageBrightnessAnalyzer:
    """
    Класс для анализа яркости изображений, основанный на путях к файлам из CSV.
    """

    def __init__(self, csv_path: str, base_dir: str):
        """
        Инициализация класса с путём к файлу аннотации и с базовой директорией для абсолютных путей.
        """
        self.csv_path = csv_path
        self.base_dir = base_dir
        self.df: pd.DataFrame = pd.DataFrame()

    def load_data(self) -> None:
        """
        Загружает данные из CSV файла и формирует DataFrame с колонками:
        'absolute_path' и 'relative_path'.
        И выводит его.
        """
        try:
            df_raw = pd.read_csv(
                self.csv_path, header=None, names=["absolute_path", "relative_path"]
            )
            self.df = df_raw
            print(self.df)
        except FileNotFoundError:
            raise RuntimeError(f"Файл {self.csv_path} не найден.")
        except pd.errors.ParserError:
            raise RuntimeError(f"Ошибка парсинга файла {self.csv_path}.")

    def get_brightness_range(self, row) -> Optional[str]:
        try:
            bin_size: int = 100
            rel_path = row["relative_path"]
            abs_path = os.path.join(self.base_dir, rel_path)
            img = cv2.imread(rel_path, cv2.IMREAD_COLOR)
            if img is None:
                return None
            brightness = np.mean(img, axis=2)
            avg_brightness = np.mean(brightness)
            bin_start = (int(avg_brightness) // bin_size) * bin_size + 1
            bin_end = bin_start + bin_size - 1
            return f"{bin_start}-{bin_end}"
        except Exception:
            return None

    def compute_brightness_ranges(self) -> None:
        """
        Добавляет колонку с диапазонами яркости изображений.
        """

        self.df["brightness_range"] = self.df.apply(self.get_brightness_range, axis=1)

        # Удаляем строки с отсутствующими диапазонами
        self.df.dropna(subset=["brightness_range"], inplace=True)

    def plot_brightness_histogram(self, save_path: str) -> None:
        """
        Строит и сохраняет гистограмму распределения яркости.
        """
        try:
            counts = (
                self.df["brightness_range"]
                .value_counts()
                .sort_index(key=lambda x: x.map(lambda r: int(r.split("-")[0])))
            )
            plt.figure(figsize=(10, 6))
            counts.plot(kind="bar")
            plt.xlabel("Диапазон яркости")
            plt.ylabel("Количество файлов")
            plt.title("Распределение яркости изображений")
            plt.tight_layout()
            plt.savefig(save_path)
            plt.close()
        except Exception as e:
            raise RuntimeError(f"Ошибка при построении графика: {e}")

    def save_dataframe(self, save_path: str) -> None:
        """
        Сохраняет DataFrame в CSV файл.
        """
        try:
            self.df.to_csv(save_path, index=False)
        except Exception as e:
            raise RuntimeError(f"Ошибка при сохранении DataFrame: {e}")

    def sort_by_brightness_range(self, ascending: bool = True) -> pd.DataFrame:
        """
        Возвращает отсортированный DataFrame по диапазону яркости.
        """

        def range_start(rng: str) -> int:
            return int(rng.split("-")[0])

        return self.df.sort_values(
            by="brightness_range",
            key=lambda col: col.map(range_start),
            ascending=ascending,
        )

    def filter_by_brightness_range(
        self, min_range: Optional[int] = None, max_range: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Возвращает отфильтрованный DataFrame по диапазону яркости.
        """

        def range_start(rng: str) -> int:
            return int(rng.split("-")[0])

        filtered_df = self.df
        if min_range is not None:
            filtered_df = filtered_df[
                filtered_df["brightness_range"].apply(
                    lambda r: range_start(r) >= min_range
                )
            ]
        if max_range is not None:
            filtered_df = filtered_df[
                filtered_df["brightness_range"].apply(
                    lambda r: range_start(r) <= max_range
                )
            ]
        return filtered_df

