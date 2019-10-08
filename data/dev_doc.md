# Internal Development Doc

## Rebasing To SDL
Here are the steps to update the database when SDL releases a new update.

1. Copy the sdl db header, `SDL2-VER\src\joystick\SDL_gamecontrollerdb.h`, into the `data` folder and append the version at the end. This is used when running our unit tests to make sure upstream mappings aren't modified.
2. Run `python check.py --import_header data\SDL_gamecontrollerdbVER.h gamecontrollerdb.txt` to see what will be imported, and if there are issues.
3. If everything is fine, run `python check.py --import_header data\SDL_gamecontrollerdbVER.h gamecontrollerdb.txt --format` to import and save the new mappings.
4. Edit `check.py` and update the version string at the top : `sdl_version = "VER"`.
5. Run `python check.py gamecontrollerdb.txt --format` one last time to make sure everything is gucci and to update the db version string.