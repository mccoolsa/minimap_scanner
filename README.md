# 🎯 Minimap Node Scanner

A lightweight, Python-based GUI tool that visually scans your on-screen minimap for specific colored nodes (like gathering nodes in MMOs) and plays a custom audio alert when one is detected.

## ✨ Features
* **Circular Region Masking:** Draws a perfect internal circle to ignore UI elements and corners, preventing false positives.
* **Smart Size Filtering:** Uses contour detection to only trigger on actual node clusters, ignoring random stray pixels or terrain noise.
* **Custom Audio Alerts:** Load any `.mp3` or `.wav` file to act as your ping.
* **Volume Control:** Built-in slider so you don't blow your ears out.
* **Performance Friendly:** Scans efficiently at 1 tick per second to conserve CPU usage.

## 🚀 Download & Use (For Regular Users)
You do not need Python installed to use this tool!
1. Go to the [Releases](../../releases) tab on the right side of this page.
2. Download the latest `minimap_scanner.exe`.
3. Run the program, select your minimap region, pick an audio file, and hit Start!

## 💻 Developer Installation (For Modding)
If you want to run the source code or tweak the color detection algorithms:

1. Clone the repository:
   ```bash
   git clone [https://github.com/mccoolsa/minimap_scanner.git](https://github.com/mccoolsa/minimap_scanner.git)

2. Install the required dependencies:
   pip install -r requirements.txt

3. Run the application
   python minimap_scanner.py
