# Requirements
Requires python packages [bs4](https://pypi.org/project/bs4/) and [selenium](https://pypi.org/project/selenium/)

Run `pip install -r requirements.txt` to install required packages

# Collecting posts
Run `python collect.py <Instagram username, such as wilmasannarbor>` to collect posts into lines of `posts.txt`

# Parsing posts
Run `python parse.py` to parse posts listed in `posts.txt`

# Extract (normalize) data
Run `python normalize.py <field name>` to collect data into `<field name>.csv`
For example, for the field `num_comments` (collected during `python parse.py`) representing number of comments on a post, running `python normalize.py num_comments` will collect the `num_comments` from all of the posts into `num_comments.csv`

# Plotting data
Use [matplotlib](https://matplotlib.org/gallery/index.html)?
