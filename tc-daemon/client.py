import requests
import subprocess
import time
import signal

r = requests.get("http://localhost:5000/iface/enp6s0")
if r.status_code == requests.codes.ok:
    val = r.json()
    print(val["iface"])

cmd_list = ["./qperf/build/qperf", "-s", "--cc", "cubic", "-t", "10"]
# p = subprocess.run(["./qperf/build/qperf", "-s", "-t", "10"], capture_output=True)
f = open("server.txt", "w")
server_process = subprocess.Popen(cmd_list, stdout=f, stderr=f)

print("Wait 2s...")
time.sleep(2)
print("2s passed.")

cmd_list = ["./qperf/build/qperf", "-c", "localhost", "--cc", "cubic", "-t", "10"]
# p = subprocess.run(["./qperf/build/qperf", "-s", "-t", "10"], capture_output=True)
f = open("client.txt", "w")
client_process = subprocess.Popen(cmd_list, stdout=f, stderr=f)

print("Wait 2s...")
time.sleep(20)
print("2s passed.")

try:
    # Send CTRL+c to kill the child process from su -
    # std_out, _ = p.communicate()
    # print(std_out.decode("utf-8").splitlines())
    server_process.send_signal(signal.SIGINT)
    print("CTRL+c killed the process")
except subprocess.TimeoutExpired:
    print("Timeout occured")


server_process.kill()
