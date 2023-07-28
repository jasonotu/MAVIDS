# MAVIDS

*This project was a PoC and is not actively being worked on. It now requires some TLC to become fully operational.*

The Micro Air Vehicle Intrusion Detection System (MAVIDS)  is a machine learning-based IDS for UAVs that use the MAVLink communication protocol.

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

Pre-processing and training can be done using the Jupyter notebooks located in the *training* folder. For more information on how this is done, see related publications. Training data is also available on IEEE DataPort.

### Credits

The [PX4 Autopilot](https://px4.io/) was used for testing along with a number of tools from the PX4 project such as Gazebo plugins and ULog scripts.

### Publications

Whelan, Jason, et al. "[Novelty-based Intrusion Detection of Sensor Attacks on Unmanned Aerial Vehicles](https://dl.acm.org/doi/abs/10.1145/3416013.3426446)." Proceedings of the 16th ACM symposium on QoS and security for wireless and mobile networks. 2020.

Whelan, Jason P. MAVIDS: An Intelligent Intrusion Detection System for Autonomous Unmanned Aerial Vehicles. Diss. 2021.

Jason Whelan, Thanigajan Sangarapillai, Omar Minawi, Abdulaziz Almehmadi, Khalil El-Khatib, February 26, 2020, "UAV Attack Dataset", IEEE Dataport, doi: (https://dx.doi.org/10.21227/00dg-0d12).


