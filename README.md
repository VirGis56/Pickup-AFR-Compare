# Pickup-AFR-Compare

A unique **string-driven** method and Python tool for analyzing and comparing guitar pickup frequency response (AFR).

## Why this method?
Traditional laboratory setups (like excitation coils) show only electrical properties. This method is **String-Driven**. It captures the signal directly from physical vibrating strings, revealing how the pickup truly interacts with a guitar in real-world conditions, including magnetic pull and physical string mass.
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

---
*Pro Tip: Try rubbing all strings simultaneously for a full-spectrum analysis. Dare to experiment! ( I personally make separate recordings for the 6th and 1st strings to analyze the full range).*
*Created for engineers and enthusiasts who value data over myths.*
