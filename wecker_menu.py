from tkinter import *
#hier sind alle Menuefunktionen 
import RPi.GPIO as GPIO # Buttons
import wecker_helper
import time

def menu_operations (arrs, vars, const):
    print(f"beginn menu-operations; vars.men = {vars.men}") 
    if arrs.sett_wakeuptime[3] == 0:
        if vars.men < 1:
            print("Es ist noch kein Menü geöffnet, HM offen->men == 0")
            if vars.btn == 5:   # HM will be opened   
                print("Hauptmenü öffnen")  
                vars.men = 1
                create_update_mainmen(vars, const)
            if vars.btn == 6:   # Pin_status_exit wurde gedrückt 
                print("exit")
                #if vars.sound_light_thread_run_status == FALSE: #und der Wecker läutet nicht bzw. die threads laufen nicht
                print("Weckerstatus ändern ")
                if arrs.sett_wakeuptime[2] == 0:
                    arrs.sett_wakeuptime[2] = 1
                    vars.pic_Weckezeit = True
                else:
                    arrs.sett_wakeuptime[2] = 0
                    vars.pic_Weckezeit = False
                wecker_helper.weckstatus_ausgeben(vars, arrs)
                wecker_helper.update_settings (arrs, const)
                # else:
                #     print("Wecken beenden")
                #     vars.sound_light_thread_run_status = FALSE
            
        elif vars.men > 0 and vars.men < 10:
            print("Das Hauptmenü ist geöffnet, Settings auswählen -> men == 10 + Menüpunkt")
            if vars.btn == 1:
                print("Pin_up")
                # Hm is open go Settingspoint up
                vars.men = vars.men - 1
                if  vars.men < 1:
                    vars.men = 4 
                create_update_mainmen(vars, const)

            if vars.btn == 2:
                print("Pin_down")
                # Hm is open go Settingspoint down         
                vars.men = vars.men + 1
                if  vars.men > 4:
                    vars.men = 1 
                create_update_mainmen(vars, const)

            if vars.btn == 4:
                print("Pin_right")
                #open the actual settingspoint
                vars.men = (vars.men * 10) + 1
                create_update_settingsmen(arrs, vars, const)

            if vars.btn == 6:   
                print("das Hauptmenü schließen")
                vars.fenster_mainmen.destroy()
                vars.fenster_mainmen = 0
                vars.men = 0

        elif vars.men >= 10 :
            if vars.btn == 6: 
                print("close_Settingsmen + update Settings")
                vars.fenster_settingsmen.destroy()
                vars.fenster_settingsmen = 0
                wecker_helper.update_settings (arrs, const)
                wecker_helper.weckzeit_anzeigen(vars, arrs)
                wecker_helper.show_grafik(vars, arrs)
                vars.men = int(vars.men / 10)
            else:
                print("Ein Settingpunkt ist auswählen -> Settings ändern men == 10 + Menüpunkt)*10 +2")
                # Settings_men is open
                create_update_settingsmen(arrs, vars, const)


