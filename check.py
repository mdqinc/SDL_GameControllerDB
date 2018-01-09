#!/usr/bin/env python

import sys
# if sys.version_info[0] != 3:
#     print("This script requires Python 3.")
#     exit(1)

from collections import defaultdict
from collections import namedtuple
import string
import collections
import shutil
import argparse
import csv
import re

FILE_HEADER = "# Game Controller DB for SDL in post 2.0.6 format\n\
# Source: https://github.com/gabomdq/SDL_GameControllerDB\n"

mappings_dict = {
    "Windows": {},
    "Mac OS X": {},
    "Linux": {},
}

class Mapping:
    BUTTON_REGEXES = {
        "+a": re.compile(r"^[0-9]+\~?$"),
        "-a": re.compile(r"^[0-9]+\~?$"),
        "a": re.compile(r"^[0-9]+\~?$"),
        "b": re.compile(r"^[0-9]+$"),
        "h": re.compile(r"^[0-9]+\.(0|1|2|4|8|3|6|12|9)$"),
    }

    def __init__(self, mappingstring, linenumber):
        self.guid = ""
        self.name = ""
        self.platform = ""
        self.linenumber = 0
        self.__keys = {
            "+leftx": "",
            "+lefty": "",
            "+rightx": "",
            "+righty"
            "-leftx": "",
            "-lefty": "",
            "-rightx": "",
            "-righty": "",
            "a": "",
            "b": "",
            "back": "",
            "dpdown": "",
            "dpleft": "",
            "dpright": "",
            "dpup": "",
            "guide": "",
            "leftshoulder": "",
            "leftstick": "",
            "lefttrigger": "",
            "leftx": "",
            "lefty": "",
            "rightshoulder": "",
            "rightstick": "",
            "righttrigger": "",
            "rightx": "",
            "righty": "",
            "start": "",
            "x": "",
            "y": "",
        }

        self.linenumber = linenumber
        reader = csv.reader([mappingstring], skipinitialspace=True)
        mapping = next(reader)
        mapping = list(filter(None, mapping))
        self.set_guid(mapping[0])
        mapping.pop(0)
        self.set_name(mapping[0])
        mapping.pop(0)
        self.set_platform(mapping)
        self.set_keys(mapping)
        self.remove_empty_mappings()


    def set_guid(self, guid):
        if guid == "xinput":
            self.guid = guid
            return

        if len(guid) != 32:
            raise ValueError("GUID length must be 32.", guid)

        hex_digits = set(string.hexdigits)
        if not all(c in hex_digits for c in guid):
            raise ValueError("GUID malformed.", guid)

        self.guid = guid


    def set_name(self, name):
        name = re.sub(r" +", " ", name)
        self.name = name


    def set_platform(self, mapping):
        platform_kv = next((x for x in mapping if "platform:" in x), None)
        if platform_kv == None:
            raise ValueError("Required 'platform' field not found.")

        platform = platform_kv.split(':')[1]

        if platform not in mappings_dict.keys():
            raise ValueError("Invalid platform.", platform)

        self.platform = platform
        index = mapping.index(platform_kv)
        mapping.pop(index)


    def set_keys(self, mapping):
        throw = False
        error_msg = ""

        for kv in mapping:
            button_key, button_val = kv.split(':')

            if not button_key in self.__keys:
                raise ValueError("Unrecognized key.", button_key)

            # Gather duplicates.
            if self.__keys[button_key] is not "":
                throw = True
                error_msg += "%s (was %s:%s), " \
                        % (kv, button_key, self.__keys[button_key])
                continue

            for butt,regex in self.BUTTON_REGEXES.items():
                if not button_val.startswith(butt):
                    continue

                val = button_val.replace(butt, "")
                if not regex.match(val):
                    raise ValueError("Invalid value.", butt, val)

                self.__keys[button_key] = button_val
                break

        if throw:
            raise ValueError("Duplicate keys detected.", error_msg)

    def remove_empty_mappings(self):
        self.__keys = {k:v for (k,v) in self.__keys.items() if v is not ""}

    def __str__(self):
        ret = "Mapping {\n  guid: %s\n  name: %s\n  platform: %s\n" \
            % (self.guid, self.name, self.platform)

        ret += "  Keys {\n"
        for key,val in self.__keys.items():
            ret += "    %s: %s\n" % (key, val)

        ret += "  }\n}"
        return ret

    def serialize(self):
        ret = "%s,%s," % (self.guid, self.name)
        for key,val in self.__keys.items():
            ret += "%s:%s," % (key, val)
        ret += "platform:%s," % (self.platform)
        return ret

