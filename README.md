# SDL_GameControllerDB

[![Build Status](https://travis-ci.org/p-groarke/SDL_GameControllerDB.svg?branch=master)](https://travis-ci.org/p-groarke/SDL_GameControllerDB)

A community source database of game controller mappings to be used with SDL2 Game Controller functionality.

## Releases
### [2.0.5](https://github.com/p-groarke/SDL_GameControllerDB/releases/tag/2.0.5)
For games or engines using the SDL 2.0.5 format. There are no range or inversion modifiers (+,-,~). It contains 282 controller entries, with duplicates removed.

### [2.0.4](https://github.com/p-groarke/SDL_GameControllerDB/releases/tag/2.0.4)
For games or engines using the SDL 2.0.4 format. GUIDs are different depending on the platform. It contains 237 controller entries, with duplicates removed.

## Create New Mappings
A mapping looks like this :
```
030000004c050000c405000000010000,PS4 Controller,a:b1,b:b2,back:b8,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b4,leftstick:b10,lefttrigger:a3,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b11,righttrigger:a4,rightx:a2,righty:a5,start:b9,x:b0,y:b3,platform:Mac OS X,
```
It is comprised of a controller GUID (`030000004c050000c405000000010000`), a name (`PS4 Controller`), button / axis mappings (`leftshoulder:b4`) and a platform (`platform:Mac OS X`).

There are a few different ways to create mappings. Here are some options. If you know of other tools, I would be happy to add them to the list.

### [SDL2 Gamepad Tool](http://www.generalarcade.com/gamepadtool/)
This seems to be the easiest and most reliable way to configure your gamepad. It is cross-platform (Windows, macOS and Linux).

<img src="http://www.generalarcade.com/gamepadtool/gamepadtool.png" height="auto" width="360">

Setup your controller and copy the ouput entry. The tool currently doesn't output SDL 2.0.5 GUIDs, but that is fine as SDL still supports these GUIDs. I will convert older GUIDs in pull requests as well.

### [Steam](http://store.steampowered.com)
In Steam's Big Picture mode, configure your joystick. Then look in `[steam_installation_directory]/config/config.vdf` in your Steam installation directory for the `SDL_GamepadBind` entry. It is one of the last entries, it will look something like this.

```
"SDL_GamepadBind"		"030000004c050000c405000000010000,PS4 Controller,a:b1,b:b2,back:b8,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b4,leftstick:b10,lefttrigger:a3,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b11,righttrigger:a4,rightx:a2,righty:a5,start:b9,x:b0,y:b3,"
```

Unfortunately, **Steam does not ouput the platform field**, so you will need to add it manually. At the end of the generated entry, add `platform:Windows,` or `platform:Mac OS X,` or `platform:Linux,`.

### [SDL2 ControllerMap](https://www.libsdl.org/download-2.0.php)
You can also use the controllermap utility provided with SDL2.

## Usage
Download gamecontrollerdb.txt, place it in your app's directory and load it.

For example :
```
SDL_GameControllerAddMappingsFromFile("gamecontrollerdb.txt");
```

# For Contributors
## Check Your Mappings
Before submitting a new Pull Request, please run the `check.py` tool to make sure everything is in order. It requires python3 installed. Run it with:
```
python3 check.py gamecontrollerdb.txt
```

If no errors were generated you can (please) send a Pull Request! Tests are automatically run on Pull Requests, so you'll easily see if there is an issue.

### New Checks
- Tests are run to ensure a platform is present.
- Tests are run to make sure inversion and range modifiers are applied to axis fields.
- Tests are run to check for duplicates.

### Options
```
usage: check.py [-h] [--sort] [--convert_guids] [--remove_dupes]
                [--add_missing_platform]
                input_file

positional arguments:
  input_file            database file to check (gamecontrollerdb.txt)

optional arguments:
  -h, --help            show this help message and exit
  --sort                sort the database on success
  --convert_guids       convert Windows and macOS GUIDs to the newer SDL 2.0.5
                        format
  --remove_dupes        automatically remove duplicates
  --add_missing_platform
                        adds a platform field if it is missing (on older pre
                        2.0.5 entries). Skips checks!
```

## References

* [SDL2](http://www.libsdl.org)
* [SDL_GameControllerAddMappingsFromFile](http://wiki.libsdl.org/SDL_GameControllerAddMappingsFromFile)
