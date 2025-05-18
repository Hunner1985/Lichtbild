import time
import wecker_menu
from tkinter import *
from PIL import Image, ImageTk
import Adafruit_DHT     # 1-Wire Sensor
import RPi.GPIO as GPIO # Buttons
import configparser # Zum Lesen der Configdaten (für's Wetter)
import requests
from datetime import datetime
from urllib.request import urlopen 
import io 
import threading
import vlc
#import pygame
import paho.mqtt.publish as publish # fürs Lichtbild
import matplotlib.pyplot as plt

def set_GPIO(const):
    GPIO.setmode(GPIO.BCM)  # BCM bedeutet dass die Pinnummern wie die GPIO... Bezeichnung ist.
                            # Alternativ gäbe es noch die Pinbezeichnung nach der Pinnreihenfolge am Stecker
    GPIO.setup(const.PIN_up, GPIO.IN)
    GPIO.setup(const.PIN_down, GPIO.IN)
    GPIO.setup(const.PIN_right, GPIO.IN)
    GPIO.setup(const.PIN_left, GPIO.IN)
    GPIO.setup(const.PIN_enter, GPIO.IN)
    GPIO.setup(const.PIN_status_exit, GPIO.IN)
    GPIO.setup(const.Audiopowerpin, GPIO.OUT)
    GPIO.setup(const.Displaydimmpin, GPIO.OUT)
    
    GPIO.output(const.Audiopowerpin, False)
    GPIO.output(const.Displaydimmpin, TRUE)

def setting_for_HumTemp_Sensor(vars):
    # Sensor und Anschluss definieren
    print("define sensor and Pins")
    # Settings for Temperatur-/ Luftfeuchtesensor
    vars.sensor=Adafruit_DHT.DHT11
    # Hier wird der Eingangs-Pin deklariert, an dem der Temperatur-/ Luftfeuchtesensor angeschlossen ist.
    vars.gpio_sense=4

def create_screen_tk(vars):
    print("init Display")
    # Objekt der Klasse Tk erstellt und Fensterüberschrift
    vars.main = Tk()
    vars.screenwidth = vars.main.winfo_screenwidth()
    vars.screenheight =  vars.main.winfo_screenheight()
    vars.main.title("Hunners Wecker")
    geometry = ("{}x{}".format(vars.screenwidth, vars.screenheight))
    print(geometry)
    vars.main.geometry(geometry)

def create_canvas_set_coordinates_and_labels(const,vars, arrs):
    print("create Canvas")
    # Create Canvas
    vars.fenster = Canvas(vars.main, width=0, height=0)
    vars.fenster.pack(fill = "both", expand = 'yes')
  
    # Display image
    path = "/home/pi/Projekt/afrika.png"
    img = Image.open(path)
    img = img.resize((vars.screenwidth,vars.screenheight), Image.ANTIALIAS)
    #img = img.resize((vars.screenwidth,vars.screenheight), PIL.Image.Resampling.LANCZOS)
    vars.bg_img = ImageTk.PhotoImage(img)
    vars.fenster.create_image(0, 0, anchor=NW, image=vars.bg_img)
    displaypositions(vars)
    set_labels(const, vars, arrs)
    #Start the GUI

def displaypositions(vars):
    # Hier werden alle Positionen, an denen dann die Labels und Bilder stehen werden angegeben
    print("set all x/y-positions for the labels")
    vars.x0 = (vars.screenwidth / 2)   #Mittelwert x-Achse
    vars.x_pict1 = (vars.screenwidth / 100) * 54.5  #Anfangs x-Wert Bild1
    vars.x1 = (vars.screenwidth / 100) * 61.3    #Mitte Wetterwerteausgabe_1
    vars.x_pict2 = (vars.screenwidth / 100) * 68.2  #Anfangs x-Wert Bild2
    vars.x2 = (vars.screenwidth / 100) * 75      #Mitte Wetterwerteausgabe_2
    vars.x_pict3 = (vars.screenwidth / 100) * 81.9  #Anfangs x-Wert Bild3
    vars.x3 = (vars.screenwidth / 100) * 88.7    #Mitte Wetterwerteausgabe_3 

    vars.x4 =  int((vars.screenwidth / 100) * 25)       # x-Mittelwert Uhr + Datum + Weckezeit
    vars.x5 =  int((vars.screenwidth / 100) * 19)       # x-Mittelwert Weckerimage
    vars.x6 =  int((vars.screenwidth / 100) * 67)       # x-Mittelwert Humilitytext + Temperaturtext
    vars.x7 =  int((vars.screenwidth / 100) * 85)       # x-Mittelwert Humilitywert + Temperaturwert

    # vars.x8 =  int((vars.screenwidth / 100) * 20)       # x-Mittelwert Debuggausgabe

    vars.y0 = (vars.screenheight / 2)    #Mittelwert y-Achse
    vars.y2 = int((vars.screenheight / 100) * 11.8)   #Anfangs y-Wert Wetter Zeit Ausgabe1
    vars.y3 = int((vars.screenheight / 100) * 14.7)   #Anfangs y-Wert Wetter Bild Ausgabe2 (Bild)
    vars.y4 = int((vars.screenheight / 100) * 36.1)   #Anfangs y-Wert Wetter Temp Ausgabe3
    vars.y5 = int((vars.screenheight / 100) * 42.8)   #Anfangs y-Wert Wetter Rain Ausgabe4

    vars.y6 = int((vars.screenheight / 100) * 22)   # y-Mittelwert Uhr
    vars.y7 = int((vars.screenheight / 100) * 30)   # y-Mittelwert Datum
    vars.y8 = int((vars.screenheight / 100) * 60)   # y-Mittelwert Weckerimage
    vars.y9 = int((vars.screenheight / 100) * 82)   # y-Mittelwert Weckzeit
    vars.y10 = int((vars.screenheight / 100) * 67)   # y-Mittelwert Humilitytext + Temperaturtext
    vars.y11 = int((vars.screenheight / 100) * 77)   # y-Mittelwert Humilitywert + Temperaturwert

    # vars.y12 = int((vars.screenheight / 100) * 50)   # y-Mittelwert Debuggausgabe

