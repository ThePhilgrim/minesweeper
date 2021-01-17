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
- Keep `image_sources.txt` up to date.
