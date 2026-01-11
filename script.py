

import os
import time
import matplotlib
matplotlib.use('Agg') # Enables background image generation
import matplotlib.pyplot as plt

# --- SETTINGS ---
WINDOW_SIZE = 30        # Smoothing factor (1 - raw, 7-15 - smooth, 30+ - heavy smoothing)
F_MIN = 40              # Minimum Frequency (Hz)
F_MAX = 10000           # Maximum Frequency (Hz)
Y_RANGE = 25            # Scale Range (dB)
REFERENCE_NAME = "Standard 5.4k Pickup"  # Name of your reference pickup

current_dir = os.path.dirname(os.path.abspath(__file__))
f1_path = os.path.join(current_dir, "1.txt") # Your New Sensor
f2_path = os.path.join(current_dir, "2.txt") # Reference Pickup
image_path = os.path.join(current_dir, "result.png")

def smooth(data, w):
    if len(data) < w: return data
    return [sum(data[i:i+w])/w for i in range(len(data)-w+1)]

print(f"--- PICKUP ANALYSIS: Sensor vs Reference RUNNING ---")
print("Waiting for updates in 2.txt...")

# Initial timestamp
last_mtime = os.path.getmtime(f2_path) if os.path.exists(f2_path) else 0
processing = False # Processing lock

while True:
    if os.path.exists(f1_path) and os.path.exists(f2_path):
        try:
            current_mtime = os.path.getmtime(f2_path)
            
            # If 2.txt has been updated and we are not currently processing
            if current_mtime > last_mtime and not processing:
                processing = True # Close the lock
                last_mtime = current_mtime # Update timestamp immediately
                
                time.sleep(0.7) # Brief delay to allow Audacity to finish writing the file
                
                # Load Test Sensor Data
                f1, l1 = [], []
                with open(f1_path, "r", encoding='utf-8') as f:
                    next(f) # Skip header
                    for line in f:
                        p = line.split('\t')
                        if len(p) >= 2:
                            f1.append(float(p[0].replace(',', '.')))
                            l1.append(float(p[1].replace(',', '.')))
                
                # Load Reference Data
                f2, l2 = [], []
                with open(f2_path, "r", encoding='utf-8') as f:
                    next(f) # Skip header
                    for line in f:
                        p = line.split('\t')
                        if len(p) >= 2:
                            f2.append(float(p[0].replace(',', '.')))
                            l2.append(float(p[1].replace(',', '.')))

                if f1 and f2:
                    # Calculate difference
                    raw_diff = [v1 - v2 for v1, v2 in zip(l1, l2)]
                    diff = smooth(raw_diff, WINDOW_SIZE)
                    f_plot = f1[:len(diff)]

                    plt.close('all')
                    fig, ax = plt.subplots(figsize=(12, 7))
                    
                    # Plotting
                    ax.semilogx(f_plot, diff, color='green', linewidth=2.5)
                    ax.axhline(0, color='red', linestyle='-', linewidth=2)
                    
                    ax.set_xlim(F_MIN, F_MAX)
                    ax.set_ylim(-Y_RANGE, Y_RANGE)
                    
                    # Set standard frequency ticks
                    ticks = [40, 100, 200, 500, 1000, 2000, 5000, 10000]
                    ax.set_xticks(ticks)
                    ax.set_xticklabels([str(t) for t in ticks])
                    
                    ax.grid(True, which="major", color='gray', linestyle='-', alpha=0.5)
                    ax.grid(True, which="minor", color='gray', linestyle=':', alpha=0.2)
                    
                    current_date = time.strftime('%Y-%m-%d')
                    current_time = time.strftime('%H:%M:%S')
                    
                    plt.title(f"NEW SENSOR vs REFERENCE [{REFERENCE_NAME}]\nDate: {current_date}  Time: {current_time}", fontsize=12)
                    plt.ylabel("Difference (dB)")
                    plt.xlabel("Frequency (Hz)")
                   
                    plt.tight_layout()
                    plt.savefig(image_path)
                    plt.close(fig)
                    
                    print(f"[{current_time}] Graph updated successfully.")
                    os.startfile(image_path) # Opens the image
                
                # Cooldown period
                time.sleep(2)
                processing = False

        except Exception as e:
            print(f"Error encountered: {e}")
            processing = False # Unlock on error
            
    time.sleep(1)

