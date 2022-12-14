#!/usr/bin/python
"""BKTEL PHOTONICS
Title   = 16x2 characters display control
Author  = Cyril Le Goas
Date    = 23/06/2016"""
version = '1.6'
imports = {}
baseurl = "http://localhost:80"
password = "MjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzM="

import time, sys
try:
    import Adafruit_CharLCD as LCD
    imports['LCD'] = True
except:
    print "WARN: Using fake LCD"
    import pygame
    import fakelcd
    imports['LCD'] = False
try:
    import RPi.GPIO as GPIO
    imports['GPIO'] = True
except:
    import fakegpio
    GPIO = fakegpio.FakeGPIO()
    print "WARN: Using fake event handler"
    imports['GPIO'] = False

import requests
import requests.auth
import requests.utils
from base64 import b64encode, b64decode
import hashlib

# CLASS
class CustomAuth(requests.auth.HTTPBasicAuth):

    def __init__(self, username, p):
        self.username = username
        self.p = p

    def __call__(self, r):
        authstr = 'x-basic ' + requests.utils.to_native_string(b64encode(('%s:%s' % (self.username, b64decode(self.p))).encode('latin1')).strip())
        r.headers['authorization'] = authstr
        return r
  
class Resource(object):
    def __init__(self, url):
        self.auth = CustomAuth("admin", password)
        self.url = url
        self.data = {}
        self.load()

    def load(self):
        print "GET(%s)" % (self.url)
        r = requests.get(self.url, auth=self.auth)
        if r.status_code != 200:
            return
        d = r.json()
        if isinstance(d, dict):
            self.data = { str(key):value for key, value in d.items() }
        else:
            self.data = d

    def __getitem__(self, key):
        return self.data[key]


class Parameters(Resource):
    """
    .time_stamp: last time value 
    .screen_update: define if an update is needed or not
    .current_screen: screen postition 
    .number_of_edfa: define the number of edfa in the rack
    """
    def __init__(self):
        self.time_stamp        		= time.time()
        self.screen_update     		= True
        self.current_screen    		= 0
        super(Parameters, self).__init__(baseurl + "/api/mcu")

    def __getitem__(self, key):
        if key == 'number_of_edfa':
            return len(self.data)
        else:
            super(Parameters, self).__getitem__(key)

    
class Info(Resource):
    """
    .serialnum : unit serial number
    .partnum : unit part number
    .date : production date
    .vendor : vendor name, string used during boot
    .hard : hardware version
    .soft : software version
    """
    def __init__(self):
        super(Info, self).__init__(baseurl + "/api2/edfa")

    
class SetAction(object):
    """
    .cursor_position: define the position of the cursor and which digit will be modified
    .temp_value:
    .flag: flag is set when the set button is pressed and clear when it's pressed another time
    """
    def __init__(self):
        self.cursor_position 	= 4
        self.temp_value 	= 0
        self.flag 		= False
        self.settable_value	= 0

    
class Screen(object):
    """
    .page_position: current page position
    .string_page1: default string for page 1
    .string_page2: default string for page 2
    .string_page3: default string for page 3 
    .string_page4: default string for page 4
    .string_page5: default string for page 5 
    .number_of_page: define the number of page for the screen X
    .TB_enabled: define if the top and bot buttons are enabled
    .SET_enabled: define if the set button is enabled
    """
    def __init__(self,string_page1,string_page2,string_page3,string_page4,string_page5,number_of_page,TB_enabled,SET_enabled):
        self.page_position 	= 1
        self.string_page1	= string_page1
        self.string_page2	= string_page2
        self.string_page3	= string_page3
        self.string_page4	= string_page4
        self.string_page5	= string_page5
        self.number_of_page	= number_of_page
        self.TB_enabled    	= TB_enabled
        self.SET_enabled   	= SET_enabled

class EDFA(Resource):
    """
    .mode: edfa operating mode
    .max_current_LD1: edfa maximum laser 1 current
    .max_current_LD2: edfa maximum laser 2 current
    .min_pc: edfa minimum pc setpoint
    .max_pc: edfa maximum pc setpoint
    .min_gc: edfa minimum gc setpoint
    .max_gc: edfa maximum gc setpoint
    .number_of_laser: number of optical stage
    .has_settable_LD1 : define if LD1 bias current is settable by the customer
    .alarms: edfa alarms
    .LD1_current: laser 1 current
    .LD2_current: laser 2 current
    .input_power: edfa optical input power
    .output_power: edfa optical output power
    .internal_temp: edfa internal temperature
    .CC1_setpoint: laser 1 current setpoint
    .CC2_setpoint: laser 2 current setpoint
    .PC_setpoint: pc mode setpoint
    .GC_setpoint: gc mode setpoint
    .has_PC_mode:
    .has_GC_mode:
    .has_output_PD:
    .has_input_PD:
    """
    def __init__(self, index):
        super(EDFA, self).__init__(baseurl + "/api2/mcu/%d" % (index))

    def update(self, d):
        print "POST(%s, %s)" % (self.url, d)
        requests.post(self.url, json=d, auth=self.auth)
    
    
# FUNCTIONS
def draw_screen(type):
    lcd.clear()
    if type.page_position == 1:
        lcd.message(type.string_page1)
    elif type.page_position == 2:
        lcd.message(type.string_page2)
    elif type.page_position == 3:
        lcd.message(type.string_page3)
    elif type.page_position == 4:
        lcd.message(type.string_page4)
    elif type.page_position == 5:
        lcd.message(type.string_page5)
    Param.screen_update = False

def fill_with_blank(value):
    if value >= 10:
        lcd.message(' ')
    elif value >= 0 and value < 10:
        lcd.message('  ')
    elif value > -10 and value < 0:
        lcd.message(' ')

def set_value():
    update = {}
    
    value = '%.0f' % Set.temp_value
    if Set.settable_value == SET_mode:
        update['mode'] = value
    
    value = '%.1f' % Set.temp_value
    if Set.settable_value == SET_PC:
        update['PC_setpoint'] = value
    elif Set.settable_value == SET_GC:
        update['GC_setpoint'] = value
    elif Set.settable_value == SET_CC1:
        update['CC1_setpoint'] = value
    elif Set.settable_value == SET_CC2:
        update['CC2_setpoint'] = value
    
    edfas[1].update(update)

    
def screen_update():	#need an update for more edfa
    if Param.current_screen == 0: #EDFA1 MONITORING
        if edfas[1]['number_of_laser'] == 1:	
            if EDFA1_MONITORING.page_position == 1:
                if edfas[1]['has_input_PD'] == True  and edfas[1]['has_output_PD'] == True:
                    lcd.set_cursor(5,0)
                    fill_with_blank(edfas[1]['input_power'])
                    lcd.message('%2.1f' % (edfas[1]['input_power']))
                    lcd.set_cursor(5,1)
                    fill_with_blank(edfas[1]['output_power'])
                    lcd.message('%2.1f' % (edfas[1]['output_power']))
                elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == True:
                    lcd.set_cursor(5,0)
                    fill_with_blank(edfas[1]['output_power'])
                    lcd.message('%2.1f' % (edfas[1]['output_power']))
                    lcd.set_cursor(6,1)
                    lcd.message('%5.0f' % (edfas[1]['LD1_current']))
                elif edfas[1]['has_input_PD'] == True  and edfas[1]['has_output_PD'] == False:
                    lcd.set_cursor(5,0)
                    fill_with_blank(edfas[1]['input_power'])
                    lcd.message('%2.1f' % (edfas[1]['input_power']))
                    lcd.set_cursor(6,1)
                    lcd.message('%5.0f' % (edfas[1]['LD1_current']))
                elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == False:
                    lcd.set_cursor(6,0)
                    lcd.message('%5.0f' % (edfas[1]['LD1_current']))
                    lcd.set_cursor(5,1)
                    fill_with_blank(edfas[1]['internal_temp'])
                    lcd.message('%2.1f' % (edfas[1]['internal_temp']))
            elif EDFA1_MONITORING.page_position == 2:
                if edfas[1]['has_input_PD'] == True  and edfas[1]['has_output_PD'] == True:
                    lcd.set_cursor(6,0)
                    lcd.message('%5.0f' % (edfas[1]['LD1_current']))
                    lcd.set_cursor(5,1)
                    fill_with_blank(edfas[1]['internal_temp'])
                    lcd.message('%2.1f' % (edfas[1]['internal_temp']))
                else:
                    lcd.set_cursor(5,0)
                    fill_with_blank(edfas[1]['internal_temp'])
                    lcd.message('%2.1f' % (edfas[1]['internal_temp']))
        elif edfas[1]['number_of_laser'] == 2:
            if EDFA1_MONITORING.page_position == 1:
                if edfas[1]['has_input_PD'] == True  and edfas[1]['has_output_PD'] == True:
                    lcd.set_cursor(5,0)
                    fill_with_blank(edfas[1]['input_power'])
                    lcd.message('%2.1f' % (edfas[1]['input_power']))
                    lcd.set_cursor(5,1)
                    fill_with_blank(edfas[1]['output_power'])
                    lcd.message('%2.1f' % (edfas[1]['output_power']))
                elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == True:
                    lcd.set_cursor(5,0)
                    fill_with_blank(edfas[1]['output_power'])
                    lcd.message('%2.1f' % (edfas[1]['output_power']))
                    lcd.set_cursor(6,1)
                    lcd.message('%5.0f' % (edfas[1]['LD1_current']))
                elif edfas[1]['has_input_PD'] == True  and edfas[1]['has_output_PD'] == False:
                    lcd.set_cursor(5,0)
                    fill_with_blank(edfas[1]['input_power'])
                    lcd.message('%2.1f' % (edfas[1]['input_power']))
                    lcd.set_cursor(6,1)
                    lcd.message('%5.0f' % (edfas[1]['LD1_current']))
                elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == False:
                    lcd.set_cursor(6,0)
                    lcd.message('%5.0f' % (edfas[1]['LD1_current']))
                    lcd.set_cursor(6,1)
                    lcd.message('%5.0f' % (edfas[1]['LD2_current']))
            elif EDFA1_MONITORING.page_position == 2:  
                if edfas[1]['has_input_PD'] == True  and edfas[1]['has_output_PD'] == True:
                    lcd.set_cursor(6,0)
                    lcd.message('%5.0f' % (edfas[1]['LD1_current']))
                    lcd.set_cursor(6,1)
                    lcd.message('%5.0f' % (edfas[1]['LD2_current']))
                elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == True:
                    lcd.set_cursor(6,0)
                    lcd.message('%5.0f' % (edfas[1]['LC2_current']))
                    lcd.set_cursor(5,1)
                    fill_with_blank(edfas[1]['internal_temp'])
                    lcd.message('%2.1f' % (edfas[1]['internal_temp']))
                elif edfas[1]['has_input_PD'] == True  and edfas[1]['has_output_PD'] == False:
                    lcd.set_cursor(6,0)
                    lcd.message('%5.0f' % (edfas[1]['LC2_current']))
                    lcd.set_cursor(5,1)
                    fill_with_blank(edfas[1]['internal_temp'])
                    lcd.message('%2.1f' % (edfas[1]['internal_temp']))
                elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == False:
                    lcd.set_cursor(5,0)
                    fill_with_blank(edfas[1]['internal_temp'])
                    lcd.message('%2.1f' % (edfas[1]['internal_temp']))
            elif EDFA1_MONITORING.page_position == 3:
                lcd.set_cursor(5,0)
                fill_with_blank(edfas[1]['internal_temp'])
                lcd.message('%2.1f' % (edfas[1]['internal_temp']))
    elif Param.current_screen == 2:
        if edfas[1]['number_of_laser'] == 1:
            if EDFA1_SETTINGS.page_position == 1:
                lcd.set_cursor(2,1)
                if edfas[1]['mode'] == OFF:
                    lcd.message('OFF')
                elif edfas[1]['mode'] == CC:
                    lcd.message(' CC')
                elif edfas[1]['mode'] == PC:
                    lcd.message(' PC')
                elif edfas[1]['mode'] == GC:
                    lcd.message(' GC')
            elif EDFA1_SETTINGS.page_position == 2:
                lcd.set_cursor(0,1)
                lcd.message('%5.0f' % (edfas[1]['CC1_setpoint']))
            elif EDFA1_SETTINGS.page_position == 3:
                lcd.set_cursor(0,1)
                if edfas[1]['has_PC_mode'] == True :
                    fill_with_blank(edfas[1]['PC_setpoint'])
                    lcd.message('%2.1f' % (edfas[1]['PC_setpoint']))
                elif edfas[1]['has_GC_mode'] == True:
                    fill_with_blank(edfas[1]['GC_setpoint'])
                    lcd.message('%2.1f' % (edfas[1]['GC_setpoint']))
            elif EDFA1_SETTINGS.page_position == 4:
                lcd.set_cursor(0,1)
                fill_with_blank(edfas[1]['GC_setpoint'])
                lcd.message('%2.1f' % (edfas[1]['GC_setpoint']))
        elif edfas[1]['number_of_laser'] == 2:
            if EDFA1_SETTINGS.page_position == 1:
                lcd.set_cursor(2,1)
                if edfas[1]['mode'] == OFF:
                    lcd.message('OFF')
                elif edfas[1]['mode'] == CC:
                    lcd.message(' CC')
                elif edfas[1]['mode'] == PC:
                    lcd.message(' PC')
                elif edfas[1]['mode'] == GC:
                    lcd.message(' GC')
            elif EDFA1_SETTINGS.page_position == 2:
                lcd.set_cursor(0,1)
                lcd.message('%5.0f' % (edfas[1]['CC1_setpoint']))
            elif EDFA1_SETTINGS.page_position == 3:
                lcd.set_cursor(0,1)
                lcd.message('%5.0f' % (edfas[1]['CC2_setpoint']))
            elif EDFA1_SETTINGS.page_position == 4:
                lcd.set_cursor(0,1)
                if edfas[1]['has_PC_mode'] == True :
                    fill_with_blank(edfas[1]['PC_setpoint'])
                    lcd.message('%2.1f' % (edfas[1]['PC_setpoint']))
                elif edfas[1]['has_GC_mode'] == True:
                    fill_with_blank(edfas[1]['GC_setpoint'])
                    lcd.message('%2.1f' % (edfas[1]['GC_setpoint']))
            elif EDFA1_SETTINGS.page_position == 5:
                lcd.set_cursor(0,1)
                fill_with_blank(edfas[1]['GC_setpoint'])
                lcd.message('%2.1f' % (edfas[1]['GC_setpoint']))
    elif Param.current_screen == 4: #EDFA1 ALARMS
        x = 7
        y = 0
        Product_info.load()
        lcd.set_cursor(x,y)
        if edfas[1]['alarms'].count('pin') == 1:
            x += 3
            if x > 15:
                for a in range(x-3,16):
                    lcd.set_cursor(a,y)
                    lcd.message(' ')
                y = 1
                lcd.set_cursor(0,y)
                x = 3
            lcd.message(' IN')
        if edfas[1]['alarms'].count('pout') == 1:
            x += 4
            if x > 15:
                for a in range(x-4,16):
                    lcd.set_cursor(a,y)
                    lcd.message(' ')
                y = 1
                lcd.set_cursor(0,y)
                x = 4
            lcd.message(' OUT')
        if edfas[1]['alarms'].count('pump_temp') == 1:
            x += 6
            if x > 15:
                for a in range(x-6,16):
                    lcd.set_cursor(a,y)
                    lcd.message(' ')
                y = 1
                lcd.set_cursor(0,y)
                x = 6
            lcd.message(' PTEMP')
        if edfas[1]['alarms'].count('pump_bias') == 1:
            x += 5
            if x > 15:
                for a in range(x-5,16):
                    lcd.set_cursor(a,y)
                    lcd.message(' ')
                y = 1
                lcd.set_cursor(0,y)
                x = 5
            lcd.message(' BIAS')
        if edfas[1]['alarms'].count('edfa_temp') == 1:
            x += 5
            if x > 15:
                for a in range(x-5,16):
                    lcd.set_cursor(a,y)
                    lcd.message(' ')
                y = 1
                lcd.set_cursor(0,y)
                x = 5
            lcd.message(' TEMP')
        if Product_info['alarms'].count('psu') == 1:
            x += 4
            if x > 15:
                for a in range(x-4,16):
                    lcd.set_cursor(a,y)
                    lcd.message(' ')
                y = 1
                lcd.set_cursor(0,y)
                x = 4
            lcd.message(' PSU')
        if Product_info['alarms'].count('fan1') == 1 or Product_info['alarms'].count('fan2') == 1 or Product_info['alarms'].count('fan3') == 1 or Product_info['alarms'].count('fan4') == 1:
            x += 4
            if x > 15:
                for a in range(x-4,16):
                    lcd.set_cursor(a,y)
                    lcd.message(' ')
                y = 1
                lcd.set_cursor(0,y)
                x = 4
            lcd.message(' FAN')
        if x == 7 and y == 0:
            lcd.message('         ')
            lcd.set_cursor(0,1)
            lcd.message('                ')
        elif y == 1:
            for a in range(x,16):
                lcd.set_cursor(a,1)
                lcd.message(' ')
        else:
            for a in range(x,16):
                lcd.set_cursor(a,0)
                lcd.message(' ')
            lcd.set_cursor(0,1)
            lcd.message('                ')                   
    elif Param.current_screen == 6: #RACK INFO
        lcd.set_cursor(4,0)
        lcd.message('%s' % (Product_info['serialnum']))
        lcd.set_cursor(5,1)
        lcd.message('%s' % (Product_info['partnum']))
    
def which_parameter(page):
    if page == 1:
        Set.temp_value = edfas[1]['mode']
        return SET_mode
    elif page == 2:
        Set.temp_value = edfas[1]['CC1_setpoint']
        return SET_CC1
    elif page == 3 and edfas[1]['number_of_laser'] == 2:
        Set.temp_value = edfas[1]['CC2_setpoint']
        return SET_CC2
    elif page == 3 and edfas[1]['has_PC_mode'] == True:
        Set.temp_value = edfas[1]['PC_setpoint']
        return SET_PC
    elif page == 3 and edfas[1]['has_GC_mode'] == True:
        Set.temp_value = edfas[1]['GC_setpoint']
        return SET_GC
    elif page == 4 and edfas[1]['has_PC_mode'] == True and edfas[1]['number_of_laser'] == 2:
        Set.temp_value = edfas[1]['PC_setpoint']
        return SET_PC
    elif page == 4 and edfas[1]['has_GC_mode'] == True:
        Set.temp_value = edfas[1]['GC_setpoint']
        return SET_GC
    elif page == 5:
        return SET_GC
    
def check_buttons():
    if GPIO.event_detected(Button_LEFT):
        if Set.flag:
            if Set.settable_value != SET_mode:
                if Set.cursor_position == 4 and (Set.settable_value == SET_PC or Set.settable_value == SET_GC):
                    Set.cursor_position -= 2
                else:
                    Set.cursor_position -= 1
                if Set.settable_value == SET_PC or Set.settable_value == SET_GC:
                    if Set.cursor_position <= 1:
                        Set.cursor_position = 1
                else:
                    if Set.cursor_position <= 0:
                        Set.cursor_position = 0
                lcd.set_cursor(Set.cursor_position,1)
        else:
            Old_screen = Param.current_screen
            if Param['number_of_edfa'] == 1:
                Param.current_screen -= 2
            elif Param['number_of_edfa'] == 2:
                Param.current_screen -= 1
            if Param.current_screen < 0:
                Param.current_screen = 6
            if Old_screen != Param.current_screen:
                Param.screen_update = True
    elif GPIO.event_detected(Button_RIGHT):
        if Set.flag:
            if Set.settable_value != SET_mode:
                if Set.cursor_position == 2 and (Set.settable_value == SET_PC or Set.settable_value == SET_GC):
                    Set.cursor_position += 2
                else:
                    Set.cursor_position += 1
                if Set.cursor_position >= 4:
                    Set.cursor_position = 4
                lcd.set_cursor(Set.cursor_position,1)
        else:
            Old_screen = Param.current_screen
            if Param['number_of_edfa'] == 1:
                Param.current_screen += 2
            elif Param['number_of_edfa'] == 2:
                Param.current_screen += 1
            if Param.current_screen > 6:
                Param.current_screen = 0
            if Old_screen != Param.current_screen:
                Param.screen_update = True
    elif GPIO.event_detected(Button_TOP):
        if Set.flag:
            if Set.settable_value == SET_mode:
                Set.temp_value += 1
                if Set.temp_value == PC and edfas[1]['has_PC_mode'] == False:
                    Set.temp_value += 1
                if Set.temp_value == GC and edfas[1]['has_GC_mode'] == False:
                    Set.temp_value += 1
                if Set.temp_value >= 5:
                    if edfas[1]['has_PC_mode'] == True:
                        Set.temp_value = PC
                    elif edfas[1]['has_GC_mode'] == True:
                        Set.temp_value = GC
                    else:
                        Set.temp_value = CC
                lcd.blink(False)
                lcd.set_cursor(2,1)
                if Set.temp_value == OFF:
                    lcd.message('OFF')
                elif Set.temp_value == CC:
                    lcd.message(' CC')
                elif Set.temp_value == PC:
                    lcd.message(' PC')
                elif Set.temp_value == GC:
                    lcd.message(' GC')
                lcd.set_cursor(Set.cursor_position,1)
                lcd.blink(True)
            elif Set.settable_value == SET_CC1 or Set.settable_value == SET_CC2:
                Set.temp_value += tab_CC[Set.cursor_position]
                if Set.temp_value <= 0:
                    Set.temp_value = 0
                elif Set.temp_value >= edfas[1]['max_current_LD1'] and Set.settable_value == SET_CC1:
                    Set.temp_value = edfas[1]['max_current_LD1']
                elif Set.temp_value >= edfas[1]['max_current_LD2'] and Set.settable_value == SET_CC2:
                    Set.temp_value = edfas[1]['max_current_LD2']
                lcd.blink(False)
                lcd.set_cursor(0,1)
                lcd.message('%5.0f' % (Set.temp_value))
                lcd.set_cursor(Set.cursor_position,1)
                lcd.blink(True)
            elif Set.settable_value == SET_GC or Set.settable_value == SET_PC:
                Set.temp_value += tab_PC_GC[Set.cursor_position]
                if Set.temp_value <= edfas[1]['min_pc'] and Set.settable_value == SET_PC:
                    Set.temp_value = edfas[1]['min_pc']
                elif Set.temp_value <= edfas[1]['min_gc'] and Set.settable_value == SET_GC:
                    Set.temp_value = edfas[1]['min_gc']
                elif Set.temp_value >= edfas[1]['max_pc'] and Set.settable_value == SET_PC:
                    Set.temp_value = edfas[1]['max_pc']
                elif Set.temp_value >= edfas[1]['max_gc'] and Set.settable_value == SET_GC:
                    Set.temp_value = edfas[1]['max_gc']
                lcd.blink(False)
                lcd.set_cursor(0,1)
                fill_with_blank(Set.temp_value)
                lcd.message('%2.1f' % (Set.temp_value))
                lcd.set_cursor(Set.cursor_position,1)
                lcd.blink(True)
        else:
            Old_page = tab[Param.current_screen].page_position
            if tab[Param.current_screen].TB_enabled == True:
                tab[Param.current_screen].page_position -= 1
            if tab[Param.current_screen].page_position < 1:
                tab[Param.current_screen].page_position = tab[Param.current_screen].number_of_page
            if Old_page != tab[Param.current_screen].page_position:
                Param.screen_update = True
    elif GPIO.event_detected(Button_BOT):
        if Set.flag:
            if Set.settable_value == SET_mode:
                Set.temp_value -= 1
                if Set.temp_value == GC and edfas[1]['has_GC_mode'] == False:
                    Set.temp_value -= 1
                if Set.temp_value == PC and edfas[1]['has_PC_mode'] == False:
                    Set.temp_value -= 1
                elif Set.temp_value <= 0:
                    Set.temp_value = OFF
                lcd.blink(False)
                lcd.set_cursor(2,1)
                if Set.temp_value == OFF:
                    lcd.message('OFF')
                elif Set.temp_value == CC:
                    lcd.message(' CC')
                elif Set.temp_value == PC:
                    lcd.message(' PC')
                elif Set.temp_value == GC:
                    lcd.message(' GC')
                lcd.set_cursor(Set.cursor_position,1)
                lcd.blink(True)
            elif Set.settable_value == SET_CC1 or Set.settable_value == SET_CC2:
                Set.temp_value -= tab_CC[Set.cursor_position]
                if Set.temp_value <= 0:
                    Set.temp_value = 0
                elif Set.temp_value >= edfas[1]['max_current_LD1'] and Set.settable_value == SET_CC1:
                    Set.temp_value = edfas[1]['max_current_LD1']
                elif Set.temp_value >= edfas[1]['max_current_LD2'] and Set.settable_value == SET_CC2:
                    Set.temp_value = edfas[1]['max_current_LD2']
                lcd.blink(False)
                lcd.set_cursor(0,1)
                lcd.message('%5.0f' % (Set.temp_value))
                lcd.set_cursor(Set.cursor_position,1)
                lcd.blink(True)
            elif Set.settable_value == SET_GC or Set.settable_value == SET_PC:
                Set.temp_value -= tab_PC_GC[Set.cursor_position]
                if Set.temp_value <= edfas[1]['min_pc'] and Set.settable_value == SET_PC:
                    Set.temp_value = edfas[1]['min_pc']
                elif Set.temp_value <= edfas[1]['min_gc'] and Set.settable_value == SET_GC:
                    Set.temp_value = edfas[1]['min_gc']
                elif Set.temp_value >= edfas[1]['max_pc'] and Set.settable_value == SET_PC:
                    Set.temp_value = edfas[1]['max_pc']
                elif Set.temp_value >= edfas[1]['max_gc'] and Set.settable_value == SET_GC:
                    Set.temp_value = edfas[1]['max_gc']
                lcd.blink(False)
                lcd.set_cursor(0,1)
                fill_with_blank(Set.temp_value)
                lcd.message('%2.1f' % (Set.temp_value))
                lcd.set_cursor(Set.cursor_position,1)
                lcd.blink(True)
        else:
            Old_page = tab[Param.current_screen].page_position
            if tab[Param.current_screen].TB_enabled == True:
                tab[Param.current_screen].page_position += 1
                if tab[Param.current_screen].page_position > tab[Param.current_screen].number_of_page:
                    tab[Param.current_screen].page_position = 1
                if Old_page != tab[Param.current_screen].page_position:
                    Param.screen_update = True
    elif GPIO.event_detected(Button_SET) and tab[Param.current_screen].SET_enabled:
        if Set.flag == False:
            if tab[Param.current_screen].page_position == 2:
                if edfas[1]['has_settable_LD1'] == True:
                    lcd.set_cursor(Set.cursor_position,1)
                    lcd.blink(True)
                    Set.flag = True
                    Set.settable_value = which_parameter(tab[Param.current_screen].page_position)
            else:
                lcd.set_cursor(Set.cursor_position,1)
                lcd.blink(True)
                Set.flag = True
                Set.settable_value = which_parameter(tab[Param.current_screen].page_position)                    
        else:
            Set.cursor_position = 4
            Set.flag = False
            set_value()
            Set.temp_value = 0
            lcd.blink(False)
            #lcd.show_cursor(False)


PC  = 1
GC  = 2
CC	= 3
OFF	= 4

SET_mode	= 0
SET_CC1		= 1
SET_CC2		= 2
SET_PC		= 3
SET_GC		= 4

tab_CC = [10000,1000,100,10,1]
tab_PC_GC = [100,10,1,0,0.1]

# LCD INIT
lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22
lcd_backlight = None
lcd_columns = 16
lcd_rows    = 2
if imports['LCD']:
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                               lcd_columns, lcd_rows, lcd_backlight)
else:
    lcd = fakelcd.FakeLCD(16, 2)

lcd.create_char(1,[0,4,10,17,0,0,0,0])
lcd.create_char(2,[0,0,0,0,17,10,4,0])
# NAVIGATION BUTTONS INIT
Button_TOP	= 2
Button_BOT	= 3
Button_LEFT	= 4
Button_RIGHT	= 10
Button_SET	= 9
bouncetime = 400

GPIO.setup(Button_TOP,GPIO.IN)
GPIO.setup(Button_BOT,GPIO.IN)
GPIO.setup(Button_LEFT,GPIO.IN)
GPIO.setup(Button_RIGHT,GPIO.IN)
GPIO.setup(Button_SET,GPIO.IN)

GPIO.add_event_detect(Button_TOP,GPIO.RISING, bouncetime=bouncetime)
GPIO.add_event_detect(Button_BOT,GPIO.RISING, bouncetime=bouncetime)
GPIO.add_event_detect(Button_LEFT,GPIO.RISING, bouncetime=bouncetime)
GPIO.add_event_detect(Button_RIGHT,GPIO.RISING, bouncetime=bouncetime)
GPIO.add_event_detect(Button_SET,GPIO.RISING, bouncetime=bouncetime)


# INIT
if len(sys.argv) > 1:
    baseurl = sys.argv[1]

if len(sys.argv) == 3:
    m = hashlib.md5()
    m.update(sys.argv[2])
    password = b64encode(m.hexdigest())

if len(sys.argv) == 4:
    if sys.argv[2] == "md5":
        password = sys.argv[3]
    else:
        print "Unknown password encoding: %s" % (sys.argv[2])
        exit(1)


Product_info = Info()
Param = Parameters()
Set = SetAction()
edfas = {}

edfas[1] = EDFA(1)
tab = []

if Param['number_of_edfa'] == 1:
    if edfas[1]['number_of_laser'] == 1:
        # MONITORING
        if edfas[1]['has_input_PD'] == True and edfas[1]['has_output_PD'] == True:
            Monitoring_PAGE_1 = 'IN      .  dBm \x01\nOUT     .  dBm \x02'
            Monitoring_PAGE_2 = 'LC1         mA \x01\nTEMP    .  C   \x02'
            Monitoring_nb = 2
        elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == True:
            Monitoring_PAGE_1 = 'OUT     .  dBm \x01\nLC1         mA \x02'
            Monitoring_PAGE_2 = 'TEMP    .  C   \x01\n               \x02'
            Monitoring_nb = 2
        elif edfas[1]['has_input_PD'] == True and edfas[1]['has_output_PD'] == False:
            Monitoring_PAGE_1 = 'IN      .  dBm \x01\nLC1         mA \x02'
            Monitoring_PAGE_2 = 'TEMP    .  C   \x01\n               \x02'
            Monitoring_nb = 2
        elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == False:
            Monitoring_PAGE_1 = 'LC1         mA \x01\nTEMP    .  C   \x02'
            Monitoring_PAGE_2 = None
            Monitoring_nb = 1
        Monitoring_PAGE_3 = None
        Monitoring_PAGE_4 = None
        Monitoring_PAGE_5 = None
        # SETTINGS
        Settings_PAGE_1 = 'OPERATING MODE \x01\n         (set) \x02'
        Settings_PAGE_2 = ' CC1 SETPOINT  \x01\n      mA (set) \x02'
        Settings_PAGE_5 = None
        if edfas[1]['has_PC_mode'] == True and edfas[1]['has_GC_mode'] == True:
            Settings_PAGE_3 = '  PC SETPOINT  \x01\n  .  dBm (set) \x02'
            Settings_PAGE_4 = '  GC SETPOINT  \x01\n  .  dBm (set) \x02'
            Settings_nb = 4
        elif edfas[1]['has_PC_mode'] == False and edfas[1]['has_GC_mode'] == True:
            Settings_PAGE_3 = '  GC SETPOINT  \x01\n  .  dBm (set) \x02'
            Settings_PAGE_4 = None
            Settings_nb = 3
        elif edfas[1]['has_PC_mode'] == True and edfas[1]['has_GC_mode'] == False:
            Settings_PAGE_3 = '  PC SETPOINT  \x01\n  .  dBm (set) \x02'
            Settings_PAGE_4 = None
            Settings_nb = 3
        elif edfas[1]['has_PC_mode'] == False and edfas[1]['has_GC_mode'] == False:
            Settings_PAGE_3 = None
            Settings_PAGE_4 = None
            Settings_nb = 2
        Settings_PAGE_5 = None
    elif edfas[1]['number_of_laser'] == 2:
        # MONITORING
        if edfas[1]['has_input_PD'] == True and edfas[1]['has_output_PD'] == True:
            Monitoring_PAGE_1 = 'IN      .  dBm \x01\nOUT     .  dBm \x02'
            Monitoring_PAGE_2 = 'LC1         mA \x01\nLC2         mA \x02'
            Monitoring_PAGE_3 = 'TEMP    .  C   \x01\n               \x02'
            Monitoring_nb = 3
        elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == True:
            Monitoring_PAGE_1 = 'OUT     .  dBm \x01\nLC1         mA \x02'
            Monitoring_PAGE_2 = 'LC2         mA \x01\nTEMP    .  C   \x02'
            Monitoring_PAGE_3 = None
            Monitoring_nb = 2
        elif edfas[1]['has_input_PD'] == True and edfas[1]['has_output_PD'] == False:
            Monitoring_PAGE_1 = 'IN      .  dBm \x01\nLC1         mA \x02'
            Monitoring_PAGE_2 = 'LC2         mA \x01\nTEMP    .  C   \x02'
            Monitoring_PAGE_3 = None
            Monitoring_nb = 2
        elif edfas[1]['has_input_PD'] == False and edfas[1]['has_output_PD'] == False:
            Monitoring_PAGE_1 = 'LC1         mA \x01\nLC2         mA \x02'
            Monitoring_PAGE_2 = 'TEMP    .  C   \x01\n               \x02'
            Monitoring_PAGE_3 = None
            Monitoring_nb = 2
        Monitoring_PAGE_4 = None
        Monitoring_PAGE_5 = None
        # SETTINGS
        Settings_PAGE_1 = 'OPERATING MODE \x01\n         (set) \x02'
        Settings_PAGE_2 = ' CC1 SETPOINT  \x01\n      mA (set) \x02'
        Settings_PAGE_3 = ' CC2 SETPOINT  \x01\n      mA (set) \x02'
        if edfas[1]['has_PC_mode'] == True and edfas[1]['has_GC_mode'] == True:
            Settings_PAGE_4 = '  PC SETPOINT  \x01\n  .  dBm (set) \x02'
            Settings_PAGE_5 = '  GC SETPOINT  \x01\n  .  dBm (set) \x02'
            Settings_nb = 5
        elif edfas[1]['has_PC_mode'] == False and edfas[1]['has_GC_mode'] == True:
            Settings_PAGE_4 = '  GC SETPOINT  \x01\n  .  dBm (set) \x02'
            Settings_PAGE_5 = None
            Settings_nb = 4
        elif edfas[1]['has_PC_mode'] == True and edfas[1]['has_GC_mode'] == False:
            Settings_PAGE_4 = '  PC SETPOINT  \x01\n  .  dBm (set) \x02'
            Settings_PAGE_5 = None
            Settings_nb = 4
        elif edfas[1]['has_PC_mode'] == False and edfas[1]['has_GC_mode'] == False:
            Settings_PAGE_4 = None
            Settings_PAGE_5 = None
            Settings_nb = 3
    else:
        raise Exception("Invalid number of laser: %s" % (edfas[1]['number_of_laser']))
    
    EDFA1_MONITORING = Screen(Monitoring_PAGE_1,
                          Monitoring_PAGE_2,
                          Monitoring_PAGE_3,
                          Monitoring_PAGE_4,
                          Monitoring_PAGE_5,
                          Monitoring_nb,
                          True,
                          False)
    EDFA1_SETTINGS = Screen(Settings_PAGE_1,
                        Settings_PAGE_2,
                        Settings_PAGE_3,
                        Settings_PAGE_4,
                        Settings_PAGE_5,
                        Settings_nb,
                        True,
                        True)
    EDFA1_ALARMS = Screen('ALARMS:',None,None,None,None,1,True,False)
    INFORMATIONS = Screen('SER\nPART',None,None,None,None,1,True,False)
    tab = [EDFA1_MONITORING,None,EDFA1_SETTINGS,None,EDFA1_ALARMS,None,INFORMATIONS]
elif Param['number_of_edfa'] == 2:
    edfas[2] = EDFA(2)
    # need to read EDFA2 config here
    #tab = [EDFA1_MONITORING,EDFA2_MONITORING, EDFA1_SETTINGS,EDFA2_SETTINGS,EDFA1_ALARMS,EDFA2_ALARMS,INFORMATIONS]
else:
    raise Exception("Invalid number of units: %s" % (Param['number_of_edfa']))

# MAIN
lcd.clear()
lcd.message(Product_info['vendor']) # "welcome" message // vendor name
time.sleep(5.0)
lcd.clear()

while True:
    check_buttons()
    if Param.screen_update == True:
        draw_screen(tab[Param.current_screen])
    if (time.time() - Param.time_stamp) > 1:
        if Set.flag == False:
            for k in edfas:
                edfas[k].load()
            screen_update()
        Param.time_stamp = time.time()
exit(0)
