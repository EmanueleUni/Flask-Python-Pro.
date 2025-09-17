from flask import Blueprint, render_template, request
import requests
from datetime import datetime, timedelta

bp = Blueprint('weather', __name__, template_folder='templates')

API_KEY = '735e51a3dbc75ddee2591fd5f6241fd8'  # inserisci qui la tua chiave

# dizionario traduzioni inglese → italiano
translations = {
    "clear sky": "cielo sereno",
    "few clouds": "poche nuvole",
    "scattered clouds": "nuvole sparse",
    "broken clouds": "nuvoloso",
    "overcast clouds": "coperto",
    "shower rain": "pioggia a rovesci",
    "rain": "pioggia",
    "thunderstorm": "temporale",
    "snow": "neve",
    "light snow": "neve leggera",
    "heavy snow": "neve intensa",
    "mist": "nebbia",
    "fog": "nebbia fitta",
    "haze": "foschia",
    "smoke": "fumo",
    "sand": "sabbia",
    "dust": "polvere",
    "ash": "cenere",
    "squall": "raffica di vento",
    "tornado": "tornado"
}

giorni_settimana = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

@bp.route('/', methods=['GET', 'POST'])
def index():
    previsioni_per_giorno = {}
    error = None
    city = None
    oggi = datetime.now().date().strftime('%d-%m-%Y')
    wd=giorni_settimana[datetime.now().weekday()]
    
    if request.method == 'POST':
        city = request.form.get('city')
        
        
        if city:
            city = city.title()
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                now = datetime.now()
                today = now.date()
                first_row_added = False
        
                for item in data['list']:
                    dt = datetime.fromtimestamp(item['dt'])
                    giorno = dt.date()
        
                    if giorno not in previsioni_per_giorno:
                        previsioni_per_giorno[giorno] = []
        
                    # Prima riga in tempo reale per oggi
                    if giorno == today and not first_row_added:
                        desc = translations.get(item['weather'][0]['description'], item['weather'][0]['description'])
                        previsioni_per_giorno[giorno].append({
                            'giorno_settimana': giorni_settimana[now.weekday()],
                            'ora': now.strftime('%H:%M'),
                            'giorno': now.strftime('%d-%m-%Y'),
                            'temp': item['main']['temp'],
                            'desc': desc
                        })
                        first_row_added = True
        
                    # Poi aggiungi le previsioni a 3 ore
                    if len(previsioni_per_giorno[giorno]) < 8:
                        desc = translations.get(item['weather'][0]['description'], item['weather'][0]['description'])
                        previsioni_per_giorno[giorno].append({
                            'giorno_settimana': giorni_settimana[dt.weekday()],
                            'ora': dt.strftime('%H:%M'),
                            'giorno': dt.strftime('%d-%m-%Y'),
                            'temp': item['main']['temp'],
                            'desc': desc
                        })
        
                    # ferma dopo 3 giorni
                    if len(previsioni_per_giorno) > 3:
                        break
            else:
                error = "Errore nella richiesta alla API"
        else:
            error = "Inserisci una città!"

    return render_template('weather/index.html',
                           previsioni_per_giorno=previsioni_per_giorno,
                           error=error,
                           city=city,oggi=oggi,wd=wd)