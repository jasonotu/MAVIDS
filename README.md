# MAVIDS

The Micro Air Vehicle Intrusion Detection System (MAVIDS)  is a machine learning-based IDS for UAVs that use the MAVLink communication protocol.

[TOC]

### Installation

MAVIDS is only supported on linux using Python 3.

Clone the repo:
```bash
git clone https://github.com/jasonotu/MAVIDS
```
Install requirements:
```bash
cd MAVIDS
pip install -r requirements.txt
```
Make migrations and migrate:
```bash
python manage.py makemigrations
python manage.py migrate
```
Run the webserver:
```bash
python manage.py runserver
```
Once the webserver is running, you can create an administrative user:
```bash
python manage.py createsuperuser
```
A dashboard user can now be created in the Django backend: *http://127.0.0.1:8000/admin/login*

### Training and tuning

Explain how to get logs for training

### Credits

This project was developed by: [@jasonotu](https://github.com/jasonotu), [@ThaniSangarapillai](https://github.com/ThaniSangarapillai), [@OmarMinawi3](https://github.com/OmarMinawi3)

The [PX4 Autopilot](https://px4.io/) was used for testing along with a number of tools from the PX4 project such as Gazebo plugins and ULog scripts.

The intrusion detection method is based on the following paper:

> Whelan, J., Sangarapillai, T., Minawi, O., Almehmadi, A., & El-Khatib, K. (2020, November). Novelty-based Intrusion Detection of Sensor Attacks on Unmanned Aerial Vehicles. In Proceedings of the 16th ACM Symposium on QoS and Security for Wireless and Mobile Networks (pp. 23-28).
