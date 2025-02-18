from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from TimeoutControl import TimeoutControl
import random
import time


class MatchThread(QThread):
    update_timer_signal = pyqtSignal(str)
    match_ended_signal = pyqtSignal()

    def __init__(self, time_remaining):
        super().__init__()
        self.time_remaining = time_remaining
        self.running = False

    def run(self):
        self.running = True
        while self.time_remaining > 0 and self.running:
            time.sleep(1)
            self.time_remaining -= 1
            minutes, seconds = divmod(self.time_remaining, 60)
            self.update_timer_signal.emit(f"{minutes}:{seconds:02d}")

        if self.running:
            self.match_ended_signal.emit()

    def stop(self):
        self.running = False


class GoalThread(QThread):
    update_score_signal = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            time.sleep(random.randint(5, 10))  # Гол раз в 5-10 секунд
            if random.random() < 0.5:  # 50% шанс гола
                team = random.choice(["real", "liverpool"])
                self.update_score_signal.emit(team, 1)

    def stop(self):
        self.running = False


class SaveThread(QThread):
    save_signal = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.data = None
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            if self.data:
                with open(self.file_path, "w") as file:
                    file.write(self.data)
                self.data = None
            time.sleep(2)  # Записываем в файл раз в 2 секунды

    def save(self, data):
        self.data = data

    def stop(self):
        self.running = False


class HockeyMatchUI(QWidget):
    def __init__(self):
        super().__init__()

        self.real_score_value = 0
        self.liverpool_score_value = 0
        self.time_remaining = 5 * 60  # 5 минут

        self.match_thread = MatchThread(self.time_remaining)
        self.goal_thread = GoalThread()
        self.save_thread = SaveThread("final_score.txt")

        self.match_thread.update_timer_signal.connect(self.update_timer_label)
        self.match_thread.match_ended_signal.connect(self.end_match)

        self.goal_thread.update_score_signal.connect(self.update_score)

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #012345; color: white;")

        self.timer_label = QLabel("PAUSED: 5'", self)
        self.timer_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("background-color: #FFC107; color: black; padding: 5px;")

        self.real_logo = QLabel(self)
        self.real_logo.setPixmap(QPixmap("assets/real_madrid.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))

        self.liverpool_logo = QLabel(self)
        self.liverpool_logo.setPixmap(QPixmap("assets/liverpool.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))

        self.real_label = QLabel("Real Madrid", self)
        self.liverpool_label = QLabel("Liverpool", self)

        self.real_score = QLabel(str(self.real_score_value), self)
        self.liverpool_score = QLabel(str(self.liverpool_score_value), self)
        for label in (self.real_score, self.liverpool_score):
            label.setFont(QFont("Arial", 18, QFont.Weight.Bold))

        team1_layout = QHBoxLayout()
        team1_layout.addWidget(self.real_logo)
        team1_layout.addWidget(self.real_label)
        team1_layout.addWidget(self.real_score)

        team2_layout = QHBoxLayout()
        team2_layout.addWidget(self.liverpool_logo)
        team2_layout.addWidget(self.liverpool_label)
        team2_layout.addWidget(self.liverpool_score)

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

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.timer_label)
        main_layout.addLayout(team1_layout)
        main_layout.addLayout(team2_layout)
        main_layout.addLayout(control_layout)
        main_layout.addLayout(extra_controls)

        self.setLayout(main_layout)

    def start_timer(self):
        if not self.match_thread.isRunning():
            self.match_thread = MatchThread(self.time_remaining)
            self.match_thread.update_timer_signal.connect(self.update_timer_label)
            self.match_thread.match_ended_signal.connect(self.end_match)
            self.match_thread.start()

            self.goal_thread = GoalThread()
            self.goal_thread.update_score_signal.connect(self.update_score)
            self.goal_thread.start()

            self.save_thread = SaveThread("final_score.txt")
            self.save_thread.start()

    def pause_timer(self):
        self.match_thread.stop()
        self.goal_thread.stop()
        self.save_thread.stop()
        self.timer_label.setText(f"PAUSED: {self.time_remaining // 60}'")

    def update_timer_label(self, time_text):
        self.timer_label.setText(time_text)

    def update_score(self, team, points):
        if team == "real":
            self.real_score_value += points
            self.real_score.setText(str(self.real_score_value))
        else:
            self.liverpool_score_value += points
            self.liverpool_score.setText(str(self.liverpool_score_value))

        # Отправляем обновленный счет в поток сохранения
        self.save_thread.save(f"Final Score: Real Madrid {self.real_score_value} - {self.liverpool_score_value} Liverpool\n")

    def add_extra_time(self):
        self.time_remaining += 60
        self.timer_label.setText(f"{self.time_remaining // 60}:{self.time_remaining % 60:02d}")

    def open_timeout(self):
        self.pause_timer()
        self.timeout_control_window = TimeoutControl()
        self.timeout_control_window.show()
        self.timeout_control_window.raise_()
        self.timeout_control_window.activateWindow()

    def end_match(self):
        self.pause_timer()
        self.timer_label.setText("MATCH ENDED")
