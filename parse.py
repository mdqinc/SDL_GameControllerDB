#!/usr/bin/env python3
# Parse gamecontrollerdb format into Python datastructures

import argparse
from collections import defaultdict
from datetime import datetime
import re
from pprint import pprint

repo_url = 'https://github.com/balthamos/SDL_GameControllerDB'
comment = '#'

def parse_guid(guid):
    return guid

def parse_token(entry, token):
    parts = token.split(':')
    if len(parts) != 2:
        return

    key = parts[0].strip()
    val = parts[1].strip()
    if not key or not val:
        return

    kind = val[0]
    if kind == 'b':
        m = re.match('\d+', val[1:])
        if not m:
            return
        idx = int(m.group(0))
        entry[key] = ('button', idx)

    elif kind == 'a':
        m = re.match('\d+', val[1:])
        if not m:
            return
        idx = int(m.group(0))
        entry[key] = ('axis', idx)

    elif kind == 'h':
        m = re.match('(\d+).(\d+)', val[1:])
        if not m:
            return
        idx     = int(m.group(1))
        sub_idx = int(m.group(2))
        entry[key] = ('hat', idx, sub_idx)

    else:
        entry[key] = val

def parse_line(i, entries, line):
    errors = 0
    clean_line = line.strip()
    if not clean_line:
        return errors

    if clean_line[0] == comment:
        m = re.match('%s\s+DUPE_OK\s+([0-9A-Fa-f]+)' % comment, clean_line)
        if m:
            entries['dupe_oks'][m.group(1)] = True
        return errors

    tokens = clean_line.split(',')
    if len(tokens) < 2:
        return errors

    meta  = {}
    entry = {}
    guid = parse_guid(tokens[0])
    meta['raw']   = clean_line
    meta['line']  = i
    entry['name'] = tokens[1].strip()

    if re.match('.*\s\s+.*', entry['name']):
        print('%4d: Name contains subsequent space characters. GUID: %s, name: %s' % (i, guid, entry['name']))
        errors += 1

    rest = tokens[2:]
    for token in rest:
        parse_token(entry, token)

    if guid in entries['guids']:
        existing = entries['guids'][guid]['data']
        if existing == entry:
            return errors

        if guid not in entries['dupe_oks']:
            existing_meta = entries['guids'][guid]['meta']
            print('Duplicate entry found for GUID %s' % guid)
            print('%4d: %s' % (existing_meta['line'], existing_meta['raw']))
            print('%4d: %s' % (meta['line'], meta['raw']))
            print('Differences:')
            differences = set(existing.items()) ^ set(entry.items())
            pprint(differences)
            print('')
            errors += 1
            return errors

        guid = '%s.%d' % (guid, meta['line'])

    entries['guids'][guid] = {'meta': meta, 'data': entry}

    platform = entry['platform'] if 'platform' in entry else 'Generic'
    entries['platforms'][platform].append(guid)
    return errors

def parse_db(db):
    entries = {'guids': {}, 'platforms': defaultdict(list), 'dupe_oks': {}}
    errors = 0
    with open(db, 'r') as f:
        for i, l in enumerate(f.readlines()):
            errors += parse_line(i + 1, entries, l)
    return (entries, errors)

def comment_box(out, lines, width=78):
    inner_width = width - 4
    out.append(comment * width)
    for line in lines:
        out.append('%s %s %s' % (comment, line.ljust(inner_width), comment))
    out.append(comment * width)

def format_value(value):
    out  = value[0][0]
    out += '%s' % value[1]
    if len(value) > 2:
        out += '.%s' % value[2]
    return out

def format_entries(entries):
    out = []

    header = []
    header.append('SDL Controller Config')
    header.append('Generated: %s' % datetime.now())
    header.append('Source:    %s' % repo_url)
    header.append('License:   MIT')
    comment_box(out, header)

    out.append('')
    for dupe_ok in entries['dupe_oks']:
        out.append('%s DUPE_OK %s' % (comment, dupe_ok))

    for platform, guids in sorted(entries['platforms'].items()):
        out.append('')
        out.append('%s %s' % (comment, platform))
        for guid in sorted(guids, key=lambda a: int(a.split('.')[0], 16)):
            fixed_guid = guid.split('.')[0]
            entry = entries['guids'][guid]['data']

            newname = re.sub('\s\s+', ' ', entry['name'])

            if newname != entry['name']:
                print('Fixed name for GUID %s:\n\tOld: %s\n\tNew: %s' % (guid, entry['name'], newname))
                entry['name'] = newname

            build = '%s,%s,' % (fixed_guid, entry['name'])
            for key, val in sorted(entry.items()):
                if key == 'name':
                    continue
                val_str = val if key == 'platform' else format_value(val)
                build += '%s:%s,' % (key, val_str)
            out.append(build)
    out.append('')
    return out

def write_output(entries, filename):
    with open(filename, 'w') as f:
        f.writelines('\n'.join(format_entries(entries)))

def main():
    parser = argparse.ArgumentParser(description='''
        Parse SDL controller database file, identify issues, and generate clean formatted file.
    ''')
    parser.add_argument('input_file', help='database file')
    parser.add_argument('-o', '--output_file', help='generated database file')
    args = parser.parse_args()

    entries, errors = parse_db(args.input_file)

    output_file = args.output_file
    if output_file:
        write_output(entries, output_file)
    elif errors:
        print('%i errors detected' % errors)
        exit(1)

if __name__ == "__main__":
    main()
