# minesweeper
This is a minesweeper game to make two amateur coders into pros.
Run these commands to play it:

```
git clone https://github.com/ThePhilgrim/minesweeper
cd minesweeper
python3 minesweeper.py
```

On Windows you likely need `py` instead of `python3`.


## Notes about developing

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

## Notes about creating executable file on Mac OS

To reproduce the installer, please run the following commands: (for reference: https://www.youtube.com/watch?v=DVOoHL2Bp_o&t=461s&ab_channel=SamanthaCruz, http://www.marinamele.com/from-a-python-script-to-a-portable-mac-application-with-py2app)
- The executable is created with py2app. Run `pip3 install -U py2app` in terminal to install.
- Make sure that you are located in the minesweeper directory. In your terminal, run `python3 setup.py py2app`
- The .app file is found in the newly created 'dist' folder.
