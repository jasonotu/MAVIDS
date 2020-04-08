import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__)) + "\..\..\libraries")
print(sys.path)

from pymavlink_custom import mavutil

os.environ['MAVLINK20'] = "1"
mavutil.set_dialect("MAVIDS")

def establish_connection():
    uav_link = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

    return uav_link

def listen_link(uav_link):
    try:
        print(master.recv_match(type=["HEARTBEAT", "MAVIDS"]).to_dict())
    except:
        pass