def set_labels(const, vars, arrs):
    print("set_labels")
    weckerimg = PhotoImage(file="/home/pi/Projekt/alarmclock.gif")
    vars.weckerimg = weckerimg.subsample(6)
    diagramimg = PhotoImage(file=const.graph_png)
    vars.graph_original = diagramimg
    vars.graph = diagramimg.subsample(2)
    # Hintergründe für  Wetter und
    vars.fenster.create_rectangle( vars.x_pict1 - 10, vars.y2 - 30, vars.x3 + 60 ,vars.y5 + 30, fill="goldenrod3", stipple="gray75", width = 0)
    # Hum, Temp
    vars.fenster.create_rectangle( vars.x6 - 75, vars.y10 - 50, vars.x7 + 75 ,vars.y11 + 60, fill="goldenrod3", stipple="gray75", width = 0)
    #_____________________________________________________________________________________________
    vars.uhr = vars.fenster.create_text(vars.x4,vars.y6,fill="black",font="Arial 46 italic bold",
                        text="Time")
    vars.datum = vars.fenster.create_text(vars.x4,vars.y7,fill="black",font="Arial 30 italic bold",
                            text="Date")
    vars.temperaturtext = vars.fenster.create_text(vars.x6 ,vars.y10,fill="black",font="Arial 20 ",
                            text="    Temp =")
    vars.feuchtigkeitstext = vars.fenster.create_text(vars.x6 ,vars.y11,fill="black",font="Arial 20 ",
                            text="Humidity =")
    vars.temperatur = vars.fenster.create_text(vars.x7,vars.y10,fill="black",font="Arial 30 italic bold",
                            text="Temp")
    vars.feuchtigkeit = vars.fenster.create_text(vars.x7,vars.y11,fill="black",font="Arial 30 italic bold",
                            text="Hum")
    vars.loggergrafik = vars.fenster.create_image(vars.x6 - 75, vars.y10 - 40,image=vars.graph, anchor='nw')
    vars.fenster.itemconfigure(vars.loggergrafik, state='hidden') 
    vars.update = 1
    show_grafik(vars, arrs)
    vars.weckstatus = vars.fenster.create_image(vars.x5,vars.y8,image=vars.weckerimg, anchor='nw')
    vars.pic_weckzeit = vars.fenster.create_text(vars.x4,vars.y9,fill="black",font="Arial 30 italic bold",
                            text="Wake up")  
    vars.wetter_zeit_1 = vars.fenster.create_text(vars.x1,vars.y2, width = 200, fill="black", font="Arial 20 italic", text ="Zeit_1")              
    vars.wetter_zeit_2 = vars.fenster.create_text(vars.x2,vars.y2, width = 200, fill="black", font="Arial 20 italic", text ="Zeit_2")
    vars.wetter_zeit_3 = vars.fenster.create_text(vars.x3,vars.y2, width = 200, fill="black", font="Arial 20 italic", text ="Zeit_3")
   
    vars.wetter_fenster_1 = (Canvas(vars.main))
    vars.wetter_fenster_1.place(x= vars.x_pict1,y= vars.y3, width = vars.screenwidth/7.8, height=vars.screenheight/5.7)
    vars.panel_1 = Label(vars.wetter_fenster_1) 
    vars.panel_1.pack(side="bottom", fill="both", expand="yes")
    vars.wetter_fenster_2 = (Canvas(vars.main))
    vars.wetter_fenster_2.place(x= vars.x_pict2,y= vars.y3, width = vars.screenwidth/7.8, height=vars.screenheight/5.7)
    vars.panel_2 = Label(vars.wetter_fenster_2) 
    vars.panel_2.pack(side="bottom", fill="both", expand="yes")
    vars.wetter_fenster_3 = (Canvas(vars.main))
    vars.wetter_fenster_3.place(x= vars.x_pict3,y= vars.y3, width = vars.screenwidth/7.8, height=vars.screenheight/5.7)
    vars.panel_3 = Label(vars.wetter_fenster_3) 
    vars.panel_3.pack(side="bottom", fill="both", expand="yes")

    vars.wetter_temp_1 = vars.fenster.create_text(vars.x1,vars.y4,width = 200, fill="black", font="Arial 20 italic",text ="Temp_1")
    vars.wetter_temp_2 = vars.fenster.create_text(vars.x2,vars.y4,width = 200, fill="black", font="Arial 20 italic",text ="Temp_2")
    vars.wetter_temp_3 = vars.fenster.create_text(vars.x3,vars.y4,width = 200, fill="black", font="Arial 20 italic",text ="Temp_3")

    vars.wetter_regen_1 = vars.fenster.create_text(vars.x1,vars.y5,width = 200, fill="black", font="Arial 20 italic",text ="Rain_1")
    vars.wetter_regen_2 = vars.fenster.create_text(vars.x2,vars.y5,width = 200, fill="black", font="Arial 20 italic",text ="Rain_2")
    vars.wetter_regen_3 = vars.fenster.create_text(vars.x3,vars.y5,width = 200, fill="black", font="Arial 20 italic",text ="Rain_3")
    
    # vars.Debuggausgabe = vars.fenster.create_text(vars.x8,vars.y12, width = 200, fill="black", font="Arial 20 italic", text ="Debugg") #Debuggausgabefenster

