#!/usr/bin/env python3
"""Probe a video file and output useful key=value pairs for the bash runner.

Usage: video_info.py <input_file> <out_width> <out_height>
Outputs lines like: FPS=23.976\nGOP=12\nTOTAL_FRAMES=1234\nIN_WIDTH=1920\nIN_HEIGHT=1080\nPREVIEW_W=640\nPREVIEW_H=360
"""
import sys
import subprocess
from fractions import Fraction

def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return ''

def probe_r_frame_rate(path):
    return run_cmd(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=r_frame_rate','-of','default=nk=1:nw=1', path])

def probe_width_height(path):
    out = run_cmd(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','default=nk=1:nw=1', path])
    parts = out.splitlines()
    if len(parts) >= 2:
        return parts[0], parts[1]
    return '', ''

def probe_total_frames(path, fps):
    # Prefer quick nb_frames (may be present in container metadata)
    out = run_cmd(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','default=nk=1:nw=1', path])
    if out.isdigit():
        return out
    # fallback: try duration and estimate frames (fast)
    dur = run_cmd(['ffprobe','-v','error','-select_streams','v:0','-show_entries','format=duration','-of','default=nk=1:nw=1', path])
    try:
        d = float(dur)
        est = int(round(d * float(fps)))
        if est > 0:
            return str(est)
    except Exception:
        pass
    return ''

def safe_float_fraction(s, default=24.0):
    try:
        return float(Fraction(s))
    except Exception:
        try:
            return float(s)
        except Exception:
            return default

def compute_preview_dim(out_w, out_h, maxdim=1080):
    try:
        w = int(out_w); h = int(out_h)
    except Exception:
        return 640, 360
    if w <=0 or h <=0:
        return 640,360
    if max(w,h) <= maxdim:
        return w,h
    if w >= h:
        nw = maxdim
        nh = max(1, int(round(h * maxdim / w)))
    else:
        nh = maxdim
        nw = max(1, int(round(w * maxdim / h)))
    return nw, nh

def main():
    if len(sys.argv) < 4:
        print('usage: video_info.py <input> <out_width> <out_height>', file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    out_w = sys.argv[2]
    out_h = sys.argv[3]

    fps_s = probe_r_frame_rate(path)
    fps = safe_float_fraction(fps_s)
    gop = max(1, int(round(fps/2.0)))

    in_w, in_h = probe_width_height(path)
    total = probe_total_frames(path, fps)
    prev_w, prev_h = compute_preview_dim(out_w, out_h)

    def q(v):
        s = str(v)
        # escape single quotes
        s = s.replace("'", "'""'""")
        return "'" + s + "'"

    print(f"FPS={q(fps)}")
    print(f"GOP={q(gop)}")
    if total:
        print(f"TOTAL_FRAMES={q(total)}")
    print(f"IN_WIDTH={q(in_w)}")
    print(f"IN_HEIGHT={q(in_h)}")
    print(f"PREVIEW_W={q(prev_w)}")
    print(f"PREVIEW_H={q(prev_h)}")

if __name__ == "__main__":
    main()
