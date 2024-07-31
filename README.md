# Web-Nmap
Web-Nmap is a web-based interface for the Nmap security scanner. It allows users to easily launch Nmap scans from a web browser, managing and viewing the results through a user-friendly dashboard.

## Features
- **Scan Management**: Users can create, view, and delete Nmap scans.
- **Scan Results**: Users can view the results of their Nmap scans, including the scan details and any vulnerabilities found.
- **Dashboard**: Users have access to a dashboard that displays an overview of their recent scans and any critical vulnerabilities found.
- **Scan Scheduling**: Users can schedule scans to run at specific times or intervals.
- **Repeat Scans on Schedule**: Users can set up recurring scans to run automatically at specified intervals.
- **Scan Profiles**: Users can create and save scan profiles with custom settings for different types of scans.

# Installation

## Step 1: Clone the Repository
First, you need to clone the repository to your local machine. Open your terminal and run the following command:
```git clone https://github.com/CrySteRz/web-nmap.git```

This command downloads the project files from GitHub to your computer.

## Step 2: Navigate to the Project Directory
After cloning, you need to move into the project directory. Run this command in your terminal:
```cd web-nmap```

This command changes your current directory to the `web-nmap` folder that you just cloned.

## Step 3: Start the Docker Containers
Finally, to get the project up and running, you'll use Docker Compose. This will start all the necessary containers for the project. Run the following command:
```docker-compose up -d --build --scale worker=3```

- `up` tells Docker Compose to start the containers.
- `-d` runs the containers in the background.
- `--build` builds the images before starting the containers.
- `--scale worker=3` starts three instances of the `worker` service.

After running this command, the project should be up and running on your machine.

# License
This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0) - see the LICENSE file for details. This license allows anyone to use, modify, and distribute the project, commercially or not, provided that all modifications and derived works are also licensed under the same terms. This ensures that the project and any modifications to it remain open source, promoting transparency and community contributions.

# Credits
This project is built upon the original work of [cldrn in rainmap-lite](https://github.com/cldrn/rainmap-lite/tree/master). My contributions are as follows:
- **Scheduled Scans**: Introduced the capability to schedule scans at specific times or intervals.
- **Repeating Scans**: Added a feature to repeat scans according to a set schedule.
- **Docker Support**: Integrated Docker to facilitate easier deployment and management.
- **Enhanced Scheduler**: Replaced cron jobs with a more efficient and flexible scheduler service.
- **Simplified Setup**: Developed clearer and more user-friendly setup instructions.