def orientierungslinien(vars):
    print("orientierungslinien zum einrichten")
    vars.fenster.create_line( vars.x0, 0, vars.x0, vars.screenheight, fill="#476042")
    vars.fenster.create_line( 0, vars.y0, vars.screenwidth, vars.y0, fill="#476042")

def read_settings(vars,arrs, const):
    print("read_settings()")
    tempstring = ""
    # Zu Beginn werden alle Einstellungen eingelesen
    #0 = weckzeit
    #1 = weckstatus
    #2 = Helligkeit [1]min [2]max
    #3 = delta_licht
    #4 = musik
    #5 = delta_audio
    #6 = lautst
    #7 = Displayhelligkeit

    parser = configparser.ConfigParser()
    parser.read(const.settings_filename)
    tempstring = parser[const.startsettings]['weckzeit']
    pos = tempstring.index(":")
    arrs.sett_temp_wakeuptime[0] = arrs.sett_wakeuptime[0] = tempstring[0: pos]
    arrs.sett_temp_wakeuptime[1] = arrs.sett_wakeuptime[1] = tempstring[pos + 1 : pos + 3]
    arrs.sett_wakeuptime[2] = parser[const.startsettings]['weckstatus']
    #tempstring = parser[const.startsettings]['helligkeit']
    #pos = tempstring.index("-")
    #arrs.sett_brightness[0] = (tempstring[pos - 1: pos])
    #arrs.sett_brightness[1] = (tempstring[pos + 1: pos + 4])
    arrs.sett_brightness[0] = parser[const.startsettings]['helligkeit_min']
    arrs.sett_brightness[1] = parser[const.startsettings]['helligkeit_max']
    arrs.sett_brightness[2] = parser[const.startsettings]['delta_licht']
    arrs.sett_audio[1]  = parser[const.startsettings]['anfangslautst']
    arrs.sett_audio[2]  = parser[const.startsettings]['endlautst']
    arrs.sett_audio[3]  = parser[const.startsettings]['delta_audio']
    arrs.sett_other[0] = parser[const.startsettings]['displayhelligkeit']
    arrs.sett_other[1] = parser[const.startsettings]['logger']
    #sett_wakeup_statusprint("helligkeit = {}-{}".format(arrs.sett_picture_brightness[0], arrs.sett_picture_brightness[1]))
    vars.Weckdauer_min = int(parser[const.not_changeable_settings]['weckdauer_min'])
    arrs.sett_audio[0] = parser[const.not_changeable_settings]['musik']
    vars.snoozetime = int(parser[const.not_changeable_settings]['snoozetime'])

