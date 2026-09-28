import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import sys
import os

out_dir = "/Users/nika/CO2_PCB/co2-monitor-PCB/visualization"
os.makedirs(out_dir, exist_ok=True)

files = ["/Users/nika/CO2_PCB/co2-monitor-PCB/sensor_data/SCD41_sensor_baseline_20260921_124456.csv",
         "/Users/nika/CO2_PCB/co2-monitor-PCB/sensor_data/SCD41_sensor_colab_baseline_20260921_160512.csv",
         "/Users/nika/CO2_PCB/co2-monitor-PCB/sensor_data/SCD41_sensor_tegaderm_colab_wrist_20260921_163920.csv",
         "/Users/nika/CO2_PCB/co2-monitor-PCB/sensor_data/SCD41_sensor_tegaderm_colab_wrist_breathr_20260921_164933.csv",
         ]

cols = ["pc_time", "device_time", "device_us", "co2_ppm",
        "temp_c", "humidity_pct", "co2_mmhg"]

plots = [
    ("co2_ppm", "CO₂ (ppm)", "tab:green"),
    ("temp_c", "Temperature (°C)", "tab:red"),
    ("humidity_pct", "Humidity (%)", "tab:blue"),
]

for path in files:
    df = pd.read_csv(path, skiprows=1, names=cols, dtype={"device_us": str})
    df["device_time"] = df["device_time"] + df["device_us"].str.strip()
    df = df.drop(columns="device_us")
    df["pc_time"] = pd.to_datetime(df["pc_time"])

    fig, axes = plt.subplots(len(plots), 1, figsize=(10, 8), sharex=True)
    for ax, (col, label, color) in zip(axes, plots):
        ax.plot(df["pc_time"], df[col], color=color, marker=".", linewidth=1)
        ax.set_ylabel(label)
        ax.grid(alpha=0.3)

    name = path.split("/")[-1].rsplit(".", 1)[0]
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    axes[-1].set_xlabel("Time")
    fig.suptitle(name)
    fig.autofmt_xdate()
    fig.tight_layout()

    out = os.path.join(out_dir, name + "_plot.png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved {out}")

