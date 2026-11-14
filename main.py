from datetime import datetime
import random, math
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.utils import platform
from kivy.animation import Animation

IS_ANDROID = platform == "android"
if IS_ANDROID:
    from android import activity
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    from plyer import tts, flashlight, call as plyer_call
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    RecognizerIntent = autoclass("android.speech.RecognizerIntent")
    Intent = autoclass("android.content.Intent")
    Uri = autoclass("android.net.Uri")
    REQ = 1001

class FuturisticCore(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_normal = ""
        self.background_color = (0,0,0,0)
        self.text = ""
        self.angle = 0
        self.pulse = 0
        with self.canvas.before:
            self.c_bg = Color(0.02, 0.08, 0.15, 1)
            self.bg_circle = Ellipse(pos=(0,0), size=(0,0))
            self.c1 = Color(0.0, 0.9, 1.0, 0.25)
            self.ring1 = Line(circle=(0,0,0), width=1.5)
            self.c2 = Color(0.0, 1.0, 0.9, 0.9)
            self.ring2 = Line(circle=(0,0,0), width=2)
            self.c3 = Color(0.2, 0.6, 1.0, 0.6)
            self.ring3 = Line(circle=(0,0,0), width=1)
            self.c4 = Color(1, 1, 1, 0.9)
            self.dot1 = Ellipse(pos=(0,0), size=(10,10))
            self.c5 = Color(0.0, 1.0, 1.0, 0.9)
            self.dot2 = Ellipse(pos=(0,0), size=(8,8))
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_interval(self.tick, 1/30)
    def redraw(self, *a):
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.38
        self.bg_circle.pos = (cx-r, cy-r)
        self.bg_circle.size = (r*2, r*2)
        self.ring1.circle = (cx, cy, r*1.25)
        self.ring2.circle = (cx, cy, r*(1.0 + self.pulse*0.08))
        self.ring3.circle = (cx, cy, r*0.65)
        a1 = math.radians(self.angle)
        a2 = math.radians(self.angle+180)
        self.dot1.pos = (cx + math.cos(a1)*r*1.25 -5, cy + math.sin(a1)*r*1.25 -5)
        self.dot2.pos = (cx + math.cos(a2)*r*1.25 -4, cy + math.sin(a2)*r*1.25 -4)
    def tick(self, dt):
        self.angle = (self.angle + 2) % 360
        self.pulse = (self.pulse + dt*2) % 1
        self.redraw()
    def speak_anim(self):
        anim = Animation(size_hint=(0.62, 0.45), duration=0.15) + Animation(size_hint=(0.55, 0.40), duration=0.15)
        anim.start(self)

class JarvisUI(FloatLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            Color(0.005, 0.01, 0.03, 1)
            self.bg = Rectangle(pos=(0,0), size=(100,100))
            Color(0.0, 0.8, 1.0, 0.15)
            self.line_top = Line(points=[0,0,0,0], width=1)
            self.line_bot = Line(points=[0,0,0,0], width=1)
        self.bind(pos=self._bg, size=self._bg)
        self.title = Label(text="J.A.R.V.I.S", font_size="28sp", bold=True, color=(0.0,0.9,1,1), pos_hint={"center_x":0.5, "center_y":0.92}, size_hint=(1,0.08))
        self.add_widget(self.title)
        self.subtitle = Label(text="JUST A RATHER VERY INTELLIGENT SYSTEM", font_size="9sp", color=(0.4,0.7,0.9,1), pos_hint={"center_x":0.5, "center_y":0.88}, size_hint=(1,0.04))
        self.add_widget(self.subtitle)
        self.time_lbl = Label(text="--:--", font_size="16sp", bold=True, color=(1,1,1,1), pos_hint={"center_x":0.18, "center_y":0.82}, size_hint=(0.3,0.05))
        self.add_widget(self.time_lbl)
        self.date_lbl = Label(text="LOADING...", font_size="10sp", color=(0.6,0.9,1,1), pos_hint={"center_x":0.82, "center_y":0.82}, size_hint=(0.3,0.05))
        self.add_widget(self.date_lbl)
        self.sys_lbl = Label(text="● CPU 12%  ● RAM 45%  ● BATTERY 87%  ● ONLINE", font_size="9sp", color=(0.0,1.0,0.6,1), pos_hint={"center_x":0.5, "center_y":0.77}, size_hint=(1,0.04))
        self.add_widget(self.sys_lbl)
        self.core = FuturisticCore(pos_hint={"center_x":0.5, "center_y":0.52}, size_hint=(0.55,0.40))
        self.add_widget(self.core)
        self.tap_lbl = Label(text="TAP TO SPEAK", font_size="11sp", bold=True, color=(0.0,1.0,1.0,1), pos_hint={"center_x":0.5, "center_y":0.52}, size_hint=(0.4,0.05))
        self.add_widget(self.tap_lbl)
        self.cmd_lbl = Label(text="Hello Sir, I am ready.", font_size="14sp", color=(1,1,1,1), pos_hint={"center_x":0.5, "center_y":0.24}, size_hint=(0.9,0.12), halign="center", valign="middle")
        self.cmd_lbl.bind(size=lambda s,v: setattr(s, "text_size", (v[0], None)))
        self.add_widget(self.cmd_lbl)
        self.bottom = Label(text="[ YOUTUBE ]  [ WHATSAPP ]  [ CALL ]  [ FLASH ]  [ CAMERA ]", font_size="10sp", color=(0.5,0.8,1,1), pos_hint={"center_x":0.5, "center_y":0.08}, size_hint=(1,0.06))
        self.add_widget(self.bottom)
        Clock.schedule_interval(self.update_clock, 1)
    def _bg(self, *a):
        self.bg.pos = (self.x, self.y)
        self.bg.size = (self.width, self.height)
        self.line_top.points = [0, self.height*0.86, self.width, self.height*0.86]
        self.line_bot.points = [0, self.height*0.15, self.width, self.height*0.15]
    def update_clock(self, dt):
        now = datetime.now()
        self.time_lbl.text = now.strftime("%I:%M %p")
        self.date_lbl.text = now.strftime("%d %b %Y")
        cpu = random.randint(8, 28)
        ram = random.randint(38, 62)
        bat = random.randint(75, 95)
        self.sys_lbl.text = f"● CPU {cpu}%  ● RAM {ram}%  ● BATTERY {bat}%  ● ONLINE"

class JarvisApp(App):
    def build(self):
        self.ui = JarvisUI()
        self.flash_on = False
        if IS_ANDROID:
            request_permissions([Permission.RECORD_AUDIO, Permission.CALL_PHONE, Permission.CAMERA, Permission.FLASHLIGHT])
            activity.bind(on_activity_result=self.on_result)
            self.ui.core.bind(on_release=lambda *a: self.listen())
            self.ui.tap_lbl.bind(on_touch_down=lambda *a: self.listen())
        else:
            self.ui.core.bind(on_release=lambda *a: self.say("Desktop mode - voice only on Android"))
        return self.ui
    def say(self, text):
        self.ui.cmd_lbl.text = text
        self.ui.core.speak_anim()
        if IS_ANDROID:
            try: tts.speak(text)
            except: pass
        print("JARVIS:", text)
    def listen(self):
        self.say("Listening Sir...")
        if not IS_ANDROID:
            self.say("Voice works only in Android App")
            return
        try:
            intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to JARVIS Sir")
            activity.startActivityForResult(intent, REQ)
        except Exception as e:
            self.say("Mic Error: " + str(e))
    def on_result(self, req, res, data):
        if req != REQ or data is None:
            self.say("I didn't hear you Sir")
            return
        try:
            res_list = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            if res_list and res_list.size() > 0:
                cmd = str(res_list.get(0)).lower()
                self.handle(cmd)
            else:
                self.say("Say again Sir")
        except Exception as e:
            self.say("Error: " + str(e))
    def handle(self, cmd):
        print("CMD:", cmd)
        if "time" in cmd or "baje" in cmd or "time kya" in cmd:
            self.say("Sir, time is " + datetime.now().strftime("%I:%M %p"))
        elif "date" in cmd or "tarikh" in cmd or "din" in cmd:
            self.say("Today is " + datetime.now().strftime("%d %B %Y"))
        elif "hello" in cmd or "hi jarvis" in cmd or "hey" in cmd or "namaste" in cmd:
            self.say("Hello Sir, I am JARVIS, fully operational and ready for your commands")
        elif "how are you" in cmd or "kaise ho" in cmd:
            self.say("I am perfect Sir, all systems online")
        elif "youtube" in cmd or "gaana" in cmd or "song" in cmd or "music" in cmd:
            self.say("Opening YouTube Sir, playing music")
            self.open_app("com.google.android.youtube")
        elif "whatsapp" in cmd:
            self.say("Opening WhatsApp Sir")
            self.open_app("com.whatsapp")
        elif "instagram" in cmd or "insta" in cmd:
            self.say("Opening Instagram Sir")
            self.open_app("com.instagram.android")
        elif "camera" in cmd or "photo" in cmd:
            self.say("Opening Camera Sir")
            self.open_app("com.google.android.GoogleCamera")
        elif "flash" in cmd or "torch" in cmd or "light" in cmd:
            self.toggle_flash()
        elif "call" in cmd:
            self.say("Opening Dialer Sir, say number")
            self.open_app("com.google.android.dialer")
        elif "battery" in cmd:
            self.say("Battery is good Sir, all systems stable")
        elif "thank" in cmd or "shukriya" in cmd:
            self.say("Always at your service Sir")
        elif "who are you" in cmd or "tum kaun" in cmd:
            self.say("I am JARVIS, your personal AI assistant, created for you")
        elif "open" in cmd:
            self.say("Opening app Sir")
            self.open_app("com.google.android.youtube")
        else:
            self.say("Command received Sir: " + cmd + ". I am learning this command.")
    def toggle_flash(self):
        if not IS_ANDROID:
            self.say("Flash only on phone Sir")
            return
        try:
            if not self.flash_on:
                flashlight.on()
                self.flash_on = True
                self.say("Flashlight On Sir")
            else:
                flashlight.off()
                self.flash_on = False
                self.say("Flashlight Off Sir")
        except Exception as e:
            self.say("Flash Error")
    def open_app(self, pkg):
        if not IS_ANDROID: return
        try:
            act = PythonActivity.mActivity
            intent = act.getPackageManager().getLaunchIntentForPackage(pkg)
            if intent:
                act.startActivity(intent)
            else:
                self.say("App not installed Sir")
        except Exception as e:
            self.say("Cannot open app Sir")

if __name__ == "__main__":
    JarvisApp().run()
