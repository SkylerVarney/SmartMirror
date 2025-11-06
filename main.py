import sys
from PySide6.QtWidgets import QApplication
from button_holder import ButtonHolder
from weather_icon import WeatherIcons

app = QApplication(sys.argv)


window = ButtonHolder()
window.show()



app.exec()

#Malgun Gothic 'Corbel'