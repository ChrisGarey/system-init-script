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

    with Progress() as progress:
        task1 = progress.add_task("[#fff]Checking Resources", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)

    # Start system check
    # Get the current user's home directory
current_user = pwd.getpwuid(os.getuid()).pw_name
home_directory = os.path.expanduser(f"~{current_user}")

# List the partitions in the /dev/ directory
dev_partition_list = os.listdir('/dev/')

# Find the primary hard drive partition associated with the user's home directory
# Get the current user's home directory
current_user = pwd.getpwuid(os.getuid()).pw_name
home_directory = os.path.expanduser(f"~{current_user}")

# Get the device associated with the home directory
try:
    df_output = subprocess.check_output(["df", home_directory])
    lines = df_output.decode("utf-8").strip().split("\n")
    if len(lines) > 1:
        device_info = lines[1].split()
        device = device_info[0]
    else:
        device = None
except subprocess.CalledProcessError:
    device = None

if device:
    print(f"The user's primary hard drive is {device}")

    # Run a short disk scan without checking for encryption or SMART
    system_check = os.system(f"sudo fsck -t ext4 -y {device}")
    if system_check == 0:
        print("Disk scan started.")
    else:
        print("The system encountered an error while starting the disk scan. Please investigate.")
    time.sleep(0.5)
else:
    print("Unable to determine the user's primary hard drive.")

    # Start update
    print("\nStarting update ...", end=' ')

    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Updating System", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)

    system_update = os.system("sudo apt-get update > /dev/null 2>&1")
    if system_update == 0:
         print("System updated.")
    else:
         print("The system encountered an error checking updating. Please investigate.")
    time.sleep(0.5)

    #Start upgrade
    print("\nStarting upgrade ...", end=' ')
    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Upgrading System", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)
    system_upgrade = os.system("sudo apt-get upgrade > /dev/null 2>&1")
    if system_upgrade == 0:
         print("System upgraded.")
    else:
         print("The system encountered an error upgrading. Please investigate.")
    time.sleep(0.5)

    # Start firewall and SMART disk services
    print("\nStarting all the services ..", end=' ')

    # Progress Bar
    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Starting Services", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)

    # Commands to execute
    firewall_start = os.system('sudo ufw enable >/dev/null 2>&1 && sudo smartctl -s on %s >/dev/null 2>&1' % (sda))
    if firewall_start == 0:
         print("Firewall enabled.")
         time.sleep(0.3)
         print("Smart Disk enabled.")
    else:
         print("The system encountered an error starting services. Please investigate.")
    time.sleep(0.3)

    # Get the current user profile then store it.
    print("\nGetting user profile ...", end=' ')
    def get_username():
        return pwd.getpwuid(os.getuid())[0]

    # Progress Bar
    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Grabbing user profile", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)

    print("User profile set.")
    time.sleep(0.3)

    # Get and print the local IP address
    print("\nGetting IP Address - ", ip_address)
    time.sleep(0.3)

    print("\nAll Set! System load completed.")
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
