#adjust system volume based on your microphone levels

import pyaudio
import wave
import sys
import audioop
import osascript
from time import sleep

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
MAX_SYSTEM_VOLUME = 30
MAX_INPUT_VOLUME = 25000

# instantiate PyAudio (1)
p = pyaudio.PyAudio()
devinfo = p.get_device_info_by_index(0)
# open stream (2)
input_stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=0
                )


while True:
	data = input_stream.read(CHUNK, exception_on_overflow=False)
	max_vol = audioop.max(data, 2);
	input_volume_percentage = max_vol*100/25000;
	print("Max volume is "+str(input_volume_percentage))
	adjusted_system_volume = MAX_SYSTEM_VOLUME - input_volume_percentage
	print("Adjusting system volume to "+str(adjusted_system_volume))
	osascript.osascript("set volume output volume "+str(adjusted_system_volume))
	# sleep(5)
# stop stream (4)
input_stream.stop_stream()
input_stream.close()

# close PyAudio (5)
p.terminate()
