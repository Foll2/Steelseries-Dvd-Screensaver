from PIL import ImageSequence
from easyhid import Enumeration
from time import sleep
from signal import signal, SIGINT, SIGTERM
from sys import exit
import animation

# Screen resolution (Keyboards have 128,40)
resolution = (128, 40)

# List of known working devices, add your PID here (Only tested Apex 5)
#                Apex 7,  7 TKL, Pro, Apex 5
supported_pid = (5650, 5656, 5648, 5660)

def getdevice():
    # Stores an enumeration of all the connected USB HID devices
    en = Enumeration()

    # Return a list devices based on the search parameters
    devices = en.find(vid=0x1038, interface=1)
    if not devices:
        exit("No SteelSeries devices found, exiting.")

    for device in devices:
        if device.product_id in supported_pid:
            print(f"Found device: {device.product_string}")
            return device

    print("Non supported PIDs:")
    for device in devices:
        print(f"{device.product_string}: {device.product_id}")

    exit("\nNo compatible SteelSeries devices found, exiting.")


def main():
    # get our keyboard
    dev = getdevice()

    # define our signal handler to blank the screen on shutdown
    def signal_handler(sig, frame):
        try:
            dev.send_feature_report(bytearray([0x61] + [0x00] * 641))
            dev.close()
            print("\n")
            exit(0)
        except Exception as e:
            exit(str(e))

    # Set up ctrl-c handler
    signal(SIGINT, signal_handler)
    # Set up SIGTERM handler
    signal(SIGTERM, signal_handler)
    dev.open()

    print("Press Ctrl-C to exit.\n")

    # set up the frame rate
    sleeptime = 0.1

    # send the frames to the keyboard
    while(True):
        # generate a new image using the DVD screensaver function
        image = animation.generate(resolution)

        # resize the image and process the frames for the keyboard
        resizedframes = []
        for frame in ImageSequence.Iterator(image):
            # Image size based on Apex 7 and Apex Pro
            frame = frame.resize(resolution)
            # Convert to monochrome
            frame = frame.convert('1')
            data = frame.tobytes()
            resizedframes.append(bytearray([0x61]) + data + bytearray([0x00]))

            # send the frames to the keyboard
            for data in resizedframes:
                dev.send_feature_report(data)
                sleep(sleeptime)


if __name__ == "__main__":
    main()
