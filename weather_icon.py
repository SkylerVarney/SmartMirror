from PySide6.QtGui import QPixmap
from pathlib import Path

class WeatherIcons():
    def __init__(self):
        super().__init__()

    def weatherIcon(self, code):

        codes = {'01d': 'clear_sky_day', '01n':'clear_sky_night',
                  '02d': 'few_clouds_day', '02n':'few_clouds_night',
                  '03d': 'scattered_clouds', '03n': 'scattered_clouds',
                  '04d':'broken_clouds', '04n': 'broken_clouds',
                  '09d': 'shower_rain_day', '09n': 'shower_rain_night',
                  '10d': 'rain_day', '10n': 'rain_night',
                  '11d': 'thunderstorm_day', '11n': 'thunderstorm_night',
                  '13d': 'snow_day', '13n': 'snow_night',
                  '50d': 'mist_day', '50n': 'mist_night'}
        
        if code in codes:
            weatherCode = codes[code]
        
        icon_path = Path("/Users/skyler/Documents/GitHub/Smart-Mirror/pyside6/weather_icons") / f"{weatherCode}.png"

        pixmap = QPixmap(str(icon_path))

        return pixmap

        

        
