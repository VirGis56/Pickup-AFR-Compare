import os
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- SETTINGS ---
WINDOW_SIZE = 900
F_MIN = 30
F_MAX = 15000
Y_RANGE = 40 
ETALON_NAME = "5.4k NoN"

# --- PEAK INDICATOR LEVELS (Adjust heights here) ---
LEVEL_D1 = 3   # Blue line height (Sensor 1)
LEVEL_D2 = -3  # Black line height (Sensor 2)

current_dir = os.path.dirname(os.path.abspath(__file__))
f1_path = os.path.join(current_dir, "1.txt") 
f2_path = os.path.join(current_dir, "2.txt") 
image_path = os.path.join(current_dir, "result.png")

def smooth(data, w):
    """Applying moving average smoothing"""
    if len(data) < w: return data
    return [sum(data[i:i+w])/w for i in range(len(data)-w+1)]

def find_sensor_peak(f_list, amp_list):
    """Finding resonance frequency, -3dB bandwidth and Q-factor"""
    if not amp_list or len(amp_list) < 10: return None
    amp_arr = np.array(amp_list)
    f_arr = np.array(f_list)
    mask = (f_arr >= F_MIN) & (f_arr <= F_MAX)
    if not any(mask): return None
    
    max_idx = np.argmax(amp_arr[mask])
    f_res = f_arr[mask][max_idx]
    max_amp = amp_arr[mask][max_idx]
    
    threshold = max_amp - 3.0
    indices_above = np.where((amp_arr >= threshold) & mask)[0]
    
    if len(indices_above) > 0:
        f_low = f_arr[indices_above[0]]
        f_high = f_arr[indices_above[-1]]
        bw = f_high - f_low
        q_val = f_res / bw if bw > 0 else 0
        return {'f_res': f_res, 'f_low': f_low, 'f_high': f_high, 'q': q_val}
    return None

print(f"--- Final_Pik Analysis Started (English Comments Mode) ---")

last_mtime = os.path.getmtime(f2_path) if os.path.exists(f2_path) else 0
processing = False 

while True:
    if os.path.exists(f1_path) and os.path.exists(f2_path):
        try:
            current_mtime = os.path.getmtime(f2_path)
            if current_mtime > last_mtime and not processing:
                processing = True 
                last_mtime = current_mtime 
                time.sleep(1.0) # Wait for file write completion
                
                def load_data(path):
                    """Loading frequency and amplitude from txt file"""
                    f, a = [], []
                    try:
                        with open(path, "r", encoding='utf-8') as file:
                            next(file) # Skip header
                            for line in file:
                                p = line.split('\t')
                                if len(p) >= 2:
                                    f.append(float(p[0].replace(',', '.')))
                                    a.append(float(p[1].replace(',', '.')))
                    except Exception: return [], []
                    return f, a

                fr1, am1 = load_data(f1_path)
                fr2, am2 = load_data(f2_path)

                if fr1 and fr2:
                    p1 = find_sensor_peak(fr1, am1)
                    p2 = find_sensor_peak(fr2, am2)

                    # Calculating differential curve
                    raw_diff = [v1 - v2 for v1, v2 in zip(am1, am2)]
                    diff = smooth(raw_diff, WINDOW_SIZE)
                    f_plot = fr1[:len(diff)]

                    plt.close('all') 
                    fig, ax = plt.subplots(figsize=(12, 8))
                    
                    # Drawing differential curve (green) and zero level (red)
                    ax.semilogx(f_plot, diff, color='green', linewidth=2, zorder=2)
                    ax.axhline(0, color='red', linestyle='-', linewidth=1.5, alpha=0.6, zorder=1)

                    # Drawing P1 resonance line (blue)
                    if p1:
                        ax.hlines(y=LEVEL_D1, xmin=p1['f_low'], xmax=p1['f_high'], colors='blue', linewidth=10, zorder=5)
                        txt1 = f"P1: {p1['f_res']:.0f}Hz | Q: {p1['q']:.2f}"
                        ax.text(p1['f_res'], LEVEL_D1 + 1.2, txt1, color='blue', fontweight='bold', ha='center', va='bottom', fontsize=10)

                    # Drawing P2 resonance line (black)
                    if p2:
                        ax.hlines(y=LEVEL_D2, xmin=p2['f_low'], xmax=p2['f_high'], colors='black', linewidth=10, zorder=5)
                        txt2 = f"P2: {p2['f_res']:.0f}Hz | Q: {p2['q']:.2f}"
                        ax.text(p2['f_res'], LEVEL_D2 - 1.2, txt2, color='black', fontweight='bold', ha='center', va='top', fontsize=10)

                    # Axis and grid configuration
                    ax.set_xlim(F_MIN, F_MAX)
                    ax.set_ylim(-Y_RANGE, Y_RANGE)
                    ticks = [40, 100, 200, 500, 1000, 2000, 5000, 10000]
                    ax.set_xticks(ticks)
                    ax.set_xticklabels([str(t) for t in ticks])
                    ax.grid(True, which="both", alpha=0.3)
                    
                    # Setting the requested title format
                    curr_date = time.strftime('%Y, %m, %d')
