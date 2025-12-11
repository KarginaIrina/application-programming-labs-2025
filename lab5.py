'''
Создать приложение с графическим интерфейсом, позволяющее просматривать датасет из лабораторной работы №2. 
Необходимо создать файл main_window.py в котором будет реализован графический интерфейс вашего приложения. 
Итератор для изображений/аудиофайлов импортировать из файлов второй лабораторной работы. 
Сделать возможность выбора папки датасета или файла аннотации (в зависимости от устройства вашего итератора).

Приложение должно иметь кнопки для получения следующего изображения/аудиофайла из датасета. 
После нажатия на них должен быть получен следующий путь при помощи итератора, 
а затем отображено следующее изображение/аудио из вашего датасета в интерфейсе вашей программы.

Для создания графического интерфейса можно использовать Qt Designer.

Варианты 1-16:

Отобразить изображение исходного размера или меньшего размера с сохранением пропорций (без деформации). 
Для работы с изображением использовать QPixmap.

'''



import csv
from typing import Optional, Iterator


class ImageIterator:
    """
    Итератор по путям к файлам из CSV аннотации
    """

    def __init__(self, annotation_file: str) -> None:
        """
        Инициализация итератора.
        """
        self.annotation_file = annotation_file
        self._file = None
        self._reader: Optional[csv.DictReader] = None
        self._lines: list[dict] = []
        self._index: int = 0

    def __enter__(self):
        """
        Автоматическое открытие файла.
        """
        self._file = open(self.annotation_file, newline='', encoding='utf-8')
        self._reader = csv.DictReader(self._file)
        self._lines = list(self._reader)
        self._index = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
         """
         Закрытие файла при выходе из контекста.
         """
         if self._file:
             self._file.close()

    def __next__(self) -> Optional[str]:
        """
        Получить следующий путь к изображению.
        """
        if self._index >= len(self._lines):
            return None
        row = self._lines[self._index]
        self._index += 1
        return row['абсолютный_путь']
        
    
