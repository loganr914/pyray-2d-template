# Pyray 2D Template
### Template for making low resolution 2D games with integer scaling for 

  This template is for making games that emulate retro 2D pixel art 
  
  Going too low on the render resolution or framerate will result in jittery movements, especially if the render resolution isn't an integer division of your display's native dimensions.


## Getting Started
### Dependencies

* Python (3.11+)
* raylib (5.5+)

### Installation

Clone this repo by running:
```
$ git clone https://github.com/loganr914/pyray-2d-pixel-template
```
in your terminal and navigate to that directory

### Running

* If you installed raylib as a system-wide Python package, run:
```
$ python filename.py
```
* If you installed raylib in a virtual environment with uv, run:
```
$ uv run filename.py
```

## Help

I anticipate that some noobs like myself would find it hard to correctly remove certain parts of the code to more closely fit the game they have in mind, so here's some different removals I think some people would want:

### Single screen

If you want to make a single screen game (no start screen or pause menus, just the gameplay), delete the ```screens.py``` file and remove:
```
$ draw dem screens
```
from the ```main.py``` file.

## License

This project is licensed under the MIT License - see the LICENSE file for details