def update_settings(arrs, const):
    print("update_settings()")
    arrs.sett_temp_wakeuptime[0] = arrs.sett_wakeuptime[0]
    arrs.sett_temp_wakeuptime[1] = arrs.sett_wakeuptime[1]
    update_parser = configparser.ConfigParser()
    update_parser.read(const.settings_filename)
    update = update_parser[const.startsettings]
    update['weckzeit'] = str(Stringzweistellig('{0}'.format(arrs.sett_wakeuptime[0]))) + ":" + str(Stringzweistellig('{0}'.format(arrs.sett_wakeuptime[1])))
    update['weckstatus'] = str(arrs.sett_wakeuptime[2])
    update['helligkeit_min'] = str(arrs.sett_brightness[0])
    update['helligkeit_max'] = str(arrs.sett_brightness[1])
    update['delta_licht'] = str(arrs.sett_brightness[2])
    #update['musik'] = str(arrs.sett_audio[0])
    update['anfangslautst'] = str(arrs.sett_audio[1])
    update['endlautst'] = str(arrs.sett_audio[2])
    update['delta_audio'] = str(arrs.sett_audio[3])
    update['displayhelligkeit'] = str(arrs.sett_other[0])
    update['logger'] = str(arrs.sett_other[1])
    with open(const.settings_filename, 'w') as configfile:
        for section in update_parser.sections():
            configfile.write(f'[{section}]\n')
            for key, value in update_parser[section].items():
                configfile.write(f'{key} = {value}\n')
            configfile.write("\n")  # Fügt eine Leerzeile nach jeder Sektion hinzu    

def makelog(temptext, humtext, const):
    with open(const.logger_filename, "a") as datei: #Text hinten anhängen
        datei.write("\n{0} | {1} | {2}".format((time.strftime('%H-%d.%m.%Y')), temptext, humtext))

def zeitanzeige(arrs, vars, const):
    print("Zeitanzeige")
    counter =3599
    actualize = True
    while True:
        vars.uhr_text = time.strftime('%H:%M:%S')
        vars.fenster.itemconfigure(vars.uhr, text = vars.uhr_text)
        act_hour = int(time.strftime('%H'))
        act_min = int(time.strftime('%M'))
        act_sec = int(time.strftime('%S'))
        if actualize == True:
            actualize = False
            #einmal zu Beginn und dann zu jeder vollen Stunde
            #weckstatus_ausgeben(vars, arrs)
            HumTemp_thread = threading.Thread(target=HumTemp, args=(vars, const))   # Stündlich einmal die Sensordaten lesen
            Wetterdaten_thread = threading.Thread(target=wetterdaten, args=(vars, const))   # und die Wetterdaten aktualisieren
            datumaktuell = time.strftime("%d.%m.%Y")
            vars.fenster.itemconfigure(vars.datum,text = datumaktuell)
            HumTemp_thread.start()
            Wetterdaten_thread.start()
        if act_sec == 0 and act_min == 0:
            print("True")
            actualize = True
        if (act_min != vars.last_min):
            vars.last_min = act_min
            Weckmich(vars, arrs, act_hour, act_min, const)
        #print("Thread_Zeit")
        time.sleep(1)

def Weckmich(vars, arrs, act_hour, act_min, const):
    print("Weckmich")
    print(f"Weckstatus (1= an): {arrs.sett_wakeuptime[2]}")
    print(f"Wecker aktiv (1= an): {arrs.sett_wakeuptime[3]}")
    print ("Weckzeit {0} - {1}".format(arrs.sett_wakeuptime[0], arrs.sett_wakeuptime[1]))
    # wird einmal pro Minute ausgeführt

    if (int(arrs.sett_wakeuptime[2]) >= 1): #Wenn der Wecker aktiv ist 
        print("Weckzeit erreicht: {0}".format(arrs.sett_wakeuptime[3]))
        if int(arrs.sett_wakeuptime[3]) >= 2: # Wenn der Wecker (Lich und Ton) schon läutet

            # berrechnen der Ausschaltzeit
            ausschaltzeit_hour = int(arrs.sett_temp_wakeuptime[0])
            ausschaltzeit_min = int(arrs.sett_temp_wakeuptime[1]) + 30
            if ausschaltzeit_min > 59:
                ausschaltzeit_hour = ausschaltzeit_hour + 1
                ausschaltzeit_min = ausschaltzeit_min - 60

            if (act_hour == ausschaltzeit_hour) and (act_min == ausschaltzeit_min):
                print("Ausschaltzeit erreicht -> Licht und Ton aus")
                Displaydimm(const, vars, arrs)
                thread = threading.Thread(target=Wecksignale_abschalten, args=[vars, arrs, const])
                thread.daemon = True
                thread.start()           # Dann gehen Licht und Ton aus 
                vars.pic_Weckzeit = False

        else:                                       # Der Wecker ist noch aus und hier werden die Licht- und Soundfunktionen gestartet
            print("act_hour = {0} act_min = {1}".format(act_hour, act_min))
            lighttime_hour = soundtime_hour = int(arrs.sett_temp_wakeuptime[0])
            soundtime_min = int(arrs.sett_audio[3])
            lighttime_min = int(arrs.sett_brightness[2])
            #print("delta_sound = {0}".format(int(arrs.sett_audio[1])))
            #print("delta_light = {0}".format(int(arrs.sett_brightness[2])))
            if int(arrs.sett_temp_wakeuptime[1]) - int(arrs.sett_audio[1]) < 0:
                print(int(arrs.sett_temp_wakeuptime[1]) - int(arrs.sett_audio[1]))
                soundtime_hour = int(arrs.sett_temp_wakeuptime[0]) - 1
                if soundtime_hour < 0:
                    soundtime_hour = soundtime_hour * (-1)
                soundtime_min = int(arrs.sett_temp_wakeuptime[1]) + 60 - int(arrs.sett_audio[3])
            else:
                #print("wakeuptime[1]: {0} set_audio[1]: {1}".format(int(arrs.sett_wakeuptime[1]), int(arrs.sett_audio[3])))
                soundtime_min = int(arrs.sett_temp_wakeuptime[1])  - int(arrs.sett_audio[3])
            print("soundtime_hour = {0} soundtime_min = {1}".format(soundtime_hour, soundtime_min))
                
            if int(arrs.sett_temp_wakeuptime[1]) - int(arrs.sett_brightness[2]) < 0:
                lighttime_hour = int(arrs.sett_temp_wakeuptime[0]) - 1
                if lighttime_hour < 0:
                    lighttime_hour = lighttime_hour * (-1)
                lighttime_min = int(arrs.sett_temp_wakeuptime[1]) + 60 - int(arrs.sett_brightness[2])
            else:
                lighttime_min = int(arrs.sett_temp_wakeuptime[1]) - int(arrs.sett_brightness[2])
            print("lighttime_hour = {0} lighttime_min = {1}".format(lighttime_hour, lighttime_min))
            
            if act_hour == soundtime_hour and act_min == soundtime_min:
                print(f"------------------Ton steigt innerhalb von {int(arrs.sett_audio[3])} min. von  {int(arrs.sett_audio[1])} auf {int(arrs.sett_audio[2])}--------") 
                # Und bleibt dann auf dem Level bis Wecker aus geht
                #vars.Weckzeit = True
                arrs.sett_wakeuptime[3] = arrs.sett_wakeuptime[3] + 1
                vars.sound_thread = threading.Thread(target=soundfkt, args=(vars, arrs, const))
                vars.sound_thread.daemon = True
                vars.sound_thread.start()

            if act_hour == lighttime_hour and act_min == lighttime_min:
                print(f"------------------Licht wird innerhalb von {int(arrs.sett_brightness[2])} min. von  {int(arrs.sett_brightness[0])} auf {int(arrs.sett_brightness[1])}--------") 
                # Und bleibt dann auf dem Level bis Wecker aus geht
                #vars.Weckzeit = True
                arrs.sett_wakeuptime[3] = arrs.sett_wakeuptime[3] + 1
                vars.light_thread = threading.Thread(target=lightfkt, args=(vars, arrs, const))
                vars.light_thread.daemon = True
                vars.light_thread.start()
            Displaydimm(const, vars, arrs)
        
