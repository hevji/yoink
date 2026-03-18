# Yoink 🎣
> Grab any YouTube video from your terminal. No fuss.
 
---
 
## What's in the box
 
| File | What it does |
|---|---|
| `yoink.py` | The Python downloader - the real brain |
| `installer.cpp` | C++ installer - sets up `C:\Yoink` and PATH |
| `wrapper.cpp` | C++ wrapper - lets you type `yoink` anywhere |
 
---
 
## Requirements
 
| Dependency | Why |
|---|---|
| Python 3.8+ | Runs the downloader |
| yt-dlp | Does the actual downloading (auto-installed) |
| ffmpeg *(recommended)* | Merges video+audio, needed for `--audio` MP3 export |
 
### Install ffmpeg (optional but recommended)
```
winget install ffmpeg
```
or download from https://ffmpeg.org/download.html and add to PATH.
 
---
 
## Build the C++ files
 
### Option A - MinGW / g++ (recommended for most users)
```bash
# Build the installer
g++ -std=c++17 -O2 -o installer.exe installer.cpp -ladvapi32
 
# Build the yoink.exe wrapper
g++ -std=c++17 -O2 -o yoink.exe wrapper.cpp
```
 
### Option B - MSVC (Visual Studio Developer Command Prompt)
```cmd
cl /EHsc /W4 installer.cpp /link advapi32.lib
cl /EHsc /W4 /O2 wrapper.cpp /Fe:yoink.exe
```
 
---
 
## Install
 
1. Put `installer.exe`, `yoink.exe`, and `yoink.py` in the **same folder**
2. Right-click `installer.exe` -> **Run as administrator**
3. Follow the prompts
4. Open a **new** terminal window
 
Done. `C:\Yoink` is now on your PATH.
 
---
 
## Usage
 
```bash
# Download a video (best quality MP4)
yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ
 
# Download audio only as MP3
yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ --audio
 
# Download to a specific folder
yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ --folder "D:\MyVideos"
 
# Download an entire playlist (asks for confirmation first)
yoink https://www.youtube.com/playlist?list=PLxxxxxx
 
# Reset your saved default download folder
yoink --reset
```
 
---
 
## First run - choosing a folder
 
On your first download, Yoink will ask where you want to save files:
 
```
  Where do you want to save downloads?
 
    [1] C:\Users\You\Downloads
    [2] C:\Users\You\Videos
    [3] C:\Users\You\Music
    [4] C:\Yoink\Downloads
    [5] Enter a custom path
 
  Choose (1-5):
```
 
You can save this as your default so it never asks again.
To change it later: `yoink --reset`
 
---
 
## Uninstall
 
Run `C:\Yoink\uninstall.bat` as Administrator.
 
This removes the folder and cleans `C:\Yoink` from PATH.
 
---
 
## Troubleshooting
 
| Problem | Fix |
|---|---|
| `yoink` not recognized | Open a **new** terminal after installing |
| ffmpeg not found warning | `winget install ffmpeg` |
| Video unavailable / private | Nothing Yoink can do - the video is restricted |
| Age-restricted video fails | yt-dlp handles most cases; very restricted ones may require cookies |
| Installer says "not admin" | Right-click -> Run as administrator |
| pip install fails | Run `pip install yt-dlp` manually |
