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
## Requirements

To run this script, you'll need the following dependencies:

### Debian-based Distributions

- [pySMART](https://pypi.org/project/pySMART/)
- [rich](https://pypi.org/project/rich/)
- [speedtest-cli](https://pypi.org/project/speedtest-cli/)

You can install these packages using `pip`:


```pip install pySMART rich speedtest-cli```

### Arch-based Distributions

On Arch-based distributions, the script relies on system package managers for dependencies. You can use the following commands to install the required packages:


```# Install pySMART and rich using pacman sudo pacman -S pySMART python-rich```

# Install speedtest-cli using pip
```pip install speedtest-cli```

# Install speedtest-cli using pip
```pip install speedtest-cli```

## Usage

Clone this repository to your local machine.

```git clone https://github.com/ChrisGarey/system-init-script.git```

Navigate to the project directory:

```cd system-init-script```

Run the script to execute system maintenance tasks.

```python3 system_maintenance.py```

Follow the on-screen prompts to initiate the system maintenance process.

## Customize

You can customize the script by modifying the code to suit your specific needs. The script provides a foundation for automating system maintenance tasks on Debian-based distributions.

### Author

Christopher Garey

GitHub: ChrisGarey