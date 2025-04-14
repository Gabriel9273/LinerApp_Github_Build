from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line, Color
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from PIL import Image as PILImage
import os

class LinerWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.input_width = TextInput(hint_text="Width", multiline=False)
        self.input_height = TextInput(hint_text="Height", multiline=False)
        self.input_coords = TextInput(hint_text="Coordinates (x1,y1,x2,y2)", multiline=False)
        self.input_thickness = TextInput(hint_text="Line Thickness", multiline=False)

        self.add_widget(self.input_width)
        self.add_widget(self.input_height)
        self.add_widget(self.input_coords)
        self.add_widget(self.input_thickness)

        self.draw_btn = Button(text="Draw Lines")
        self.draw_btn.bind(on_press=self.draw_lines)
        self.add_widget(self.draw_btn)

        self.select_img_btn = Button(text="Select Background Image")
        self.select_img_btn.bind(on_press=self.select_image)
        self.add_widget(self.select_img_btn)

        self.save_btn = Button(text="Save Image")
        self.save_btn.bind(on_press=self.save_image)
        self.add_widget(self.save_btn)

        self.canvas_widget = Image()
        self.add_widget(self.canvas_widget)

        self.selected_image_path = None

    def select_image(self, instance):
        chooser = FileChooserIconView()
        popup = Popup(title="Select Image", content=chooser, size_hint=(0.9, 0.9))

        def on_selection(*args):
            if chooser.selection:
                self.selected_image_path = chooser.selection[0]
                self.canvas_widget.source = self.selected_image_path
                self.canvas_widget.reload()
                popup.dismiss()

        chooser.bind(on_submit=lambda *args: on_selection())
        popup.open()

    def draw_lines(self, instance):
        if not self.selected_image_path:
            return

        coords_text = self.input_coords.text
        thickness = int(self.input_thickness.text) if self.input_thickness.text.isdigit() else 1

        try:
            x1, y1, x2, y2 = map(int, coords_text.split(','))
            with self.canvas_widget.canvas:
                Color(1, 0, 0, 1)
                Line(points=[x1, y1, x2, y2], width=thickness)
        except Exception as e:
            print("Error drawing line:", e)

    def save_image(self, instance):
        if not self.selected_image_path:
            return
        filename = "output.png"
        self.export_to_png(filename)
        print("Saved:", filename)

class LinerApp(App):
    def build(self):
        return LinerWidget()

if __name__ == "__main__":
    LinerApp().run()