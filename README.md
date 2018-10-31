# Snake
>Neural Networks playing snake game trained by genetic algorithm

<p align="center">
  <img src="./animation.gif">
</p>

A personal project consisting in training neural networks to play the game "Snake"

This repository contains:
- The Snake Game itself
- A Genetic Algorithm module
- A Neural Network module
- A main file with toy examples

## Installation

Python 3 was used for this project and I can't promess that older versions are compatibles

Libraries you'll need to run the project:

{``joblib``, ``numpy``, ``numba``, ``pygame``}

Clone the repo using

```sh
git clone https://github.com/valentinmace/snake.git
```

## Usage


## Notes

Do not hesitate to contact me if you need some help

Everything is made by me, I did not want to use existing framework for the genetic algorithm or neural network for learning purposes. I also coded the game with performance in mind rather than conception elegance.

I timed most functions to be sure to improve speed and used numba jit for compiling some functions, the genetic algorithm is parallelized for its main part (snakes evaluation) using multiprocessing and joblib

I have published (or will publish depending on when you read this) a serie of youtube tutorial videos on my channel (in french):

``https://www.youtube.com/channel/UCMIW0JKxoxBDM5yiiF17SrA``

## Meta

Macé Valentin – [LinkedIn](https://www.linkedin.com/in/valentin-mac%C3%A9-310683165/) – valentin.mace@kedgebs.com

Distributed under the MIT license. See ``LICENSE`` for more information.
