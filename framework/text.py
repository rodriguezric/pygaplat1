from framework.screen import screen, WIDTH, HEIGHT
from framework.font import font_16
from framework import color

class Text:
    def __init__(self, text='', font=font_16, color=color.white, width=None):
        self.text = text
        self.font = font
        self.color = color
        self.width = width
        if width is None:
            self.width = self.font.render(self.text, True, self.color).get_rect().w

    def render(self):
        return self.font.render(self.text, True, self.color)


class ScrollingText:
    def __init__(self, text='', font=font_16, color=color.white, width=None):
        self.text = text
        self.font = font
        self.color = color
        self.i = 0
        self.width = width
        if width is None:
            self.width = self.font.render(self.text, True, self.color).get_rect().w
        
    @property
    def finished(self):
        return self.i == len(self.text)

    def inc(self):
        if not self.finished:
            self.i += 1

    def fill(self):
        self.i = len(self.text)

    def render(self):
        return self.font.render(self.text[:self.i], True, self.color)

def center_text(text_obj, y=None):
    if y is None: y = HEIGHT//2

    screen.blit(text_obj.render(), (WIDTH//2 - text_obj.width//2,y))

def draw_text(text_obj, x, y):
    screen.blit(text_obj.render(), (x, y))

