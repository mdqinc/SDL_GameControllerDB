#!/usr/bin/env python3

#import fileinput
import string
import sys
from collections import defaultdict
import collections
import shutil
import argparse

success = True
current_line = ""
current_lineno = 0
entry_dict = defaultdict(tuple)
dupe_dict = defaultdict(list)

def get_current_line():
    return current_line

def get_current_lineno():
    return current_lineno

def error (message):
    global success
    success = False
    print("Error at line #" + str(get_current_lineno()), ":", message)
    print(get_current_line())

def check_guid (guid):
    if len (guid) != 32:
        error ("The length of the guid string must be equal to 32")
    for c in guid:
        if not c in string.hexdigits:
            error ("Each character in guid string must be a hex character "
                + string.hexdigits)

def check_mapping (mappingstring):
    keys = ["platform", "leftx", "lefty", "rightx", "righty", "a", "b", \
            "back", "dpdown", \
            "dpleft", "dpright", "dpup", "guide", "leftshoulder", "leftstick", \
            "lefttrigger", "rightshoulder", "rightstick", "righttrigger", \
            "start", "x", "y"]
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
                           "\". Should be followed by a number after 'a' or " +
                           "'b'")
            else:
                dpad_positions = map(str, [0, 1, 2, 4, 8, 1|2, 2|4, 4|8, 8|1])
                dpad_index = value[1:].split ('.')[0]
                dpad_position = value[1:].split ('.')[1]
                if not dpad_index.isnumeric():
                    error ("Invalid value \"" + value + "\" for key \"" + key +
                           "\". Dpad index \"" + dpad_index + "\" should be " +
                           "a number")
                if not dpad_position in dpad_positions:
                    error ("Invalid value \"" + value + "\" for key \"" + key +
                           "\". Dpad position \"" + dpad_position + "\" " +
                           "should be one of" + ', '.join(dpad_positions))

def get_platform (mappingstring):
    mappings = mappingstring.split (',')
    for mapping in mappings:
        if not mapping:
            continue
        key = mapping.split(':')[0]
        value = mapping.split(':')[1]
        if key == "platform":
            return value
    error ("No platform specified " + mapping)

def has_duplicate(guids):
    seen = set()
    seen_add = seen.add
    seen_twice = set( x for x in guids if x in seen or seen_add(x) )
    return len(seen_twice) != 0

def check_duplicates(guid, platform):
    guids = list(dupe_dict[platform])
    guids.append(guid)
    if has_duplicate(guids):
        error("\nDuplicate entry :")
        print("Original at line #" + entry_dict[guid][0] +
                ":\n" + entry_dict[guid][1])
    else:
        dupe_dict[platform].append(guid)
        entry_dict[guid] = (str(get_current_lineno()), get_current_line())

def do_tests(filename):
    global current_line
    global current_lineno
    input_file = open(filename, 'r')
    for lineno, line in enumerate(input_file):
        current_line = line
        current_lineno = lineno + 1
        if line.startswith('#') or line == '\n':
            continue
        splitted = line[:-1].split(',', 2)
        if len(splitted) < 3 or not splitted[0] or not splitted[1] \
            or not splitted[2]:
            error ("Either GUID/Name/Mappingstring is missing or empty")
        check_guid(splitted[0])
        check_mapping(splitted[2])
        check_duplicates(splitted[0].lower(), get_platform(splitted[2]))
    input_file.close()

def sort_by_name(filename):
    input_file = open(filename, 'r')
    sorted_dict = dict({"Windows": list(tuple()), "Mac OS X": list(tuple()), \
        "Linux": list(tuple())})

    for line in input_file:
        if line.startswith('#') or line == '\n':
            continue
        splitted = line[:-1].split(',', 2)
        if len(splitted) < 3 or not splitted[0] or not splitted[1] \
            or not splitted[2]:
            continue
        platform = get_platform(splitted[2])
        sorted_dict[platform].append((splitted[1], line))

    out_file = open("gamecontrollerdb_sorted.txt", 'w')
    for platform, name_tuples in sorted_dict.items():
        if platform != "Windows":
            out_file.write("\n")
        out_file.write("# " + platform + "\n")
        for tuples in sorted(name_tuples, key=lambda tup: tup[0].lower()):
            out_file.write(tuples[1])
    out_file.close()
    input_file.close()
    shutil.copyfile(input_file.name, ".bak." + input_file.name)
    shutil.move("gamecontrollerdb_sorted.txt", "gamecontrollerdb.txt")

# https://hg.libsdl.org/SDL/rev/20855a38e048
def convert_guids(filename):
    input_file = open(filename, 'r')
    out_file = open("gamecontrollerdb_converted.txt", 'w')
    for lineno, line in enumerate(input_file):
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

        out = line.replace(splitted[0], guid)
        out_file.write(out)
    out_file.close()
    input_file.close()
    shutil.copyfile(input_file.name, ".bak." + input_file.name)
    shutil.move("gamecontrollerdb_converted.txt", "gamecontrollerdb.txt")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="database file to check \
        (gamecontrollerdb.txt)")
    parser.add_argument("--no_sort", help="don't sort the database on success",
        action="store_true")
    parser.add_argument("--guid_convert", help="convert Windows and macOS \
            GUIDs to the newer SDL 2.0.5 format", action="store_true")
    args = parser.parse_args()

    do_tests(args.input_file)
    if success:
        print("No mapping errors found.")
        if not args.no_sort:
            print("Sorting by human readable name.")
            sort_by_name(args.input_file)
        if args.guid_convert:
            print("Converting GUIDs to SDL 2.0.5 format.")
            convert_guids(args.input_file)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
