import pyglet
from settings import *

# class BlackTile(pyglet.sprite.Sprite):
#     def __init__(self, *args, **kwargs):
#         self.black_tile = pyglet.image.load(SPRITES_DIR+"TileBlack.png")
        
#         super(BlackTile, self).__init__(*args, **kwargs)
        
#         self.color = "black"

class GameOfLife(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(GameOfLife, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.black_tile = pyglet.resource.image("TileBlue.png")
        self.tile = pyglet.sprite.Sprite(self.black_tile, x=0, y=0, batch=self.batch)
        # self.caption = "Game of Life"

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    pyglet.resource.path = [SPRITES_DIR]
    pyglet.resource.reindex()
    gol = GameOfLife(*WIN_SIZE, caption="Game of Life")
    pyglet.app.run()
