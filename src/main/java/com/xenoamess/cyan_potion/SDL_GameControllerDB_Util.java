package com.xenoamess.cyan_potion;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

/**
 * @author XenoAmess
 */
public class SDL_GameControllerDB_Util {
    private static String SDL_GameControllerDB = null;

    public static String getSDL_GameControllerDB() {
        if (SDL_GameControllerDB == null) {
            SDL_GameControllerDB = loadFile("/gamecontrollerdb.txt");
        }
        return SDL_GameControllerDB;
    }

    private static URL getURL(String resourceFilePath) {
        final URL res = SDL_GameControllerDB_Util.class.getResource(resourceFilePath);
        return res;
    }

    private static String loadFile(String resourceFilePath) {
        String res = "";
        try (
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(getURL(resourceFilePath).openStream()));
        ) {
            final StringBuffer sb = new StringBuffer();
            String tmp;
            while (true) {
                tmp = bufferedReader.readLine();
                if (tmp == null) {
                    break;
                }
                sb.append(tmp);
                sb.append("\n");
            }
            res = sb.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return res;
    }
}