[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Auto Blog Banner Generator

A Python script to generate blog banners. This script is used at [RavSam](https://www.ravsam.in/blog/).

The following image is an example of the blog banner generated by this script:

![](/assets/banner.png)

## Prerequisites

These things are required before setting up the project.

- Git
- Ubuntu 18.04 or 20.04
- Python

## Usage

Follow these instructions to get the project up and running.

```bash
# clone the repo
$ git clone https://github.com/ravsamhq/auto-blog-banner.git

# change directory
$ cd auto-blog-banner

# set up project
$ bash src/scripts/setup.sh

# run main
$ python src/main.py $icons $path $name

# example
$ python src/main.py 'font/svgs/solid/robot.svg,font/svgs/brands/google.svg' '/home/username/Public/blogs/hello-world/assets/images/' 'this-is-a-demo-title'
```

## Development

Follow these instructions to get the project up and running.

```bash
# clone the repo
$ git clone https://github.com/ravsamhq/auto-blog-banner.git

# change directory
$ cd auto-blog-banner

# set up project
$ bash src/scripts/setup.sh

# run main
$ python src/main.py
```

## Tech Stack

- [Python](https://python.org/)

## Authors

- [Ravgeet Dhillon](https://github.com/ravgeetdhillon)

## Extra

- We are open for [issues and feature requests](https://github.com/ravsamhq/notify-slack-action/issues).
- In case you get stuck at somewhere, feel free to contact at [Mail](mailto:info@ravsam.in).

<small>&copy; 2021 RavSam Web Solutions</small>
