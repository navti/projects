import pyglet
from settings import *
from pyglet.window import mouse
from pyglet.window import key
import random
import argparse

class BlackTile(pyglet.sprite.Sprite):
    """
    Class BlackTile to create new black tile sprites
    """
    def __init__(self, **kwargs):
        img = pyglet.resource.image("TileBlack.png")
        super(BlackTile, self).__init__(img, **kwargs)
        self.life = 1

class BlueTile(pyglet.sprite.Sprite):
    """
    Class BlueTile to create new black tile sprites
    """
    def __init__(self, **kwargs):
        img = pyglet.resource.image("TileBlue.png")
        super(BlueTile, self).__init__(img, **kwargs)
        self.life = 0

class GameOfLife(pyglet.window.Window):
    """
    Class GameOfLife creates new game/board of Conway's game of life.
    
    Rules:
    1. A live cell dies if it has fewer than two live neighbors.
    2. A live cell with two or three live neighbors lives on to the next generation.
    3. A live cell with more than three live neighbors dies.
    4. A dead cell will be brought back to live if it has exactly three live neighbors.
    """
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
        """
        on_mouse_press checks for mouse left click and draws brings a cell to life.       
        :param x: x coordinate of mouse click
        :param y: y coordinate of mouse click
        :param button: the button on mouse that was pressed
        :param modifiers: the modifier key pressed on keyboard (ctrl, shift, etc)
        :return: None
        """
        if self.game_state == 0 and (button & mouse.LEFT):
            c = x // SPRITE_WIDTH
            r = y // SPRITE_HEIGHT
            self.toggle_tile(r,c)

    def on_key_press(self, symbol, modifiers):
        """
        on_key_press checks for space key press and clears the board
        :param symbol: the pressed key symbol passed to this function from the OS
        :param modifiers: modifier key pressed like ctrl or shift 
        :return: None
        """
        # Return to play/pause, Space to clear
        if symbol & key.RETURN:
            self.game_state = 1 - self.game_state
        elif symbol & key.SPACE:
            self.clear_board()

    def on_draw(self):
        """
        on_draw call to redraw window contents, called every frame
        :return: None
        """
        self.clear()
        self.batch.draw()

    def seed_init(self):
        """
        seed_init to initialize board with live cells.
        :return: None
        """
        if isinstance(self.seed, int) and 0<self.seed<=self.rows*self.cols:
            while len(self.update_q) < self.seed:
                rlow = self.rows//2 - 5
                rhigh = rlow + 9
                clow = self.cols//2 - 5
                chigh = clow + 9
                r, c = random.randint(rlow, rhigh), random.randint(clow, chigh)
                self.toggle_tile(r,c) 

    def clear_board(self):
        """
        clear_board to clear out live cells and reset all board parameters.
        :return: None
        """
        self.game_state = 0
        for r,c in self.alive:
            self.toggle_tile(r,c)
        self.alive.clear()
        self.seed_init()

    def update(self, dt):
        """
        update method to call every dt seconds and update board state.
        :param dt: passed implicitly by pyglet clock
        :return: None
        """
        if self.game_state:
            self.take_step()
        self.update_snapshot()

    def update_snapshot(self):
        """
        update_snapshot updates the buffered board state to be used in next generation
        :return: None
        """
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
        """
        toggle_tile toggles the cell, alive->dead, dead->alive
        :param r: the row number on the board
        :param c: the column number on the board
        :return: None
        """
        self.sprites[(r,c)].life = 1 - self.sprites[(r,c)].life
        self.sprites[(r,c)].image = self.imgs[self.sprites[(r,c)].life]
        if (r,c) in self.update_q:
            del self.update_q[(r,c)]
        else:
            self.update_q[(r,c)] = self.sprites[(r,c)].life

    def take_step(self):
        """
        take_step computes the next generation board state
        :return: None
        """
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
        """
        get_neighbors gets the neighbors of the cell with distance one
        :param r: row of the cell
        :param c: col of the cell
        :return: set of neighbors
        """
        neighbors = set()    
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                nr, nc = r+i, c+j
                if (0<=nr<self.rows) and (0<=nc<self.cols):          
                    neighbors.add((nr,nc))
        return neighbors
            
    def get_new_state(self, r, c):
        """
        get_new_state to get the new state of the cell
        :param r: the row no. of the current cell
        :param c: the col no. of the current cell
        :return: returns the new state of the cell, alive or dead
        """
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

def get_args():
    """
    get_args to get command line arguments
    """
    parser = argparse.ArgumentParser(description="Conway's Game of Life!")
    parser.add_argument('--seed', '-s', metavar='S', type=int, default=None, help='Initial number of live cells.')

    return parser.parse_args()

if __name__ == "__main__":
    """
    main block 
    set resource path for sprites
    adjust window size to fit in integral no. of sprites
    run pyglet app
    """
    args = get_args()
    pyglet.resource.path = [SPRITES_DIR]
    pyglet.resource.reindex()
    width, height = WIN_SIZE
    width = (width // SPRITE_WIDTH) * SPRITE_WIDTH
    height = (height // SPRITE_HEIGHT) * SPRITE_HEIGHT
    gol = GameOfLife(width, height, seed=args.seed, caption="Game of Life: select tiles, hit Enter to start/stop, Space to reset")
    pyglet.clock.schedule_interval(gol.update, interval=0.1)
    pyglet.app.run()
