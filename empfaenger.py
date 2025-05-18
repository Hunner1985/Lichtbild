import RPi.GPIO as GPIO
import time
import signal
import sys

RECEIVER_PIN = 9  # BCM-Nummer für GPIO 9
SAMPLESIZE = 1000

timings = []
last_time = 0

def handle_interrupt(channel):
    global last_time, timings

    now = time.time()
    duration = now - last_time
    last_time = now

    timings.append(int(duration * 1_000_000))

    if len(timings) > SAMPLESIZE:
        timings.pop(0)

def exit_gracefully(signal_num, frame):
    GPIO.cleanup()
    print("\nSignal aufgezeichnet:")
    print(",".join(map(str, timings)))
    sys.exit(0)

def main():
    global last_time

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVER_PIN, GPIO.IN)

    print("Warte auf 433 MHz-Signal... Drücke Strg+C zum Beenden")

    last_time = time.time()
    GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH, callback=handle_interrupt)

    signal.signal(signal.SIGINT, exit_gracefully)

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
