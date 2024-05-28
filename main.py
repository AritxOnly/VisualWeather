# modules
import sys
from PyQt6.QtWidgets import QApplication

from ui import UserInterface

if __name__ == '__main__':
    # 初始化窗口
    app = QApplication(sys.argv)
    dialog = UserInterface()
    dialog.show()
    sys.exit(app.exec())