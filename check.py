#!/usr/bin/env python3

import fileinput
import string
import sys

success = True

def error (message):
    global success;
    success = False
    print("Error at #" + str(fileinput.lineno()), ":", message)
    print(line)

def check_guid (guid):
    if len (guid) != 32:
        error ("The length of the guid string must be equal to 32")
    for c in guid:
        if not c in string.hexdigits:
            error ("Each character in guid string must be a hex character " + string.hexdigits)

def check_mapping (mappingstring):
    keys = ["platform", "leftx", "lefty", "rightx", "righty", "a", "b", "back", "dpdown", \
            "dpleft", "dpright", "dpup", "guide", "leftshoulder", "leftstick", \
            "lefttrigger", "rightshoulder", "rightstick", "righttrigger", "start", "x", "y"]
    platforms = ["Linux", "Mac OS X", "Windows"]
    mappings = mappingstring.split (',')
    for mapping in mappings:
        if not mapping:
            continue
        if len (mapping.split(':')) != 2:
            error ("Invalid mapping : " + mapping)
            continue
        key = mapping.split (':')[0]
        value = mapping.split (':')[1]
        if not key in keys:
            error ("Invalid key \"" + key + "\" in mapping string")

        # Check values
        if key == "platform":
            if value not in platforms:
                error ("Invalid platform \"" + value + "\" in mapping string")
        else:
            if not value:
                continue
            if not value[0] in ['a', 'h', 'b']:
                error ("Invalid value \"" + value + "\" for key \"" + key +
                       "\". Should start with a, b, or h")
            elif value[0] in ['a', 'b']:
                if not value[1:].isnumeric():
                    error ("Invalid value \"" + value + "\" for key \"" + key +
                           "\". Should be followed by a number after 'a' or 'b'")
            else:
                dpad_positions = map(str, [0, 1, 2, 4, 8, 1|2, 2|4, 4|8, 8|1])
                dpad_index = value[1:].split ('.')[0]
                dpad_position = value[1:].split ('.')[1]
                if not dpad_index.isnumeric():
                    error ("Invalid value \"" + value + "\" for key \"" + key +
                           "\". Dpad index \"" + dpad_index + "\" should be a number")
                if not dpad_position in dpad_positions:
                    error ("Invalid value \"" + value + "\" for key \"" + key +
                           "\". Dpad position \"" + dpad_position + "\" should be one of" +
                           ', '.join(dpad_positions))

for line in fileinput.input():
    if line.startswith('#') or line == '\n':
        continue
    splitted = line[:-1].split(',', 2)
    if len(splitted) < 3 or not splitted[0] or not splitted[1] or not splitted[2]:
        error ("Either GUID/Name/Mappingstring is missing or empty")
    check_guid(splitted[0])
    check_mapping(splitted[2])

if not success:
    sys.exit(1)
