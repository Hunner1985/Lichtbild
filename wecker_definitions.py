"""All definitions for wecker2.py"""

class Arrays:
    def __init__(self):
        print("__init__ array")
        self.Buttonarray = [0] * 6 #Liste mit sechs Listenelementen, in denen die letzten Statis der Buttons steht
        self.sett_wakeuptime = [0] * 4      # h; m; 
                                            # weckerstatus (ob der Wecker an- oder ausgeschalten ist), 
                                            # weckstatus (ob gerade geweckt wird)
                                            # Liste mit vier Elementen (Weckzeit Stunde und Minute, Weckerstatus und weckstatus)
        self.sett_temp_wakeuptime = [0] * 2 # - Aufgrund der Snoozefunktion sollen beim Anzeigen der Weckzeit
                                            # und beim Überprüfen, ob die Weckzeit/Snoozezeit mit der aktuellen Uhrzeit übereinstimmt die sett_wakeuptime auch in die sett_temp_wakeuptimegeschrieben und, ausser im
                                            # Menü überall verwendet werden nach dem Wecken wird die temp wieder mit der wakeuütime überschrieben
        self.sett_brightness = [0] * 3 # Liste mit drei Elementen (Anfangs, Endwert, delta-Einschaltzeit)
        self.sett_audio = [0] * 4   # Liste mit vier Elementen (Musikpfad, Anfangslautst, Endlautst, delta-Einschaltzeit)
        self.sett_other = [0] * 2   # Liste mit zwei Elementen (Displaydimmwert, Format der Logginganzeige)


class Variables:
    def __init__(self ,wert = 0):
        print("__init__ Variables")
        self.men = wert  # 0 ist Ausgangspos. und <0 ist ein und markiert den jweiligen Menüpunkt, war vorher men11 und ist jetzt für men11 und men12 da
        #self.umen = wert  # 0 ist Ausgangspos. und <0 ist ein und markiert den jweiligen Menüpunkt, war vorher men12
        self.btn = wert    # je nach Wert wurde der eine oder der andere Button gedrückt
        self.btn_trk = wert
        #self.noButton_dimm = wert    # zählt hoch, sobald keineTaste gedrückt wird (zum dimmen des Displays), war vorher Buttontrack
        self.fenster = wert    # Für das Hauptfenster
        self.main = wert
        self.fenster_mainmen = wert   # Für das erste Menü, war vorher men1_fenster
        self.fenster_settingsmen = wert

        self.screenwidth = wert
        self.screenhigh = wert
        #self.umen_fenster = wert  # Für das Untermenü, war vorher men11_fenster
        self.Wetter_fenster_1 = wert   # Fenster! zum Anzeigen de ersten Wetterbildes
        self.Wetter_fenster_2 = wert   # Fenster! zum Anzeigen de zweiten Wetterbildes
        self.Wetter_fenster_3 = wert   # Fenster! zum Anzeigen de dritten Wetterbildes

        self.uhr = wert
        self.datum_text = wert
        self.datum = wert
        self.uhr_text = wert    #war vorher zeit
        self.last_min = wert   # zum Vergleichen der Minuten (Weckzeit) mit der Istzeit
        
        self.temperatur = wert
        self.temperaturtext = wert
        self.feuchtigkeit = wert
        self.feuchtigkeitstext = wert
        self.loggergrafik = wert
        
        self.wetter_zeit_1 = wert           
        self.wetter_zeit_2 = wert
        self.wetter_zeit_3 = wert

        self.btn_wait = 0
        self.sound_light_thread_run_status = 0  # 0 = Wecksignale aus
                                                # 2 = Wecker an
        self.last_Buttonpressedtime = 0
        self.Displaydimmstatus = 1
        self.pic_Weckzeit = False   # Hier wird die Referenz zur angezeigten Weckzeit gespeichert
        self.weckstatus = True      # Hier wird die Referenz zum angezeigten Bild vom Weckerstatus gespeichert
        self.Weckdauer_min = 30   
        self.snoozetime = 10

        self.sound_thread = 0
        self.light_thread = 0
        self.server_thread = 0
        self.update_settings = 0
        self.key = None
        self.graph = 0
        self.update = 0 # Wird nur gebraucht, um einen neuen Graph einzubinden, da dies von der main aus geschehen muss
        self.graph_original= 0
        
class Constantes:
    def __init__(self):
        print("__init__ Constantes")
        self.settings_filename = '/home/pi/Projekt/settings.ini'
        self.startsettings = 'startvalues'
        self.logger_filename = 'logger.log'
        self.graph_png = '/home/pi/Projekt/graph.png'
        self.not_changeable_settings = 'not_changable_values'
        #self.MQTT_SERVER = "192.168.3.31"   #die IP-Adresse des ESP vom Lichtbild in Tettenwang
        self.MQTT_SERVER = "192.168.1.10"   #die IP-Adresse des ESP vom Lichtbild in Ingolstadt
        self.MQTT_PATH = "ESP"             #der Pfad des ESP vom Lichtbild
        
        self.PIN_status_exit = 25       	#braun
        self.PIN_up = 23         	        #rot
        self.PIN_left = 22       	        #orange
        self.PIN_enter = 16      	        #schwarz
        self.PIN_right = 27      	        #gelb
        self.PIN_down = 17       	        #grün
        self.Audiopowerpin = 13             #Spannungsversorgung für den Verstärker
        self.Signalpin = 26                 #Leuchtring um Exittaste
        self.Displaydimmpin = 19            #PWM1 pin connected to LED
        #self.Transmitter_datainput = 10    #Pin19
        #self.Receiver_dataoutput = 9      #Pin21
        
        #das erste Teilarray ist immer with, height, y-Pos der Untermenüs
        self.array_menpoints = ["Weckereinstellungen", "Lichteinstellungen", "Soundeinstellungen", "Sonstiges"]

        self.array_settingpoints = [[[200,40,25], [10,20,"Weckzeit:"],[95,20,"Wert"],[125,20,"h"],[145,20,"Wert"],[165,20,"m"]],
                                    [[500,70,60], [10,20,"Helligkeit:"],[135,20,"Wert"],[155,20," -"],[175,20,"Wert"],[10,50,"Einschaltzeit:"],[135,50,"Wert"],[155,50,"Min. bevor der Wecker läutet"]],
                                    [[600,130,125], [10,20,"Musikauswahl:"],[145,20,"Wert"],[10,50,"Anfangslautstärke:"],[160,50,"Wert"],[10,80,"Endlautstärke:"],[155,80,"Wert"],[10,110,"Anstiegszeit:"],[145,110,"Wert"],[170,110,"min. bis Lautstärke erreicht ist"]],
                                    [[250,70,130], [10,20,"Displayhelligkeit:"],[165,20,"Wert"],[10,50,"Logganzeige:"],[165,50,"Wert"]]]
