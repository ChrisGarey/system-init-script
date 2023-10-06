import subprocess
import time
import os
import pwd
import random
import socket
from pySMART import SMARTCTL, DeviceList
from rich.progress import Progress
import speedtest

SMARTCTL.sudo = True

# Variables
devlist = DeviceList()
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Function to apply a randomized rainbow effect similar to lolcat
def apply_lolcat_colors(text):
    color_codes = [str(random.randint(31, 37)) for _ in text]
    colored_text = ''.join(f'\033[{code}m{char}' for code, char in zip(color_codes, text))
    return colored_text

# Function to run the SMART disk check with a progress bar
def run_smart_disk_check(device_to_check):
    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Checking Disks", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)

    print("Running SMART disk check... [Done]")
    smart_check_command = f"sudo smartctl --test=short {device_to_check} > /dev/null 2>&1"
    smart_check_result = os.system(smart_check_command)

    if smart_check_result == 0:
        print("SMART disk check completed successfully.\n")
    else:
        print("Error running SMART disk check. Please investigate.")
        

# Function to update the system (Debian-based distributions)
def update_debian_system():
    sources_list_file = '/etc/apt/sources.list'
    
    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Updating System", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)

    system_update = os.system(f"sudo apt-get update > /dev/null 2>&1 -o Dir::Etc::sourcelist='{sources_list_file}'")
    if system_update == 0:
        print("System updated.")
    else:
        print("The system encountered an error checking updating. Please investigate.")
        

# Function to rank and update mirrors (Debian-based distributions)
def rank_and_update_debian_mirrors():
    # Update package lists to ensure we have the latest mirror information
    update_command = "sudo apt-get update > /dev/null 2>&1"
    subprocess.run(update_command, shell=True, check=True)

    # Get a list of available Debian mirrors
    get_mirror_list_command = "apt-get -y --print-uris update > /dev/null 2>&1"
    mirror_list = subprocess.check_output(get_mirror_list_command, shell=True).decode("utf-8")

    # Parse mirror URIs
    mirrors = [line.split()[0][1:-1] for line in mirror_list.splitlines()]

    # Select the fastest mirror
    fastest_mirror = select_fastest_mirror(mirrors)

    if fastest_mirror:
        # Update the 'sources.list' file with the selected mirror
        update_sources_command = f"sudo sed -i 's#http://[^/]\+/debian/#{fastest_mirror}#' /etc/apt/sources.list > /dev/null 2>&1"
        subprocess.run(update_sources_command, shell=True, check=True)
        print("Fastest mirror selected and updated.")
    else:
        print("No suitable mirrors found.\n")

# Placeholder function for selecting the fastest mirror
def select_fastest_mirror(mirrors):
    # Measure the response times of mirrors and select the fastest one
    fastest_mirror = None
    min_response_time = float('inf')

    for mirror in mirrors:
        response = os.system(f"ping -c 1 -q {mirror} > /dev/null 2>&1")
        if response == 0:
            # Mirror is responsive, measure response time
            start_time = time.time()
            os.system(f"curl -o /dev/null -s -w '%{time_total}' {mirror}")
            end_time = time.time()
            response_time = end_time - start_time

            if response_time < min_response_time:
                min_response_time = response_time
                fastest_mirror = mirror

    return fastest_mirror

# Function to rank and update mirrors (Arch-based distributions)
def rank_and_update_arch_mirrors():
    try:
        # Automatically detect the user's country
        reader = geoip2.database.Reader('/usr/share/GeoIP/GeoLite2-Country.mmdb')
        response = reader.country(ip_address)
        user_country = response.country.iso_code.lower()

        # Rank and update mirrors using reflector
        rank_mirrors_command = f"sudo reflector --country {user_country} --age 6 --protocol https --sort rate --save /etc/pacman.d/mirrorlist"
        subprocess.run(rank_mirrors_command, shell=True, check=True)
        print("Mirrors ranked and updated.")
    except Exception as e:
        print(f"Error detecting user's country: {e}")

# Define the device_to_check variable at a higher scope
device_to_check = None

