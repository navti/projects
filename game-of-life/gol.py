import pyglet
from settings import *
import random

class BlackTile(pyglet.sprite.Sprite):
    def __init__(self, **kwargs):
        img = pyglet.resource.image("TileBlack.png")
        super(BlackTile, self).__init__(img, **kwargs)
        self.life = 1

class BlueTile(pyglet.sprite.Sprite):
    def __init__(self, **kwargs):
        img = pyglet.resource.image("TileBlue.png")
        super(BlueTile, self).__init__(img, **kwargs)
        self.life = 0

class GameOfLife(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(GameOfLife, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.black_tile_img = pyglet.resource.image("TileBlack.png")
        self.blue_tile_img = pyglet.resource.image("TileBlue.png")
        self.imgs = {0: self.blue_tile_img, 1:self.black_tile_img}
        rows, cols = self.height//SPRITE_HEIGHT, self.width//SPRITE_WIDTH
        self.snapshot = [[0 for _ in range(cols)] for _ in range(rows)]
        self.sprites = {}
        for r in range(rows):
            for c in range(cols):
                x, y = c*SPRITE_WIDTH, r*SPRITE_HEIGHT
                self.sprites[(r,c)] = BlueTile(x=x, y=y, batch=self.batch)
    
    def on_mouse_press(self, x, y, button, modifiers):
        c = x // SPRITE_WIDTH
        r = y // SPRITE_HEIGHT
        self.toggle_tile(r,c)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def toggle_tile(self, r, c):
        self.sprites[(r,c)].life = 1 - self.sprites[(r,c)].life
        self.sprites[(r,c)].image = self.imgs[self.sprites[(r,c)].life]

    def update(self, dt):
        pass


if __name__ == "__main__":
    pyglet.resource.path = [SPRITES_DIR]
    pyglet.resource.reindex()
    width, height = WIN_SIZE
    width = (width // SPRITE_WIDTH) * SPRITE_WIDTH
    height = (height // SPRITE_HEIGHT) * SPRITE_HEIGHT
    gol = GameOfLife(width, height, caption="Game of Life")
    pyglet.clock.schedule_interval(gol.update, interval=0.2)
    pyglet.app.run()
