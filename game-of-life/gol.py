import pyglet
from settings import *
from pyglet.window import mouse
from pyglet.window import key

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
        self.update_q = {}
        self.alive = set()
        for r in range(rows):
            for c in range(cols):
                x, y = c*SPRITE_WIDTH, r*SPRITE_HEIGHT
                self.sprites[(r,c)] = BlueTile(x=x, y=y, batch=self.batch)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if (button & mouse.LEFT):
            c = x // SPRITE_WIDTH
            r = y // SPRITE_HEIGHT
            self.toggle_tile(r,c)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def toggle_tile(self, r, c):
        self.sprites[(r,c)].life = 1 - self.sprites[(r,c)].life
        self.sprites[(r,c)].image = self.imgs[self.sprites[(r,c)].life]
        if (r,c) in self.update_q:
            del self.update_q[(r,c)]
        else:
            self.update_q[(r,c)] = self.sprites[(r,c)].life

    def update(self, dt):
        self.update_snapshot()
        print("something")

    def update_snapshot(self):
        for (r,c), life in self.update_q.items():
            if self.sprites[(r,c)].life:
                self.alive.add((r,c))
            elif (r,c) in self.alive:
                self.alive.remove((r,c))
            self.snapshot[r][c] = life
        self.update_q.clear()

if __name__ == "__main__":
    pyglet.resource.path = [SPRITES_DIR]
    pyglet.resource.reindex()
    width, height = WIN_SIZE
    width = (width // SPRITE_WIDTH) * SPRITE_WIDTH
    height = (height // SPRITE_HEIGHT) * SPRITE_HEIGHT
    gol = GameOfLife(width, height, caption="Game of Life: select live tiles and hit spacebar!")
    pyglet.clock.schedule_interval(gol.update, interval=5.0)
    pyglet.app.run()