# Start script
if __name__ == "__main__":
    print("INITIATING SYSTEM")
    print("-----------------")
    time.sleep(0.3)

    # Check filesystem for any errors and if so, display an error message.
    print("Checking system resources ...", end=" ")

    with Progress() as progress:
        task1 = progress.add_task("[#fff]Checking Resources", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)
            
    # Function to get the user's primary hard drive
    def get_primary_hard_drive():
        # Get the current user's home directory
        current_user = pwd.getpwuid(os.getuid()).pw_name
        home_directory = os.path.expanduser(f"~{current_user}")

        # List the partitions in the /dev/ directory
        dev_partition_list = os.listdir('/dev/')

        for partition in dev_partition_list:
            full_path = os.path.join('/dev/', partition)

            # Check if the partition contains the user's home directory
            if os.path.exists(os.path.join(home_directory, 'Documents')) and os.path.exists(full_path):
                # Check if it's a block device
                if os.path.isfile(f"/sys/class/block/{partition}/size"):
                    return full_path

        return None

    # Function to check if a device is mounted
    def is_device_mounted(device):
        mount_check = subprocess.run(["mountpoint", "-q", device])
        return mount_check.returncode == 0

    # Function to safely unmount a device if it's mounted
    def unmount_device(device):
        if is_device_mounted(device):
            # Unmount the device
            unmount_command = f"sudo umount {device}"
            unmount_result = os.system(unmount_command)

            if unmount_result == 0:
                print(f"{device} unmounted successfully.")
            else:
                print("Error unmounting the device. Please investigate.")
                
        else:
            print(f"The device {device} is not mounted.")

    # Function to remount a device without unmounting it
    def remount_device(device):
        remount_command = f"sudo mount -o remount {device}"
        remount_result = os.system(remount_command)

        if remount_result == 0:
            print(f"{device} remounted successfully.\n")
           
        else:
            print("Error remounting the device. Please investigate.")
            

    # Start system check
    # Detect the user's primary hard drive
    device_to_check = get_primary_hard_drive()

    if device_to_check:
        print(f"Detected primary hard drive: {device_to_check}")

        # Unmount the device safely
        unmount_device(device_to_check)

        # Remount the device safely
        remount_device(device_to_check)

        # Run the SMART disk check with a progress bar
        run_smart_disk_check(device_to_check)
    else:
        print("Unable to determine the user's primary hard drive.")
        time.sleep(0.5)

    # Update the system
    update_debian_system()

    try:
        # Call the function to rank and update mirrors
        rank_and_update_debian_mirrors()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    time.sleep(0.5)

    # Start upgrade
    print("Starting upgrade ...", end=' ')
    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Upgrading System", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)
            print("\r", end=' ')

    system_upgrade = os.system("sudo apt-get upgrade -y > /dev/null 2>&1")
    if system_upgrade == 0:
         print("System upgraded.\n")
    else:
         print("The system encountered an error upgrading. Please investigate.")
    time.sleep(0.5)

    # Start firewall and SMART disk services
    print("Starting all the services ..", end=' ')

    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Starting Services", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)
            print("\r", end=' ')

    # Commands to execute
    if device_to_check:
        firewall_start = os.system('sudo ufw enable >/dev/null 2>&1 && sudo smartctl -s on %s >/dev/null 2>&1' % (device_to_check))
        if firewall_start == 0:
             print("Firewall enabled.")
             time.sleep(0.3)
             print("Smart Disk enabled.\n")
        else:
             print("The system encountered an error starting services. Please investigate.")
    else:
        print("Skipping firewall and SMART disk services as device_to_check is not defined.")
    time.sleep(0.3)

    # Get the current user profile then store it.
    print("Getting user profile ...", end=' ')
    def get_username():
        return pwd.getpwuid(os.getuid())[0]

    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Grabbing user profile", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)
            print("\r", end=' ')

    print("User profile set.\n")
    time.sleep(0.3)

    # Get and print the local IP address
    print("Getting IP Address...", end=' ')

    # Progress Bar
    with Progress() as progress:
        task1 = progress.add_task("[#fff]Getting system IP address", total=500)

        while not progress.finished:
            progress.update(task1, advance=7)
            time.sleep(0.02)
            print("\r", end=' ')

    print("System IP address - ", ip_address, "\n")
    time.sleep(0.3)

    print("All Set! System load completed.")
    time.sleep(0.3)

    print("Launching the Machine ...")
    time.sleep(0.5)

    print("Welcome", get_username().capitalize())
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
