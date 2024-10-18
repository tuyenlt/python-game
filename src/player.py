import pyglet

class Player:
    def __init__(self, x, y):
        self.width = 50  # Size of the player box
        self.height = 50
        self.color = (0, 0, 255)  # Player color (blue)
        self.shape = pyglet.shapes.Rectangle(x - self.width // 2, y - self.height // 2,
                                             self.width, self.height, color=self.color)

    def draw(self):
        self.shape.draw()  # Simply draw the rectangle (no need for glColor3f)

    def move(self, dx, dy):
        # Move the player by changing the shape's position
        self.shape.x += dx
        self.shape.y += dy

    def keep_in_bounds(self, window_width, window_height):
        # Ensure the player stays within the window bounds
        if self.shape.x < 0:
            self.shape.x = 0
        if self.shape.x + self.shape.width > window_width:
            self.shape.x = window_width - self.shape.width

        if self.shape.y < 0:
            self.shape.y = 0
        if self.shape.y + self.shape.height > window_height:
            self.shape.y = window_height - self.shape.height
