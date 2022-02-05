
import sys
import zmq
import socket


context = zmq.Context()

socket = context.socket(zmq.SUB)

srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
connect_str = "tcp://" + srv_addr + ":5556"

print("Collecting updates from weather server...")
socket.connect(connect_str)

zip_filter = sys.argv[2] if len(sys.argv) > 2 else "10001"

if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')


socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

total_temp = 0
temperature_publishers = {}
humidity_publishers = {}
for update_nbr in range(10):
    data = socket.recv_string()
    data_1, data_2, data_3, data_4 = data.split()
    # total_temp += int(temperature)
    if data_3 == "temperature":
        temperature_publishers[data_4] = data_4
    else:
        humidity_publishers[data_4] = data_4


print(temperature_publishers)
print(humidity_publishers)

# print("Average temperature for zipcode '%s' was %dF" % (
#       zip_filter, total_temp / (update_nbr+1))
# )
