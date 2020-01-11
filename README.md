sswave
------------

*Wavetable processing tools for the Intellijel/Cylonix Shapeshifter Eurorack module*

sswave is a command-line program that enables import, export and plotting of wavetable data from Intellijel Shapeshifter firmware files.

Most commands will require you to refer to a .jic file. Download the latest firmware from https://intellijel.com/eurorack-modules/cylonix-shapeshifter/.

**This project is incomplete – it doesn't actually enable import of wavetables yet.** I lost interest at some point, no longer own a Shapeshifter and cannot verify working import. The project is made available so others may use the export functions or develop it further.

Work on this project started in a [Jupyter notebook](https://github.com/tangram/sswave/blob/master/Shapeshifter%20avetable%20workbook.ipynb), which is supplied.


Local development setup
=======================

Install [poetry](https://python-poetry.org/), then install dependencies with:

    $ poetry install

Run sswave:

    $ poetry shell
    $ sswave --help
    $ sswave list shapeshifter_v2.03.jic


License
=======

Copyright © 2020 Eirik Krogstad, MIT License – see [LICENSE](https://github.com/tangram/sswave/blob/master/LICENSE) for details.
