# client.py
from colorama import Fore, Back, Style
import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(Fore.GREEN + '\nsocket successfully created!'+ Style.RESET_ALL)
except socket.error as err:
    print(Fore.RED +'\nsocket creation failed with error'+Style.RESET_ALL+ f' {err}')

port = 80

try:
    host_ip = socket.gethostbyname('www.github.com')
except socket.gaierror:
    print(Fore.YELLOW+'Hostname could not be resolved.'+Style.RESET_ALL)
    sys.exit()
s.connect((host_ip, port))
print(Fore.GREEN + Style.BRIGHT +'\nSocket has successfully connect to Github on port =='+Style.RESET_ALL+ f' {host_ip}')