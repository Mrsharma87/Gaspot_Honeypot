#######################################################################
# gaspot.py
#
# This is a 'honeypot' to record any commands that were provided to the
# system. This will record the connection, and if any attempts are made.
# This is a basic attempt, with lots of room for improvement.
#
# 03/24/21 - Changed to Python3 (finally)
#
#   Authors: Kyle Wilhoit
#            Stephen Hilt
#
########################################################################

import socket
import select
import datetime
import random
import configparser
import ast
import argparse
import os
import sys

# Argument parsing only takes care of a configuration file to be specified
parser = argparse.ArgumentParser()
parser.add_argument('--config', help='specify a configuration file to be read', required=False)
parser.add_argument('--log', help='specify a path to log to', required=False, default='all_attempts.log')
parser.add_argument('--quiet', help='be quiet; log only to the logfile and not STDOUT', dest='quiet', action='store_true')
parser.set_defaults(quiet=False)
args = parser.parse_args()

# Determine the configuration file to use
configuration_file = args.config if args.config else 'config.ini'

# Check if the configuration file actually exists; exit if not.
if not os.path.isfile(configuration_file):
    print('Please specify a configuration file or rename config.ini.dist to config.ini!')
    sys.exit(1)

# Reading configuration information
config = configparser.ConfigParser()
config.read(configuration_file)

# Set vars for connection information
TCP_IP = config.get('host', 'tcp_ip')
TCP_PORT = config.getint('host', 'tcp_port')
BUFFER_SIZE = config.get('host', 'buffer_size')
NOW = datetime.datetime.utcnow()
FILLSTART = NOW - datetime.timedelta(minutes=313)
FILLSTOP = NOW - datetime.timedelta(minutes=303)

# Get the localized decimal separator
DS = config.get('parameters', 'decimal_separator')

# Default Product names, changed based on config.ini file
PRODUCT1 = config.get('products', 'product1').ljust(22)
PRODUCT2 = config.get('products', 'product2').ljust(22)
PRODUCT3 = config.get('products', 'product3').ljust(22)
PRODUCT4 = config.get('products', 'product4').ljust(22)

# Create random Numbers for the volumes
min_vol = config.getint('parameters', 'min_vol')
max_vol = config.getint('parameters', 'max_vol')
Vol1 = random.randint(min_vol, max_vol)
vol1tc = random.randint(Vol1, Vol1+200)
Vol2 = random.randint(min_vol, max_vol)
vol2tc = random.randint(Vol2, Vol2+200)
Vol3 = random.randint(min_vol, max_vol)
vol3tc = random.randint(Vol3, Vol3+200)
Vol4 = random.randint(min_vol, max_vol)
vol4tc = random.randint(Vol4, Vol4+200)

# unfilled space ULLAGE
min_ullage = config.getint('parameters', 'min_ullage')
max_ullage = config.getint('parameters', 'max_ullage')
ullage1 = str(random.randint(min_ullage, max_ullage))
ullage2 = str(random.randint(min_ullage, max_ullage))
ullage3 = str(random.randint(min_ullage, max_ullage))
ullage4 = str(random.randint(min_ullage, max_ullage))

# Height of tank
min_height = config.getint('parameters', 'min_height')
max_height = config.getint('parameters', 'max_height')
height1 = str(random.randint(min_height, max_height)) + DS + str(random.randint(10, 99))
height2 = str(random.randint(min_height, max_height)) + DS + str(random.randint(10, 99))
height3 = str(random.randint(min_height, max_height)) + DS + str(random.randint(10, 99))
height4 = str(random.randint(min_height, max_height)) + DS + str(random.randint(10, 99))

# Water in tank, this is a variable that needs to be low
min_h2o = config.getint('parameters', 'min_h2o')
max_h2o = config.getint('parameters', 'max_h2o')
h2o1 = str(random.randint(min_h2o, max_h2o)) + DS + str(random.randint(10, 99))
h2o2 = str(random.randint(min_h2o, max_h2o)) + DS + str(random.randint(10, 99))
h2o3 = str(random.randint(min_h2o, max_h2o)) + DS + str(random.randint(10, 99))
h2o4 = str(random.randint(min_h2o, max_h2o)) + DS + str(random.randint(10, 99))

