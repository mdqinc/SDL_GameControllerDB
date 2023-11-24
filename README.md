# SDL_GameControllerDB

A community sourced database of game controller mappings to be used with SDL2 Game Controller functionality.

# Usage
Download gamecontrollerdb.txt, place it in your app's directory and load it.

SDL2:
```c
SDL_GameControllerAddMappingsFromFile("gamecontrollerdb.txt");
```

SDL3:
```c
SDL_AddGamepadMappingsFromFile("gamecontrollerdb.txt");
```

The database is compatible with SDL v2.0.10 and newer.

## Create New Mappings
A mapping looks like this:
```
030000004c050000c405000000010000,PS4 Controller,a:b1,b:b2,back:b8,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b4,leftstick:b10,lefttrigger:a3,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b11,righttrigger:a4,rightx:a2,righty:a5,start:b9,x:b0,y:b3,platform:Mac OS X,
```
It includes controller GUID (`030000004c050000c405000000010000`), a name (`PS4 Controller`), button / axis mappings (`leftshoulder:b4`) and a platform (`platform:Mac OS X`).

Please make sure to check that the name is a good description of the controller. If relevant, include the controller's name and model number.

## Mapping Guide

![SDL Game Controller Mapping Guide](mapping_guide.png)

## Mapping Tools
There are a few different tools that let you create mappings.

### [SDL2 Gamepad Tool](http://www.generalarcade.com/gamepadtool/)
Third party cross-platform tool with GUI (Windows, macOS and Linux)

#### Note: While convenient, this tool has fallen out of date as SDL has amended and added new features for gamepad support (see issue [#478](https://github.com/gabomdq/SDL_GameControllerDB/issues/476)). As such, maps authored with this tool require greater scrutiny to ensure they will not break support for explicit mappings the SDL project provides.

### [SDL2 Gamepad Mapper](https://gitlab.com/ryochan7/sdl2-gamepad-mapper/-/releases)
Open source GUI app for authoring mappings. Builds available for Windows and Linux.

### [SDL](https://github.com/libsdl-org/SDL/releases/latest)
[testcontroller (SDL3)](https://github.com/libsdl-org/SDL/blob/main/test/testcontroller.c) and [controllermap (SDL2)](https://github.com/libsdl-org/SDL/blob/SDL2/test/controllermap.c) utilities are the official tools to create these mappings on all SDL supported platforms (Windows, Mac, Linux, iOS, Android, etc).

### [Steam](http://store.steampowered.com)
In Steam's Big Picture mode, configure your gamepad. Then look in `[steam_installation_directory]/config/config.vdf` in your Steam installation directory for the `SDL_GamepadBind` entry. It is one of the last entries, it will look something like this:

```
"SDL_GamepadBind"		"030000004c050000c405000000010000,PS4 Controller,platform:Windows,a:b1,b:b2,back:b8,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b4,leftstick:b10,lefttrigger:a3,leftx:a0,lefty:a1,rightshoulder:b5,rightstick:b11,righttrigger:a4,rightx:a2,righty:a5,start:b9,x:b0,y:b3,"
```

## Resources

* [SDL2](http://www.libsdl.org)
* [SDL_GameControllerAddMappingsFromFile](http://wiki.libsdl.org/SDL_GameControllerAddMappingsFromFile)
