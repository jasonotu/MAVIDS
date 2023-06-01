# MAVIDS

*This project was a PoC and is not actively being worked on. It now requires some TLC to become fully operational*

The Micro Air Vehicle Intrusion Detection System (MAVIDS)  is a machine learning-based IDS for UAVs that use the MAVLink communication protocol.

[TOC]

### Installation

MAVIDS is only supported on linux using Python 3.7.

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
python manage.py makemigrations gcsclient
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

The [PX4 Autopilot](https://px4.io/) was used for testing along with a number of tools from the PX4 project such as Gazebo plugins and ULog scripts.