#################################################################################################################################            
        # if vars.btn == 6:   #Pin_status_exit wurde gedrückt 
        #     print("exit")
        #     if vars.men < 1 :
        #         if vars.sound_light_thread_run_status == FALSE: #und der Wecker läutet nicht bzw. die threads laufen nicht
        #             print("to do: Weckerstatus ändern ")
        #             if arrs.sett_wakeuptime[2] == 0:
        #                 arrs.sett_wakeuptime[2] = 1
        #             else:
        #                 arrs.sett_wakeuptime[2] = 0
        #             wecker_helper.weckstatus_ausgeben(vars, arrs)
        #             wecker_helper.update_settings (arrs, const)
        #         else:
        #             vars.sound_light_thread_run_status = FALSE
        #     else:
        #         if vars.men < 10:
        #             vars.fenster_mainmen.destroy()
        #             vars.fenster_mainmen = 0
        #             vars.men = 0
        #         else:
        #             print("close_Settingsmen + update Settings")
        #             vars.fenster_settingsmen.destroy()
        #             vars.fenster_settingsmen = 0
        #             wecker_helper.update_settings (arrs, const)
        #             wecker_helper.weckzeit_anzeigen(vars, arrs)
        #             vars.men = int(vars.men / 10)
        # print(f"end menu-operations; vars.men = {vars.men}") 
    else:
        print("Es wird gerade geweckt")
        if vars.btn == 5:
            print("Snooze wurde aktiviert")
            # Sound- und Lichtfunktionen beenden
            # Weckzeit anpassen
            arrs.sett_temp_wakeuptime[1] = int(arrs.sett_temp_wakeuptime[1]) + int(vars.snoozetime)
            if int(arrs.sett_temp_wakeuptime[1]) > 59:
                arrs.sett_temp_wakeuptime[1] = int(arrs.sett_temp_wakeuptime[1]) - 60
                arrs.sett_temp_wakeuptime[0] = int(arrs.sett_temp_wakeuptime[0]) + 1
                if arrs.sett_temp_wakeuptime[0] > 23:
                    arrs.sett_temp_wakeuptime[0] = int(arrs.sett_temp_wakeuptime[0]) - 24
            print("Die neue Weckzeit ist {0} : {1}".format(arrs.sett_temp_wakeuptime[0], arrs.sett_temp_wakeuptime[1]))
        elif vars.btn == 6:
            print("Der Weckvorgang wird abgebrochen") 
        if vars.btn == 5  or vars.btn == 6:
            wecker_helper.Wecksignale_abschalten(vars, arrs, const)
        wecker_helper.weckzeit_anzeigen(vars, arrs)

def create_update_mainmen(vars, const):
    print("create_mainmen")   
    if vars.fenster_mainmen == 0:
        print("new")   
        vars.fenster_mainmen = Canvas(vars.main, bd=5, highlightcolor="blue")
        vars.fenster_mainmen.place(x=10,y=10, width = 200, height=175)
    vars.fenster_mainmen.delete(ALL)
    x = 0
    for text in const.array_menpoints:
        x = x + 1
        if x == vars.men:
            Format = "Arial 13 italic bold"
        else:
            Format = "Arial 13"
        vars.fenster_mainmen.create_text(100 ,x * 35,fill="black",font = Format,#anchor = "e" ,
                            text = text)
    if vars.fenster_mainmen != 0:
        print("update")    
        vars.fenster_mainmen.update()

