# ltr303.py
from smbus2 import SMBus
import time




'''
From a gain test
Control Byte	CH0	CH1	Notes
0x41	3	3	Low gain baseline
0x45	7	6	Slightly higher gain
0x49	15	12	Medium gain
0x4D	29	25	High gain
0x59	160	142	Very high gain (~48×)
0x5D	332	301	Even higher (~96×)
0x79	299	142	Another very high gain reading
0x7D	623	295	Maximum gain reading

'''




class LTR303:
    I2C_ADDR         = 0x29
    REG_CONTROL      = 0x80
    REG_MEAS_RATE    = 0x85
    REG_DATA_CHAN1   = 0x88
    REG_DATA_CHAN0   = 0x8A
    REG_PART_ID      = 0x86

    # Gain fields for your board (3-bit field shifted left one)
    _GAIN_FIELDS = {
        1 : 0x0,   # 0x41
        2 : 0x2,   # 0x45
        4 : 0x4,   # 0x49
        8 : 0x6,   # 0x4D
        48: 0xC,   # 0x59
        96: 0xE    # 0x5D
    }

    # Integration times (again use values your board supports)
    _INT_TIME_CODES = {
        100: 0x00,
        150: 0x01,
        200: 0x02,
        250: 0x03,
        300: 0x04,
        350: 0x05,
        400: 0x06
    }

    def __init__(self, bus_num=1):
        self.bus = SMBus(bus_num)
        self.gain = 1
        self.integration_time = 100  # default
        self._gain_field = self._GAIN_FIELDS[self.gain]

    def begin(self, gain=1, integration_time=100, meas_rate=None):
        # Verify sensor
        pid = self.bus.read_byte_data(self.I2C_ADDR, self.REG_PART_ID)
        # optional: check if pid is expected

        self.set_gain(gain)
        self.set_integration_time(integration_time, meas_rate)
        return True

    def set_gain(self, gain):
        if gain not in self._GAIN_FIELDS:
            raise ValueError(f"Gain {gain}× not supported.")
        self.gain = gain
        self._gain_field = self._GAIN_FIELDS[gain]
        # Construct control byte: bit6=1 (active), bits[3:1] = gain_field, bit0=1
        control_val = 0x40 | (self._gain_field << 1) | 0x01
        self.bus.write_byte_data(self.I2C_ADDR, self.REG_CONTROL, control_val)
        time.sleep(0.05)

    def set_integration_time(self, integration_time, meas_rate=None):
        if integration_time not in self._INT_TIME_CODES:
            raise ValueError(f"Integration time {integration_time}ms not supported.")
        self.integration_time = integration_time
        code = self._INT_TIME_CODES[integration_time]
        if meas_rate is None:
            # If you want meas_rate same as integration, maybe use code
            meas_rate_code = code
        else:
            # map meas_rate to code if supported
            meas_rate_code = code  # placeholder; adjust if you have mapping
        val = (meas_rate_code << 3) | code
        self.bus.write_byte_data(self.I2C_ADDR, self.REG_MEAS_RATE, val)
        time.sleep(0.01)

    def read_raw(self):
        # Wait for integration to complete
        time.sleep(self.integration_time / 1000.0 + 0.01)
        lsb1 = self.bus.read_byte_data(self.I2C_ADDR, self.REG_DATA_CHAN1)
        msb1 = self.bus.read_byte_data(self.I2C_ADDR, self.REG_DATA_CHAN1 + 1)
        lsb0 = self.bus.read_byte_data(self.I2C_ADDR, self.REG_DATA_CHAN0)
        msb0 = self.bus.read_byte_data(self.I2C_ADDR, self.REG_DATA_CHAN0 + 1)
        ch1 = (msb1 << 8) | lsb1
        ch0 = (msb0 << 8) | lsb0
        return ch0, ch1

    def calculate_lux(self, ch0, ch1):
        # This formula comes from https://github.com/automote/LTR303/blob/master/LTR303.cpp
        # Andy isn't suuuuuuure how much he trusts it
        ratio = ch1 / float(ch0) if ch0 != 0 else 0
        
        #normalize for integration time
        ch0 *= (402.0/self.integration_time);
        ch1 *= (402.0/self.integration_time);
        
        # Example from Arduino library (may need adapting)
        if ratio < 0.5:
            lux = (0.0304 * ch0) - (0.062 * ch1)
        elif ratio < 0.61:
            lux = (0.0224 * ch0) - (0.031 * ch1)
        elif ratio < 0.80:
            lux = (0.0128 * ch0) - (0.0153 * ch1)
        elif ratio < 1.30:
            lux = (0.00146 * ch0) - (0.00112 * ch1)
        else:
            lux = 0
        # Adjust for gain 
        lux = lux / (self.gain) 
        return lux

    def read_lux(self):
        ch0, ch1 = self.read_raw()
        lux = self.calculate_lux(ch0, ch1)
        return lux, ch0, ch1
