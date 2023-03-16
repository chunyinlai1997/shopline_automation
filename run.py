import sys
import subprocess

os_name = sys.platform

if os_name == 'win32':
    subprocess.call(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'])
elif os_name == 'darwin':
    subprocess.call(['python3', '-m', 'pip', 'install', '-r', 'requirements.txt'])
else:
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
# Update the repository
subprocess.call(['git', 'pull'])

#run main program
if os_name == 'win32':
    subprocess.call(['python', '-m', 'main.py'])
elif os_name == 'darwin':
    subprocess.call(['python3', 'main.py'])
else:
    subprocess.call(['python', 'main.py'])
