from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock


APP_ID = '93b4bc2c1a8637730962f114155febb5'
url = 'http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s'


class WeatherDashboard(BoxLayout):
    degree = NumericProperty(0)
    humid = NumericProperty(0)
    location = StringProperty('Taipei')
    status = StringProperty('Clear') # Clear, Clouds, Rain, Mist
    bg_pic = StringProperty('wether-photos/sunny.jpg')
    weather_icon = StringProperty('icons/clear-256.png')


    def __init__(self, **kwargs):
        super(WeatherDashboard, self).__init__(**kwargs)
        req = UrlRequest(url % ('Taipei', APP_ID), self.got_weather)

    def got_weather(self, req, results):
        temp = results['main']['temp']
        self.degree = int(temp - 273)
        self.humid = results['main']['humidity']
        self.status = results['weather'][0]['main']
        self.change_status()

    def change_status(self):
        if self.status == 'Clear':
            self.bg_pic = 'wether-photos/sunny.jpg'
            self.weather_icon = 'icons/clear-256.png'
        elif self.status == 'Rain':
            self.bg_pic = 'wether-photos/raining.jpg'
            self.weather_icon = 'icons/raining-256.png'
        else:
            self.bg_pic = 'wether-photos/cloudy.jpg'
            self.weather_icon = 'icons/cloudy-256.png'
    
    def change_location(self, cityname):
        self.location = cityname
        req = UrlRequest(url % (cityname, APP_ID), self.got_weather)
        print cityname

    def update(self, dt):
        req = UrlRequest(url % (self.location, APP_ID), self.got_weather)
        print 'update'

class MyApp(App):

    def build(self):
        weatherapp = WeatherDashboard()
        # update every 3 minute
        Clock.schedule_interval(weatherapp.update, 60.0 / 1.0)
        return weatherapp


if __name__ == '__main__':
    MyApp().run()