def create_update_settingsmen(arrs, vars, const):
    print("create_update_settingsmen")
    print(f"vars.men = {vars.men}")
    print("Settingsmenue es gehen rechts, links, up und down")

    #Weckerwerte------------------------------------------------------------------------
    if vars.men > 10 and vars.men < 20:     
        if vars.men == 11:
            print("create_window for_settingsmenue")
            vars.fenster_settingsmen = Canvas(vars.main, bd=5, highlightcolor="blue")
            vars.fenster_settingsmen.place(x = 200,y = const.array_settingpoints[0][0][2], width = const.array_settingpoints[0][0][0], height = const.array_settingpoints[0][0][1])
            vars.men = 12

        else:
            if vars.btn == 1:
                print("Settings_Pin_up")
                if vars.men == 12:
                    arrs.sett_wakeuptime[0] = int(arrs.sett_wakeuptime[0]) + 1
                    if int(arrs.sett_wakeuptime[0]) > 23:
                        arrs.sett_wakeuptime[0] = 0
                else:
                    arrs.sett_wakeuptime[1] = int(arrs.sett_wakeuptime[1]) + 1
                    if int(arrs.sett_wakeuptime[1]) > 59:
                        arrs.sett_wakeuptime[1] = 0
            if vars.btn == 2:
                print("Settings_Pin_down")  
                if vars.men == 12: 
                    arrs.sett_wakeuptime[0] = int(arrs.sett_wakeuptime[0]) - 1
                    if int(arrs.sett_wakeuptime[0]) < 0:
                        arrs.sett_wakeuptime[0] = 23
                else:
                    arrs.sett_wakeuptime[1] = int(arrs.sett_wakeuptime[1]) - 1
                    if int(arrs.sett_wakeuptime[1]) < 0:
                        arrs.sett_wakeuptime[1] = 59
            if vars.btn == 3:
                print("Settings_Pin_left")
                vars.men = vars.men - 1
                if  vars.men < 12:
                    vars.men = 13
            if vars.btn == 4:
                print("Settings_Pin_right")
                vars.men = vars.men + 1
                if vars.men > 13:
                    vars.men = 12
        print(f"Settings_vars.men= {vars.men}")
        print(f"Settings_arrs.sett_wakeuptime[0]= {arrs.sett_wakeuptime[0]}")
        print(f"Settings_arrs.sett_wakeuptime[1]= {arrs.sett_wakeuptime[1]}")
        vars.fenster_settingsmen.delete(ALL)

    #Lichtwerte------------------------------------------------------------------------
    elif vars.men > 20 and vars.men < 30:
        print("Lichteinstellungen")
        if vars.men == 21:
            print("create_window for_settingsmenue")
            vars.fenster_settingsmen = Canvas(vars.main, bd=5, highlightcolor="blue")
            vars.fenster_settingsmen.place(x = 200,y = const.array_settingpoints[1][0][2], width = const.array_settingpoints[1][0][0], height = const.array_settingpoints[1][0][1])
            vars.men = 22

        else:
            if vars.btn == 1:
                print("Settings_Pin_up")
                if vars.men == 22:
                    arrs.sett_brightness[0] = int(arrs.sett_brightness[0]) + 1
                    if arrs.sett_brightness[0] >= int(arrs.sett_brightness[1]):
                        arrs.sett_brightness[0] = 0
                elif vars.men == 23:
                    arrs.sett_brightness[1] = int(arrs.sett_brightness[1]) + 1
                    if arrs.sett_brightness[1] > 100:
                        arrs.sett_brightness[1] = int(arrs.sett_brightness[0]) + 1
                else:
                    arrs.sett_brightness[2] = int(arrs.sett_brightness[2]) + 1
                    if arrs.sett_brightness[2] > 59:
                        arrs.sett_brightness[2] = 0
            if vars.btn == 2:
                print("Settings_Pin_down")  
                if vars.men == 22: 
                    arrs.sett_brightness[0] = int(arrs.sett_brightness[0]) - 1
                    if arrs.sett_brightness[0] < 1:
                        arrs.sett_brightness[0] = int(arrs.sett_brightness[1]) - 1
                elif vars.men == 23:
                    arrs.sett_brightness[1] = int(arrs.sett_brightness[1]) - 1
                    if int(arrs.sett_brightness[1]) <= int(arrs.sett_brightness[0]):
                        arrs.sett_brightness[1] = 100
                else:
                    arrs.sett_brightness[2] = int(arrs.sett_brightness[2]) - 1
                    if arrs.sett_brightness[2] < 0:
                        arrs.sett_brightness[2] = 59
            if vars.btn == 3:
                print("Settings_Pin_left")
                vars.men = vars.men - 1
                if  vars.men < 22:
                    vars.men = 24
            if vars.btn == 4:
                print("Settings_Pin_right")
                vars.men = vars.men + 1
                if vars.men > 24:
                    vars.men = 22
        print(f"Settings_vars.men= {vars.men}")
        vars.fenster_settingsmen.delete(ALL)
        
    #Soundwerte------------------------------------------------------------------------
    elif vars.men > 30 and vars.men < 40:
        print("Soundeinstellungen {0} {1} {2}".format(arrs.sett_audio[1], arrs.sett_audio[2], arrs.sett_audio[3]))
        if vars.men == 31:
            print("create_window for_settingsmenue")
            vars.fenster_settingsmen = Canvas(vars.main, bd=5, highlightcolor="blue")
            vars.fenster_settingsmen.place(x = 200,y = const.array_settingpoints[2][0][2], width = const.array_settingpoints[2][0][0], height = const.array_settingpoints[2][0][1])
            vars.men = 33

        else:
            if vars.btn == 1:
                print("Settings_Pin_up")
                if vars.men == 33:
                    arrs.sett_audio[1] = int(arrs.sett_audio[1]) + 1
                    if arrs.sett_audio[1] >= int(arrs.sett_audio[2]):
                        arrs.sett_audio[1] = 0
                if vars.men == 34:
                    arrs.sett_audio[2] = int(arrs.sett_audio[2]) + 1
                    if arrs.sett_audio[2] > 100:
                        arrs.sett_audio[2] = int(arrs.sett_audio[1]) + 1
                if vars.men == 35:
                    arrs.sett_audio[3] = int(arrs.sett_audio[3]) + 1
                    if arrs.sett_audio[3] > 59:
                        arrs.sett_audio[3] = 0
            if vars.btn == 2:
                print("Settings_Pin_down")  
                if vars.men == 33: 
                    arrs.sett_audio[1] = int(arrs.sett_audio[1]) - 1
                    if arrs.sett_audio[1] < 0:
                        arrs.sett_audio[1] = int(arrs.sett_audio[2]) - 1
                if vars.men == 34:
                    arrs.sett_audio[2] = int(arrs.sett_audio[2]) - 1
                    if arrs.sett_audio[2] <= int(arrs.sett_audio[1]):
                        arrs.sett_audio[2] = 100
                if vars.men == 35:
                    arrs.sett_audio[3] = int(arrs.sett_audio[3]) - 1
                    if arrs.sett_audio[3] < 0:
                        arrs.sett_audio[3] = 59
            if vars.btn == 3:
                print("Settings_Pin_left")
                vars.men = vars.men - 1
                if  vars.men < 33:
                    vars.men = 35
            if vars.btn == 4:
                print("Settings_Pin_right")
                vars.men = vars.men + 1
                if vars.men > 35:
                    vars.men = 33
        print(f"Settings_vars.men= {vars.men}")
        vars.fenster_settingsmen.delete(ALL)

    #Sonstige Werte------------------------------------------------------------------------
    elif vars.men > 40 and vars.men < 50:
        print("Sonstiges") 
        if vars.men == 41:
            print("create_window for_settingsmenue")
            vars.fenster_settingsmen = Canvas(vars.main, bd=5, highlightcolor="blue")
            vars.fenster_settingsmen.place(x = 200,y = const.array_settingpoints[3][0][2], width = const.array_settingpoints[3][0][0], height = const.array_settingpoints[3][0][1])
            vars.men = 42

        else:

            if vars.btn == 1:
                print("Settings_Pin_up")
                if vars.men == 42:
                    arrs.sett_other[0] = int(arrs.sett_other[0]) + 1
                    if arrs.sett_other[0] > 100:
                        arrs.sett_other[0] = 0
                if vars.men == 43:
                    arrs.sett_other[1] = int(arrs.sett_other[1]) + 1
                    if arrs.sett_other[1] > 1:
                        arrs.sett_other[1] = 0

            if vars.btn == 2:
                print("Settings_Pin_down")  
                if vars.men == 42:
                    arrs.sett_other[0] = int(arrs.sett_other[0]) - 1
                    if arrs.sett_other[0] < 0:
                        arrs.sett_other[0] = 100
                if vars.men == 43:
                    arrs.sett_other[1] = int(arrs.sett_other[1]) - 1
                    if arrs.sett_other[1] < 0:
                        arrs.sett_other[1] = 1
            if vars.btn == 3:
                print("Settings_Pin_left")
                vars.men = vars.men - 1
                if  vars.men < 42:
                    vars.men = 43
            if vars.btn == 4:
                print("Settings_Pin_right")
                vars.men = vars.men + 1
                if vars.men > 43:
                    vars.men = 42

        print(f"Settings_vars.men= {vars.men}")
        vars.fenster_settingsmen.delete(ALL)

    make_settings_menue(arrs, vars, const)

