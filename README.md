# IPA-Lab-Week03

This repository contains lab exercises and code related to network automation, focusing on the use of Python libraries like `Netmiko`, `Paramiko`, and `Jinja2` for device interaction and configuration templating.

## Table of Contents

- [IPA-Lab-Week03](#ipa-lab-week03)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Contents](#contents)
  - [Requirements](#requirements)

## Overview

This lab aims to provide hands-on experience with:
- **Netmiko**: A multi-vendor SSH Python library for network automation, simplifying the process of connecting to network devices and executing commands.
- **Paramiko**: A Python implementation of the SSHv2 protocol, providing both client and server functionality, often used for more granular control over SSH connections.
- **Jinja2**: A modern and designer-friendly templating language for Python, used here to create dynamic network configurations from templates.

The exercises likely cover tasks such as connecting to devices, executing show commands, pushing configurations, and generating configurations using templates.

## Contents

The repository is organized into the following main directories and files:

- **`instruction/`**: Contains lab instructions or documentation.
- **`jinja2_template/`**: Stores Jinja2 templates used for generating configurations.
- **`keys/`**: Potentially holds SSH keys or other sensitive access credentials (ensure these are handled securely and not committed directly in a real-world scenario).
- **`netmiko_module/`**: Contains Python scripts or modules specifically using the Netmiko library.
- **`paramiko_module/`**: Contains Python scripts or modules specifically using the Paramiko library.
- **`test/`**: Includes test scripts or configurations for verifying lab exercises.

- **`.gitignore`**: Specifies intentionally untracked files to ignore.
- **`netmiko-jinja2.py`**: A Python script likely demonstrating the integration of Netmiko with Jinja2 for configuration deployment.
- **`netmiko_re.py`**: A Python script possibly showcasing regular expression parsing of command output with Netmiko.
- **`netmikolab.py`**: A core Python script for Netmiko-based lab exercises.
- **`paramikolab.py`**: A core Python script for Paramiko-based lab exercises.
- **`requirement.txt`**: Lists the Python dependencies required to run the scripts in this repository.
- **`textfsmlab.py`**: (Likely related to TextFSM, a Google project for parsing semi-structured text data into Python dictionaries/lists, often used with Netmiko.)

## Requirements

To run the Python scripts in this repository, you will need to install the dependencies listed in `requirement.txt`.

```bash
pip install -r requirement.txt