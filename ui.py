from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

def indexToCity(index: int):
    from datavisualization import Where
    match index:
        case 0:
            return Where.Nanjing
        case 1:
            return Where.Beijing
        case 2:
            return Where.Shanghai
        case 3:
            return Where.Guangzhou
        case 4:
            return Where.Wuhan
        case 5:
            return Where.Lichuan

class UserInterface(QDialog):
    cities = ['南京', '北京', '上海', '广州', '武汉', '利川']

    def __init__(self, parent: QWidget | None = None, 
                 flags: Qt.WindowType = Qt.WindowType.Dialog) -> None:
        super().__init__(parent, flags)
        self.setWindowTitle('Visual Weather')
        self.setWindowIcon(QIcon('res/logo.png'))
        self.setupUi()
        self.setInteraction()

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
        self.yearBox.addItems(['2021', '2022', '2023', '2024'])
        self.yearLabel = QLabel('年')
        self.monthBox = QComboBox()
        dateLayout.addWidget(self.yearBox)
        dateLayout.addWidget(self.yearLabel)
        dateWidget.setLayout(dateLayout)

        mainFrame.addWidget(dateWidget)

        self.btnRangeBarChart = QPushButton('生成月温度范围在18-26的天数统计柱状图')    # 1
        self.btnRangePieChart = QPushButton('生成高温天气或低温天气统计饼图')    # 2
        self.btnLineChart = QPushButton('生成温差最大月气温分析图') # 3
        self.btnWordCloud = QPushButton('生成年天气状况描述词云图') # 4
        self.btnCmp3DChart = QPushButton('生成年气温变化分析图（3D）')  # 5
        self.btnHeatmap = QPushButton('生成气温热力图')   # 6
        self.btnCmpBarChart = QPushButton('生成年平均气温比较图（条形）')   # 7
        
        mainFrame.addWidget(self.btnRangeBarChart)
        mainFrame.addWidget(self.btnRangePieChart)
        mainFrame.addWidget(self.btnLineChart)
        mainFrame.addWidget(self.btnWordCloud)
        mainFrame.addWidget(self.btnCmp3DChart)
        mainFrame.addWidget(self.btnHeatmap)
        mainFrame.addWidget(self.btnCmpBarChart)

        self.setLayout(mainFrame)
        self.setFixedSize(500, 335)

        self.yearBox.setCurrentIndex(2)

    def setInteraction(self):
        self.btnRangePieChart.clicked.connect(self.generateRangePieChart)
        self.btnRangeBarChart.clicked.connect(self.generateRangeBarChart)
        self.btnLineChart.clicked.connect(self.generateLineChart)
        self.btnWordCloud.clicked.connect(self.generateWordCloud)
        self.btnCmp3DChart.clicked.connect(self.generateCmp3DChart)
        self.btnHeatmap.clicked.connect(self.generateHeatmap)
        self.btnCmpBarChart.clicked.connect(self.generateCmpBarChart)

    def getCustomization(self):
        city_index = self.citiesBox.currentIndex()
        year = self.yearBox.currentText()
        return city_index, year

    def generateRangePieChart(self):
        import datavisualization as dv
        city_index, year = self.getCustomization()
        dv.mainFunc(indexToCity(city_index), dv.GraphType.RangePieChart, year, self)
    
    def generateRangeBarChart(self):
        import datavisualization as dv
        city_index, year = self.getCustomization()
        dv.mainFunc(indexToCity(city_index), dv.GraphType.RangeBarChart, year, self)

    def generateLineChart(self):
        import datavisualization as dv
        city_index, year = self.getCustomization()
        dv.mainFunc(indexToCity(city_index), dv.GraphType.LineChart, year, self)
    
    def generateWordCloud(self):
        import datavisualization as dv
        city_index, year = self.getCustomization()
        dv.mainFunc(indexToCity(city_index), dv.GraphType.WordCloud, year, self)

    def generateCmp3DChart(self):
        import datavisualization as dv
        city_index, year = self.getCustomization()
        dv.mainFunc(indexToCity(city_index), dv.GraphType.Cmp3DChart, year, self)

    def generateHeatmap(self):
        import datavisualization as dv
        city_index, year = self.getCustomization()
        dv.mainFunc(indexToCity(city_index), dv.GraphType.Heatmap, year, self)

    def generateCmpBarChart(self):
        import datavisualization as dv
        city_index, year = self.getCustomization()
        dv.mainFunc(indexToCity(city_index), dv.GraphType.CmpBarChart, year, self)


class ChartDisplay(QMainWindow):
    def __init__(self, parent: QWidget | None = None, 
                 flags: Qt.WindowType = Qt.WindowType.Window) -> None:
        super().__init__(parent, flags)
        self.setWindowTitle('Data Analysis')
        self.setupUi()

    def setupUi(self):
        self.setMinimumSize(920, 540)
        self.webView = QWebEngineView(self)
        self.setCentralWidget(self.webView)

    def setHtml(self, html: str):
        with open(html, 'r', encoding='utf-8') as htmlFile:
            # htmlLines = htmlFile.readlines()
            # htmlContent = '\n'.join(line for line in htmlLines)
            htmlContent = htmlFile.read()
        self.webView.setHtml(htmlContent)
        