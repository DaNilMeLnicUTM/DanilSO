import sys
import threading
from PyQt6.QtWidgets import QApplication
from HockeyMatchUI import HockeyMatchUI

def run_gui():
    app = QApplication(sys.argv)
    window = HockeyMatchUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    gui_thread = threading.Thread(target=run_gui)
    gui_thread.start()
