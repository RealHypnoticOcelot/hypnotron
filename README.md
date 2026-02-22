# Hypnotron
###### Multi-purpose Discord Bot

## How to use:

**(Optional: create a virtual environment)**

Not necessary if using Nix.

Navigate to the directory the script was downloaded in, and run the following command:
```python
python3 -m venv env && source env/bin/activate
```
Uses Python version 3.13.11!

**Install Dependencies:**

#### For normal users:

Install the dependencies required with the following command:

```python
pip3 install -r requirements.txt
```

Install ffmpeg at [ffmpeg.org](https://www.ffmpeg.org/download.html), if you don't have it already.
If you're on MacOS and have `brew` installed, you can just run `brew install ffmpeg`.

#### For Nix users:

Simply navigate to the application, run `nix develop`, and use the commands below!

### Usage

1. Enable/disable modules.

Edit main.py, and toggle on or off anything you'd like to enable/disable from the modules folder.

2. Configure `.env` file

Edit the `.env` file, and replace the options with the relevant ones for your enabled modules!

3. Run the bot
```python
python3 main.py
```
That's it!

### (Optional: Generate country images)
Country images are provided by default, but maybe they've become outdated!
```python
python3 generate_countries.py /path/to/shapefile
```
This script expects to be fed the path to your shapefile(`.shp`) containing all of your countries.
It's designed specifically to read the [Natural Earth 1:10m Admin-0 country dataset](<https://www.naturalearthdata.com/downloads/10m-cultural-vectors/>), v5.1.1(though it might support later).
It'll also generate a pickle(`.pkl`) containing information about each country! Most information is provided by the dataset, but emojis are from the `country_flags.pkl`.

###### If you have any issues, questions, concerns or suggestions, create an issue or pull request