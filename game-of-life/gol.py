import pyglet
from settings import *

class BlackTile(pyglet.sprite.Sprite):
    def __init__(self, **kwargs):
        img = pyglet.resource.image("TileBlack.png")
        super(BlackTile, self).__init__(img, **kwargs)

class BlueTile(pyglet.sprite.Sprite):
    def __init__(self, **kwargs):
        img = pyglet.resource.image("TileBlue.png")
        super(BlueTile, self).__init__(img, **kwargs)


class GameOfLife(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(GameOfLife, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.sprites = {}
        rows, cols = self.height//SPRITE_HEIGHT, self.width//SPRITE_WIDTH
        for r in range(rows):
            for c in range(cols):
                x, y = c*SPRITE_WIDTH, r*SPRITE_HEIGHT
                self.sprites[(r,c)] = BlueTile(x=x, y=y, batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    pyglet.resource.path = [SPRITES_DIR]
    pyglet.resource.reindex()
    width, height = WIN_SIZE
    width = (width // SPRITE_WIDTH) * SPRITE_WIDTH
    height = (height // SPRITE_HEIGHT) * SPRITE_HEIGHT
    gol = GameOfLife(width, height, caption="Game of Life")
    pyglet.app.run()
