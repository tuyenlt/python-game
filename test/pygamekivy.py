import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen

# Màn hình chơi game
class GameWidget(Widget):
    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.square_size = 50
        self.position = (self.width / 2 - self.square_size / 2, self.height / 2 - self.square_size / 2)
        self.direction = (1, 1)
        Clock.schedule_interval(self.update, 1.0 / 60.0)  # Cập nhật 60 FPS

    def on_size(self, *args):
        self.position = (self.width / 2 - self.square_size / 2, self.height / 2 - self.square_size / 2)

    def update(self, dt):
        # Di chuyển hình vuông
        self.position = (self.position[0] + self.direction[0] * 5, self.position[1] + self.direction[1] * 5)

        # Kiểm tra va chạm với biên
        if self.position[0] <= 0 or self.position[0] >= self.width - self.square_size:
            self.direction = (-self.direction[0], self.direction[1])
        if self.position[1] <= 0 or self.position[1] >= self.height - self.square_size:
            self.direction = (self.direction[0], -self.direction[1])

        self.canvas.clear()  # Xóa canvas trước khi vẽ
        with self.canvas:
            Color(1, 0, 0)  # Màu đỏ
            Rectangle(pos=self.position, size=(self.square_size, self.square_size))

# Màn hình chỉ dẫn
class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructionsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Instructions:\n\nMove the red square around the screen.\nPress back to return to the main menu.'))
        back_button = Button(text='Back to Menu')
        back_button.bind(on_press=self.back_to_menu)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def back_to_menu(self, instance):
        self.manager.current = 'menu'

# Màn hình menu chính
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        title = Label(text='Game Menu', font_size='40sp')
        layout.add_widget(title)
        start_button = Button(text='Start Game')
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)
        instructions_button = Button(text='Instructions')
        instructions_button.bind(on_press=self.show_instructions)
        layout.add_widget(instructions_button)
        exit_button = Button(text='Exit')
        exit_button.bind(on_press=self.exit_game)
        layout.add_widget(exit_button)
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'game'

    def show_instructions(self, instance):
        self.manager.current = 'instructions'

    def exit_game(self, instance):
        App.get_running_app().stop()

# Màn hình trò chơi
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

# Lớp chính của ứng dụng
class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(InstructionsScreen(name='instructions'))
        return sm

if __name__ == '__main__':
    GameApp().run()
