import pyglet
from settings import *
from pyglet.window import mouse
from pyglet.window import key
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
    def __init__(self, *args, seed=None, **kwargs):
        super(GameOfLife, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.game_state = 0
        self.seed = seed
        self.black_tile_img = pyglet.resource.image("TileBlack.png")
        self.blue_tile_img = pyglet.resource.image("TileBlue.png")
        self.imgs = {0: self.blue_tile_img, 1:self.black_tile_img}
        self.rows, self.cols = self.height//SPRITE_HEIGHT, self.width//SPRITE_WIDTH
        self.snapshot = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.sprites = {}
        self.update_q = {}
        self.alive = set()
        for r in range(self.rows):
            for c in range(self.cols):
                x, y = c*SPRITE_WIDTH, r*SPRITE_HEIGHT
                self.sprites[(r,c)] = BlueTile(x=x, y=y, batch=self.batch)
        self.seed_init()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_state == 0 and (button & mouse.LEFT):
            c = x // SPRITE_WIDTH
            r = y // SPRITE_HEIGHT
            self.toggle_tile(r,c)

    def on_key_press(self, symbol, modifiers):
        if symbol & key.RETURN:
            self.game_state = 1 - self.game_state
        elif symbol & key.SPACE:
            self.clear_board()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def seed_init(self):
        if isinstance(self.seed, int) and 0<self.seed<=self.rows*self.cols:
            while len(self.update_q) < self.seed:
                r, c = random.randint(20, 30), random.randint(20, 30)
                self.toggle_tile(r,c) 

    def clear_board(self):
        self.game_state = 0
        for r,c in self.alive:
            self.toggle_tile(r,c)
        self.alive.clear()
        self.seed_init()

    def update(self, dt):
        if self.game_state:
            self.take_step()
        self.update_snapshot()

    def update_snapshot(self):
        for (r,c), life in self.update_q.items():
            if self.sprites[(r,c)].life:
                self.alive.add((r,c))
            elif (r,c) in self.alive:
                self.alive.remove((r,c))
            self.snapshot[r][c] = life
        self.update_q.clear()
        if len(self.alive) == 0:
            self.game_state = 0

    def toggle_tile(self, r, c):
        self.sprites[(r,c)].life = 1 - self.sprites[(r,c)].life
        self.sprites[(r,c)].image = self.imgs[self.sprites[(r,c)].life]
        if (r,c) in self.update_q:
            del self.update_q[(r,c)]
        else:
            self.update_q[(r,c)] = self.sprites[(r,c)].life

    def take_step(self):
        candidates = set()
        for key in self.alive:
            r, c = key
            candidates = candidates.union(self.get_neighbors(r,c))

        for r,c in candidates:
            cur_state = self.snapshot[r][c]
            new_state = self.get_new_state(r,c)
            if new_state != cur_state:
                self.toggle_tile(r,c)

    def get_neighbors(self, r, c):
        neighbors = set()    
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                nr, nc = r+i, c+j
                if (0<=nr<self.rows) and (0<=nc<self.cols):          
                    neighbors.add((nr,nc))
        return neighbors
            
    def get_new_state(self, r, c):
        neighbors = self.get_neighbors(r,c)
        neighbors.remove((r,c))
        live_neighbor_count = 0
        is_alive = self.snapshot[r][c]
        new_state = 0
        for nr,nc in neighbors:
            live_neighbor_count += self.snapshot[nr][nc]
        if live_neighbor_count == 3:
            new_state = 1
        elif live_neighbor_count == 2 and is_alive:
            new_state = 1
        return new_state
        

if __name__ == "__main__":
    pyglet.resource.path = [SPRITES_DIR]
    pyglet.resource.reindex()
    width, height = WIN_SIZE
    width = (width // SPRITE_WIDTH) * SPRITE_WIDTH
    height = (height // SPRITE_HEIGHT) * SPRITE_HEIGHT
    gol = GameOfLife(width, height, seed=50, caption="Game of Life: select tiles, hit Enter to start/stop, Space to clear")
    pyglet.clock.schedule_interval(gol.update, interval=0.1)
    pyglet.app.run()
