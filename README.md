# Snake
>Neural Networks playing snake game trained by genetic algorithm

<p align="center">
  <img src="./animation.gif">
</p>

A personal project made by Robin Mancini and myself, consisting in training neural networks to play the game "Snake"

This repository contains:
- The Snake Game itself
- A Genetic Algorithm module
- A Neural Network module
- A main file with toy examples

I timed most functions to be sure to improve speed and used numba jit for compiling some functions, the genetic algorithm is parallelized for its main part (snakes evaluation) using multiprocessing and joblib


## Installation

Python 3 was used for this project and I can't promess that older versions are compatibles

Libraries you'll need to run the project:

{``joblib``, ``numpy``, ``numba``, ``pygame``}

Clone the repo using

```sh
git clone https://github.com/valentinmace/snake.git
```

## Usage

You will find some ready to run examples in ``main.py`` file.

You can try to:
- Play snake
- Train your own neural networks (it can take a while to get good results)
- Display a game played by neural networks that I trained and selected four you

Everything is explaind in the file, just uncomment parts that you want to execute, then go to terminal and do:
```sh
python main.py
```

## Notes

Do not hesitate to contact me if you need some help

Everything is made by me, I did not want to use existing framework for the genetic algorithm or neural network for learning purposes. I also coded the game with performance in mind rather than conception elegance.

I have published (or will publish depending on when you read this) a serie of youtube tutorial videos on [my channel](https://www.youtube.com/channel/UCMIW0JKxoxBDM5yiiF17SrA) (in french)


## Meta

Valentin Macé – [LinkedIn](https://www.linkedin.com/in/valentin-mac%C3%A9-310683165/) – [YouTube](https://www.youtube.com/channel/UCMIW0JKxoxBDM5yiiF17SrA) – [Twitter](https://twitter.com/ValentinMace) - valentin.mace@kedgebs.com

Distributed under the MIT license. See ``LICENSE`` for more information.
