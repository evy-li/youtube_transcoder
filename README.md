# YouTube Transcoder

Automatically transcode using compression and container options recommended by YouTube, and force encoding using libx264 on CPU with tuning that preserves fine details in high quality film content.

<mark style="background: LightCoral!important">⚠ Remember that YouTube supports uploading ProRes and DNxHR, and this should always be your default option when possible.</mark>

## Demo

The first clip (00:00>00:10) is exported from Resolve using the YouTube preset, the second clip (00:10>00:20) is transcoded from ProRes4444 with this script. The video was then concatenated without re-encoding.

Click the image below to watch:

[<img src="https://evy-li-github-r2.evy.li/concat_thumb.jpeg" width="640">](https://evy-li-github-r2.evy.li/concat.mp4)


## Prerequisites

You should be connected to the internet on the computer you wish to use. These instructions are for macOS.

If you don't have Homebrew then install it first:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then if you don't have Python 3.x then install it:

```bash
brew install python
```

## Clone

Navigate to the directory to clone to:

```bash
cd ~/your_path
```
Alternatively, simply clone to your home directory;

Clone the repo (it will create its own folder):

```bash
git clone --depth 1 https://github.com/evy-li/youtube_transcoder.git
```
Navigate to that folder, check the clone was successful:

```bash
cd youtube_transcoder
ls -la
```

## Usage

Double click the 'run' executable.

Or open a terminal at the folder you cloned to. You can secondary click (control-click) on the folder and select "New Terminal at Folder".

Or at the terminal:

```bash
cd ~/your_path/youtube_transcoder
```

Run the script:

```bash
./run
```

Follow the interactive prompts.

To exit at any time press: ⌘Command + .

<mark>⚠ Using the preview feature may require granting Accessibility Permissions to Terminal.</mark>

## CLI mode

A non-interactive CLI mode is also available (useful for scripting or automation). The CLI supports:

- `-i, --input FILE`        Input file (skip prompt).
- `-o, --output FILE`       Output file (skip prompt).
- `-r, --resolution VAL`    Target resolution (index, name or WxH). Use `--list-res` to view choices.
- `-t, --tune NAME`         Tune option.  Use `--list-tunes` to view choices.
- `--show-frame`            Enable live preview.
- `-y, --yes`               Non-interactive: accept defaults and skip confirmations.
- `--list-res`              Print available target resolutions and exit.
- `--list-tunes`            Print available tune options and exit.
- `--force-install`         Force fresh installation.

Example:

```bash
./run -i input.mov -o output.mp4 -r FHD -t film -y
```

## Cleanup

If an encode crashes or you quit while it's running, temporary files may be left behind. Use the cleanup script to delete these and kill any running processes.

```bash
./cleanup
```
