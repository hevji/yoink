<div align="center">
<pre>
   :::   :::  :::::::: ::::::::::: ::::    ::: :::    ::: 
  :+:   :+: :+:    :+:    :+:     :+:+:   :+: :+:   :+:  
  +:+ +:+  +:+    +:+    +:+     :+:+:+  +:+ +:+  +:+    
  +#++:   +#+    +:+    +#+     +#+ +:+ +#+ +#++:++      
  +#+    +#+    +#+    +#+     +#+  +#+#+# +#+  +#+      
 #+#    #+#    #+#    #+#     #+#   #+#+# #+#   #+#      
###     ######## ########### ###    #### ###    ###      
</pre>
</div>

**Download any YouTube video straight from your terminal.**  
No ads. No browser. No bullshit.

![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

</div>

---

## What it does

```
yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

That's it. Best quality MP4, saved to your folder of choice.

---

## Requirements

| Dependency | Notes |
|---|---|
| Python 3.8+ | Must be on PATH |
| yt-dlp | Auto-installed by the installer |
| ffmpeg | Optional — needed for `--audio` and best-quality merging |

**Install ffmpeg:**
```
winget install ffmpeg
```

---

## Installation

1. Go to [Releases](../../releases) and download the latest zip
2. Extract — make sure `installer.exe`, `yoink.exe`, and `yoink.py` are in the same folder
3. Double-click `installer.exe` and follow the steps
4. Open a **new** terminal window

Done. `yoink` is now available everywhere.

---

## Usage

```bash
# Download best quality MP4
yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Download audio only as MP3
yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ --audio

# Save to a specific folder
yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ --folder "D:\MyVideos"

# Download an entire playlist
yoink https://www.youtube.com/playlist?list=PLxxxxxx

# Reset your saved default download folder
yoink --reset
```

---

## First run

On your first download Yoink will ask where to save files:

```
  Where do you want to save downloads?

    [1] C:\Users\You\Downloads
    [2] C:\Users\You\Videos
    [3] C:\Users\You\Music
    [4] C:\Yoink\Downloads
    [5] Enter a custom path

  Choose (1-5):
```

Say yes to save it as your default — it won't ask again.  
To change it later: `yoink --reset`

---

## Building from source

```bash
# installer.exe
g++ -std=c++17 -O2 -o installer.exe installer.cpp -ladvapi32

# yoink.exe
g++ -std=c++17 -O2 -o yoink.exe wrapper.cpp
```

> Requires MinGW or MSVC. For MSVC use a Visual Studio Developer Command Prompt and replace `g++` with `cl /EHsc /W4 /O2` and add `/link advapi32.lib` for the installer.

---

## Uninstall

Run `uninstall.bat` as Administrator, or just delete `C:\Yoink` and remove it from your system PATH manually.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `yoink` not recognized | Open a **new** terminal after installing |
| ffmpeg not found | `winget install ffmpeg` |
| Video unavailable / private | The video is restricted - nothing Yoink can do |
| Age-restricted video fails | yt-dlp handles most cases; some may need cookies |
| Installer says not admin | Right-click -> Run as administrator |
| pip install fails | Run `pip install yt-dlp` manually |

---

## License

MIT - see [LICENSE](LICENSE)
