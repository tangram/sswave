sswave
======

*Wavetable processing tools for the Intellijel/Cylonix Shapeshifter Eurorack module*

sswave is a command-line program that enables import, export and plotting of wavetable data from Intellijel Shapeshifter firmware files.

Most commands will require you to refer to a .jic file. Download the latest firmware from https://intellijel.com/eurorack-modules/cylonix-shapeshifter/.

**Please observe: The Wavetable data in these files should be considered Intellijel's and/or Cylonix' intellectual property. Distributing these separately is probably illegal.** However, manipulating firmware data for yourself, for a device you own, should be considered fair use.

**This project is incomplete – it doesn't actually enable import of wavetables yet.** I lost interest at some point, no longer own a Shapeshifter and cannot verify working import. The project is made available so others may use the export functions or develop it further.

Work on this project started in a [Jupyter notebook](https://github.com/tangram/sswave/blob/master/Shapeshifter%20wavetable%20workbook.ipynb), which is supplied.


Setup and usage
---------------

Python 3.6 or higher is required.

Clone or download this project, install [poetry](https://python-poetry.org/), then install dependencies with:

    $ poetry install

Run sswave:

    $ poetry shell
    $ sswave --help

Example for listing wavetables:
 
    $ sswave list shapeshifter_v2.03.jic

Further usage instructions can be found using the `--help` switch with each command.


License
-------

Copyright © 2020 Eirik Krogstad, MIT License – see [LICENSE](https://github.com/tangram/sswave/blob/master/LICENSE) for details.
