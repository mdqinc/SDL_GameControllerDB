# SDL_GameControllerDB

[![Build Status](https://travis-ci.org/gabomdq/SDL_GameControllerDB.svg?branch=master)](https://travis-ci.org/gabomdq/SDL_GameControllerDB)

A community source database of game controller mappings to be used with SDL2 Game Controller functionality.

## SDL Variants
### gamecontrollerdb.txt
For games or engines using the SDL >= 2.0.6 format. This is the most recent version.

### gamecontrollerdb_205.txt
For games or engines using the SDL >= 2.0.5 format. There are no range or inversion modifiers (+,-,~).

### gamecontrollerdb_204.txt
For games or engines using the SDL 2.0.4 format. GUIDs are different depending on the platform. Note that SDL > 2.0.4 can still read this format.

## Create New Mappings
A mapping looks like this :
```
030000004c050000c405000000010000,PS4 Controller,a:b1,b:b2,back:b8,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b4,leftstick:b10,lefttrigger:a3,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b11,righttrigger:a4,rightx:a2,righty:a5,start:b9,x:b0,y:b3,platform:Mac OS X,
```
It is comprised of a controller GUID (`030000004c050000c405000000010000`), a name (`PS4 Controller`), button / axis mappings (`leftshoulder:b4`) and a platform (`platform:Mac OS X`).

## Naming Convention
- If the controller has a unique name, use that (ex. XBox Controller, XBox One Controller).
- If the controller doesn't have a unique name, or when in doubt, use brand + model (ex. ACME GA09, 8Bitdo NES30 Pro).
- You can add `Wireless` for controllers with such an option. (ex. XBox Wireless Controller).

## Mapping Tools
There are a few different tools that let you create mappings.

### [SDL2 Gamepad Tool](http://www.generalarcade.com/gamepadtool/)
Third party cross-platform tool with GUI (Windows, macOS and Linux). Likely the easiest tool to use.

### [SDL2 ControllerMap](https://www.libsdl.org/download-2.0.php)
The controllermap utility provided with SDL2 is the official tool to create these mappings, it runs on all the platforms SDL runs (Windows, Mac, Linux, iOS, Android, etc).

### [Steam](http://store.steampowered.com)
In Steam's Big Picture mode, configure your joystick. Then look in `[steam_installation_directory]/config/config.vdf` in your Steam installation directory for the `SDL_GamepadBind` entry. It is one of the last entries, it will look something like this.

```
"SDL_GamepadBind"		"030000004c050000c405000000010000,PS4 Controller,platform:Windows,a:b1,b:b2,back:b8,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b4,leftstick:b10,lefttrigger:a3,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b11,righttrigger:a4,rightx:a2,righty:a5,start:b9,x:b0,y:b3,"
```

Unfortunately, Steam outputs the platform field at the beginning, so you will need to move it to the end manually. Move `platform:Windows,` or `platform:Mac OS X,` or `platform:Linux,` to the end of the mapping (with the trailing comma).

You will also need check that the name is a good description of the controller. If relevant, include the controller's name and model number.

## Standard Mappings
Some controllers are a little tricky to figure out. Here are the recommended mappings.

![mapping standard](data/mapping_guide.png)

# Usage
Download gamecontrollerdb.txt, place it in your app's directory and load it.

For example :
```
SDL_GameControllerAddMappingsFromFile("gamecontrollerdb.txt");
```

## Upstream SDL Mappings
This project includes all mappings from the latest SDL_gamecontrollerdb.h. The community db adds a superset of mappings to the official ones, it does not modify them in any way.

If you ever wish to modify one of these mappings, you will need to send a PR directly to the SDL project. The changes will get pulled in the community db when a new SDL release occurs.

# For Contributors
## Check Your Mappings
The currently active version is gamecontrollerdb.txt. If your mappings work on older SDL versions, you can add them to the appropriate files.
Before submitting a new Pull Request, please run the `check.py` tool to make sure everything is in order.

Run it with:
```
python check.py gamecontrollerdb.txt
```

Once no issues are detected, run the script with the `--format` option to sort the database in the appropriate format.
```
python check.py --format gamecontrollerdb.txt
```

You may now send a Pull Request. Tests are automatically run on Pull Requests, so you'll easily see if there is an issue.

### Unit Tests
- GUID is correct length and is hexadecimal.
- GUID is in 2.0.5+ format.
- Platform is present and supported.
- Inversion and range modifiers are applied to axis fields.
- No duplicate mappings.
- No duplicate keys.
- Buttons conform to supported values.
- Hats aren't 0 or diagonals.
- No upstream official mappings are modified.
- All mappings end with a comma.

### Formatting
- The database is sorted by platform, then by name.
- Individual mapping keys are sorted alphabetically.
- Names are parsed for extraneous spaces.

### Options
```
usage: check.py [-h] [--format] [--convert_guids] [--add_missing_platform]
                [--import_header sdl_header]
                input_file

positional arguments:
  input_file            database file to check, ex. gamecontrollerdb.txt

optional arguments:
  -h, --help            show this help message and exit
  --format              sorts, formats and removes duplicates
  --convert_guids       convert Windows and macOS GUIDs to the newer SDL 2.0.5
                        format
  --add_missing_platform
                        adds a platform field if it is missing on Windows and
                        Mac OS X 2.0.4 entries
  --import_header sdl_header
                        imports and overrides mappings using
                        SDL_gamecontrollerdb.h
```

## Resources

* [SDL2](http://www.libsdl.org)
* [SDL_GameControllerAddMappingsFromFile](http://wiki.libsdl.org/SDL_GameControllerAddMappingsFromFile)
