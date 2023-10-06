import subprocess
import time
import os
import pwd
import random
import socket
from pySMART import SMARTCTL, DeviceList
from rich.progress import Progress

SMARTCTL.sudo = True

# Variables
devlist = DeviceList()
sda = '/dev/nvme0n1'
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Define Progress bar for later use
def progress_bar():
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Starting Services", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)

# Function to apply a randomized rainbow effect similar to lolcat
def apply_lolcat_colors(text):
    color_codes = [str(random.randint(31, 37)) for _ in text]
    colored_text = ''.join(f'\033[{code}m{char}' for code, char in zip(color_codes, text))
    return colored_text

# Start script
if __name__ == "__main__":
    print("INITIATING SYSTEM")
    print("-----------------")
    time.sleep(0.3)

    # Check filesystem for any errors and if so, display an error message.
    print("Checking system resources ...", end=' ')

    # Progress Bar
    print(progress_bar()) if progress_bar() else None

    # Start system check
    system_check = os.system("sudo smartctl --test=short -H %s >/dev/null 2>&1" % (sda))
    if system_check == 0:
         print("OK")
    else:
         print("The system encountered an error checking disks. Please investigate.")
    time.sleep(0.5)

    # Start firewall and SMART disk services
    print("Starting all the services ..", end=' ')

    # Progress Bar
    print(progress_bar()) if progress_bar() else None

    # Commands to execute
    firewall_start = os.system('sudo ufw enable >/dev/null 2>&1 && sudo smartctl -s on %s >/dev/null 2>&1' % (sda))
    if firewall_start == 0:
         print("OK")
    else:
         print("The system encountered an error starting services. Please investigate.")
    time.sleep(0.3)

    # Get the current user profile then store it.
    print("Getting user profile ...", end=' ')
    def get_username():
        return pwd.getpwuid(os.getuid())[0]

    # Progress Bar
    print(progress_bar()) if progress_bar() else None

    print("OK")
    time.sleep(0.3)

    # Get and print the local IP address
    print("Getting IP Address - ", ip_address)
    time.sleep(0.3)

    print("All Set! System load completed.")
    time.sleep(0.3)

    print("Launching the Machine ...")
    time.sleep(0.5)

    print("\nWelcome", get_username().capitalize())
    print("----------------")

    # Run the command and capture its output
    try:
        banner_process = subprocess.Popen(
            'lsb_release -ds | figlet',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        banner_output, _ = banner_process.communicate()

        colored_banner = apply_lolcat_colors(banner_output)

        # Print the colored banner
        print(colored_banner, end='')
    except subprocess.CalledProcessError:
        print("An error occurred while running the command")
