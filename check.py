#!/usr/bin/env python

import sys
# if sys.version_info[0] != 3:
#     print("This script requires Python 3.")
#     exit(1)

from os import path
from collections import OrderedDict
import string
import collections
import shutil
import argparse
import csv
import re

FILE_HEADER = "# Game Controller DB for SDL in 2.0.6 format\n" \
        "# Source: https://github.com/gabomdq/SDL_GameControllerDB\n"

mappings_dict = OrderedDict([
    ("Windows", {}),
    ("Mac OS X", {}),
    ("Linux", {}),
    ("Android", {}),
    ("iOS", {}),
])

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="database file to check, " \
        "ex. gamecontrollerdb.txt")
parser.add_argument("--format", help="sorts, formats and removes duplicates",
        action="store_true")
parser.add_argument("--convert_guids", help="convert Windows and macOS " \
        "GUIDs to the newer SDL 2.0.5 format",
        action="store_true")
parser.add_argument("--add_missing_platform", help="adds a platform "\
        "field if it is missing on Windows and Mac OS X 2.0.4 entries",
        action="store_true")
parser.add_argument("--import_header", metavar="sdl_header",
        help="imports and overrides mappings using SDL_gamecontrollerdb.h")

class Mapping:
    GUID_REGEX = re.compile(r"^(xinput|[0-9a-fA-F]{32,32})$")

    BUTTON_REGEXES = {
        "+a": re.compile(r"^[0-9]+\~?$"),
        "-a": re.compile(r"^[0-9]+\~?$"),
        "a": re.compile(r"^[0-9]+\~?$"),
        "b": re.compile(r"^[0-9]+$"),
        "h": re.compile(r"^[0-9]+\.(1|2|4|8|3|6|12|9)$"),
    }

    def __init__(self, mapping_string, line_number, add_missing_platform = False):
        self.guid = ""
        self.name = ""
        self.platform = ""
        self.line_number = 0
        self.__keys = {
            "+leftx": "",
            "+lefty": "",
            "+rightx": "",
            "+righty": "",
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

        self.line_number = line_number
        reader = csv.reader([mapping_string], skipinitialspace=True)
        mapping = next(reader)
        mapping = list(filter(None, mapping))
        self.set_guid(mapping[0])
        mapping.pop(0)
        self.set_name(mapping[0])
        mapping.pop(0)
        self.set_platform(mapping, add_missing_platform)
        self.set_keys(mapping)

        # Remove empty mappings.
        self.__keys = {k:v for (k,v) in self.__keys.items() if v is not ""}


    def set_guid(self, guid):
        if not self.GUID_REGEX.match(guid):
            raise ValueError("GUID malformed.", guid)

        self.guid = guid


    def set_name(self, name):
        name = re.sub(r" +", " ", name)
        self.name = name


    def __get_missing_platform(self):
        if self.guid[20:32] == "504944564944":
            print("Adding 'platform:Windows' to %s" % (self.name))
            return ("platform:Windows")
        elif self.guid[4:16] == "000000000000" \
                and self.guid[20:32] == "000000000000":
            print("Adding 'platform:Mac OS X' to %s" % (self.name))
            return ("platform:Mac OS X")
        else:
            raise ValueError("Add missing platform : Cannot determine platform"\
                    " confidently.")


    def set_platform(self, mapping, add_missing_platform):
        remove_field_from_mapping = True
        platform_kv = next((x for x in mapping if "platform:" in x), None)
        if platform_kv == None:
            if add_missing_platform:
                platform_kv = self.__get_missing_platform()
                remove_field_from_mapping = False
            else:
                raise ValueError("Required 'platform' field not found.")

        platform = platform_kv.split(':')[1]
        if platform not in mappings_dict.keys():
            raise ValueError("Invalid platform.", platform)

        self.platform = platform
        if not remove_field_from_mapping:
            return
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
        sorted_keys = sorted(self.__keys.items())
        for key,val in sorted_keys:
            ret += "%s:%s," % (key, val)
        ret += "platform:%s," % (self.platform)
        return ret


    # https://hg.libsdl.org/SDL/rev/20855a38e048
    def convert_guid(self):
        if self.platform == "Windows":
            if self.guid[20:32] != "504944564944":
                return False

            guid = self.guid
            guid = guid[:20] + "000000000000"
            guid = guid[:16] + guid[4:8] + guid[20:]
            guid = guid[:8] + guid[:4] + guid[12:]
            guid = "03000000" + guid[8:]
            guid = guid.lower()
            print("%s : Converted %s GUID. From %s to %s" \
                %(self.platform, self.name, self.guid, guid))
            self.guid = guid

        elif self.platform == "Mac OS X":
            if self.guid[4:16] != "000000000000" \
                    or self.guid[20:32] != "000000000000":
                return False

            guid = self.guid
            guid = guid[:20] + "000000000000"
            guid = guid[:8] + guid[:4] + guid[12:]
            guid = "03000000" + guid[8:]
            guid = guid.lower()
            print("%s : Converted %s GUID. From %s to %s" \
                % (self.platform, self.name, self.guid, guid))
            self.guid = guid

        else:
            return False
        return True


def import_header(filepath, debug_out = False):
    class Platform:
        XINPUT = 0
        WINDOWS = 1
        OSX = 2
        LINUX = 3
        ANDROID = 4
        IOS = 5
        NONE = 6

    global mappings_dict # { "platform": { "guid": Mapping }}
    current_platform = Platform.NONE

    input_file = open(filepath, mode="r")
    for lineno, line in enumerate(input_file):
        if "#if SDL_JOYSTICK_XINPUT" in line:
            current_platform = Platform.XINPUT
            continue
        elif "#if SDL_JOYSTICK_DINPUT" in line:
            current_platform = Platform.WINDOWS
            continue
        elif "#if defined(__MACOSX__)" in line:
            current_platform = Platform.OSX
            continue
        elif "#if defined(__LINUX__)" in line:
            current_platform = Platform.LINUX
            continue
        elif "#if defined(__ANDROID__)" in line:
            current_platform = Platform.ANDROID
            continue
        elif "#if defined(SDL_JOYSTICK_MFI)" in line:
            current_platform = Platform.IOS
            continue
        elif "#endif" in line:
            current_platform = Platform.NONE
            continue

        if current_platform == Platform.NONE:
            continue

        mapping_string = line[line.find('"') + 1:]
        mapping_string = mapping_string[:mapping_string.find('"')]

        if current_platform == Platform.XINPUT:
            mapping_string += "platform:Windows,"
        if current_platform == Platform.WINDOWS:
            mapping_string += "platform:Windows,"
        if current_platform == Platform.OSX:
            mapping_string += "platform:Mac OS X,"
        if current_platform == Platform.LINUX:
            mapping_string += "platform:Linux,"
        if current_platform == Platform.ANDROID:
            mapping_string += "platform:Android,"
        if current_platform == Platform.IOS:
            mapping_string += "platform:iOS,"

        try:
            mapping = Mapping(mapping_string, lineno + 1)
        except ValueError as e:
            print("\nError at line #" + str(lineno + 1))
            print(e.args)
            print("Ignoring mapping")
            print(line)
            continue

        if debug_out:
            print("%s : Importing %s" % (mapping.platform, mapping.name))

        mappings_dict[mapping.platform][mapping.guid] = mapping
    input_file.close()


def main():
    global mappings_dict # { "platform": { "guid": Mapping }}
    global parser
    args = parser.parse_args()
    success = True

    if args.add_missing_platform:
        print("Will try to add missing platforms. Requires SDL 2.0.4 GUID.")
        if not args.format:
            print("Use --format option to save database. Running in debug "\
                    "output mode...")


    # Tests.
    print("\nApplying checks.")

    input_file = open(args.input_file, mode="r")
    for lineno, line in enumerate(input_file):
        if line.startswith('#') or line == '\n':
            continue
        try:
            mapping = Mapping(line, lineno + 1, args.add_missing_platform)
        except ValueError as e:
            print("\nError at line #" + str(lineno + 1))
            print(e.args)
            print("In mapping")
            print(line)
            success = False
            continue

        if mapping.guid in mappings_dict[mapping.platform]:
            print("Duplicate detected at line #" + str(lineno + 1))
            prev_mapping = mappings_dict[mapping.platform][mapping.guid]
            print("Previous mapping at line #" + str(prev_mapping.line_number))
            print("In mapping")
            print(line)
            success = False
            continue

        mappings_dict[mapping.platform][mapping.guid] = mapping
    input_file.close()

    if success:
        print("No mapping errors found.")
    else:
        sys.exit(1)


    # Misc tools.

    if args.convert_guids:
        print("Converting GUIDs to SDL 2.0.5+ format.")
        if not args.format:
            print("Use --format option to save database. Running in debug " \
                    "output mode...")
        for platform,p_dict in mappings_dict.items():
            for guid,mapping in p_dict.items():
                if mapping.convert_guid():
                    del mappings_dict[platform][guid]
                    if mapping.guid in mappings_dict[platform]:
                        print("\nDuplicate detected when converting GUID.")
                        prev_mapping = mappings_dict[platform][mapping.guid]
                        print("Previous mapping %s" % prev_mapping.name)
                        print("Ignoring new mapping")
                        print(mapping.serialize())
                        print("\n")
                        continue
                    mappings_dict[platform][mapping.guid] = mapping

    if args.import_header is not None:
        print("Importing mappings from SDL_gamecontrollerdb.h.")
        if not args.format:
            print("Use --format option to save database. Running in debug "\
                    "output mode...")
        import_header(args.import_header, not args.format)

    if args.format:
        print("\nFormatting db.")
        out_filename = path.splitext(input_file.name)[0] + "_format.txt"
        out_file = open(out_filename, 'w')
        out_file.write(FILE_HEADER)
        for platform,p_dict in mappings_dict.items():
            out_file.write("\n")
            out_file.write("# " + platform + "\n")
            sorted_p_dict = sorted(p_dict.items(),
                    key=lambda x: x[1].name.lower())

            for guid,mapping in sorted_p_dict:
                out_file.write(mapping.serialize() + "\n")

        out_file.close()
        backup_filename = (path.join(path.split(input_file.name)[0],
                ".bak." + path.split(input_file.name)[1]))
        shutil.copyfile(input_file.name, backup_filename)
        shutil.move(out_filename, input_file.name)


if __name__ == "__main__":
    main()

