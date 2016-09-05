import subprocess, sys

connect_to_server(); # Assumed to exist.

proc = subprocess.Popen(sys.argv[1], stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

while True:
    s = get_string() # Assume to exist.
    if s.split(' ')[0] == "Result:":
        print(s)
        break
    proc.communicate(s)
