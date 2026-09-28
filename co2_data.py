import serial, serial.tools.list_ports
import re, datetime
import time

PORT = "/dev/cu.usbmodem0010506414411" #hardcoded for my device, change if needed
BAUD = 115200
DURATION_SEC = 120

available = [p.device for p in serial.tools.list_ports.comports()]
if PORT not in available:
    print("Port not found. Available ports:")
    for p in serial.tools.list_ports.comports():
        print(" ", p.device, "-", p.description)
    raise SystemExit(1)


ansi = re.compile(r"\x1b\[[0-9;]*m")                    # strips ANSI color codes from the logger
dev_ts = re.compile(r"\[(\d+:\d+:\d+\.\d+,\d+)\]")      # grabs the board timestamp

pat = re.compile(
    r"CO2:\s*(-?\d+\.\d+)\s*ppm.*?"
    r"Temp:\s*(-?\d+\.\d+).*?"
    r"Humidity:\s*(-?\d+\.\d+).*?"
    r"CO2:\s*(-?\d+\.\d+)\s*mmHg"
)

# Make sure to rename according to the device and film used.
fname = datetime.datetime.now().strftime("SCD41_sensor_tegaderm_colab_wrist_breathr_%Y%m%d_%H%M%S.csv")

with serial.Serial(PORT, BAUD, timeout=1) as ser, open(fname, "w") as f:
    f.write("pc_time,device_time,co2_ppm,temp_c,humidity_pct,co2_mmhg\n")
    print(f"Logging {PORT} -> {fname} for {DURATION_SEC}s (Ctrl+C to stop early)")
    start = time.time()
    try:
        while time.time() - start < DURATION_SEC:
            raw = ser.readline().decode(errors="ignore")
            line = ansi.sub("", raw).strip()
            m = pat.search(line)
            if not m:
                continue
            t = dev_ts.search(line)
            device_time = t.group(1) if t else ""
            pc_time = datetime.datetime.now().isoformat(timespec="seconds")
            f.write(",".join([pc_time, device_time, *m.groups()]) + "\n")
            f.flush()
            print(line)
    except KeyboardInterrupt:
        print("Stopped early.")

print(f"Done. Saved to {fname}")
