import sys
import os
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QFileDialog, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from lab5 import ImageIterator


class MainWindow(QMainWindow):
    """
    Окно приложения для просмотра изображений датасета.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("lab5")
        self.resize(800, 600)

        # Основной виджет и разметка
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        self._layout = QVBoxLayout()
        self._central_widget.setLayout(self._layout)

        # Метка для отображения изображения
        self.image_label = QLabel("Здесь будет отображаться изображение")
        self.image_label.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.image_label)

        # Кнопки
        self.btn_load_annotation = QPushButton("Выбрать файл аннотации")
        self.btn_next = QPushButton("Следующее изображение")
        self.btn_next.setEnabled(False)

        self._layout.addWidget(self.btn_load_annotation)
        self._layout.addWidget(self.btn_next)

        # Обработчики событий
        self.btn_load_annotation.clicked.connect(self.load_annotation_file)
        self.btn_next.clicked.connect(self.show_next_image)

        # Переменные для работы с итератором
        self.iterator: Optional[ImageIterator] = None
        self.annotation_file_path: Optional[str] = None

    def load_annotation_file(self) -> None:
        """
        Открывает диалог для выбора файла annotation.csv и инициализирует итератор.
        """
        try:
            
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите файл annotation.csv", "", "CSV Files (*.csv)"
            )
            if file_path:
                self.annotation_file_path = file_path
                # Инициализация итератора
                self.iterator = ImageIterator(self.annotation_file_path)
                self.iterator.__enter__()
                self.btn_next.setEnabled(True)
                self.image_label.clear()
                self.image_label.setText("Здесь будет отображаться изображение")
                QMessageBox.information(self, "Успех", "Файл аннотации загружен.")
            else:
                QMessageBox.warning(self, "Внимание", "Файл не выбран.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке файла: {e}")

    def show_next_image(self) -> None:
        """
        Получает следующий путь изображения и отображает его.
        """
        if not self.iterator:
            QMessageBox.warning(self, "Внимание", "Загрузите файл аннотации.")
            return

        try:
            image_path = self.iterator.__next__()
            if image_path is None:
                QMessageBox.information(self, "Конец", "Достигнут конец датасета.")
                return

            if not os.path.isabs(image_path):
                base_dir = os.path.dirname(self.annotation_file_path)
                image_path = os.path.join(base_dir, image_path)

            if not os.path.exists(image_path):
                QMessageBox.warning(self, "Предупреждение", f"Изображение не найдено: {image_path}")
                return

            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                QMessageBox.warning(self, "Предупреждение", "Не удалось загрузить изображение.")
                return

            # Масштабируем изображение, сохраняя пропорции
            scaled_pixmap = pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при отображении изображения: {e}")

    def resizeEvent(self, event):
        """
        Обрабатывает изменение размера окна для масштабирования изображения.
        """
        if self.image_label.pixmap():
            self.image_label.setPixmap(
                self.image_label.pixmap().scaled(
                    self.image_label.width(),
                    self.image_label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        super().resizeEvent(event)


def main():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print("Ошибка: ", ex)

if __name__ == "__main__":
    main()
