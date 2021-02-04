# Minesweeper
This is a minesweeper game to make two amateur coders into pros.
On Mac, you can install it from [the releases page](https://github.com/ThePhilgrim/minesweeper/releases).
Alternatively, if you have Python installed, you can run these commands to download and play it:

```
git clone https://github.com/ThePhilgrim/minesweeper
cd minesweeper
python3 minesweeper.py
```

On Windows you likely need `py` instead of `python3`.


## Developing

New changes should usually be made with pull requests.
Before merging, your pull request must be reviewed and approved by at least one other person.
When merging a pull request, choose "Squash and merge" from the little arrow in the merge button.
This way, each pull request shows up as one commit when looking at the commit log of `main` branch.

Run these commands to start working on a new pull request:

```
git checkout main
git pull
git checkout -b put_name_of_new_branch_here
```

This project uses [black](https://github.com/psf/black) to clean up code style.
Run these commands to use it:

```
python3 -m pip install black
python3 -m black minesweeper.py
```

Images:
- There is a big and small version of each image. The big images are used to produce the small images.
- If you change the sizes of the small images, change `minesweeper.py` to use the new size.
- When resizing a big image to make a small image, make sure that the small image has transparent background.
- Keep `images/sources.txt` up to date.

When a new commit is pushed (or a pull request is merged) to `main` branch,
a Mac `.app` is created and uploaded automatically by `.github/workflows/mac_build.yml`.

## Creating Windows .exe file

- code used in cmd console: pyinstaller --onefile --add-data images\button_small.png;. --add-data images\pressed_button_small.png;. --add-data images\flag_small.png;. --add-data images\bomb_small.png;. --add-data images\doomguy.gif;. --add-data images\bomb.png;. minesweeper.py
