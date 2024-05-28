from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget

from datavisualization import Where

class UserInterface(QDialog):
    cities = ['南京', '北京', '上海', '广州', '武汉', '利川']

    def __init__(self, parent: QWidget | None = None, 
                 flags: Qt.WindowType = Qt.WindowType.Dialog) -> None:
        super().__init__(parent, flags)
        self.setupUi()

    def setupUi(self):
        # 初始化UI框架
        mainFrame = QVBoxLayout()
        self.citiesLabel = QLabel('选择城市')
        self.citiesBox = QComboBox()
        self.citiesBox.addItems(UserInterface.cities)

        mainFrame.addWidget(self.citiesLabel)
        mainFrame.addWidget(self.citiesBox)

        dateWidget = QWidget(self)
        dateLayout = QHBoxLayout()
        self.yearBox = QComboBox()
        self.yearBox.addItems(['2022', '2023', '2024'])
        self.yearLabel = QLabel('年')
        self.monthBox = QComboBox()
        self.monthBox.addItems([str(i) for i in range(1, 13, 1)])
        self.monthLabel = QLabel('月')
        dateLayout.addWidget(self.yearBox)
        dateLayout.addWidget(self.yearLabel)
        dateLayout.addWidget(self.monthBox)
        dateLayout.addWidget(self.monthLabel)
        dateWidget.setLayout(dateLayout)

        mainFrame.addWidget(dateWidget)

        self.btnLineChart = QPushButton('生成单月气温分析图（折线）')
        self.btnCmp3DChart = QPushButton('生成年气温变化分析图（3D）')
        self.btnCmpBarChart = QPushButton('生成年平均气温比较图（条形）')
        self.btnCondBarChartM = QPushButton('生成月气象状况统计（条形）')
        self.btnCondBarChartY = QPushButton('生成年气象状况统计（条形）')
        self.btnCondPieChartM = QPushButton('生成月气象状况统计（扇形）')
        self.btnCondPieChartY = QPushButton('生成年气象状况统计（扇形）')
        mainFrame.addWidget(self.btnLineChart)
        mainFrame.addWidget(self.btnCmp3DChart)
        mainFrame.addWidget(self.btnCmpBarChart)
        mainFrame.addWidget(self.btnCondBarChartM)
        mainFrame.addWidget(self.btnCondBarChartY)
        mainFrame.addWidget(self.btnCondPieChartM)
        mainFrame.addWidget(self.btnCondPieChartY)

        self.setLayout(mainFrame)
        self.setFixedSize(self.size())
