import minimalmodbus
import time
import enum
import time

CASSETTE_LOGS_CHUNK_SIZE = 10
CASSETTE_LOGS_NUM_CHUNKS = 12
CASSETTE_MAX_TEMPERATURE = 50
CASSETTE_MIN_TEMPERATURE = 10
CASSETTE_MAX_VOLTAGE = 50
CASSETTE_MIN_VOLTAGE = 46

class CASSETTE_STATE(enum.IntEnum):
    POWERUP = 0
    MISSION_READY = 1
    LOAD_DESCENDING = 2
    DRONE_ASCENDING = 3


class CASSETTE_MODBUS_REGISTERS(enum.IntEnum):
    FIRMWARE_VERSION = 1
    DEVICE_ID_UPPER = 2
    DEVICE_ID_LOWER = 3
    SYSTEM_CONTROL = 4
    BATTERY_VOLTAGE = 5
    THERMISTOR_TEMPERATURE = 6
    CRITICAL_TIMEOUT = 7
    MODBUS_ERRORS = 8
    LOGS_PAGE_SELECT = 9
    LOGS_START_BRAKE_ENGAGEMENT = 10
    LOGS_START_MICROS_UPPER = LOGS_START_BRAKE_ENGAGEMENT + CASSETTE_LOGS_CHUNK_SIZE
    LOGS_START_MICROS_LOWER = LOGS_START_MICROS_UPPER + CASSETTE_LOGS_CHUNK_SIZE


class CASSETTE_MODBUS_STATUS_REGISTER(enum.IntEnum):
    SYSTEM_STATE_LOWER = 0
    SYSTEM_STATE_UPPER = 1
    COMMAND_START_MISSION = 4
    COMMAND_END_MISSION = 5
    COMMAND_OVERWRITE_ID = 6
    COMMAND_TRIGGER_RAPID_CUTTING = 7
    ERROR_INTERRUPT_TIMED_OUT = 8
    ERROR_LOGS_OVERFLOWED = 9
    ERROR_ADC121_UNRESPONSIVE = 10
    ERROR_THERMISTOR_UNRESPONSIVE = 11


class HEATER_STATE(enum.IntEnum):
    POWERUP = 0
    DISABLED = 1
    MONITORING = 2
    HEATING = 3


class HEATER_MODBUS_REGISTERS(enum.IntEnum):
    FIRMWARE_VERSION = 1
    DEVICE_ID_UPPER = 2
    DEVICE_ID_LOWER = 3
    SYSTEM_CONTROL = 4
    TEMPERATURE_TARGET_LOWER = 5
    TEMPERATURE_TARGET_UPPER = 6
    TEMPERATURE1 = 7
    TEMPERATURE2 = 8
    CRITICAL_TEMPERATURE = 9
    MODBUS_ERRORS = 10


class HEATER_STATUS_REGISTER(enum.IntEnum):
    SYSTEM_STATE_LOWER = 0
    SYSTEM_STATE_UPPER = 1
    COMMAND_OVERWRITE_ID = 4
    ERROR_TEMPERATURE_1_UNKNOWN = 8
    ERROR_TEMPERATURE_2_UNKNOWN = 9
    ERROR_HARDWARE_CONFIG = 10


cassette = minimalmodbus.Instrument('COM48', 1)  # port name, slave address (in decimal)
cassette.serial.baudrate = 76800         # Baud

heater = minimalmodbus.Instrument('COM48', 2)  # port name, slave address (in decimal)
heater.serial.baudrate = 76800         # Baud


global last_cassette_status
global last_heater_status

last_cassette_status = 0
last_heater_status = 0

def print_status():

    global last_cassette_status
    global last_heater_status

    try:
        system_control_bits = cassette.read_register(CASSETTE_MODBUS_REGISTERS.SYSTEM_CONTROL)
        temperature = cassette.read_register(CASSETTE_MODBUS_REGISTERS.THERMISTOR_TEMPERATURE, number_of_decimals=2)
        voltage = cassette.read_register(CASSETTE_MODBUS_REGISTERS.BATTERY_VOLTAGE)
        errors = cassette.read_register(CASSETTE_MODBUS_REGISTERS.MODBUS_ERRORS)
        t1 = heater.read_register(HEATER_MODBUS_REGISTERS.TEMPERATURE1, number_of_decimals=2)
        t2 = heater.read_register(HEATER_MODBUS_REGISTERS.TEMPERATURE2, number_of_decimals=2)
        comms_errors = heater.read_register(HEATER_MODBUS_REGISTERS.MODBUS_ERRORS)
        __status = 0b0000000000000011 & system_control_bits
        
        print(temperature)
        print(errors)
        
        if __status is not last_cassette_status:
            print(CASSETTE_STATE(__status))

        last_cassette_status = __status

        # system_control_bits = heater.read_register(HEATER_MODBUS_REGISTERS.SYSTEM_CONTROL)
        # __status = 0b0000000000000011 & system_control_bits

        # if __status is not last_heater_status:
        #     print(HEATER_STATE(__status))

        # last_heater_status = __status

    except IOError:

        print("Failed!")

# instrument.write_register(5, 2600)
# instrument.write_register(6, 2700)


print_status()

# instrument.write_register(5, 0)
# instrument.write_register(6, 2600)

# system_control_bits = instrument.read_register(4)
# new_control_bits = system_control_bits
# new_control_bits |= (0x01 << 4)
# instrument.write_register(4, new_control_bits)

# print_status()

# time.sleep(3)

# system_control_bits = instrument.read_register(4)
# new_control_bits = system_control_bits
# new_control_bits |= (0x01 << 5)
# # print("{:03b}".format(system_control_bits))
# # print("NEW=")
# # print("{:03b}".format(new_control_bits))
# instrument.write_register(4, new_control_bits)
# # print('--')
# # time.sleep(2)

# system_control_bits = cassette.read_register(4)
# new_control_bits = system_control_bits
# new_control_bits |= (0x01 << 4)
# cassette.write_register(4, new_control_bits)

while True:




    # temperature = instrument.read_register(7, signed=True)  # Registernumber, number of decimals
    # print(temperature)
    start_time = time.time() # start time of the loop
    print_status()
    # time.sleep(0.5)
    print("FPS: ", 1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop

    #instrument.read_register(1)  # Registernumber, number of decimals
    #print(temperature)