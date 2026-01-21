# Pickup-AFR-Compare
![Views](https://komarev.com/ghpvc/?username=VirGis56&repo=Pickup-AFR-Compare&label=Project%20Views&color=blue&style=flat)
A unique string-driven method using Audacity and Python for analyzing and comparing guitar pickup frequency response (AFR).

### My Philosophy
I am not here to tell you **that** your ears are wrong. I believe **that** human hearing is a great tool for music, but it can be easily fooled by volume or expectations. My goal is to provide a "digital microscope" for those who want to see the data. 

**Note:** My findings are often just "hints" or observations. They could be breakthroughs or just experimental flaws — decide for yourself!

* 🔍 **[Read my observations and latest findings here]**(https://github.com/VirGis56/Pickup-AFR-Compare/discussions/1)

**Tools required:**
* Audacity
* Python 3.x

**Key Advantage:** No additional hardware required! You don't need any specialized equipment, excitation coils, or DIY signal generators. All you need is your guitar, a PC, and the software.

**Versatility:** This method is equally valuable for large guitar companies for quality control, and for independent pickup winders or enthusiasts who want to compare sensors without investing in expensive laboratory equipment.

## Why this method?
 This method is **String-Driven**. It captures the signal directly from physical vibrating strings, revealing how the pickup truly interacts with a guitar in real-world conditions, including magnetic pull and physical string mass.
---
## Step-by-Step Workflow

### 1. Initial Setup
* **Create a Folder:** Create a new folder on your computer named **TEST**.
* **Install Script:** Download `script.py` from this repository and move it into your **TEST** folder. All your data files must be in this folder.

### 2. Hardware Setup
* **Connection:** Pickup -> 0.5m cable (critical to minimize capacitance) -> Amp (Clean channel).
* **Signal Path:** Amp Headphone Out -> PC Line-In.
* **Muting (Crucial):** Mute strings at the nut using foam, rubber, or crumpled paper. **Check by ear:** the strings must not ring or have any pitch!
* **Excitation:** Use a pick or a metal file as a "bow" to rub the string back and forth to create "white noise".

### 3. Preparation & Recording
1. **Open Audacity.**
2. **Audacity Hotkey:** Go to **Edit -> Preferences -> Keyboard**. Bind **"Plot Spectrum"** to the **"S"** key.

3. **Record Test Pickup:** Start recording in Audacity. Rub the 6th string for 5 seconds using all possible methods (pick/file) with your test pickup underneath. Stop rubbing for 5 seconds, then stop the recording.

4. **Record Reference:** Swap the pickup for the reference one. **Crucial:** Place it in the exact same position and at the same height. Repeat the recording process (5s rubbing, 5s silence).
5. **Start the Script:** Open your terminal/CMD, 
  * Type `python` and press **SPACE**.
   * Drag your `script.py` from the **TEST** folder into the terminal window.
   * Hit **ENTER**.
   * *The script is now active and waiting for your files.*
   
### 4. Exporting Data
1. **The Test Pickup:** Select a 1-2 second fragment from the first recorded graph in Audacity -> Press **"S"** -> **Export** -> Save as `1.txt` in your **TEST** folder.
2. **The Reference:** Select a similar fragment from the second recorded graph -> Press **"S"** -> **Enter** (to export) -> Save as `2.txt` in your **TEST** folder.

### 5. The Result
The script will automatically detect the files and generate a chart with a **Green Curve**:
* **Above the Red Line (0dB):** Your pickup is stronger/brighter than the reference.
* **Below the Red Line:** Your pickup has less output.

> [!TIP]
> ### **The "Sandwich" Mounting Method**
> Instead of replacing the internal pickup (which requires disassembly), you can lower it and place your test sensor directly above the strings using a custom support.
> 
> **Key Advantages:**
> * **Zero Disassembly:** Perfect for capturing the character of a reference guitar (e.g., at a friend’s house) without modifying the instrument.
> * **Simultaneous Stereo Capture:** This setup allows for recording both sensors at once (Left: Internal / Right: External). It ensures both pickups react to the exact same string vibration, providing a perfect A/B comparison.
> 
> **Important:** Keep a sufficient distance between the sensors to minimize mutual magnetic interference and string pull. Users should account for different signal levels and harmonic responses due to the "sandwich" placement.
---
*Pro Tip: Try rubbing all strings simultaneously for a full-spectrum analysis. Dare to experiment! ( I personally make separate recordings for the 6th and 1st strings to analyze the full range).*
*Created for engineers and enthusiasts who value data over myths.*
---
**Author:** [nE_Er](https://github.com/VirGis56)
---
**Project Updates:**
* **2026.01.14:** New experimental method added: "Sandwich" mounting and synchronous stereo recording.

* **2026.01.15:**
### **Advanced Acoustic Analysis**
The analysis script now automatically detects and displays key technical parameters for each pickup:

* **Resonance Peak Identification:** The script finds the exact peak frequency (Hz) and marks it on the graph.
* **-3dB Bandwidth Lines:** Visual lines are drawn at the -3dB level to show the resonance width.
* **Q-Factor Calculation:** The quality factor is calculated and displayed, allowing you to evaluate the "sharpness" or "warmth" of the sensor.

> [!IMPORTANT]
> **Note on Sharp Peaks:** If a resonance peak is extremely sharp (due to pickup properties or specific FFT settings in Audacity), the horizontal -3dB line might not render on the graph. In such cases, the script will still provide the numerical data for peak frequency and Q-factor.