# Temperature of the tank
low_temp = config.getint('parameters', 'low_temperature')
high_temp = config.getint('parameters', 'high_temperature')
temp1 = str(random.randint(low_temp, high_temp)) + DS + str(random.randint(10, 99))
temp2 = str(random.randint(low_temp, high_temp)) + DS + str(random.randint(10, 99))
temp3 = str(random.randint(low_temp, high_temp)) + DS + str(random.randint(10, 99))
temp4 = str(random.randint(low_temp, high_temp)) + DS + str(random.randint(10, 99))

# List for station name from config
station_name = ast.literal_eval(config.get("stations", "list"))
slength = len(station_name)
station = station_name[random.randint(0, slength-1)]

def I20100():
    I20100_1 = '''
I20100
'''
    I20100_2 = '''

    ''' + station + '''

IN-TANK INVENTORY

TANK PRODUCT             VOLUME TC VOLUME   ULLAGE   HEIGHT    WATER     TEMP
  1  '''+ PRODUCT1 + '''''' + str(Vol1) + '''      '''+ str(vol1tc) +'''     '''+ ullage1 +'''    '''+ height1 +'''     '''+ h2o1 +'''    '''+ temp1 +'''
  2  '''+ PRODUCT2 + '''''' + str(Vol2) + '''      '''+ str(vol2tc) +'''     '''+ ullage2 +'''    '''+ height2 +'''     '''+ h2o2 +'''    '''+ temp2 +'''
  3  '''+ PRODUCT3 + '''''' + str(Vol3) + '''      '''+ str(vol3tc) +'''     '''+ ullage3 +'''    '''+ height3 +'''     '''+ h2o3 +'''    '''+ temp3 +'''
  4  '''+ PRODUCT4 + '''''' + str(Vol4) + '''      '''+ str(vol4tc) +'''     '''+ ullage4 +'''    '''+ height4 +'''     '''+ h2o4 +'''    '''+ temp4 +'''
'''
    return I20100_1 + str(NOW.strftime('%m/%d/%Y %H:%M')) + I20100_2

def I20200():
    I20200_1 = '''
I20200
'''
    I20200_2 = '''

''' + station + '''

DELIVERY REPORT

T 1:'''+ PRODUCT1 +'''
INCREASE   DATE / TIME             GALLONS TC GALLONS WATER  TEMP DEG F  HEIGHT

      END: '''+ str(FILLSTOP.strftime('%m/%d/%Y %H:%M')) +'''         '''+ str(Vol1 + 300) +'''       '''+ str(vol1tc + 300) +'''   '''+ h2o1 +'''      '''+ temp1 +'''   '''+ height1 +'''
    START: '''+ str(FILLSTART.strftime('%m/%d/%Y %H:%M')) +'''         '''+ str(Vol1 - 300) +'''       '''+ str(vol1tc - 300) +'''   '''+ h2o1 +'''      '''+ temp1 +'''   '''+ str(float(height1) - 23) +'''
   AMOUNT:                          '''+ str(Vol1)+'''       '''+ str(vol1tc) +'''

'''
    return I20200_1 + str(NOW.strftime('%m/%d/%Y %H:%M')) + I20200_2

def I20300():
    I20300_1 = '''
I20300
'''
    I20300_2 = '''

''' + station + '''

TANK 1    '''+ PRODUCT1 +'''
    TEST STATUS: OFF
LEAK DATA NOT AVAILABLE ON THIS TANK

TANK 2    '''+ PRODUCT2 +'''
    TEST STATUS: OFF
LEAK DATA NOT AVAILABLE ON THIS TANK

TANK 3    '''+ PRODUCT3 +'''
    TEST STATUS: OFF
LEAK DATA NOT AVAILABLE ON THIS TANK

TANK 4    '''+ PRODUCT4 +'''
    TEST STATUS: OFF
LEAK DATA NOT AVAILABLE ON THIS TANK
'''
    return I20300_1 + str(NOW.strftime('%m/%d/%Y %H:%M')) + I20300_2

def I20400():
    I20400_1 = '''
I20400
'''
    I20400_2 = '''

''' + station + '''

 SHIFT REPORT

SHIFT 1 TIME: 12:00 AM

TANK PRODUCT

  1  '''+ PRODUCT1 +'''                  VOLUME TC VOLUME  ULLAGE  HEIGHT  WATER   TEMP
SHIFT  1 STARTING VALUES      ''' + str(Vol1) +'''     '''+ str(vol1tc) +'''    '''+ ullage1 +'''   '''+ height1 +'''   '''+ h2o1 +'''    '''+ temp1 +'''
         ENDING VALUES        ''' + str(Vol1 + 940) +'''     '''+ str(vol1tc + 886) +'''    '''+ str(int(ullage1) + 345) +'''   '''+ str(float(height1) + 53)+'''  '''+ h2o1 +'''    '''+ temp1 +'''
         DELIVERY VALUE          0
         TOTALS                940

'''
    return I20400_1 + str(NOW.strftime('%m/%d/%Y %H:%M')) + I20400_2