def Wecksignale_abschalten(vars, arrs, const):    
    # diese Funktion muss in einem separatem Thread ablaufen,
    # da ansonsten time.sleep auch die GUI anhält
    #vars.Weckzeit = False
    print("Wecksignale_abschalten")
    #print("Exit gedrückt -> Licht und Ton aus")
    while arrs.sett_wakeuptime[3] != 0:
        GPIO.output(const.Audiopowerpin, False)
        print("Verstärker abgeschalten")
        arrs.sett_wakeuptime[3] = 0
    arrs.sett_wakeuptime[3] = 0
    print("Threads beendet")
    
def HumTemp(vars, const, arrs) :
    print("HumTemp")
    # Sensordaten lesen
    humidity, temperature = Adafruit_DHT.read_retry(vars.sensor, vars.gpio_sense)
    if humidity is not None and temperature is not None:
        temptext = ('{0:0.1f} °C'.format(temperature))
        humtext = ('{0:0.1f} %'.format(humidity))
        
        vars.fenster.itemconfigure(vars.temperatur,text = temptext)
        vars.fenster.itemconfigure(vars.feuchtigkeit,text = humtext)
        #Die Werte in die Loggdatei schreiben
        makelog(temptext, humtext, const) 
        #vars.update = 1

def show_grafik(vars, arrs):
    print("show_grafik = {0}".format(int(arrs.sett_other[1])))
    if int(arrs.sett_other[1]) == 0: #Wenn keine Grafik angezeigt werden soll   
        
        vars.fenster.itemconfigure(vars.loggergrafik, state='hidden')          
        vars.fenster.itemconfigure(vars.temperatur, state='normal')
        vars.fenster.itemconfigure(vars.feuchtigkeit, state='normal')
        vars.fenster.itemconfigure(vars.temperaturtext, state='normal')
        vars.fenster.itemconfigure(vars.feuchtigkeitstext, state='normal')
    else:
        vars.fenster.itemconfigure(vars.temperatur, state='hidden')
        vars.fenster.itemconfigure(vars.feuchtigkeit, state='hidden')
        vars.fenster.itemconfigure(vars.temperaturtext, state='hidden')
        vars.fenster.itemconfigure(vars.feuchtigkeitstext, state='hidden')
        vars.fenster.itemconfigure(vars.loggergrafik, state='normal')
        if vars.men == 43:
            vars.update = 1  # Markiert, dass ein neues Bild vorliegt
 

