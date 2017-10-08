## SDL_GameControllerDB

[![Build Status](https://travis-ci.org/p-groarke/SDL_GameControllerDB.svg?branch=master)](https://travis-ci.org/p-groarke/SDL_GameControllerDB)

A community source database of game controller mappings to be used with SDL2 Game Controller functionality.

#### Usage:

Download gamecontrollerdb.txt, place it in your app's directory and load with:

```
SDL_GameControllerAddMappingsFromFile("gamecontrollerdb.txt");
```

#### Creating new mappings:

To create new mappings, you can use the controllermap utility provided with SDL2.

You can also use Steam's Big Picture mode. Configure your joystick and then look in config/config.vdf in your Steam installation directory for the SDL_GamepadBind entry.

#### Checking your mappings:
You need to have python3 installed. Run

```
python3 check.py gamecontrollerdb.txt
```

If no errors were generated, the database file will be sorted. You can now send a Pull Request.

#### References:

* [SDL2](http://www.libsdl.org)
* [SDL_GameControllerAddMappingsFromFile](http://wiki.libsdl.org/SDL_GameControllerAddMappingsFromFile)
