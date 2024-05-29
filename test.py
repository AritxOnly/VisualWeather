import pyecharts.charts as pc
from ui import ChartDisplay
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    bar = pc.Bar()
    bar.add_xaxis([1, 2, 3, 4, 5])
    bar.add_yaxis('random', [3, 4 , 5, 1, 2])
    bar.render()
    display = ChartDisplay()
    display.setHtml(html='render.html')
    display.show()
    sys.exit(app.exec())