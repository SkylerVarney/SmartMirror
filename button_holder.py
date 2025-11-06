from PySide6.QtWidgets import QMainWindow, QPushButton, QToolBar, QLabel, QFrame, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt, QTimer, QTime
from PySide6.QtGui import QColor, QIcon, QPixmap, QImage, QFont, QFontDatabase
from quickstart import calendar
from weather_icon import WeatherIcons

import datetime
import requests

class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.textColor = 'white'
        self.widgetColor = 'black'
        self.labelColor = 'black'
        self.textSize = 1
        self.defaultFont = 'Yu Gothic'
       
        #this is the main window
        self.setWindowTitle("this is window name")
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setStyleSheet("background-color: black;")
        #layout of main window
        layout = QGridLayout(centralWidget)
        centralWidget.setLayout(layout)

      

        #CALENDAR

        #calendar container widget
        calendarWidget = QWidget(centralWidget)
        layout.addWidget(calendarWidget,0, 0, Qt.AlignLeft | Qt.AlignTop)
        calendarWidget.setStyleSheet(f"background-color: {self.widgetColor};")

        #calendar container layout
        self.calendarLayout = QGridLayout(calendarWidget)
        calendarWidget.setLayout(self.calendarLayout)
        self.calendarLayout.setColumnMinimumWidth(1, 20)

        calendarHeader = QLabel("Calendar")
        self.calendarLayout.addWidget(calendarHeader, 0, 0, 1, 3, Qt.AlignLeft)
        calendarHeader.setStyleSheet(f"color: {self.textColor};"
                                     f"background-color: {self.labelColor};"
                                     f"font-size: {self.textSize * 14}pt;"
                                     f"font-family: {self.defaultFont};")
        

        calendarHeaderLine = QLabel(calendarWidget)
        self.calendarLayout.addWidget(calendarHeaderLine, 1, 0, 1, 3)
        calendarHeaderLine.setStyleSheet(f"background-color: {self.textColor};")
        calendarHeaderLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        calendarHeaderLine.setFixedHeight(5)

        self.calendarEvents = calendar()
        self.formatEvents()
        calendarTimer = QTimer(self)
        calendarTimer.timeout.connect(self.formatEvents)
        calendarTimer.start(10000)

        
        
        #CLOCK
    
        #widget to hold the time/date
        timeWidget = QWidget(centralWidget)
        layout.addWidget(timeWidget, 0, 0, Qt.AlignCenter | Qt.AlignTop)
        timeWidget.setStyleSheet(f"background-color: {self.widgetColor};"
                                 "border-radius: 100px")


        #layout within timeWidget
        timeLayout = QGridLayout()
        timeWidget.setLayout(timeLayout)   
        timeLayout.setSpacing(0)     

        #hh:mm time
        self.time = QLabel(timeWidget)
        self.time.setStyleSheet(f"color: {self.textColor};"
                                f"font-size: {self.textSize * 72}pt;"
                                f"background-color: {self.labelColor};"
                                f"font-family: {self.defaultFont};"
                                )
        timeLayout.addWidget(self.time, 0, 0, 1, 2, alignment=Qt.AlignCenter)

        

        #month and date
        self.dayAndDate = QLabel(timeWidget)
        self.dayAndDate.setStyleSheet(f"color: {self.textColor};"
                                      f"font-size: {self.textSize * 28}pt;"
                                      f"background-color: {self.labelColor};"
                                      f"font-family: {self.defaultFont};")
        timeLayout.addWidget(self.dayAndDate, 1, 0, 1, 2, alignment=Qt.AlignCenter)

        #timer to update time every 1sec
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)


        #WEATHER

        self.weatherApiKey = ""

        weatherWidget = QWidget(centralWidget)
        layout.addWidget(weatherWidget,0, 0, Qt.AlignRight | Qt.AlignTop)
        weatherWidget.setStyleSheet(f"background-color: {self.widgetColor};")

        weatherLayout = QGridLayout()
        weatherWidget.setLayout(weatherLayout)   
        weatherLayout.setSpacing(0)

        self.tempLabel = QLabel(weatherWidget)
        self.tempLabel.setStyleSheet(f"color: {self.textColor};"
                                     f"font-size: {self.textSize * 56}pt;"
                                     f"background-color: {self.labelColor};"
                                     f"font-family: {self.defaultFont};")
        weatherLayout.addWidget(self.tempLabel, 0, 0, 2, 1, Qt.AlignCenter)

        self.highLabel = QLabel(weatherWidget)
        self.highLabel.setStyleSheet(f"color: {self.textColor};"
                                     f"font-size: {self.textSize * 20}pt;"
                                     f"background-color: {self.labelColor};"
                                     f"font-family: {self.defaultFont};")
        weatherLayout.addWidget(self.highLabel, 0, 1)

        self.lowLabel = QLabel(weatherWidget)
        self.lowLabel.setStyleSheet(f"color: {self.textColor};"
                                    f"font-size: {self.textSize * 20}pt;"
                                    f"background-color: {self.labelColor};"
                                    f"font-family: {self.defaultFont};")
        weatherLayout.addWidget(self.lowLabel, 1, 1)

        self.weatherCondition = QLabel(weatherWidget)
        self.weatherCondition.setStyleSheet(f"color: {self.textColor};"
                                            f"font-size: {self.textSize * 14}pt;"
                                            f"background-color: {self.labelColor};"
                                            f"font-family: {self.defaultFont};")
        weatherLayout.addWidget(self.weatherCondition, 3, 0, 1, 2, Qt.AlignCenter)

        #weather condition png
        self.image_label = QLabel(weatherWidget)
        weatherLayout.addWidget(self.image_label, 2, 0, 1, 2, Qt.AlignCenter)
        
        

        #get the weather every 5 min        
        self.getWeather()
        weatherTimer = QTimer(self)
        weatherTimer.timeout.connect(self.getWeather)
        weatherTimer.start(300000)

        #STOCK
        
        stockHolder = QWidget(centralWidget)
        layout.addWidget(stockHolder, 0, 0, Qt.AlignBottom | Qt.AlignCenter)
        stockHolder.setStyleSheet(f"background-color: {self.widgetColor};")
        stockLayout = QGridLayout()
        stockHolder.setLayout(stockLayout)

        stockLayout.setColumnMinimumWidth(1, 20)
        stockLayout.setColumnMinimumWidth(3, 20)
        stockLayout.setColumnMinimumWidth(5, 20)

        
        stockAPIKey = ''
        tickers = 'SPY, QQQ, AAPL, NVDA'
        
        
        
        
        stockPrices = requests.get(f"https://api.twelvedata.com/price?symbol={tickers}&apikey={stockAPIKey}")
        eodPrices = requests.get(f"https://api.twelvedata.com/eod?symbol={tickers}&apikey={stockAPIKey}")
        self.eodPrices = eodPrices

        spyPrice = stockPrices.json()['SPY']['price']
        qqqPrice = stockPrices.json()['QQQ']['price']
        aaplPrice = stockPrices.json()['AAPL']['price']
        nvdaPrice = stockPrices.json()['NVDA']['price']

        self.spyClose = 1
        self.qqqClose = 1
        self.aaplClose = 1
        self.nvdaClose = 1

        self.setEOD()


        self.SPYLabel = QLabel(stockHolder)
        stockLayout.addWidget(self.SPYLabel, 0, 0)
        self.SPYLabel.setStyleSheet(f"color: {self.textColor};"
                                    f"font-size: {self.textSize * 18}pt;"
                                    f"background-color: {self.labelColor};"
                                    f"font-family: {self.defaultFont};")
        self.formatGainLoss(self.spyClose, spyPrice, "SPY")

        self.QQQLabel = QLabel(stockHolder)
        stockLayout.addWidget(self.QQQLabel, 0, 2)
        self.QQQLabel.setStyleSheet(f"color: {self.textColor};"
                                    f"font-size: {self.textSize * 18}pt;"
                                    f"background-color: {self.labelColor};"
                                    f"font-family: {self.defaultFont};")
        self.formatGainLoss(self.qqqClose, qqqPrice, "QQQ")

        self.AAPLLabel = QLabel(stockHolder)
        stockLayout.addWidget(self.AAPLLabel, 0, 4)
        self.AAPLLabel.setStyleSheet(f"color: {self.textColor};"
                                    f"font-size: {self.textSize * 18}pt;"
                                    f"background-color: {self.labelColor};"
                                    f"font-family: {self.defaultFont};")
        self.formatGainLoss(self.aaplClose, aaplPrice, "AAPL")

        self.NVDALabel = QLabel(stockHolder)
        stockLayout.addWidget(self.NVDALabel, 0, 6)
        self.NVDALabel.setStyleSheet(f"color: {self.textColor};"
                                    f"font-size: {self.textSize * 18}pt;"
                                    f"background-color: {self.labelColor};"
                                    f"font-family: {self.defaultFont};")
        self.formatGainLoss(self.nvdaClose, nvdaPrice, "NVDA")
        
        
        
        
        
        


    def formatGainLoss(self, oldPrice, dayPrice, ticker):
        dayPrice = round(float(dayPrice), 2)
        oldPrice = round(float(oldPrice), 2)
        percentChange = (dayPrice - oldPrice) / oldPrice * 100
        percentChange = str(round(float(percentChange), 2)) + chr(37)

        getattr(self, ticker + "Label").setText(ticker + " " + percentChange + " " + "(" + str(dayPrice) + ")")

        print("stock formatted")

    def setEOD(self):
        spyClose = self.eodPrices.json()['SPY']['close']
        qqqClose = self.eodPrices.json()['QQQ']['close']
        aaplClose = self.eodPrices.json()['AAPL']['close']
        nvdaClose = self.eodPrices.json()['NVDA']['close']

        self.spyClose = spyClose
        self.qqqClose = qqqClose
        self.aaplClose = aaplClose
        self.nvdaClose = nvdaClose

    def getWeather(self):

        weatherData = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={92115}&units=imperial&APPID={self.weatherApiKey}")

        conditionCode = (weatherData.json()['weather'][0]['icon'])
        self.weatherCondition.setText(weatherData.json()['weather'][0]['description'])


        icons = WeatherIcons()

        pixmap = QPixmap('C:\\Users\\skyle\\OneDrive\\Desktop\\weather_icons\\rain_day')
        pixmap = icons.weatherIcon(conditionCode)
       

        self.image_label.setPixmap(pixmap)

        temp = str(round(weatherData.json()['main']['temp'])) + chr(176)
        high = str(round(weatherData.json()['main']['temp_max'])) + chr(176)
        low = str(round(weatherData.json()['main']['temp_min'])) + chr(176)

        self.tempLabel.setText(temp)
        self.lowLabel.setText("L: " + low)
        self.highLabel.setText("H: " + high)

        print("weather update")


    def showTime(self):
    
            x = datetime.datetime.now()

            month = x.strftime("%B")
            date = x.strftime("%d")
            day = x.strftime("%A")
            self.dayAndDate.setText(day + ", " + month + " " + date)

            hour = x.strftime("%I")
            minute = x.strftime("%M")
            second = x.strftime("%S")
            if hour[0] == '0':
                hour = hour[1:2]
            self.time.setText(hour +":"+ minute)

            #minute before market open, call setEOD
            if (hour+minute+second == '06:29:55'):
                self.setEOD()

            print("time update")


    def formatEvents(self):

        self.calendarEvents.pullCalendarMain()

        for i in range(10):
            eventLabel = getattr(self.calendarEvents, f'eventlabel{i}')
            eventLabel.setStyleSheet(f"color: {self.textColor};"
                                     f"font-size: {self.textSize * 16}pt;"
                                     f"background-color: {self.labelColor};"
                                     f"font-family: {self.defaultFont};")
            self.calendarLayout.addWidget(eventLabel, (i+2), 0)

        for i in range(10):
            timeTill = getattr(self.calendarEvents, f'timeTill{i}')
            timeTill.setStyleSheet(f"color: {self.textColor};"
                                     f"font-size: {self.textSize * 14}pt;"
                                     f"background-color: {self.labelColor};"
                                     f"font-family: {self.defaultFont};")
            self.calendarLayout.addWidget(timeTill, (i+2), 2)

        print('formatted next 10 events')
        