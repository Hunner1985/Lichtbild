import time
import os
from flask import Flask, render_template, request, send_file, render_template_string
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser
from werkzeug.utils import secure_filename


settings_path = '/home/pi/Projekt/settings.ini'     # Pfad zur settings.ini-Datei
picture_path = '/home/pi/Projekt/graph.png'         # Pfad zur Logggergrafik

def start_server(vars):
    print("Start server")  # Debug-Ausgabe
    app = Flask(__name__)

    # Flask-Routen
    @app.route('/bild')
    def zeige_bild():
        return send_file(picture_path, mimetype='image/png')
    @app.route('/', methods=['GET', 'POST'])
    def index():
        config = configparser.ConfigParser()
        config.read(settings_path)

        # Werte aus der settings.ini lesen
        weckzeit = config.get('startvalues', 'weckzeit')
        weckstatus = config.get('startvalues', 'weckstatus')

        # Konvertiere die notwendigen Werte in int
        helligkeit_min = int(config.get('startvalues', 'helligkeit_min'))
        helligkeit_max = int(config.get('startvalues', 'helligkeit_max'))
        delta_licht = int(config.get('startvalues', 'delta_licht'))
        anfangslautst = int(config.get('startvalues', 'anfangslautst'))
        endlautst = int(config.get('startvalues', 'endlautst'))  # Korrigierte Schreibweise
        delta_audio = int(config.get('startvalues', 'delta_audio'))
        displayhelligkeit= int(config.get('startvalues', 'displayhelligkeit'))
        logger= int(config.get('startvalues', 'logger'))
        error_message = None  # Fehlernachricht initialisieren

        # POST-Request verarbeiten
        if request.method == 'POST':
            weckzeit = request.form.get('weckzeit', weckzeit)
            weckstatus = '1' if request.form.get('weckstatus') == 'on' else '0'
            logger = '1' if request.form.get('logger') == 'on' else '0'

            # Helligkeit und Lautstärke sicher konvertieren
            try:
                helligkeit_min = int(request.form.get('helligkeit_min', helligkeit_min))
                helligkeit_max = int(request.form.get('helligkeit_max', helligkeit_max))
                delta_licht = int(request.form.get('delta_licht', delta_licht))
                anfangslautst = int(request.form.get('anfangslautst', anfangslautst))
                endlautst = int(request.form.get('endlautst', endlautst))  # Korrigierte Schreibweise
                delta_audio = int(request.form.get('delta_audio', delta_audio))
                displayhelligkeit = int(request.form.get( 'displayhelligkeit', displayhelligkeit))
                
                # Eingaben validieren
                if helligkeit_min >= helligkeit_max:
                    error_message = "Helligkeit Min muss kleiner sein als Helligkeit Max."
                elif anfangslautst >= endlautst:
                    error_message = "Anfangslautstärke muss kleiner sein als Endlautstärke."
                else:
                    # Speichern der veränderten Werte in der settings.ini
                    config.set('startvalues', 'weckzeit', weckzeit)
                    config.set('startvalues', 'weckstatus', weckstatus)
                    config.set('startvalues', 'helligkeit_min', str(helligkeit_min))
                    config.set('startvalues', 'helligkeit_max', str(helligkeit_max))
                    config.set('startvalues', 'delta_licht', str(delta_licht))
                    config.set('startvalues', 'anfangslautst', str(anfangslautst))
                    config.set('startvalues', 'endlautst', str(endlautst))  # Korrigierte Schreibweise
                    config.set('startvalues', 'delta_audio', str(delta_audio))
                    config.set('startvalues', 'displayhelligkeit', str(displayhelligkeit))  
                    config.set('startvalues', 'logger', str(logger))
                               
                    with open(settings_path, 'w') as configfile:
                        config.write(configfile)

            except ValueError as e:
                error_message = f"Ein Fehler ist aufgetreten: {str(e)}"

        return render_template('index.html', weckzeit=weckzeit, weckstatus=weckstatus,
                               helligkeit_min=helligkeit_min, helligkeit_max=helligkeit_max,
                               delta_licht=delta_licht, anfangslautst=anfangslautst,
                               endlautst=endlautst, delta_audio=delta_audio, displayhelligkeit=displayhelligkeit, 
                               logger=logger, error_message=error_message)  # Fehlernachricht übergeben

    # Überwacht die Änderungen an der settings.ini
    class SettingsFileHandler(FileSystemEventHandler):
        def __init__(self):
            self.last_modified_time = 0
            self.debounce_delay = 1

        def on_modified(self, event):
            if event.src_path == settings_path:
                current_time = time.time()
                if current_time - self.last_modified_time > self.debounce_delay:
                    self.last_modified_time = current_time
                    print("Die settings.ini wurde geändert!")
                    vars.update_settings = 1  # Setze das Flag

    # Initialisiere den Event-Handler und den Observer
    event_handler = SettingsFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(settings_path), recursive=False)
    observer.start()

    try:
        # Flask startet auf allen Schnittstellen des Raspberry Pi (0.0.0.0)
        print("Starting Flask server...")
        app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
    finally:
        observer.stop()
        observer.join()
