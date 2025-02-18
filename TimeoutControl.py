from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPalette, QColor, QFont
import time

class TimerThread(QThread):
    update_signal = pyqtSignal(int)
    
    def __init__(self, start_time):
        super().__init__()
        self.time_remaining = start_time
        self.running = False
    
    def run(self):
        self.running = True
        while self.time_remaining > 0 and self.running:
            time.sleep(1)
            self.time_remaining -= 1
            self.update_signal.emit(self.time_remaining)
    
    def stop(self):
        self.running = False
    
    def add_time(self, seconds):
        self.time_remaining += seconds
        self.update_signal.emit(self.time_remaining)
    
    def subtract_time(self, seconds):
        if self.time_remaining > seconds:
            self.time_remaining -= seconds
            self.update_signal.emit(self.time_remaining)

class TimeoutControl(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()
        self.init_threads()

    def init_ui(self):
        # Настройка UI
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        
        # Метки таймеров
        self.timer_labels = [QLabel("Timeout: 5:00", self) for _ in range(3)]
        for label in self.timer_labels:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: white; font-size: 24px; background-color: #FF6347; padding: 10px;")
            label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        
        # Кнопки
        self.start_button = QPushButton("Start All", self)
        self.start_button.clicked.connect(self.start_timers)
        
        self.pause_button = QPushButton("Pause All", self)
        self.pause_button.clicked.connect(self.pause_timers)
        
        self.add_time_button = QPushButton("Add 1 min", self)
        self.add_time_button.clicked.connect(lambda: self.modify_time(60))
        
        self.subtract_time_button = QPushButton("Subtract 1 min", self)
        self.subtract_time_button.clicked.connect(lambda: self.modify_time(-60))
        
        self.end_button = QPushButton("End Timeout", self)
        self.end_button.clicked.connect(self.close)

        # Layout
        layout = QVBoxLayout()
        for label in self.timer_labels:
            layout.addWidget(label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.add_time_button)
        layout.addWidget(self.subtract_time_button)
        layout.addWidget(self.end_button)
        self.setLayout(layout)
        
        self.setWindowTitle("Timeout Control")
        self.setStyleSheet("background-color: #898989")

    def init_threads(self):
        self.threads = [TimerThread(5 * 60) for _ in range(3)]
        for i, thread in enumerate(self.threads):
            thread.update_signal.connect(lambda time, idx=i: self.update_label(idx, time))
    
    def start_timers(self):
        for thread in self.threads:
            if not thread.isRunning():
                thread.start()
    
    def pause_timers(self):
        for thread in self.threads:
            thread.stop()
    
    def modify_time(self, seconds):
        for thread in self.threads:
            if seconds > 0:
                thread.add_time(seconds)
            else:
                thread.subtract_time(abs(seconds))
    
    def update_label(self, index, time_remaining):
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        self.timer_labels[index].setText(f"Timeout: {minutes}:{seconds:02d}")
