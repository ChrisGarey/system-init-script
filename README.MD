# System Initialization and Maintenance Script

![](https://github.com/ChrisGarey/system-init-script/blob/main/images/demo.gif)

This Python script automates system initialization and maintenance tasks for Debian-based distributions. It checks and optimizes your system for performance, updates package sources, ranks and updates mirrors, upgrades the system, and enables essential services like the firewall and SMART disk monitoring. The script also provides a colorful and welcoming terminal interface for a delightful user experience.

## Features

🚀 Initiates system maintenance tasks with progress bars.
📊 Runs SMART disk checks and optimizes disk health.
🔄 Updates package sources for the latest software.
🌐 Ranks and updates mirrors for faster package downloads.
⬆ Upgrades the system to the latest packages.
🛡 Enables the firewall for enhanced security.
💽 Enables SMART disk monitoring to detect disk issues.
📈 Displays system information, including IP address.
🎨 Adds a colorful and customizable terminal banner.

## Requirements

    Python 3.x
    pySMART Python package
    rich Python package
    speedtest-cli for network speed testing

## Usage

Clone this repository to your local machine.

```git clone https://github.com/yourusername/system-maintenance-script.git```

Before running the script, make sure you have the required Python packages installed. You can install them using `pip`:


```pip install -r REQUIREMENTS```

Run the script as a superuser (root) to execute system maintenance tasks.

```sudo python system_maintenance.py```

Follow the on-screen prompts to initiate the system maintenance process.

## Customize

You can customize the script by modifying the code to suit your specific needs. The script provides a foundation for automating system maintenance tasks on Debian-based distributions.

### Author

Christopher Garey
GitHub: ChrisGarey