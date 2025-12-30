import sys
import time
from pid.pid import PID

pid = PID(20, 0, 0, setpoint=10)

print(pid(5))