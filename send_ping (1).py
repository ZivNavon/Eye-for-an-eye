import subprocess
import re
import pickle

def ping_address_from_pickle(pickle_obj):
    try:
        ip_dict = pickle.loads(pickle_obj)
    except pickle.UnpicklingError:
        return "Invalid pickle object"

    if "command" in ip_dict and "ip_address" in ip_dict:
        command = ip_dict["command"]
        if command != "ping":
            return "Invalid command - only ping allowed"
        
        ip_address = ip_dict["ip_address"]
        ip_pattern = re.compile(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        
        if ip_pattern.match(ip_address):
            try:
                # Execute ping command
                result = subprocess.run([command, '-c', '4', ip_address], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return "Ping successful", result.stdout
                else:
                    return "Ping failed", result.stdout
            except subprocess.TimeoutExpired:
                return "Ping timed out"
        else:
            return "Invalid IP address"
    else:
        return "Invalid dictionary"
