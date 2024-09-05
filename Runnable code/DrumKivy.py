#DrumPad sample app -- Stars of the Sky | Reşat Berk

from kivy.app import App               # Kivy version == 2.1.0  -- sound .mp3 trim == https://mp3cut.net/
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader 
from kivy.graphics import Rectangle, Color, Line
from kivy.clock import Clock
from kivy.uix.popup import Popup


drum_pad_data = {0:'drum1.png', 17:'drum2.png', 34:'drum3.png', 51:'drum4.png', 68:'drum5.png', 85:'drum6.png'} # -- drum set pieces
pause_data = [] # -- start n pause for 
sound_data1 = [None]
sound_data2 = [None]
sound_data3 = [None] #player sounds of pads.
sound_data4 = [None]
sound_data5 = [None]
sound_data6 = [None]
start_data = [0] # -- time for movement

# -- !! not added try...except() might be error. -- !!

class CanvasButton(Button):        # -- for button border colors (line movement when touched start.)
    def __init__(self, **kwargs):
        super(CanvasButton, self).__init__(**kwargs)

        self._border_color = (0, 0, 0, 0)  
        self.border_width = 1
        
        with self.canvas.after:
            self.border_color_instruction = Color(*self._border_color)
            self.border_line = Line(width=self.border_width, rectangle=self.pos + self.size)
        
        self.bind(pos=self.update_border, size=self.update_border)
    
    @property
    def border_color(self):
        return self._border_color
    
    @border_color.setter
    def border_color(self, value):
        self._border_color = value
        
        if hasattr(self, 'border_color_instruction'):
            self.border_color_instruction.rgba = value  
        
        self.update_border()
    
    def update_border(self, *args):
        self.border_line.rectangle = self.pos + self.size


