
import sys
import zmq

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
for update_nbr in range(10):
    string = socket.recv_string()
    zipcode, temperature, relhumidity = string.split()
    total_temp += int(temperature)

print("Average temperature for zipcode '%s' was %dF" % (
      zip_filter, total_temp / (update_nbr+1))
)