# https://hg.libsdl.org/SDL/rev/20855a38e048
def convert_guids(filename):
    global current_line
    global current_lineno
    input_file = open(filename, 'r')
    out_file = open("gamecontrollerdb_converted.txt", 'w')
    for lineno, line in enumerate(input_file):
        current_line = line
        current_lineno = lineno + 1
        if line.startswith('#') or line == '\n':
            out_file.write(line)
            continue
        splitted = line[:-1].split(',', 2)
        guid = splitted[0]
        if get_platform(splitted[2]) == "Windows":
            if guid[20:32] != "504944564944":
                out_file.write(line)
                continue
            guid = guid[:20] + "000000000000"
            guid = guid[:16] + guid[4:8] + guid[20:]
            guid = guid[:8] + guid[:4] + guid[12:]
            guid = "03000000" + guid[8:]
            guid = guid.lower()
        elif get_platform(splitted[2]) == "Mac OS X":
            if guid[4:16] != "000000000000" or guid[20:32] != "000000000000":
                out_file.write(line)
                continue
            guid = guid[:20] + "000000000000"
            guid = guid[:8] + guid[:4] + guid[12:]
            guid = "03000000" + guid[8:]
            guid = guid.lower()
        else:
            out_file.write(line)
            continue

        out = line.replace(splitted[0], guid)
        out_file.write(out)
        print("\nConverted :\t" + splitted[0] + "\nTo :\t\t" + guid)
    out_file.close()
    input_file.close()
    shutil.copyfile(input_file.name, ".bak." + input_file.name)
    shutil.move("gamecontrollerdb_converted.txt", "gamecontrollerdb.txt")

def add_missing_platforms(filename):
    global current_line
    global current_lineno
    input_file = open(filename, 'r')
    out_file = open("gamecontrollerdb_platforms.txt", 'w')
    for lineno, line in enumerate(input_file):
        current_line = line
        current_lineno = lineno + 1
        if line.startswith('#') or line == '\n':
            out_file.write(line)
            continue
        splitted = line[:-1].split(',', 2)
        guid = splitted[0]
        platform = get_platform(splitted[2])
        if platform:
                out_file.write(line)
                continue

        out = line[0:-1]
        if guid[20:32] == "504944564944":
            print("Adding Windows platform to #" + str(lineno) + " :\n" + line)
            out += "platform:Windows,"
        elif guid[4:16] == "000000000000" and guid[20:32] == "000000000000":
            print("Adding Mac OS X platform to #" + str(lineno) + " :\n" + line)
            out += "platform:Mac OS X,"
        else:
            print("Adding Linux platform to #" + str(lineno) + " :\n" + line)
            out += "platform:Linux,"
        out += "\n"
        out_file.write(out)
    out_file.close()
    input_file.close()
    shutil.copyfile(input_file.name, ".bak." + input_file.name)
    shutil.move("gamecontrollerdb_platforms.txt", "gamecontrollerdb.txt")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Database file to check, \
        ex. gamecontrollerdb.txt.")
    parser.add_argument("--format", help="Should be run before a pull \
            request. Sorts, formats and removes duplicates.",
            action="store_true")

# Disable misc tools until refactor
#    parser.add_argument("--convert_guids", help="convert Windows and macOS \
#            GUIDs to the newer SDL 2.0.5 format. Skips checks!",
#            action="store_true")
#    parser.add_argument("--add_missing_platform", help="adds a platform \
#            field if it is missing (on older pre 2.0.5 entries). Skips checks!",
#            action="store_true")

    args = parser.parse_args()

    # Misc tools.
#    if args.convert_guids:
#        print("Converting GUIDs to SDL 2.0.5 format.")
#        convert_guids(args.input_file)
#        return
#
#    if args.add_missing_platform:
#        print("Adding missing platforms.")
#        add_missing_platforms(args.input_file)
#        return

    # Tests.
    print("Applying checks.")
    global mappings_dict # { "platform": { "guid": Mapping }}
    success = True
    input_file = open(args.input_file, mode="r")

    for lineno, line in enumerate(input_file):
        if line.startswith('#') or line == '\n':
            continue
        try:
            mapping = Mapping(line, lineno + 1)
        except ValueError as e:
            print("Error at line #" + str(lineno + 1))
            print(e.args)
            print("\nIn mapping")
            print(line)
            success = False
            continue

        if mapping.guid in mappings_dict[mapping.platform]:
            print("Duplicate detected at line #" + str(lineno + 1))
            prev_mapping = mappings_dict[mapping.platform][mapping.guid]
            print("Previous mapping at line #" + str(prev_mapping.linenumber))
            print("\nIn mapping")
            print(line)
            success = False
            continue

        mappings_dict[mapping.platform][mapping.guid] = mapping
    input_file.close()

    if success:
        print("No mapping errors found.")
    else:
        sys.exit(1)

    if args.format:
        print("\nFormatting db.")
        out_file = open("gamecontrollerdb_formatted.txt", 'w')
        out_file.write(FILE_HEADER)
        for platform,p_dict in mappings_dict.items():
            out_file.write("\n")
            out_file.write("# " + platform + "\n")
            sorted_p_dict = sorted(p_dict.items(),
                    key=lambda x: x[1].name.lower())

            for guid,mapping in sorted_p_dict:
                out_file.write(mapping.serialize() + "\n")

        out_file.close()
        shutil.copyfile(input_file.name, ".bak." + input_file.name)
        shutil.move("gamecontrollerdb_formatted.txt", "gamecontrollerdb.txt")


if __name__ == "__main__":
    main()