class DrumKV(App):

    def settime(self, dt): # -- for metronome on label
        t = 0
        if dt =='plus':
            t += 1
            edit = self.bpm_text.text.replace(' BPM','')
            edit1 = int(edit) + t
            self.bpm_text.text = str(edit1)+' BPM'
        elif dt =='minus':
            t -= 1
            edit = self.bpm_text.text.replace(' BPM','')
            edit1 = int(edit) + t
            self.bpm_text.text = str(edit1)+' BPM'


    def func_time(self, *args):
        edit = self.bpm_text.text.replace(' BPM','')   # -- movement play
        metronome = 60 / int(edit)
        t = start_data[-1]-1 

        for t in range(t,102,17):
            self.pads.get(str(t)).border_color = (0, 0 ,0 ,1)

        Clock.schedule_once(self.start_pause, metronome)


    def start_pause(self, arg):  # -- start and pause
        
        if len(pause_data) == 1:
            self.setting2_play.text = 'Pause'

            i = start_data[-1]
            while i < 16:
                i += 1

                for i in range(i,102,17):
                    if self.pads.get(str(i)) in sound_data1:
                        self.sound1.play()
                    if self.pads.get(str(i)) in sound_data2:
                        self.sound2.play()
                    if self.pads.get(str(i)) in sound_data3:
                        self.sound3.play()
                    if self.pads.get(str(i)) in sound_data4:
                        self.sound4.play()
                    if self.pads.get(str(i)) in sound_data5:
                        self.sound5.play()
                    if self.pads.get(str(i)) in sound_data6:
                        self.sound6.play()
                    
                    self.pads.get(str(i)).border_color = (1, 1, 1, 1)
                    #self.pads.get(str(i)).background_color='#FFFFFF'
            
                    if i >85 and i<=102:
                        start_data.append(start_data[-1]+1)
                        return self.func_time()

            if i == 16:
                t = start_data[-1]
                for t in range(t,102,17):
                    self.pads.get(str(t)).border_color = (0, 0 ,0 ,1)

                start_data.clear()
                start_data.append(0)
                return self.start_pause(arg)

        elif len(pause_data) == 2:
            self.setting2_play.text = 'Start'
            pause_data.clear()
            pass



    def replace_pad(self, *args):
        pass # -- not need this is a sample


    def pad_event(self, ppos):

        if ppos.background_normal != '':
            popup_layout = GridLayout(rows=2, cols=3, spacing = '4dp')
            self.butt = {}
    
            for i,j in drum_pad_data.items():

                buttons = Button(text = '',background_color='#FFFFFF',background_normal=j)  
                self.butt[f'{i}'] = buttons #id
                buttons.bind(on_release = lambda pad=buttons,change=ppos : self.replace_pad(pad,change)) 
                popup_layout.add_widget(buttons)
            
                        
            popup = Popup(title='Choose one', title_color='white',content=popup_layout, size_hint = (0.5,0.5), auto_dismiss=True,
                    background_color = (0,0,0,1),separator_color='white')
            buttons.bind(on_touch_down = popup.dismiss)
            popup.open() 

    
        elif ppos.background_color == [0.3058823529411765, 0.09803921568627451, 0.2627450980392157, 1.0]:
            ppos.background_color = '#DA23B1'
            sound_data1.append(ppos) 

        elif ppos.background_color == [0.8549019607843137, 0.13725490196078433, 0.6941176470588235, 1.0]:
            ppos.background_color = '#4E1943'
            sound_data1.remove(ppos)

        elif ppos.background_color == [0.25882352941176473, 0.18823529411764706, 0.0392156862745098, 1.0]:
            ppos.background_color = '#DD9D22' 
            keys = [key for key, value in self.pads.items() if value == ppos]
            if int(keys[-1]) in tuple(range(18,34)):
                sound_data2.append(ppos)  
            else:
                sound_data3.append(ppos)


        elif ppos.background_color == [0.8666666666666667, 0.615686274509804, 0.13333333333333333, 1.0]:
            ppos.background_color = '#42300A'
            keys = [key for key, value in self.pads.items() if value == ppos]
            if int(keys[-1]) in tuple(range(18,34)):
                sound_data2.remove(ppos)  
            else:
                sound_data3.remove(ppos)

        elif ppos.background_color == [0.03529411764705882, 0.24705882352941178, 0.24705882352941178, 1.0]:
            ppos.background_color = '#1FD1D3' 
            keys = [key for key, value in self.pads.items() if value == ppos]
            if int(keys[-1]) in tuple(range(52,68)):
                sound_data4.append(ppos)  
            else:
                sound_data5.append(ppos)

        elif ppos.background_color == [0.12156862745098039, 0.8196078431372549, 0.8274509803921568, 1.0]:
            ppos.background_color = '#093F3F'
            keys = [key for key, value in self.pads.items() if value == ppos]
            if int(keys[-1]) in tuple(range(52,68)):
                sound_data4.remove(ppos)  
            else:
                sound_data5.remove(ppos)

        elif ppos.background_color == [0.09803921568627451, 0.2549019607843137, 0.11764705882352941, 1.0]:
            ppos.background_color = '#21D52C' 
            sound_data6.append(ppos)

        elif ppos.background_color == [0.12941176470588237, 0.8352941176470589, 0.17254901960784313, 1.0]:
            ppos.background_color = '#19411E'
            sound_data6.remove(ppos)


    def restart(self, arg):
        start_data.clear()
        start_data.append(0)
        pause_data.clear()
        App.get_running_app().stop() # -- restart app
        DrumKV().run()

    def layout(self):

        main_layout = BoxLayout(orientation = 'vertical')
        title_label = Label(text = 'DrumKV - MusicPAD', font_size = '42sp', valign = 'top', halign='center', size_hint_y = 0.2) # -- or use image!
        drum_pad = GridLayout(cols=17, rows=6, spacing='3dp')

        settings_layout = FloatLayout(size_hint_y = 0.2)
        setting1_lay = BoxLayout(orientation = 'horizontal', size_hint=(0.3,0.5), pos_hint = {'center_y':0.5})
        save_but = Button(text = 'Save')
        load_but = Button(text = 'Load')
        res_but = Button(text = 'Restart')
        res_but.bind(on_release = self.restart)
        setting1_lay.add_widget(save_but)
        setting1_lay.add_widget(load_but)
        setting1_lay.add_widget(res_but)
        settings_layout.add_widget(setting1_lay)

        self.setting2_play = Button(text = 'Start', pos_hint = {'center_x':0.5, 'center_y':0.5}, size_hint=(0.1,0.5)) # -- use play/pause image
        self.setting2_play.bind(on_release = lambda _: self.start_pause(pause_data.append(1))) # -- start or pause
        settings_layout.add_widget(self.setting2_play)

        setting1_bpm = BoxLayout(orientation = 'horizontal', size_hint=(0.3,0.5), pos_hint = {'center_x':0.85, 'center_y':0.5})
        self.bpm_text = Label(text = '100 BPM')
        but_plus = Button(text = '+', font_size = '26sp') # -- use image or symbol!
        but_minus = Button(text = '-', font_size = '30sp')
        but_plus.bind(on_release = lambda dt : self.settime(dt='plus'))
        but_minus.bind(on_release = lambda dt : self.settime(dt='minus'))
        setting1_bpm.add_widget(self.bpm_text)
        setting1_bpm.add_widget(but_plus)
        setting1_bpm.add_widget(but_minus)
        settings_layout.add_widget(setting1_bpm)


       
        self.pads = {} # -- for button id 
        for i in range(102):
            if i in range(0,102,17):
                pad_buttons = Button(text='', background_normal = drum_pad_data[i], 
                    size_hint_y = 1.8, size_hint_x = 1.8)
                
            else:
                if i in range(1,17,1):
                    pad_buttons = CanvasButton(text='', background_color='#4E1943', background_normal ='')
                elif i in range(18,51,1):
                    pad_buttons = CanvasButton(text='', background_color='#42300A', background_normal ='') 
                elif i in range(52,85,1):
                    pad_buttons = CanvasButton(text='', background_color='#093F3F', background_normal ='') 
                else:
                    pad_buttons = CanvasButton(text='', background_color='#19411E', background_normal ='')


            self.pads[f'{i}'] = pad_buttons # -- buttons id.
            pad_buttons.bind(on_release= lambda ppos = pad_buttons: self.pad_event(ppos)) # -- event of pad 
            drum_pad.add_widget(pad_buttons)

        main_layout.add_widget(title_label)
        main_layout.add_widget(drum_pad)
        main_layout.add_widget(settings_layout)

        return main_layout


    def on_start(self):
        self.sound1 = SoundLoader.load('sound1.mp3') # -- mp3 sounds
        self.sound2 = SoundLoader.load('sound2.mp3')
        self.sound3 = SoundLoader.load('sound3.mp3')
        self.sound4 = SoundLoader.load('sound4.mp3')
        self.sound5 = SoundLoader.load('sound5.mp3')
        self.sound6 = SoundLoader.load('sound6.mp3')
        
    def build(self):

        return self.layout()

kv = DrumKV().run()