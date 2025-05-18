#Beschreibung:
#Tasten:
#Es gibt sechs Tasten (
#    Bezeichnung | Belegung GPIO | Kabelfarbe
#    PIN_status_exit = 	25       	braun
#    PIN_up = 		    23         	rot
#    PIN_left = 		22       	orange
#    PIN_enter = 		16      	schwarz
#    PIN_right = 		27      	gelb
#    PIN_down = 		17       	grün
# )
# besteht ine vnc-Verbindung, so kann auch mit den Tasten der Tastatur gesteuert werden
#   PIN_enter           'q'
#   PIN_up              'w'
#   PIN_status_exit     'e'
#   PIN_left            'a'
#   PIN_down            's'
#   PIN_right           'd'
#
#Der Temperatur-/Luftfeuchtesensor ist mittels virtual-Wire mit
#   GPIO 4 verbunden
#
#Der Audioverstärker wird über einen Fet an GPIO 19 (13) verorgt
#
#Das Display wird über einen Fet an GPIO 19 verorgt
#Die Dimmfunktion des Displays wird an GPIO 24 (35) mittels PWM erzeugt (aktuell aber nur 1 oder 0)
#
#Die Wetterdaten werden von OpenWeatherMap als Json-Datei heruntergeladen und alle 6 Stunden aktualisiert (reicht völlig)
#
#Das Bild wird mittels MQTT angesteuert,
#dafür wird Mosquitto verwendet. 
#Anleitung unter https://www.elektronik-kompendium.de/sites/raspberry-pi/2709041.htm
#Der Server (Broker) ist auf dem raspberry installiert und die IP-Adresse ist die vom Raspberry.
#Die Kommunikation erfolgt mittels WLAN.
#Für die Uhrzeit wird die Systemzeit verwendet.

#Um Musik abzuspielen wird die Sounddatei mittels vlc wiedergegeben
#Die wiedergabe läuft über eine Usb-Soundkarte
#Das Signal wird mittels eines externen Monoverstärker an zwei kleine Lautsprecher geschickt.
#
#Der 433Mhz-Receiver ist mit GPIO 09 (21) verbunden
#
#Der 433Mhz-Transmitter ist an GPIO 10 (19) angeschlossen

#die letzten 10 werte von humptemp in einer grafik darstellen
# - anlegen einer Loggdatei (logger.log)
# - einfügen eines switch im Menü um die Grafik oder nur die aktuellen Werte im display anzuzeigen (Menü->Sonstiges->Logganzeige; sett_other[1])
# - speichern des werts in der settings.ini (logger =...)
# - beim Erzeugen der GUI eine ausblendbare Fläche für die Grafik erstellen (self.loggergrafik)
# 
#!/usr/bin/python3 
'''imports'''
import wecker_definitions
import wecker_helper
import fileserver_thread
from tkinter import *
import sys
import threading
import Adafruit_DHT     # 1-Wire Sensor
import time
import RPi.GPIO as GPIO # Buttons
import keyboard

#print("Variables created")

###################################################################################
def get_key (event):
    vars.key = event.char
    print("Keythread")
    print(event.char)

def Hauptschleife(vars):
    print("Hauptschleife")
    global update_settings

    while True:

        if (GPIO.input(const.PIN_up) == GPIO.HIGH) or (vars.key == 'w'):
            print("____PIN_up____") #=0
            vars.btn = 1     # War vorher Buttonfkt_high
        elif (GPIO.input(const.PIN_down) == GPIO.HIGH) or (vars.key == 's'):
            print("____PIN_down____")   #=1
            vars.btn = 2
        elif (GPIO.input(const.PIN_left) == GPIO.HIGH) or (vars.key == 'a'):      #Nur wenn kein Menü geöffnet ist kann der Weckstatus geändert werden
            print("____PIN_left____")   #=2
            vars.btn = 3
        elif (GPIO.input(const.PIN_right) == GPIO.HIGH) or (vars.key == 'd'):
            print("____PIN_right____")  #=3
            vars.btn = 4
        elif (GPIO.input(const.PIN_enter) == GPIO.HIGH) or (vars.key == 'q'):
            print("____PIN_enter____")  #=4
            vars.btn = 5
        elif (GPIO.input(const.PIN_status_exit) == GPIO.HIGH) or (vars.key == 'e'):
            print("____PIN_status_exit____")   #=5
            vars.btn = 6
        else:
            vars.btn = 0
        vars.key = None
        wecker_helper.Buttonabfrage(arrs, vars, const)
        if vars.update_settings == 1:
            print("update_settings1")
            vars.update_settings = 0
            wecker_helper.read_settings(vars, arrs, const)
            wecker_helper.Wecksignale_abschalten(vars, arrs, const)
            wecker_helper.weckstatus_ausgeben(vars, arrs)
            wecker_helper.weckzeit_anzeigen(vars, arrs)
        if vars.update == 1:
            vars.update = 0
            vars.main.after(0, wecker_helper.create_graph, const, vars)
        time.sleep(0.15)
        
    #wecker_helper.zeitanzeige(vars)

if __name__ == "__main__":
    '''create variables, arrays and lists'''

    vars = wecker_definitions.Variables()
    arrs = wecker_definitions.Arrays()
    const = wecker_definitions.Constantes()

    vars.update_settings = 0  # Initialisiere das Flag
    
    try:
        print("start_name__")
        arrs.sett_wakeuptime[3] = 0 # Zu beginn ist der Wecker aus
        wecker_helper.set_GPIO(const)
        wecker_helper.read_settings(vars, arrs, const)
        wecker_helper.setting_for_HumTemp_Sensor(vars)
        wecker_helper.create_screen_tk(vars)
        wecker_helper.create_canvas_set_coordinates_and_labels(const, vars, arrs)
        #wecker_helper.orientierungslinien(vars)
        vars.main.bind('q', get_key)
        vars.main.bind('w', get_key)
        vars.main.bind('e', get_key)
        vars.main.bind('a', get_key)
        vars.main.bind('s', get_key)
        vars.main.bind('d', get_key)
        wecker_helper.weckzeit_anzeigen(vars, arrs)
        wecker_helper.HumTemp(vars, const, arrs)
        #wecker_helper.show_grafik(const, vars, arrs)
        # Weckmich()
        #weckzeit_anzeigen()
        # schreibesettings()
        # master.after(1, Soundfkt())  #nur für Test
        # Erzeuge den Thread
        master_thread = threading.Thread(target=Hauptschleife, args=(vars,))
        master_thread.daemon = True
        time_thread = threading.Thread(target=wecker_helper.zeitanzeige, args=(arrs, vars, const))
        time_thread.daemon = True
        vars.sound_light_thread_run_status = FALSE
        vars.server_thread = threading.Thread(target=fileserver_thread.start_server, args=(vars,))
        vars.server_thread.daemon = True
        vars.server_thread.start()
        #s_thread = threading.Thread(target=wecker_helper.soundfkt, args=(vars, arrs,const))
        #s_thread.daemon = True
        #l_thread = threading.Thread(target=wecker_helper.lightfkt, args=(vars, arrs,const))
        #l_thread.daemon = True
        #vars.counter_2 = 0
        #Hauptschleife()

        # Starte den Thread
        master_thread.start()
        time_thread.start()
        #s_thread.start()
        #l_thread.start()
        
        vars.main.mainloop()
    # Aufraeumarbeiten nachdem das Programm händisch beendet wurde
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("mist")
        sys.exit()