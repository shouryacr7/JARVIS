import os
import json
import asyncio
import threading
import datetime
import edge_tts
import pygame
import speech_recognition as sr
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation

# Android specific imports
try:
    from android.permissions import request_permissions, Permission
    ANDROID = True
except ImportError:
    ANDROID = False

# --- CONFIGURATION ---
VOICE_FILE = "jarvis_voice.mp3"
JARVIS_VOICE = "en-GB-RyanNeural"
Window.clearcolor = (0, 0, 0, 1)

# --- BRAIN & MEMORY ---
class JarvisBrain:
    def __init__(self):
        self.file = "jarvis_memory.json"
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({"boss_name": "Boss", "habits": {}}, f)

    def get_mem(self, key):
        with open(self.file, "r") as f:
            return json.load(f).get(key, "Boss")

# --- UI INTERFACE ---
class JarvisHUD(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.brain = JarvisBrain()
        self.angle = 0
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 400
        
        if ANDROID:
            request_permissions([Permission.RECORD_AUDIO, Permission.CALL_PHONE, Permission.SEND_SMS])
        
        self.setup_ui()
        Clock.schedule_interval(self.update_ui, 1/60)

    def setup_ui(self):
        with self.canvas.before:
            Color(0, 0, 0.05, 1)
            self.bg = Ellipse(pos=(-Window.width, -Window.height), size=(Window.width*3, Window.height*3))
        
        self.status = Label(text="[color=00f2ff]SYSTEM READY[/color]", markup=True,
                          pos_hint={'center_x': 0.5, 'center_y': 0.1}, font_size='16sp')
        self.add_widget(self.status)

    def update_ui(self, dt):
        self.angle += 2
        self.canvas.clear()
        self.setup_ui()
        with self.canvas:
            Color(0, 0.8, 1, 0.6) # Arc Reactor Blue
            Line(circle=(Window.width/2, Window.height/2, 140, self.angle, self.angle+100), width=2.5)
            Line(circle=(Window.width/2, Window.height/2, 140, self.angle+180, self.angle+280), width=2.5)
            Color(0, 1, 1, 0.1)
            Ellipse(pos=(Window.width/2-90, Window.height/2-90), size=(180, 180))

    def speak(self, text):
        async def _gen():
            c = edge_tts.Communicate(text, JARVIS_VOICE, pitch="-5Hz", rate="+5%")
            await c.save(VOICE_FILE)
        asyncio.run(_gen())
        pygame.mixer.init()
        pygame.mixer.music.load(VOICE_FILE)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): continue

    def process_command(self):
        with sr.Microphone() as source:
            self.status.text = "[color=00ff00]LISTENING...[/color]"
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                query = self.recognizer.recognize_google(audio).lower()
                self.status.text = f"[color=00f2ff]{query}[/color]"
                
                if "jarvis" in query:
                    self.speak("Yes Boss, standing by.")
                # Add more logic here (whatsapp, calls, etc.)
            except:
                self.status.text = "[color=00f2ff]SYSTEM IDLE[/color]"

    def on_touch_down(self, touch):
        threading.Thread(target=self.process_command).start()

# --- MAIN APP ---
class JarvisApp(App):
    def build(self):
        self.hud = JarvisHUD()
        return self.hud

    def on_start(self):
        # Jaise hi app khulega, Jarvis Greet karega
        Clock.schedule_once(self.welcome_note, 1)

    def welcome_note(self, dt):
        threading.Thread(target=self.initial_greeting).start()

    def initial_greeting(self):
        hour = datetime.datetime.now().hour
        name = self.hud.brain.get_mem("boss_name")
        greet = "Good Morning" if 0 <= hour < 12 else "Good Afternoon" if 12 <= hour < 18 else "Good Evening"
        
        self.hud.status.text = "[color=00f2ff]GREETING BOSS...[/color]"
        self.hud.speak(f"{greet} {name}. All systems are online. How can I help you today?")
        self.hud.status.text = "[color=00f2ff]SYSTEM ONLINE[/color]"

if __name__ == "__main__":
    JarvisApp().run()