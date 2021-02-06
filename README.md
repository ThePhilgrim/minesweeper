# Minesweeper
This is a minesweeper game to make two amateur coders into pros.
On Windows, you can download `minesweeper.exe` from [the releases page](https://github.com/ThePhilgrim/minesweeper/releases).
On other operating systems, make sure you have Python with Tkinter, and run these commands:

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

When a commit is pushed (or a pull request is merged) to `main`,
`.github/workflows/windows_build.yml` automatically builds a file named `minesweeper.exe`
and makes a new release containing it.

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

Virtual Environments:
- To keep installations project-specific, a virtual environment can be used. This prevents ones computer
  from being affected by black, pyinstaller, and other things used for the game.

- Installation: cd to the minesweeper folder in your terminal, and run `python3 -m venv env`
- Activation: Activate the virtual env –
  Windows;  `env\Scripts\activate`
  Mac; `source/env/bin/activate`
- To delete the virtual env, simply delete the "env" folder inside of the minesweeper folder.

Images:
- There is a big and small version of each image. The big images are used to produce the small images.
- If you change the sizes of the small images, change `minesweeper.py` to use the new size.
- When resizing a big image to make a small image, make sure that the small image has transparent background.
- Keep `images/sources.txt` up to date.

## Creating Mac .app file

To reproduce the installer, please run the following commands: (for reference: https://www.youtube.com/watch?v=DVOoHL2Bp_o&t=461s&ab_channel=SamanthaCruz, http://www.marinamele.com/from-a-python-script-to-a-portable-mac-application-with-py2app)
- The executable is created with py2app. Run `pip3 install -U py2app` in terminal to install.
- Make sure that you are located in the minesweeper directory. In your terminal, run `python3 setup.py py2app`
- The .app file is found in the newly created 'dist' folder.
