#!/usr/bin/env python3
"""Simple ffmpeg progress parser used as a process-substitution consumer.

Reads ffmpeg '-progress' key=value lines from stdin and writes a single-line
status to stdout: percentage (if total frames known), frame, fps, speed.
"""
import sys
import os

def main():
    total_env = os.environ.get('TOTAL_FRAMES', '')
    try:
        total = int(total_env) if total_env.isdigit() else None
    except Exception:
        total = None

    frame = None
    fps = None
    speed = None

    def flush_line():
        perc = '?'
        if total and frame:
            try:
                perc = f"{int((int(frame)/int(total))*100 + 0.5):3d}"
            except Exception:
                perc = '?'
        f = frame or '?'
        _fps = fps or '?'
        _speed = speed or '?'
        sys.stdout.write(f"\rProgress: {perc}% | frame={f} | fps={_fps} | speed={_speed} ")
        sys.stdout.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if line.startswith('frame='):
            frame = line.split('=',1)[1]
        elif line.startswith('fps='):
            fps = line.split('=',1)[1]
        elif line.startswith('speed='):
            speed = line.split('=',1)[1]
            # when speed appears, update the single-line status
            flush_line()
        elif line == 'progress=end':
            sys.stdout.write('\n')
            sys.stdout.flush()
            break

if __name__ == '__main__':
    main()
