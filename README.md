# Open 13

Open13 is a project to collect information on provincial legislatures in Canada, including legislators, bills, votes, committees, events and speeches. This data is made available through a [website](http://open13.ca/) and its [API](http://open13.ca/api/).

## Getting Started

Follow the instructions in the [Python Quick Start Guide](https://github.com/opennorth/opennorth.ca/wiki/Python-Quick-Start%3A-OS-X) to install Homebrew, Git, MongoDB, Python, virtualenv, GDAL and PostGIS.

On Ubuntu, run:

    sudo apt-get install git virtualenvwrapper python-lxml mongodb-10gen

If your shell is `bash`, it should automatically load `virtualenvwrapper` through `/etc/bash_completion.d/virtualenvwrapper`.

Fork [the main Git repository](https://github.com/opennorth/open13) on GitHub, clone your fork, and change into its directory:

    mkvirtualenv open13
    git clone https://github.com/YOURUSERNAME/open13.git
    cd open13
    pip install -r requirements.txt

You're now ready to work on Open13!

## Running Scrapers

Run `billy-update -h` to read the documentation. For now, we don't use `billy-util` for anything.

## Writing a Scraper

For now, see the [OpenStates documentation](http://openstates.org/contributing/).

## Acknowledgements

We would like to express our gratitude to [James Turk](https://twitter.com/jamesturk), [Paul Tagliamonte](https://twitter.com/paultag) and [Thom Neale](https://twitter.com/twneale) of [Sunlight Labs](http://sunlightlabs.com/)'s [OpenStates](http://openstates.org/) team for helping Open North start this project in Canada.

## Bugs? Questions?

This project's main repository is on GitHub: [http://github.com/opennorth/open13](http://github.com/opennorth/open13), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Copyright (c) 2012 Open North Inc., released under the MIT license
