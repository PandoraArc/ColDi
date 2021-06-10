<img src="https://github.com/PandoraArc/ColDi/blob/main/ColDi/ColDi_logo.png" width="150">

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

#or in case the enviroment is imported from ColDi.yml
conda activate pyimageJ_ColDi
```

then go to the ColDi directory and and run the main.py

```
cd ~/ColDi
python main.py
```
if everything can run perfectly, the graphica interface like this should be shown up

<img src="https://github.com/PandoraArc/ColDi/blob/main/ColDi_userinterface.png" width="250">

All parameters are same as parameter found in imageJ program. When every parameter is added, you can analyze colony diameter by just clicking "Analyze" button
the result of your input will be save in save location as .csv and .xlsx file. The program also provide every picture along the process

## Example input and result

For example input image and result from ColDI can be found in folder Example
