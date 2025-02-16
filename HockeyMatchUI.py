# main_window.py
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer
from TimeoutControl import TimeoutControl  # Убедитесь, что импорт правильный

class HockeyMatchUI(QWidget):
    def __init__(self):
        super().__init__()

        self.time_remaining = 5 * 60  # 5 минут в секундах
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.real_score_value = 0
        self.liverpool_score_value = 0

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #012345; color: white;")

        # Таймер
        self.timer_label = QLabel("PAUSED: 5'", self)
        self.timer_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("background-color: #FFC107; color: black; padding: 5px;")

        # Логотипы команд
        self.real_logo = QLabel(self)
        self.real_logo.setPixmap(QPixmap("assets/real_madrid.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))

        self.liverpool_logo = QLabel(self)
        self.liverpool_logo.setPixmap(QPixmap("assets/liverpool.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))

        # Названия команд
        self.real_label = QLabel("Real Madrid", self)
        self.liverpool_label = QLabel("Liverpool", self)

        # Счетчик
        self.real_score = QLabel(str(self.real_score_value), self)
        self.liverpool_score = QLabel(str(self.liverpool_score_value), self)
        for label in (self.real_score, self.liverpool_score):
            label.setFont(QFont("Arial", 18, QFont.Weight.Bold))

        # Комбинированные элементы команд
        team1_layout = QHBoxLayout()
        team1_layout.addWidget(self.real_logo)
        team1_layout.addWidget(self.real_label)
        team1_layout.addWidget(self.real_score)

        team2_layout = QHBoxLayout()
        team2_layout.addWidget(self.liverpool_logo)
        team2_layout.addWidget(self.liverpool_label)
        team2_layout.addWidget(self.liverpool_score)

        # Кнопки управления
        self.pause_button = QPushButton("⏸")
        self.play_button = QPushButton("▶")
        self.extra_time_button = QPushButton("➕ Доп. время")
        self.timeout_button = QPushButton("⏳ Тайм-аут")

        self.pause_button.clicked.connect(self.pause_timer)
        self.play_button.clicked.connect(self.start_timer)
        self.extra_time_button.clicked.connect(self.add_extra_time)
        self.timeout_button.clicked.connect(self.open_timeout)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)

        extra_controls = QHBoxLayout()
        extra_controls.addWidget(self.extra_time_button)
        extra_controls.addWidget(self.timeout_button)

        # Основной макет
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.timer_label)
        main_layout.addLayout(team1_layout)
        main_layout.addLayout(team2_layout)
        main_layout.addLayout(control_layout)
        main_layout.addLayout(extra_controls)

        self.setLayout(main_layout)

    def start_timer(self):
        self.timer.start(1000)
        self.timer_label.setText(f"{self.time_remaining // 60}:{self.time_remaining % 60:02d}")

    def pause_timer(self):
        self.timer.stop()
        self.timer_label.setText(f"PAUSED: {self.time_remaining // 60}'")

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.setText(f"{self.time_remaining // 60}:{self.time_remaining % 60:02d}")

    def add_extra_time(self):
        self.time_remaining += 60
        self.timer_label.setText(f"{self.time_remaining // 60}:{self.time_remaining % 60:02d}")

    def open_timeout(self):
        """Открывает окно тайм-аута и останавливает таймер."""

        print("Попытка открыть окно тайм-аута...")  # Отладка

        # Останавливаем основной таймер
        self.pause_timer()

        print("Создаём окно тайм-аута...")  # Отладка
        self.timeout_control_window = TimeoutControl()  # Создаём окно тайм-аута

        print("Показываем окно тайм-аута...")  # Отладка
        self.timeout_control_window.show()
        self.timeout_control_window.raise_()
        self.timeout_control_window.activateWindow()

    def on_timeout_closed(self):
        """Обработчик закрытия окна тайм-аута."""
        #self.timeout_control_window = None
        pass
