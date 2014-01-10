##SDL_GameControllerDB


A community source database of game controller mappings to be used with SDL2 Game Controller functionality.

####Usage:

Download gamecontrollerdb.txt, place it in your app's directory and load with:

```
SDL_GameControllerAddMappingsFromFile("gamecontrollerdb.txt");
```

####Creating new mappings:

To create new mappings, you can use the controllermap utility provided with
SDL2, or using Steam's Big Picture mode, configure your joystick and then 
look in config/config.vdf in your Steam installation directory for the 
SDL_GamepadBind entry.

####References:

* [SDL2](http://www.libsdl.org)
* [SDL_GameControllerAddMappingsFromFile](http://wiki.libsdl.org/SDL_GameControllerAddMappingsFromFile)