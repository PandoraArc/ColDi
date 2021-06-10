# ColDi
A fast way to measure bacterial colony diameter by imageJ

The python project provides a wrapper functions for analyzing bacterial colony diameter using pyimagej with a simple graphical user interface.

## Installation
ColDi can be run in pyimageJ enviroment. In order to install the enviroment, please fellow the link https://github.com/imagej/pyimage.
ColDi alos require additional python library including pandas, numpy, matplotlib.pyplot.

Alternatively, the enviroment used compatibly with ColDi is also provided. you can import enviroment by using conda command

```
conda env create -n pyimageJ_ColDi -f ColDi.yml
```

## Usage
The first step when using ColDi is to activate pyimageJ enviroment by using command 

```
conda activate pyimagej
```

then go to the ColDi directory and and run the main.py

```
cd ~/ColDi
python main.py
```
