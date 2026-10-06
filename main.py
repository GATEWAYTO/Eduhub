import os
import webbrowser
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.utils import platform

DOWNLOAD_LINKS = {
    "Syllabus": {
        "2026": {
            "Physics": "https://raw.githubusercontent.com/GATEWAYTO/Board-Exam-2027-CBSE/main/Syllabus/Physics_SecP2_2026-27.pdf",
            "Math": "https://raw.githubusercontent.com/GATEWAYTO/Board-Exam-2027-CBSE/main/Syllabus/Maths_SecP2_2026-27.pdf",
            "Chemistry": "https://raw.githubusercontent.com/GATEWAYTO/Board-Exam-2027-CBSE/main/Syllabus/Chemistry_SecP2_2026-27.pdf",
            "English": "https://raw.githubusercontent.com/GATEWAYTO/Board-Exam-2027-CBSE/main/Syllabus/English_core_SecP2_2026-27.pdf",
        }
    },
    "Question Paper": {},
    "Marking Scheme": {},
}


# --- SPLASH SCREEN ---
class SplashScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Fallback dark background for splash
        with self.canvas.before:
            Color(0.05, 0.05, 0.08, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(Widget())

        # Start with solid white text
        self.logo_label = Label(
            text="Edu Hub",
            font_size="50sp",
            bold=True,
            color=(1, 1, 1, 1), 
            size_hint_y=None,
            height=100,
        )
        layout.add_widget(self.logo_label)
        layout.add_widget(Widget())

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def on_enter(self):
        # Expands in size and fades to 0 opacity to simulate a blurry/out-of-focus exit
        anim = Animation(font_size=120, opacity=0, duration=2.0)
        anim.start(self.logo_label)

        # Transition to main screen after 2.5 seconds
        Clock.schedule_once(self.switch_to_main, 2.5)

    def switch_to_main(self, dt):
        self.manager.current = "main"


# --- MAIN APP SCREEN ---
class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Custom Uploaded Background Image Handling
        with self.canvas.before:
            Color(1, 1, 1, 1)
            if os.path.exists('background.jpg'):
                self.bg_rect = Rectangle(source='background.jpg', size=self.size, pos=self.pos)
            else:
                # Dark fallback if image is missing
                Color(0.1, 0.1, 0.15, 1) 
                self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Main UI Layout
        layout = BoxLayout(orientation="vertical", padding=30, spacing=15)

        # App Header
        header = Label(
            text="Edu Hub",
            font_size="40sp",
            bold=True,
            size_hint_y=None,
            height=60,
            color=(1, 1, 1, 1), # White header
        )
        layout.add_widget(header)

        # --- Apple UI Style Settings (Glassmorphism) ---
        glass_bg = (1, 1, 1, 0.25) # Transparent white tiles
        text_col = (1, 1, 1, 1)    # White text
        label_col = (0.9, 0.9, 0.9, 1)

        # Resource Type
        layout.add_widget(Label(text="Select Resource Type", font_size="16sp", color=label_col, size_hint_y=None, height=20, halign="left"))
        self.type_spinner = Spinner(
            text="Syllabus", values=("Syllabus", "Question Paper", "Marking Scheme"),
            size_hint_y=None, height=55, font_size="18sp", bold=True,
            background_normal='', background_color=glass_bg, color=text_col
        )
        layout.add_widget(self.type_spinner)

        # Year
        layout.add_widget(Label(text="Select Year", font_size="16sp", color=label_col, size_hint_y=None, height=20))
        self.year_spinner = Spinner(
            text="2026", values=("2026", "2027"),
            size_hint_y=None, height=55, font_size="18sp", bold=True,
            background_normal='', background_color=glass_bg, color=text_col
        )
        layout.add_widget(self.year_spinner)

        # Subject
        layout.add_widget(Label(text="Select Subject", font_size="16sp", color=label_col, size_hint_y=None, height=20))
        self.subject_spinner = Spinner(
            text="Physics", values=("Physics", "Math", "Chemistry", "English"),
            size_hint_y=None, height=55, font_size="18sp", bold=True,
            background_normal='', background_color=glass_bg, color=text_col
        )
        layout.add_widget(self.subject_spinner)

        # Status Label
        self.status_label = Label(text="", size_hint_y=None, height=40, color=(0.4, 1, 0.4, 1), bold=True)
        layout.add_widget(self.status_label)

        # Premium Modern Download Button
        download_btn = Button(
            text="Confirm & Download",
            background_normal='',
            background_color=(0, 0.47, 1, 0.85), # Apple/Premium Translucent Blue
            color=(1, 1, 1, 1),
            font_size="20sp",
            bold=True,
            size_hint_y=None,
            height=60,
        )
        download_btn.bind(on_press=self.trigger_download)
        layout.add_widget(download_btn)

        # Spacer pushes everything to the top
        layout.add_widget(Widget())

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def trigger_download(self, instance):
        doc_type = self.type_spinner.text
        year = self.year_spinner.text
        subject = self.subject_spinner.text

        links_for_type = DOWNLOAD_LINKS.get(doc_type, {})
        links_for_year = links_for_type.get(year, {})
        url = links_for_year.get(subject)

        if url:
            self.status_label.text = f"Opening {subject}..."
            self.status_label.color = (0.4, 1, 0.4, 1)
            if platform == "android":
                try:
                    from jnius import autoclass
                    PythonActivity = autoclass("org.kivy.android.PythonActivity")
                    Intent = autoclass("android.content.Intent")
                    Uri = autoclass("android.net.Uri")
                    intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                    PythonActivity.mActivity.startActivity(intent)
                except Exception:
                    webbrowser.open(url)
            else:
                webbrowser.open(url)
        else:
            self.status_label.text = "File not available yet."
            self.status_label.color = (1, 0.3, 0.3, 1)


class EduHubApp(App):

    def build(self):
        sm = ScreenManager(transition=FadeTransition(duration=1.0))
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        return sm


if __name__ == "__main__":
    EduHubApp().run()
