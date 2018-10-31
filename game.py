# Valentin Macé
# valentin.mace@kedgebs.com
# Developed for fun
# Feel free to use this code as you wish as long as you quote me as author

"""
game.py
~~~~~~~~~~

This module defines a game of snake which can be displayed or not, playable or not
It uses Pygame for the display

Todos:
- It would be cool to make it more general in order to have a game of "anything" so
  the Genetic algorithm could run games regardless of what it's playing, I'll work on it
  for later projects
- Rethink the class and be able to save the state of the game
"""

from map import *
from pygame.locals import *
from snake import *


class Game:
    """ Game Class """

    def __init__(self):
        self.game_score = 0     # contains the snake fitness at the end of the game
        self.game_time = 0      # number of iteration de game has been played (useful to stop long games)

    def start(self, display=False, neural_net=None, playable=False, speed=20):
        """
        Wraps run_invisible and run_visibile for simplicity when starting a game

        Note:
        Arguments are not checked for the sake of performance when starting a big amount
        of games (in the GA typically) so you might generate bugs if you start using something like
        playable=True and passing a neural_net so .."we are all consenting adults here" ;)

        :param display: boolean display or not the game
        :param neural_net: NeuralNetwork to provide for not playable game
        :param playable: boolean to play manually or not the game
        :param speed: game speed for displayed games
        :return: int score achieved
        """
        if not display:
            return self.run_invisible(neural_net=neural_net)
        else:
            return self.run_visible(neural_net=neural_net, playable=playable, speed=speed)

    def run_invisible(self, neural_net=None):
        """
        Runs a undisplayed game played by a neural network

        The game is played as fast as possible, you might want fix a limit for the duration of the game,
        I advise to add 'or self.game_time > x' to the end condition

        :param neural_net: NeuralNetwork that will play the game
        :return: int score achieved
        """
        snake = Snake(neural_net=neural_net)        # creation of the snake and of its little brain
        map = Map(snake)                            # map creation

        cont = True                                 # main game loop
        while cont:
            self.game_time += 1
            map.scan()                              # gives vision of the environment to the snake
            snake.AI()                              # decision of the neural net (brain of the snake)
            snake.update()                          # snake is moving and aging
            map.update()                            # checking for collision of snake with walls or food
            if not snake.alive:
                cont = False
                self.game_time = 0
        self.game_score = snake.fitness()           # if the game is over, returns the score
        return self.game_score

    def run_visible(self, playable=False, neural_net=None, speed=20):
        """
        Runs a displayed game played by a neural network or by human

        :param playable: boolean to play manually or not the game
        :param neural_net: NeuralNetwork to provide for not playable game
        :param speed: game speed
        :return: int score achieved
        """
        pygame.init()                                                               # pygame initialization
        game_window = pygame.display.set_mode((int(WINDOW_SIZE*2), WINDOW_SIZE))    # opens window
        pygame.display.set_caption(WINDOW_TITLE)

        snake = Snake(neural_net=neural_net)
        map = Map(snake)

        cont = [True]
        while cont[0]:                               # main game loop
            pygame.time.Clock().tick(speed)             # display speed
            self.inputs_management(snake, cont)      # inputs handling
            if not playable:
                map.scan()                           # gives vision to the snake
                snake.AI()                           # snake makes decision
            self.render(game_window, map)            # render the game
            snake.update()
            map.update()
            if not snake.alive:
                cont[0] = False

        self.game_score = snake.fitness()            # if the game is over, returns the score
        return self.game_score

    def inputs_management(self, snake, cont):
        """
        Keyboard inputs management
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                cont[0] = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:       # escape
                    cont[0] = False
                if event.key == K_RIGHT:        # right
                    snake.turn_right()
                elif event.key == K_LEFT:       # left
                    snake.turn_left()
                elif event.key == K_UP:         # up
                    pass

    def render(self, window, map):
        """
        Renders the game
        Works by calling render() for the map which in turn will call render for the snake etc.
        """
        map.render(window)
        pygame.display.flip()
