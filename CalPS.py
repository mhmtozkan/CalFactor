import visa
import time
import math
from RsInstrument.RsInstrument import RsInstrument

a=visa.ResourceManager()
print(a.list_resources())
Rohde=a.get_instrument('USB::0x0aad::0x0018::130589::INSTR')
Fluke=a.get_instrument('GPIB0::18::INSTR')
b=Fluke.query('*IDN?')
c=Rohde.query('*IDN?')
print(b)
print(c)
Fluke.write("INST SINE")
Fluke.write("UNIT:POWer DBM")
Fluke.write("POWER -12.2")
Fluke.write("FREQ 3.9E6")
Fluke.write("*OPC?")
Fluke.read()

Fluke.write("OUTPUT ON")

i: str = "3.9e6"

Rohde.write("*RST") # Reset the instrument, clear the Error queue
Rohde.write("INIT:CONT OFF") # Switch OFF the continuous sweep
# -----------------------------------------------------------
# Basic Settings:
# -----------------------------------------------------------
Rohde.write('INIT:CONT OFF')
Rohde.write('SENS:FUNC \"POW:AVG\"')
Rohde.write("SENS:FREQ 3.9e6")
Rohde.write('SENS:AVER:COUNT:AUTO OFF')
Rohde.write('SENS:AVER:COUN 256')
Rohde.write('SENS:AVER:STAT ON')
Rohde.write('SENS:AVER:TCON REP')
Rohde.write('SENS:POW:AVG:APER 5e-3')
# -----------------------------------------------------------
# SyncPoint 'SettingsApplied' - all the settings were applied
# -----------------------------------------------------------
Rohde.write("INIT:IMM")  # Start the sweep
# -----------------------------------------------------------
# Fetching the results, format does not matter, the driver function always parses it correctly
# -----------------------------------------------------------
Rohde.write('FORMAT ASCII')
results = Rohde.query('FETCH?').split(',')
power_watt = float(results[0])
if power_watt < 0:
	power_watt = 1E-12
power_dbm = 10 * math.log10(power_watt / 1E-3)
print(f'Measured power: {power_watt} Watt, {power_dbm:.3f} dBm')


def startmeasurement(self):
    a = visa.ResourceManager()
    ResourceTupple = a.list_resources()
    ResorceStringList = []
    instrumentname = ''
    for i in ResourceTupple:
        ResorceStringList.append(i)
    for i in ResorceStringList:
        if i.startswith('USB'):
            instrumentname = i

    PowerSensor = a.get_instrument(instrumentname)
    Fluke = a.get_instrument('GPIB0::18::INSTR')
    freqlist = ["110E6", "120E6", "310E6", "330E6", "960E6", "1100E6", "1250E6", "2700E6", "2900E6", "4000E6"]

    # initializing the RF reference source
    Fluke.write("INST SINE")
    Fluke.write("UNIT:POWer W")
    Fluke.write("POWER 0.0001")
    Fluke.write("OUTPUT ON")
    # initializing the Power Sensor
    PowerSensor.write('SENS:FUNC \"POW:AVG\"')
    PowerSensor.write('SENS:AVER:COUNT:AUTO OFF')
    PowerSensor.write('SENS:AVER:COUN 1024')
    PowerSensor.write('SENS:AVER:STAT ON')
    PowerSensor.write('SENS:AVER:TCON REP')
    PowerSensor.write('SENS:POW:AVG:APER 5e-3')
    measurementlist = []

    for freq in freqlist:
        Fluke.write("FREQ " + freq + "")
        Fluke.write("OUTPUT ON")
        time.sleep(2)
        PowerSensor.write('SENS:FREQ ' + freq)
        PowerSensor.write('INIT:CONT OFF')
        time.sleep(3)
        Fluke.write("OUTPUT OFF")
        time.sleep(2)

    print(measurementlist)

