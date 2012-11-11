# Open 13

Open13 is a project to collect information on provincial legislatures in Canada, including legislators, bills, votes, committees, events and speeches. This data is made available through a [website](http://open13.ca/) and its [API](http://open13.ca/api/).

## Dependencies

You need Python 2.7 or greater. Install [Git](http://git.io/) and [virtualenv](http://pypi.python.org/pypi/virtualenv) to create isolated Python development environments. Restart your shell after running the commands below.

### Ubuntu

```sh
sudo apt-get install git virtualenvwrapper python-lxml
```

If your shell is `bash`, it should automatically load `virtualenvwrapper` through `/etc/bash_completion.d/virtualenvwrapper`.

### OS X

Use the Homebrew package manager.

```sh
ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)"
brew install git
sudo easy_install pip
sudo pip install virtualenv virtualenvwrapper
cd $HOME
mkdir .virtualenvs
```

Have your shell run `/usr/local/bin/virtualenvwrapper.sh` on login, e.g.:

```sh
echo "source /usr/local/bin/virtualenvwrapper.sh" >> .bash_login
```

Or:

```sh
echo "source /usr/local/bin/virtualenvwrapper.sh" >> .zshrc
```

## Getting Started

Fork [the main Git repository](https://github.com/opennorth/open13) on GitHub, clone your fork, and change into its directory:

```sh
git clone https://github.com/YOURUSERNAME/open13.git
cd open13
```

Next, create a development environment. If your version of `virtualenv` is less than 1.7, omit the `--system-site-packages` switch:

```sh
mkvirtualenv open13 --system-site-packages
```

Finally, install the requirements:

```sh
pip install -r requirements.txt
cp billy_settings.py.example billy_settings.py
```

You're now ready to work on Open13!

## Writing a Scraper

For now, see the [OpenStates documentation](http://openstates.org/contributing/).

## Acknowledgements

We would like to express our gratitude to [James Turk](https://twitter.com/jamesturk), [Paul Tagliamonte](https://twitter.com/paultag) and [Thom Neale](https://twitter.com/twneale) of [Sunlight Labs](http://sunlightlabs.com/)'s [OpenStates](http://openstates.org/) team for helping Open North start this project in Canada.

## Bugs? Questions?

This project's main repository is on GitHub: [http://github.com/opennorth/open13](http://github.com/opennorth/open13), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Copyright (c) 2012 Open North Inc., released under the MIT license
