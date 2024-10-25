from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.182"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show interface", use_textfsm=True)
        for status in result:
            if status["interface"].startswith('G'):
                ans += " "+status["interface"]
                if status["link_status"] == "up":
                    up += 1
                    ans += " "+status["link_status"]
                elif status["link_status"] == "down":
                    down += 1
                    ans += " "+status["link_status"]
                elif status["link_status"] == "administratively down":
                    admin_down += 1
                    ans += " "+status["link_status"]
        ans += f"-> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans


