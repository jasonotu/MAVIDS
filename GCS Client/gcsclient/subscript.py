import sys, os, time
#from ....libraries import pymavlink
#
# sys.path.append(os.path.join(os.path.dirname(__file__)) + "\..\..\libraries")
# print(sys.path)
from pymavlink import mavutil
import requests
#from pymavlink import mavutil

os.environ['MAVLINK20'] = "1"
mavutil.set_dialect("common")


"""
MAVIDS:
time_usec: timestamp, either from system boot, or Epoch time.
target_system: if 0, surface agent sent the msg, if 1, UAV agent sent the message
message_mode: bitmap of info contained within [1,1,1,0,0,0,0,0] settings, attack, response
# ----------------------Alert Specific: message_mode[2] must be 1 -------------------------------
# ignore_alert: flag indicating whether to ignore alert
----------------------Alert Specific: message_mode[1] must be 1--------------------------------
alert_id: The alert ID
attack_name: 3 character id representing the attack 
attack_score: float representing attack score
----------------------Setting Specific: message_mode[0] must be 1------------------------------
default_action: default mitigation action when attack is detected
default_initiate_time: time until default mitigation action is initiated
default_return_time: time until return to previous flight mode
modules_enabled: bitmap of attack modules enabled. [GPS, DOS, .....]
"""

#@background()

#@background(schedule=0)
# def establish_connection():
#     global uav_link, heartbeat_timeout, connection_status, established, counter
#     #uav_link = mavutil.mavlink_connection('udp:127.0.0.1:14550')
#     uav_link = mavutil.mavlink_connection('udpin:0.0.0.0:14551')
#
#     # Send a ping to start connection and wait for any reply.
#     # wait_conn(master)
#     # uav_link.wait_heartbeat()
#     # print("Heartbeat from system (system %u component %u)")
#     print("establishing Connection....")
#     established = True
#     return uav_link


"""
runs as a background task on startup. have to issue the python manage.py process_tasks command for it to work
If three heartbeats are missed, the "connection_status" global var is set to false.
"""
def main():
    pending_data = {}
    established = False
    serv_conn = False
    serv_conn_counter = 3
    counter = 3
    mav = mavutil.mavlink_connection('/dev/ttyTHS1', baud=57600, source_system=11)
    
    while True:
        try:
            messages = mav.recv_match(blocking=False, type=['HEARTBEAT', 'MAVIDS'])
            if (not messages and established):
                counter -= 1
            elif messages:
                print(messages.get_srcSystem())
                if messages.get_type() == 'HEARTBEAT' and int(messages.get_srcSystem()) == 10:
                    established = True
                    counter = 3
                    print(messages)
                elif int(messages.get_srcSystem()) == 1:
                    continue
                else:
                    counter -= 1
            else:
                counter -= 1


            if counter < 0:
                established = False

            try:
                serv_resp = requests.get('http://127.0.0.1:8000/heartbeat/', json={
                    'established': established
                }, timeout=1)
                
                if serv_resp.status_code == 200:
                    data = serv_resp.json()
                    del data['timestamp']
                    if pending_data != data:
                        pending_data = data
                        print(pending_data)
                    serv_conn = True
                else:
                    serv_conn_counter -= 1

            except:
                serv_conn = False
                serv_conn_counter -= 1

            if established:
                send_message(mav)

            if serv_conn_counter <= 0:
                return

            #except Exception as e:
            #   print(e)
            #   established = False
                # if heartbeat_timeout == 0 and connection_status:
                #     print("Connection lost!")
                #     connection_status = False
                # else:
                #     heartbeat_timeout -= 1
                # uav_link = mavutil.mavlink_connection('udpin:0.0.0.0:14551')
            time.sleep(1)
        except:
            mav = mavutil.mavlink_connection('/dev/ttyTHS1', baud=57600, source_system=11)


def parse_mavids(message):
    print("sending", time.time())
    if message.target_system == 1:
        if message.message_mode[1] == 1:
            attack_dict = {"time_usec":message.time_usec, "alert_id":message.alert_id, "attack_name":message.attack_name, "attack_score":message.attack_score}
            return attack_dict
        else:
            pass
    else:
        return None
    pass


def settings_change():
    global uav_link
    setting = Settings.objects.first()
    print("sending")
    modules = ""
    modules += str(int(setting.dos_enabled))
    modules += str(int(setting.gps_enabled))
    modules += "000000"
    uav_link.mav.mavids_send(int(time.time()), int(0), int('10000000', 2), int(0), b'NAN', float(0), setting.default_action.encode(), int(setting.default_initiate_time), int(setting.default_return_time),
                             int(modules, 2))

"""
function to send message to UAV, indicating to ignore alert.
"""
def ignore_alert():
    global uav_link
    print("sending")
    uav_link.mav.mavids_send(int(time.time()), int(0), int('00100000', 2), int(0), b'NAN', float(0), b'AAAAAA', int(0), int(0),
                             int('00000000', 2))


"""
function to test sending of messages. Sends a heartbeat along with a MAVIDS message.
"""
def send_message(mav):
    print("sending", time.time())
    mav.mav.heartbeat_send(type=2, autopilot=12, base_mode=81, custom_mode=65536, system_status=3,
                                mavlink_version=3)
    #uav_link.mav.heartbeat_send(type=6, autopilot=8, base_mode=192, custom_mode=0, system_status=4, mavlink_version=3)
    # uav_link.mav.mavids_send(int(time.time()), int(0), int('10000000', 2), int(0), b'NAN', float(0), b'AAAAAA', int(1),
    #                          int(1), int('11000000', 2))
    # print("hello")
    #listen_link()


main()