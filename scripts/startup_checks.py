#!/usr/bin/env python3
"""Emit startup checks and enforce ffmpeg tools.

By default prints Homebrew (macOS), Python3 and ffmpeg/ffprobe/ffplay versions.
If --require-latest is provided on macOS the script will query Homebrew's
JSON info for the stable ffmpeg version and fail if the installed ffmpeg
does not match the Homebrew stable version.
"""
import sys
import shutil
import subprocess
import platform
import argparse
import json
import re


def run(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return out.decode().splitlines()[0]
    except Exception:
        return None


def extract_ffmpeg_version(line):
    # typical: "ffmpeg version 8.0 ..."
    m = re.search(r"ffmpeg version\s*([0-9A-Za-z.+-]+)", line)
    if m:
        return m.group(1)
    # fallback: first token
    parts = line.split()
    return parts[2] if len(parts) > 2 else None


def brew_latest_ffmpeg():
    brew = shutil.which('brew')
    if not brew:
        return None
    try:
        out = subprocess.check_output([brew, 'info', '--json=v2', 'ffmpeg'], stderr=subprocess.DEVNULL)
        data = json.loads(out.decode())
        formulae = data.get('formulae') or data.get('casks') or []
        if not formulae:
            return None
        item = formulae[0]
        # try several locations for the stable version
        ver = None
        if isinstance(item.get('versions'), dict):
            ver = item['versions'].get('stable')
        for key in ('stable_version','version','current_version'):
            if not ver:
                ver = item.get(key)
        return ver
    except Exception:
        return None


def require_tools():
    missing = []
    for cmd in ('ffmpeg', 'ffprobe', 'ffplay'):
        if not shutil.which(cmd):
            missing.append(cmd)
    if missing:
        print('\nERROR: missing required tools: ' + ', '.join(missing), file=sys.stderr)
        print('Please install them (on macOS: brew install ffmpeg)\n', file=sys.stderr)
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description='Startup checks for youtube_transcoder')
    parser.add_argument('--require-latest', action='store_true', help='On macOS require Homebrew stable ffmpeg to match installed ffmpeg')
    args = parser.parse_args()

    print()
    print('Startup checks:')
    if platform.system() == 'Darwin':
        brew = shutil.which('brew')
        if brew:
            ver = run([brew, '--version']) or ''
            print(f'  Homebrew: {ver.splitlines()[0] if ver else ver}')
        else:
            print('  Homebrew: not found')

    py = shutil.which('python3')
    if py:
        ver = run([py, '--version']) or ''
        print(f'  Python3: {ver}')
    else:
        print('  Python3: not found')

    # enforce presence of ffmpeg tools
    if not require_tools():
        sys.exit(2)

    for cmd in ('ffmpeg', 'ffprobe', 'ffplay'):
        c = shutil.which(cmd)
        ver_line = run([c, '-version']) or ''
        ver = extract_ffmpeg_version(ver_line) or ver_line
        print(f'  {cmd}: {ver}')

    # optional: check Homebrew's stable ffmpeg version and compare
    if args.require_latest:
        if platform.system() != 'Darwin':
            print('\n--require-latest is supported only on macOS', file=sys.stderr)
            sys.exit(3)
        brew = shutil.which('brew')
        if not brew:
            print('\nERROR: Homebrew not found; cannot check latest ffmpeg', file=sys.stderr)
            sys.exit(3)
        latest = brew_latest_ffmpeg()
        if not latest:
            print('\nWARNING: could not determine Homebrew latest ffmpeg version; skipping latest check', file=sys.stderr)
        else:
            installed_line = run(['ffmpeg', '-version']) or ''
            installed = extract_ffmpeg_version(installed_line)
            if installed != latest:
                print(f"\nERROR: installed ffmpeg ({installed}) does not match Homebrew stable ({latest}).", file=sys.stderr)
                print('Please run: brew update && brew upgrade ffmpeg', file=sys.stderr)
                sys.exit(4)

    print()


if __name__ == '__main__':
    main()

