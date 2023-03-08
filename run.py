import platform
import subprocess

# Get the operating system name
os_name = platform.system()

# Install dependencies
if os_name == 'Windows':
    subprocess.call(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'])
else:
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

# Update the repository
subprocess.call(['git', 'pull'])

#run main program
if os_name == 'Windows':
    subprocess.call(['python', '-m', 'main.py'])
else:
    subprocess.call(['python', 'main.py'])
