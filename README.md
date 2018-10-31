# snake
>Neural Networks playing snake game trained by genetic algorithm

<p align="center">
  <img src="./animation.gif">
</p>

The main purpose of this repository is to run the FCM for the relation classification task on several corpus, using multiples word embeddings and to compute results (such as micro-f1, macro-f1, weighted-f1 etc.)

This repository is made of multiple pieces, the heart being the FCM C++ [implementation by Mo Yu](https://github.com/Gorov/FCM_nips_workshop)

I have build two python scripts around it:

- 1- The first (main) one is used to run the FCM on a chosen corpus, tuning learning rate and number of epochs, using one or many word embeddings and finally getting results in a file

- 2- The second one is used to convert a corpus from a Semeval 2010 format to a format usable by the FCM (adding various taggs, dependency path information etc.), if you ever wish to use my work on another corpus and if you can easily have your corpus in a Semeval 2010 format ..

These 2 scripts are **INDEPENDANT**, if you wish to just use one of them no need to care for installation of the other

I already provide Semeval 2010, Semeval 2018 and reAce 2005 corpus with all results using several word embeddings (see ``results/macro_f1`` folder) so the conversion script may not be that useful

## Installation

This repository is for Windows use, a linux version might come in a near future and it should be relatively easy to make it yourself

For the main script you need python 3 and the following packages:

{ ``numpy``, ``sklearn``, ``scipy``}

For the conversion script you need python 3 and the following packages:

{ ``numpy``,  ``scipy``, ``spacy``, ``networkx`` }

Sorry for not making an executable but these are useful libraries anyway :)


- To use the main script, you first need to compile the FCM code, open a terminal in ``fcm`` folder and ``make``, since this repo is for Windows I recommend using [MinGW](https://sourceforge.net/projects/mingw-w64/) (don't forget to add it to your PATH environment variable)

Example: make with MinGW

```sh
mingw32-make
```

- To use the conversion script, you need to compile the SST code (which is a tagger), open a terminal in ``data/corpus/raw_to_formated_script/sst`` folder and ``make`` (as before I recommend MinGW and ``mingw32-make``)

For this script to run you also need gzip (precisely you need gunzip, its decompression tool) installed for command line usage, you can get it [here](http://gnuwin32.sourceforge.net/packages/gzip.htm) (don't forget to add it to your PATH environment variable), gunzip might not be recognized as a terminal command, please refer to [my Stackoverflow answer](https://stackoverflow.com/questions/51905489/using-gunzip-on-windows-in-command-line/51905574#51905574) in that case

>In conclusion the installation might seem complicated but for the main script to run you just need to "make" the FCM and the few python libraries listed, for the conversion script you need to "make" the SST and get gunzip as a terminal command


## Usage main script

Open a terminal in the ``root`` folder and execute:
```sh
python fcm_global.py <train data> <test_data> <epochs> <learning rate> [word embeddings]
```
Example:
```sh
python fcm_global.py semeval2018_train semeval2018_test 30 0.005
```
Get results in the ``results/macro_f1`` folder

Notes:
- If you do not write a word embedding argument, it will run on every word embeddings available in the ``data/word_emb`` folder
- Train data and test data files have to be in the ``data/corpus/formated folder``
- In this repo I only provide one small word embeddings (github size restriction) but you can get bigger and better performing on [my drive](https://drive.google.com/drive/folders/18KrHhJcpOouFEf1Dgqw8N6Hpg6gxEZjH)


## Usage conversion script

To convert a corpus in Semeval 2010 format to a format usable by FCM (see ``data/corpus/raw_to_formated_script.py`` comments for more details)

Open a terminal in the ``data/corpus/raw_to_formated_script`` folder and execute:
```sh
python raw_to_formated.py <file to convert>
```
Example:
```sh
python raw_to_formated.py semeval2018_train
```
Get results in the ``data/corpus/formated`` folder

Notes:
- File to convert has to be in the ``data/corpus/raw folder`` and of course in a Semeval 2010 format
- This script is available in a jupyter notebook version (in french) for better visual understanding in the ``...notebook`` folder

## Notes

Do not hesitate to contact me if you need some help

I let the Semeval 2010 official scorer il the ``results`` folder if you ever need to use it

## Meta

Macé Valentin – [LinkedIn](https://www.linkedin.com/in/valentin-mac%C3%A9-310683165/) – valentin.mace@kedgebs.com

Distributed under the MIT license. See ``LICENSE`` for more information.
