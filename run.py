import sys
import subprocess

os_name = sys.platform

subprocess.call(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'])
# Update the repository
subprocess.call(['git', 'pull'])

#run main program
subprocess.call(['python', 'main.py'])