def make_settings_menue(arrs, vars, const):
    print("---------make_settings_menue---------------")
    settinglist=[]
    menval_1 = int((vars.men / 10)) - 1
    menval_1_1 = int(vars.men % 10)
    print(f"varsmen = {vars.men}")
    print(f"menval_1 = {menval_1}")
    print(f"menval_1_1 = {menval_1_1}")

    if menval_1 == 0:
        settinglist = arrs.sett_wakeuptime
    elif menval_1 == 1:
        settinglist = arrs.sett_brightness
    elif menval_1 == 2:
        settinglist = arrs.sett_audio
    elif menval_1 == 3:
        settinglist = arrs.sett_other
    settinglistcounter = 0
    counter_1 = 0
    for i in const.array_settingpoints[menval_1]:
        if counter_1 > 0:
            Format = "Arial 13"
            if i[2] == "Wert":
                Wert = settinglist[settinglistcounter]
                settinglistcounter = settinglistcounter + 1
                #print(f"settinglistcounter = {settinglistcounter} menval_1_1 = {menval_1_1}")
                if menval_1_1 == settinglistcounter + 1:
                    Format = "Arial 13 italic bold"
            else:
                Wert = i[2]
            print(i[0], i[1], Wert)
            print(f"Format = {Format}")
            vars.fenster_settingsmen.create_text(i[0],i[1],fill="black" ,font = Format ,anchor = W ,text = Wert)
        counter_1 = counter_1 + 1

