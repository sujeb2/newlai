import psutil

def getBattery():
    return psutil.sensors_battery() 

def getBattConnectStatus():
    batt = getBattery()
    return batt is not None and batt.power_plugged

def getBattPowerGauge():
    batt = getBattery()
    return None if batt is None else round(batt.percent)