![image](https://github.com/patternizer/birdpy/blob/master/title_frame.png)

# birdpy

Development version of code to convert .mov clips of birds in flight to ornitographic trajectories inspired by
the work of http://www.xavibou.com/

## Contents

* `birdpy.py` - main script to be run with Python 3.6+

The first step is to clone latest birdpy code and step into the check out directory: 

    $ git clone https://github.com/patternizer/birdpy.git
    $ cd birdpy
    
### Using Standard Python 

The code should run with the [standard CPython](https://www.python.org/downloads/) installation and was tested 
in a conda virtual environment running a 64-bit version of Python 3.6+.

birdpy can be run from sources directly, once the following module requirements are resolved:

* `moviepy`
* 'film.MOV' (your raw footage)
* 'soundtrack.mp3'

with durations suitably set.

Run with:

    $ python birdpy.py
        
## License

The code is distributed under terms and conditions of the [MIT license](https://opensource.org/licenses/MIT).

## Contact information

* [Michael Taylor](https://patternizer.github.io)


