progetto flask:
i file includono anche annotazioni che spiegano i funzioanmenti di alcuni metodi e ogetti.

la struttura è divisa come segue:

flask-tutorial/
│
├── flaskr/                      # Pacchetto principale dell'app Flask
│   ├── __init__.py              # Qui c'è la tua factory create_app()
│   ├── auth.py                  # Blueprint per autenticazione (login, register)
│   ├── db.py                    # Connessione e gestione database
│   ├── weather.py               # Il blueprint per le previsioni meteo
│   ├── quiz.py                  # Il blueprint per i quiz
│   ├── schema.sql               # File SQL per creare le tabelle
│   │
│   ├── static/                  # File statici
│   │   └── style.css
│	  │
│   ├──data/
│	  │	└── questions.json       # Il file con le tue domande del quiz
│   │
│   └── templates/               # Template HTML
│       ├── base.html
│       │
│       ├── auth/                # Template per login e registrazione
│       │   ├── login.html
│       │   └── register.html
│       │
│       │
│       ├── weather/             # Template per le previsioni meteo
│       │   └── index.html
│       │
│       └── quiz/                # Template per il quiz
│           ├── index.html
│           └── placement.html
│
│
├── instance/                    # Configurazione e database runtime
│   └── flaskr.sqlite
│
└──__paycache__/




