## SDL_GameControllerDB

A community source database of game controller mappings to be used with SDL2
Game Controller functionality.

#### Notes:

This repo originally came from
[gabomdq/SDL_GameControllerDB](https://github.com/gabomdq/SDL_GameControllerDB).
However, the repo looked abandoned with lots of outstanding pull requests. I
went ahead and took the initiative to clone the repo, find all outstanding forks
with meaningful changes in them, merge everything all back together, and develop a
system to try and maintain order. Hopefully, it will stay like this (at least for
a little bit).

#### Usage:

Download gamecontrollerdb.txt, place it in your app's directory and load with:

```
SDL_GameControllerAddMappingsFromFile("gamecontrollerdb.txt");
```

#### Creating new mappings:

To create new mappings, you can use the controllermap utility provided with SDL2.

You can also use Steam's Big Picture mode. Configure your joystick and then look
in config/config.vdf in your Steam installation directory for the
SDL_GamepadBind entry.

#### Checking your mappings:

Do not check in any duplicate mappings unless they are necessary. Run the
following script to make sure you aren't duplicating anything. If everything is
ok, nothing will be printed:

```
./parse.py gamecontrollerdb.txt
```

Once you are happy with the results, generate a new file with:

```
./parse.py gamecontrollerdb.txt -o new.txt
# or for the adventerous
./parse.py gamecontrollerdb.txt -o gamecontrollerdb.txt
```

This will sort the file and place everything in the right spot. Use this before
committing any changes.

#### Duplicate GUIDs:

If you absolutely need to duplicate a GUID, place a `DUPE_OK` comment at the top of the
file to indicate to the script that this is ok. For example:

```
# DUPE_OK 03000000790000001100000000000000
...
03000000790000001100000000000000,Retrolink Classic Controller,a:b2,b:b1,back:b8,leftshoulder:b4,leftx:a3,lefty:a4,platform:Mac OS X,rightshoulder:b5,start:b9,x:b3,y:b0,
...
03000000790000001100000000000000,Sega Saturn Gamepad,a:b1,b:b2,leftshoulder:b6,lefttrigger:b3,leftx:a0,lefty:a4,platform:Windows,rightshoulder:b7,righttrigger:b0,start:b8,x:b4,y:b5,
```

However, note that if you do this, and you are targeting those devices, you will
need to have a custom `gamecontrolledb.txt` for each platform. When SDL loads
the file, it overwrites existing GUIDs. The platform tag is only used as a final
check before loading the configuration. So for the example above, the controller
would only work properly in Windows, not Mac.

#### General ideas:

- Don't duplicate GUIDs unless you need to
- Keep the file clean
- Come up with good names for the devices

#### References:

* [SDL2](http://www.libsdl.org)
* [SDL_GameControllerAddMappingsFromFile](http://wiki.libsdl.org/SDL_GameControllerAddMappingsFromFile)
* [SDL_joystick.c](https://hg.libsdl.org/SDL/file/c48ab2c208a2/src/joystick/SDL_joystick.c)
* [SDL_gamecontroller.c](https://hg.libsdl.org/SDL/file/c48ab2c208a2/src/joystick/SDL_gamecontroller.c)
