from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPalette, QColor, QFont

class TimeoutControl(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.time_remaining = 5 * 60  # Начальное время тайм-аута (5 минут)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # Настройка фона и текста
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))
        self.setPalette(palette)

        # Виджет для отображения времени тайм-аута
        self.timer_label = QLabel(f"Timeout: {self.time_remaining // 60}:{self.time_remaining % 60:02d}", self)
        self.timer_label.setStyleSheet("color: white; font-size: 24px; background-color: #FF6347; padding: 10px;")
        self.timer_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))

        # Кнопки для управления тайм-аута
        button_style = """
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                font-size: 18px;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """

        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet(button_style)
        self.start_button.clicked.connect(self.start_timer)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.setStyleSheet(button_style)
        self.pause_button.clicked.connect(self.pause_timer)

        self.add_time_button = QPushButton("Add 1 min", self)
        self.add_time_button.setStyleSheet(button_style)
        self.add_time_button.clicked.connect(self.add_time)

        self.subtract_time_button = QPushButton("Subtract 1 min", self)
        self.subtract_time_button.setStyleSheet(button_style)
        self.subtract_time_button.clicked.connect(self.subtract_time)

        self.end_button = QPushButton("End Timeout", self)
        self.end_button.setStyleSheet(button_style)
        self.end_button.clicked.connect(self.end_timeout)

        # Размещение виджетов в вертикальном layout
        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.add_time_button)
        layout.addWidget(self.subtract_time_button)
        layout.addWidget(self.end_button)
        self.setLayout(layout)

        self.setWindowTitle("Timeout Control")
        self.setStyleSheet("background-color: #333333;")

    def start_timer(self):
        """Запускает таймер."""
        self.timer.start(1000)

    def pause_timer(self):
        """Останавливает таймер."""
        self.timer.stop()

    def add_time(self):
        """Добавляет 1 минуту ко времени тайм-аута."""
        self.time_remaining += 60  # Добавляем 1 минуту
        self.update_label()

    def subtract_time(self):
        """Уменьшает время тайм-аута на 1 минуту, если это возможно."""
        if self.time_remaining > 60:
            self.time_remaining -= 60  # Уменьшаем на 1 минуту
            self.update_label()

    def end_timeout(self):
        """Закрывает окно тайм-аута."""
        self.timer.stop()
        self.close()

    def update_timer(self):
        """Обновляет время тайм-аута и отображает его."""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_label()
        else:
            self.end_timeout()  # Автоматически закрываем окно по завершении тайм-аута

    def update_label(self):
        """Обновляет текст на метке с временем."""
        self.timer_label.setText(f"Timeout: {self.time_remaining // 60}:{self.time_remaining % 60:02d}")