def lese_daten(pfad, anzahl=10):
    daten = []
    with open(pfad, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Entferne Kopfzeile und leere Zeilen
    for line in lines[1:]:
        if line.strip():
            teile = line.strip().split('|')
            if len(teile) == 3:
                datum = teile[0].strip()
                try:
                    temp = float(teile[1].replace('°C', '').strip())
                    hum = float(teile[2].replace('%', '').strip())
                    daten.append((datum, temp, hum))
                except ValueError:
                    continue  # Fehlerhafte Werte überspringen

    return daten[-anzahl:]  # nur die letzten 'anzahl' Zeilen

def create_graph(const, vars):
    print("make graph")

    daten = lese_daten(const.logger_filename)
    temperaturen = [d[1] for d in daten]
    feuchtigkeit = [d[2] for d in daten]
    
    num_points = len(daten)
    fig, ax1 = plt.subplots(figsize=(5, 3))

    ax1.set_ylabel("Temperatur (°C)", color='tab:red', fontsize=8)
    ax1.set_ylim(min(temperaturen) - 0.5, max(temperaturen) + 0.5)
    ax1.plot(range(num_points), temperaturen, color='tab:red', marker='o', linewidth=5)
    ax1.tick_params(axis='y', labelcolor='tab:red', labelsize=7)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Feuchtigkeit (%)", color='tab:blue', fontsize=8)
    ax2.plot(range(num_points), feuchtigkeit, color='tab:blue', marker='s', linewidth=5)
    ax2.tick_params(axis='y', labelcolor='tab:blue', labelsize=7)

    fig.tight_layout()
    plt.title("Raumluft", fontsize=9)
    plt.grid(True)

    try:
        print("Speichere nach:", const.graph_png)
        plt.savefig(const.graph_png, dpi=150)
    except Exception as e:
        print("Fehler beim Speichern:", e)
    finally:
        plt.close("all")
    update_graph(const, vars)

def update_graph(const, vars):
    print("update_graph")
    try:
        # Bild mit PIL öffnen
        bild = Image.open(const.graph_png).convert("RGBA")
        #Hintergrund durchsichtig machen
        neue_pixel = []
        for pixel in bild.getdata():
            # Wenn der Pixel fast weiß ist (Toleranz beachten)
            if pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240:
                neue_pixel.append((255, 255, 255, 0))  # vollständig transparent
            else:
                neue_pixel.append(pixel)

        # Neue Bilddaten anwenden
        bild.putdata(neue_pixel)
        # Bild verkleinern
        faktor = 0.39
        neue_breite = int(bild.width * faktor)
        neue_hoehe = int(bild.height * faktor)
        bild_klein = bild.resize((neue_breite, neue_hoehe), Image.LANCZOS)

        # Für Tkinter vorbereiten
        temp_bild = ImageTk.PhotoImage(bild_klein)

        # Vorherige Anzeige aktualisieren
        if vars.loggergrafik is not None:
            vars.fenster.itemconfig(vars.loggergrafik, image=temp_bild)
        else:
            vars.loggergrafik = vars.fenster.create_image(
                vars.x6 - 75, vars.y10 - 40, image=temp_bild, anchor='nw'
            )

        vars.graph = temp_bild  # Referenz behalten

    except Exception as e:
        print("Fehler bei Bildanzeige:", e)

def Stringzweistellig(String):
    #Diese funktion ist zum umwandeln von evtl. einstelligen Zahlen/Strings zu zweistelligen Strings
    Zahl = int(String)
    if Zahl < 10 and String[0] != '0':
        String = '0{0}'.format(String)
    return String

def wetterdaten(vars, const):
    Regen = '0.0'
    try:
        parser = configparser.ConfigParser()
        parser.read(const.settings_filename)
        vars.api_key = parser['openweathermap']['api']
        vars.city_name = parser['openweathermap']['city']
        vars.url_1 = parser['openweathermap']['url1']
        vars.url_2 = parser['openweathermap']['url2']
        url = ('%s%s%s%s' % (vars.url_1, vars.api_key,vars.url_2, vars.city_name))
        res = requests.get(url)
        data = res.json()
        for i in range( 0, 3):
            date = datetime.fromtimestamp(data['list'][i]['dt'])
            Temperatur = round(data['list'][i]['main']['temp'],1)
            Beschreibung1 = data['list'][i]['weather'][0]['main']
            Bild = data['list'][i]['weather'][0]['icon']
            if (Beschreibung1 == 'Rain'):
                Regen = data['list'][i]['rain']['3h']
            else :
                Regen = 0.0

            image_url = ('http://openweathermap.org/img/wn/{0}@2x.png'.format(Bild))
            my_page = urlopen(image_url)
            # create an image file object
            my_picture = io.BytesIO(my_page.read())
            # use PIL to open image formats like .jpg  .png  .gif  etc.
            pil_img = Image.open(my_picture)
            # convert to an image Tkinter can use
            tk_img = ImageTk.PhotoImage(pil_img)
            if i == 0:
                vars.fenster.itemconfigure(vars.wetter_zeit_1, text = "{0}:{1}".format(Stringzweistellig('{0}'.format(date.hour)), Stringzweistellig('{0}'.format(date.minute))))
                vars.panel_1.configure(image=tk_img)
                vars.panel_1.image = tk_img
                vars.fenster.itemconfigure(vars.wetter_temp_1, text = "{0}°C".format(Temperatur,))
                vars.fenster.itemconfigure(vars.wetter_regen_1, text = "{0}mm".format(Regen))
            if i == 1:
                vars.fenster.itemconfigure(vars.wetter_zeit_2, text = "{0}:{1}".format(Stringzweistellig('{0}'.format(date.hour)), Stringzweistellig('{0}'.format(date.minute))))
                vars.panel_2.configure(image=tk_img)
                vars.panel_2.image = tk_img
                vars.fenster.itemconfigure(vars.wetter_temp_2, text = "{0}°C".format(Temperatur))
                vars.fenster.itemconfigure(vars.wetter_regen_2, text = "{0}mm".format(Regen))
            if i == 2:
                vars.fenster.itemconfigure(vars.wetter_zeit_3, text = "{0}:{1}".format(Stringzweistellig('{0}'.format(date.hour)), Stringzweistellig('{0}'.format(date.minute))))
                vars.panel_3.configure(image=tk_img)
                vars.panel_3.image = tk_img
                vars.fenster.itemconfigure(vars.wetter_temp_3, text = "{0}°C".format(Temperatur))
                vars.fenster.itemconfigure(vars.wetter_regen_3, text = "{0}mm".format(Regen))
        vars.fenster.update()
    except:
        print ("Wetterdaten konnten nicht geladen")

def weckstatus_ausgeben(vars, arrs):    
    #Weckstatus anpassen
    print(f"Weckerstatus {arrs.sett_wakeuptime[2]}")
    if int(arrs.sett_wakeuptime[2]) == 1:
        print("Yes")
        vars.fenster.itemconfigure(vars.weckstatus, state='normal')
        vars.fenster.itemconfigure(vars.pic_weckzeit, state='normal')
    else:
        print("No")
        vars.fenster.itemconfigure(vars.weckstatus, state='hidden')
        vars.fenster.itemconfigure(vars.pic_weckzeit, state='hidden')

def weckzeit_anzeigen(vars, arrs):
    print("Weckzeit in der GUI anzeigen")
    vars.fenster.itemconfigure(vars.pic_weckzeit, text = "{0}:{1}".format(Stringzweistellig('{0}'.format(arrs.sett_temp_wakeuptime[0])), Stringzweistellig('{0}'.format(arrs.sett_temp_wakeuptime[1]))))

def Buttonabfrage(arrs, vars, const):
    # sobald irgendeine Taste gedrückt wurde, wird das Display hochgedimmt
    # wird 5s lang nichts mehr gedrückt, wird das Display wieder heruntergedimmt
    # je nach taste, wir der entsprechende Status/der entsprechende Menüpunkt oder 
    # der entsprechende Wert geändert
    # nach erstmaligen drücken eines Buttons soll 500ms gewartet werden, danach 150ms

    if vars.btn > 0:
        print(f"vars.men = {vars.men}")
        print(f"vars.btn = {vars.btn}")
        vars.last_Buttonpressedtime = 0
        if vars.Displaydimmstatus == 0:
            vars.Displaydimmstatus = 1
            #vars.Weckzeit = False
            Displaydimm(const, vars, arrs) #Display einschalten
        else:
            wecker_menu.menu_operations(arrs, vars, const)
            if vars.men < 1 and vars.btn == 6 and arrs.sett_wakeuptime[3] > 0:
                print("Exit-Taste gedrückt ->Wecksignale abschalten")
                #vars.sound_light_thread_run_status = 0
                Wecksignale_abschalten(vars, arrs, const)
            else:
                if vars.btn_wait == 0:
                    time.sleep(0.8)
                    vars.btn_wait = 1
                else:
                    time.sleep(0.15)
    else:
        time.sleep(0.15)        
        vars.btn_wait = 0
        vars.last_Buttonpressedtime = vars.last_Buttonpressedtime + 1
        if vars.last_Buttonpressedtime >= 30 and vars.Displaydimmstatus == 1: #Ca. 5sek
            vars.Displaydimmstatus = 0
            Displaydimm(const, vars, arrs)  #Display ausschalten

###################################################################################
def Displaydimm(const, vars, arrs):
    #solange die Weckzeit aktiv ist, bleibt das Display an
    print("Displaydimm")
    if arrs.sett_wakeuptime[3] > 0:    
        print("Dimmpin on")
        GPIO.output(const.Displaydimmpin, True) 
    else:
        if vars.Displaydimmstatus == FALSE:
            GPIO.output(const.Displaydimmpin, FALSE) 
        else:
            GPIO.output(const.Displaydimmpin, True) 

def soundfkt(vars, arrs, const):

	print("soundfkt start")
	i = 0
	song = arrs.sett_audio[0]
	valueval = 0.0

	valueval = int(arrs.sett_audio[1])
	delta_lautst = (int(arrs.sett_audio[2]) - int(arrs.sett_audio[1]))
	durchlaeufe_s = int(arrs.sett_audio[3]) * 60 #6 Durchlaeufe/sek (Anstiegszeit)
	lautstaerkenerhoehung = float(delta_lautst / durchlaeufe_s)
	print("delta_lautst. = {0} durchlaeufe_s = {1} lautstaerkenerhoehung = {2}".format(delta_lautst, durchlaeufe_s, lautstaerkenerhoehung)) 
	print("song = {0}".format(song))
	# Creating Instance class object 
	player = vlc.Instance()
	# Creating a new media list 
	media_list = player.media_list_new() 
	# Creating a media player object 
	media_list_player = player.media_list_player_new() 
	# Creating a new media 
	media = player.media_new(song) 
	# Adding media to media list 
	media_list.add_media(media) 
	# Setting media list to the media player 
	media_list_player.set_media_list(media_list) 

	# Create MediaPlayer for volume control
	media_player = player.media_player_new()
	media_player.set_media(media)
	media_list_player.set_media_player(media_player)

	#Verstärker einschalten
	GPIO.output(const.Audiopowerpin, True)
	time.sleep(1)
	#Berechnung, der Lautstärkenerhöhung pro 10s/ start mit 1

	# Musik abspielen in Endlosschleife
	if arrs.sett_wakeuptime[3] > 0:
		media_list_player.set_playback_mode(vlc.PlaybackMode.loop)
		# setting volume
		media_player.audio_set_volume(0)
		# start playing video 
		media_player.play()
	else:
		return

	while i <= durchlaeufe_s and arrs.sett_wakeuptime[3] > 0:
		print("Lautstaerke = {0} i = {1}". format(int(valueval), i))
		# setting volume
		media_player.audio_set_volume(int(valueval))
		valueval = float(valueval + lautstaerkenerhoehung)
		time.sleep(1)
		i = i + 1

	valueval = int(arrs.sett_audio[2]) 
	time.sleep(15)
	print("Lautstaerke = {0}".format(valueval))
	media_player.audio_set_volume(valueval)
	print("sett_wakeuptime[3] = {0}".format(arrs.sett_wakeuptime[3]))
	while arrs.sett_wakeuptime[3] > 0:
		time.sleep(1)
	media_player.audio_set_volume(0)
	media_player.stop()
	print("Soundfkt_ende")

def lightfkt(vars, arrs, const):
    print("lightfkt start")
    # vars.fenster.itemconfigure(vars.Debuggausgabe, text = 'Lichtfunktion_start')

    i = j = k = 0
    delta_v = delta_t = wait_t = sendval = 0,0
    
    #print("delt = {0}".format(i))
    i = int(arrs.sett_brightness[0])    # Minimum
    j = int(arrs.sett_brightness[1])    # Maximum
    k = int(arrs.sett_brightness[2])    # Anstiegszeit in min. ist die Zeit von Minimum bis Maximum (der Wecker läutet)

    print("i = {0} | j = {1} | k = {2}".format(i, j, k))
    # Differenz vom Minimalwert zum Maximalwert
    delta_v = j - i
    # Anstiegszeit in Sekunden
    delta_t = k * 60 
    # Wartezeit zwischen dem Versenden zweier Werte in Sekunden mit drei Nachkommastellen
    wait_t = round(float(delta_t/delta_v ) ,3) 

    print("delta_v = {0} | delta_t = {1} | wait_t = {2}".format(delta_v, delta_t, wait_t))
    # ausgeben der Zeit die zwischen zwei Werten vergeht (+200, damit der esp erkennt, dass es sich hier um den Wert der Anstiegszeit handelt)
    varc = str(wait_t + 200)
    # in sekunden plus drei Nachkommastellen)
    publish.single(const.MQTT_PATH, varc, hostname=const.MQTT_SERVER)
    time.sleep(1)

    # Start der Simulation
    while (i < j) and arrs.sett_wakeuptime[3] > 0:
        varc = str(i)
        # print("varc= {0}".format(varc))
        # vars.fenster.itemconfigure(vars.Debuggausgabe, text = "varc= {0}".format(varc))
        publish.single(const.MQTT_PATH, varc, hostname=const.MQTT_SERVER)
        i = i + 1
        time.sleep(wait_t)   #Sekunden

    publish.single(const.MQTT_PATH, j, hostname=const.MQTT_SERVER)

    while arrs.sett_wakeuptime[3] > 0:
        time.sleep(1)
    varc = "0"
    publish.single(const.MQTT_PATH, varc, hostname=const.MQTT_SERVER)
    print("Lichtfkt_ende")