# Conway's Game of Life

The game starts with an initial configuration of live and dead cells. The rules are then applied repeatedly to each cell in the grid, creating a sequence of generations.  

Key Features:

- Emergence: Despite the simple rules, complex patterns and structures can emerge from the initial configuration.   

- Self-replication: Some patterns can create copies of themselves, demonstrating a form of self-replication.  
- Turing Completeness: The Game of Life has been proven to be Turing complete, meaning it can simulate any computer algorithm.

# Run
You can run with clean initial board using:

`python gol.py`

You can also initialize the board with live cells using the `--seed` command line argument:

`python gol.py --seed 50`

The default window size is 960x960. You can change few settings in settings.py file.

# Controls

- Use mouse left click to toggle cell state. 
- Use Enter to start/pause/resume the animation.
- Use Sapcebar to reset the board.