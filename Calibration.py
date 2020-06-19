from RsInstrument.RsInstrument import RsInstrument
import time
import math

instr = None
try:
	# -----------------------------------------------------------
	# Initialization:
	# -----------------------------------------------------------
	# Adjust the VISA Resource string to fit your instrument
	nrpz = RsInstrument('USB::0x0aad::0x0018::130589::INSTR', True, False)
	# instr = RsInstrument('RSNRP::0x0095::104015::INSTR', True, False)
	nrpz.visa_timeout = 3000  # Timeout for VISA Read Operations
	nrpz.instrument_status_checking = True  # Error check after each command
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

print(f'Visa manufacturer: {nrpz.visa_manufacturer}')
print(f'Instrument Identification string: {nrpz.idn_string}')

nrpz.write_str("*RST") # Reset the instrument, clear the Error queue
nrpz.write_str("INIT:CONT OFF") # Switch OFF the continuous sweep
# -----------------------------------------------------------
# Basic Settings:
# -----------------------------------------------------------
nrpz.write_str('INIT:CONT OFF')
nrpz.write_str('SENS:FUNC \"POW:AVG\"')
nrpz.write_str('SENS:FREQ 1e9')
nrpz.write_str('SENS:AVER:COUNT:AUTO OFF')
nrpz.write_str('SENS:AVER:COUN 16')
nrpz.write_str('SENS:AVER:STAT ON')
nrpz.write_str('SENS:AVER:TCON REP')
nrpz.write_str('SENS:POW:AVG:APER 5e-3')
# -----------------------------------------------------------
# SyncPoint 'SettingsApplied' - all the settings were applied
# -----------------------------------------------------------
nrpz.write_str("INIT:IMM")  # Start the sweep

success = False
for x in range(0, 200):
	status = nrpz.query_int('STAT:OPER:COND?')
	if (status & 16) == 0:
		# Status register bit 4 signals MEASURING status
		# Finished measuring, break
		success = True
		break
	time.sleep(0.02)

if not success:
	raise TimeoutError("Measurement timed out")

# -----------------------------------------------------------
# Fetching the results, format does not matter, the driver function always parses it correctly
# -----------------------------------------------------------
nrpz.write_str('FORMAT ASCII')
results = nrpz.query_str('FETCH?').split(',')
power_watt = float(results[0])
if power_watt < 0:
	power_watt = 1E-12
power_dbm = 10 * math.log10(power_watt / 1E-3)
print(f'Measured power: {power_watt} Watt, {power_dbm:.3f} dBm')

# Close the session
nrpz.close()
