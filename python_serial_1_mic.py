import serial
import numpy as np
import wave
import time
import sys

# Configuration
sample_rate = 8000
port = 'COM6'  # Update with your ESP32's serial port (COM3 on Windows)
baudrate = 921600
output_file = '20251024_mictest1.wav'
max_recording_seconds = 10  # Set to None for continuous recording

print(f"Opening serial port {port} at {baudrate} baud...")
try:
    ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
    print("Serial port opened successfully")
except Exception as e:
    print(f"Error opening serial port: {e}")
    import serial.tools.list_ports
    ports = [p.device for p in serial.tools.list_ports.comports()]
    print(f"Available ports: {ports}")
    sys.exit(1)

# Prepare WAV file
with wave.open(output_file, 'wb') as wf:
    wf.setnchannels(1)  # Mono
    wf.setsampwidth(2)  # 16-bit
    wf.setframerate(sample_rate)
    
    print(f"Recording audio (max {max_recording_seconds}s)...")
    print("Press Ctrl+C to stop recording")
    
    start_time = time.time()
    total_bytes = 0
    
    try:
        while True:
            # Check if we've reached the maximum recording time
            if max_recording_seconds and (time.time() - start_time >= max_recording_seconds):
                print(f"\nReached maximum recording time of {max_recording_seconds} seconds")
                break
                
            # Read a chunk of audio data
            data = ser.read(1024)  # Read up to 1024 bytes
            
            if data:
                # Write to WAV file
                wf.writeframes(data)
                total_bytes += len(data)
                
                # Print progress every second
                elapsed = time.time() - start_time
                if int(elapsed) == elapsed:  # Only print once per second
                    print(f"\rRecording: {elapsed:.1f}s - {total_bytes} bytes", end="")
            else:
                # No data received in timeout period
                print("\rWaiting for data...", end="")
    
    except KeyboardInterrupt:
        print("\nRecording stopped by user")

print(f"\nRecording complete! Saved to {output_file}")
print(f"Total recorded: {total_bytes} bytes ({total_bytes/2} samples)")

# Close the serial connection
ser.close()

print("Audio file saved. You can now process or play it.")