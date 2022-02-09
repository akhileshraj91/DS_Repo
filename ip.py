import os
import subprocess


# result = os.system("ip -4 addr show h1-eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'")
# result = os.system("ip -4 addr show enp4s0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'")
#
#
# print(result)


# output = subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
# output = subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)

# out_2 = subprocess.run(["ip -4 addr show enp4s0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'"], capture_output=True)
out_1 = subprocess.check_output("ifconfig", shell=True)
out_string = out_1.decode()
words_actual = out_string.split()
# print(words_actual)
res = words_actual.index("inet")
print(words_actual[res+1])
# out_2 = subprocess.check_output("ip -4 addr show h1-eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'", shell=True)
# print(out_2)
# print(out_2.decode())