def Weckersettings(arrs, vars, const):
    print("------------Weckersettings-----------------")
    #print(f"vars.men = {vars.men}")
    settingslist=[]
    menval_1 = int((vars.men / 10)) - 1
    menval_1_1 = int(vars.men % 10)
    #print(f"menval_1 = {menval_1}")
    #print(f"menval_1_1 = {menval_1_1}")

    counter_1 = 0
    for i in const.array_settingpoints[menval_1]:
        if counter_1 > 0:
            counter_2 = 0
            #print(i)
            for j in i:
                #print(f"counter_1: {counter_1}")
                #print(f"counter_2: {counter_2}")
                if counter_1 == menval_1_1 and counter_2 == 2:
                    text = str(arrs.sett_wakeuptime[menval_1_1 - 2]) + " " + str(j)
                    #print(f"bould-text= {text}")
                    settingslist.append(text)
                    vars.fenster_settingsmen.create_text(settingslist[0],settingslist[1],fill="black" ,font = "Arial 13 italic bold" ,anchor = W ,text = settingslist[2])
                    settingslist.clear()
                    counter_2 = 0
                else:
                    if counter_1 > 1  and counter_2 == 2:
                        val = menval_1_1 *(- 1) + 3
                        #print(f"val={val}")
                        text = str(arrs.sett_wakeuptime[val]) + " " + str(j)
                        #print(f"text= {text}")
                    else:
                        text = str(j)
                    settingslist.append(text)
                    if counter_2 == 2:
                        vars.fenster_settingsmen.create_text(settingslist[0],settingslist[1],fill="black" ,font = "Arial 13" ,anchor = W ,text = settingslist[2])
                        settingslist.clear()
                        counter_2 = 0
                counter_2 = counter_2 + 1
        counter_1 = counter_1 + 1

    #vars.fenster_settingsmen.create_text(const.array_settingpoints[menval_1_1][1][0] ,const.array_settingpoints[menval_1_1][1][1] ,fill="black" ,font = "Arial 13" ,anchor = W ,text = const.array_settingpoints[menval_1_1][1][2])