def I20500():
    I20500_1 = '''
I20500
'''
    I20500_2 = '''

''' + station + '''

TANK   PRODUCT                 STATUS

  1    '''+ PRODUCT1 +'''                   NORMAL

  2    '''+ PRODUCT2 +'''                  HIGH WATER ALARM
                               HIGH WATER WARNING

  3    '''+ PRODUCT3 +'''                  NORMAL

  4    '''+ PRODUCT4 +'''                 NORMAL
'''
    return I20500_1 + str(NOW.strftime('%m/%d/%Y %H:%M')) + I20500_2

def log(mesg, destinations):
    now = datetime.datetime.utcnow()
    prefix = now.strftime('%m/%d/%Y %H:%M') + ': '
    for destination in destinations:
        destination.write(prefix + mesg)
        destination.flush()

log_destinations = [open(args.log, 'a')]
if not args.quiet:
    log_destinations.append(sys.stdout)

# create the socket, bind, and start listening for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setblocking(0)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(10)

active_sockets = [server_socket]
while True:
    readable, writeable, errored = select.select(active_sockets, [], [], 5)
    for conn in readable:
        if conn is server_socket:
            new_con, addr = server_socket.accept()
            new_con.settimeout(30.0)
            active_sockets.append(new_con)
        else:
            try:
                addr = conn.getpeername()
                TIME = datetime.datetime.utcnow()
                log("Connection from : %s\n" % addr[0], log_destinations)
                
                response = conn.recv(4096)
                if not response:
                    active_sockets.remove(conn)
                    conn.close()
                    continue
                
                while not (b'\n' in response or b'00' in response):
                    response += conn.recv(4096)
                
                # Handle both ^A and \x01 prefixes, as well as raw commands
                cmd = None
                if response.startswith(b'^A'):
                    cmd = response[2:8].decode(errors='replace').strip()
                elif response.startswith(b'\x01'):
                    cmd = response[1:7].decode(errors='replace').strip()
                else:
                    # Try to extract command directly
                    try:
                        cmd = response.decode(errors='replace').strip()[:6]
                    except:
                        cmd = None
                
                if not cmd:
                    log("Invalid Command Attempt from: %s\n" % addr[0], log_destinations)
                    conn.close()
                    active_sockets.remove(conn)
                    continue

                cmds = {
                    "I20100": I20100,
                    "I20200": I20200,
                    "I20300": I20300,
                    "I20400": I20400,
                    "I20500": I20500
                }

                if cmd in cmds:
                    log("Handling %s Command Attempt from: %s\n" % (cmd, addr[0]), log_destinations)
                    response = cmds[cmd]()
                    conn.send(response.encode(errors='replace'))
                elif cmd.startswith("S6020"):
                    # Handle tank name changes
                    if cmd.startswith("S60201"):
                        TEMP = response.split('S60201'.encode(errors='replace'))
                        if len(TEMP) < 2:
                            conn.send("9999FF1B\n".encode(errors='replace'))
                        else:
                            TEMP1 = TEMP[1].rstrip(b"\r\n").decode(errors='replace')
                            if len(TEMP1) < 22:
                                PRODUCT1 = TEMP1.ljust(22)
                            elif len(TEMP1) > 22:
                                PRODUCT1 = TEMP1[:20] + "  "
                            else:
                                PRODUCT1 = TEMP1
                        log("S60201: "+ TEMP1 +" Command Attempt from: %s\n" % addr[0], log_destinations)
                    # Similar handlers for S60202, S60203, S60204...
                else:
                    conn.send("9999FF1B\n".encode(errors='replace'))
                    log("Unknown Command Attempt from: %s - Command: %s\n" % (addr[0], cmd), log_destinations)
                
            except OSError as OSerr:
                print("Error in OS Call: {}".format(str(OSerr)))
                active_sockets.remove(conn)
                conn.close()
                continue
            except Exception as e:
                print('Unknown Error: {}'.format(str(e)))
                raise
            except KeyboardInterrupt:
                conn.close()
            except select.error:
                conn.close()
                for log in log_destinations:
                    log.close()
