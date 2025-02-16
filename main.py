from HockeyMatchUI import HockeyMatchUI

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = HockeyMatchUI()
    window.show()

    sys.exit(app.exec())
