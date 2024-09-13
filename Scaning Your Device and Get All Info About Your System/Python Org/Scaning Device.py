import platform
import json
import psutil
import socket
import uuid
import os

# جمع معلومات النظام
system_info = {
    "system": platform.system(),
    "node_name": platform.node(),
    "release": platform.release(),
    "version": platform.version(),
    "machine": platform.machine(),
    "processor": platform.processor(),
    "cpu_count": psutil.cpu_count(logical=True),
    "memory": psutil.virtual_memory().total,
    "disk": psutil.disk_usage('/').total,
    "ip_address": socket.gethostbyname(socket.gethostname()),
    "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1]),
    "boot_time": psutil.boot_time(),
    "cpu_usage": psutil.cpu_percent(interval=1),
    "memory_usage": psutil.virtual_memory().percent,
    "disk_usage": psutil.disk_usage('/').percent,
    "hostname": socket.gethostname(),
    "platform": platform.platform(),
    "architecture": platform.architecture(),
    "python_version": platform.python_version(),
    "user": os.getlogin(),
    "network_interfaces": psutil.net_if_addrs(),
    "network_connections": psutil.net_connections(),
    "sensors_temperatures": psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else "Not available",
    "sensors_fans": psutil.sensors_fans() if hasattr(psutil, "sensors_fans") else "Not available",
    "sensors_battery": psutil.sensors_battery() if hasattr(psutil, "sensors_battery") else "Not available"
}

# حفظ المعلومات في ملف JSON
with open('system_info.json', 'w') as json_file:
    json.dump(system_info, json_file, indent=4)

print("\nتم حفظ معلومات النظام في ملف system_info.json\n")



# Get system information
# Developer ~~::~~ Mohammed Alaa Mohammed