def lightsettings(arrs, vars, const):
    vars.fenster_settingsmen = Canvas(vars.main, bd=5, highlightcolor="blue")
    vars.fenster_settingsmen.place(x=200,y=70, width = const.array_settingpoints[1][0][0], height = const.array_settingpoints[1][0][1])
    Format = "Arial 13"
    vars.fenster_settingsmen.create_text(const.array_settingpoints[1][1][0] ,const.array_settingpoints[1][1][1] ,fill="black" ,font = Format ,anchor = W ,text = const.array_settingpoints[1][1][2])
    vars.fenster_settingsmen.create_text(const.array_settingpoints[1][2][0] ,const.array_settingpoints[1][2][1] ,fill="black" ,font = Format ,anchor = W ,text = arrs.sett_brightness[0] + " " + const.array_settingpoints[1][2][2])
    vars.fenster_settingsmen.create_text(const.array_settingpoints[1][3][0] ,const.array_settingpoints[1][3][1] ,fill="black" ,font = Format ,anchor = W ,text = arrs.sett_brightness[1])

    vars.fenster_settingsmen.create_text(const.array_settingpoints[1][4][0] ,const.array_settingpoints[1][4][1] ,fill="black" ,font = Format ,anchor = W ,text = const.array_settingpoints[1][4][2])
    vars.fenster_settingsmen.create_text(const.array_settingpoints[1][5][0] ,const.array_settingpoints[1][5][1] ,fill="black" ,font = Format ,anchor = W ,text = arrs.sett_brightness[2] + " " + const.array_settingpoints[1][5][2])

def soundsettings(arrs, vars, const):
    vars.fenster_settingsmen = Canvas(vars.main, bd=5, highlightcolor="blue")
    vars.fenster_settingsmen.place(x=200,y=105, width = const.array_settingpoints[2][0][0], height = const.array_settingpoints[2][0][1])
    Format = "Arial 13"
    vars.fenster_settingsmen.create_text(const.array_settingpoints[2][1][0] ,const.array_settingpoints[2][1][1] ,fill="black" ,font = Format ,anchor = W ,text = const.array_settingpoints[2][1][2])
    vars.fenster_settingsmen.create_text(const.array_settingpoints[2][2][0] ,const.array_settingpoints[2][2][1] ,fill="black" ,font = Format ,anchor = W ,text = arrs.sett_audio[1] + " " + const.array_settingpoints[2][2][2])
    
    vars.fenster_settingsmen.create_text(const.array_settingpoints[2][3][0] ,const.array_settingpoints[2][3][1] ,fill="black" ,font = Format ,anchor = W ,text = const.array_settingpoints[2][3][2])
    vars.fenster_settingsmen.create_text(const.array_settingpoints[2][4][0] ,const.array_settingpoints[2][4][1] ,fill="black" ,font = Format ,anchor = W ,text = arrs.sett_audio[2] + " " + const.array_settingpoints[2][4][2])

    vars.fenster_settingsmen.create_text(const.array_settingpoints[2][5][0] ,const.array_settingpoints[2][5][1] ,fill="black" ,font = Format ,anchor = W ,text = const.array_settingpoints[2][5][2])
    vars.fenster_settingsmen.create_text(const.array_settingpoints[2][6][0] ,const.array_settingpoints[2][6][1] ,fill="black" ,font = Format ,anchor = W ,text = arrs.sett_audio[0] + " " + const.array_settingpoints[2][6][2])

def other_settings(arrs, vars, const):
    vars.fenster_settingsmen = Canvas(vars.main, bd=5, highlightcolor="blue")
    vars.fenster_settingsmen.place(x=200,y=140, width = const.array_settingpoints[3][0][0], height = const.array_settingpoints[3][0][1])
    Format = "Arial 13"
    vars.fenster_settingsmen.create_text(const.array_settingpoints[3][1][0] ,const.array_settingpoints[3][1][1] ,fill="black" ,font = Format ,anchor = W ,text = const.array_settingpoints[3][1][2])
    vars.fenster_settingsmen.create_text(const.array_settingpoints[3][2][0] ,const.array_settingpoints[3][2][1] ,fill="black" ,font = Format ,anchor = W ,text = arrs.sett_wakeuptime[0] + " " + const.array_settingpoints[3][2][2])
    vars.fenster_settingsmen.create_text(const.array_settingpoints[3][3][0] ,const.array_settingpoints[3][3][1] ,fill="black" ,font = Format ,anchor = W ,text = arrs.sett_wakeuptime[1] + " " + const.array_settingpoints[3][3][2])

