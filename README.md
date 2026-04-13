# 🎯 Minimap Node Scanner

A lightweight, Python-based GUI tool that visually scans your on-screen minimap for specific colored nodes (like gathering nodes in MMOs) and plays a custom audio alert when one is detected.

## ✨ Features
* **Circular Region Masking:** Draws a perfect internal circle to ignore UI elements and corners, preventing false positives.
* **Smart Size Filtering:** Uses contour detection to only trigger on actual node clusters, ignoring random stray pixels or terrain noise.
* **Custom Audio Alerts:** Load any `.mp3` or `.wav` file to act as your ping.
* **Volume Control:** Built-in slider so you don't blow your ears out.
* **Performance Friendly:** Scans efficiently at 1 tick per second to conserve CPU usage.

## 🚀 Download & Use 
1. Go to the [Releases](../../releases) tab on the right side of this page. (in beta testing, link may be invalid)
2. Run the program, select your minimap region, pick an audio file, and hit Start!
3. Instant ping mp3/wav file for maximum efficiency!

## 💻 Developer Installation (For Modding)
If you want to run the source code or tweak the color detection algorithms:

1. Clone the repository:
   ```bash
   git clone [https://github.com/mccoolsa/minimap_scanner.git](https://github.com/mccoolsa/minimap_scanner.git)

2. Install the required dependencies:
   pip install -r requirements.txt

3. Run the application
   python minimap_scanner.py

## ⚠️ ⚠️ DISCLAIMER ⚠️ ⚠️
This file is in its maiden version, expect bugs to occur (where other yellow instances occur on the map that are similar to nodes), also glitches out and pings where there are valid quest givers, so this file is primarily for people on mining routes / AFK farming within WoW. In future versions, we aim to increase the rate of scanning with a stronger focus on the colour scheme of nodes to avoid over-sensitivity. 
