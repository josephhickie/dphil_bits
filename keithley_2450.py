# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 14:59:52 2020

@author: joseph
"""

# Imports
from Control import Control 
import pyvisa

class keithley_2450(Control) : 
    def __init__(self, config, name) : 
        
        super(keithley_2450, self).__init__(config, name)
        
        self.set_address(self.cfg[self.name]["address"])
        
        self.config(self.configs)

        # Set the termination character for Keithley outputs
        self.visainstrument.write_termination = '\n'
        self.visainstrument.read_termination = '\n'

        # Make the params equal to the initial configs 
        self.params = list(self.configs.values())

        # Allows the source to be read back out of the Keithley
        self.visainstrument.write('SOUR:VOLT:READ:BACK ON')

        # Somehow integrate the birthday keithley easter egg : 
        # self.birthday_keithley() runs happy keithday

# --------------------------------------
#           pygor functions
# --------------------------------------

    def pushparams(self, params) : 
        self.params[0] = self.set_source(params[0])
        self.params[1] = self.set_status(params[1])
    

    def pullparams(self) : 
        return self.params

# --------------------------------------
#           functions
# --------------------------------------

    #def config_to_param(self, args) : 
        #for config, key in config

    def set_address(self, address) : 
        self.visainstrument = pyvisa.ResourceManager().open_resource(address)
        
    
    # Sets the voltage (V)
    def set_source(self, val) : 
        self.visainstrument.write('SOUR:VOLT {}'.format(val)) 

        # Measures the actual voltage at the device 
        #self.visainstrument.read_termination = '\n'
        true_val = float(self.visainstrument.query(':MEAS:VOLT?'))

        # print(val/true_val)

        '''
        if abs(val/true_val - 1) <= 0.01  : 
            return val 
        else : 
            print("Error: Keithley reporting value outside 1% of set value. Trying again...")
            self.set_source(val)
        '''


    # Sets the output to ON (1) or OFF (0)
    def set_status(self, val) : 
        self.visainstrument.write('OUTP {}'.format(val))
        return val

        
        
    def reset(self) :
        self.visainstrument.write('*RST; STAT:PRES; *CLS')   
    
    def get_current(self) :
        return self.visainstrument.query('READ? "defbuffer1", READ')
    
    def get_source(self) : 
        # The following line sets the readout to the measured source voltage rather than set source voltage
        self.visainstrument.write('SOUR:VOLT:READ:BACK ON')
        return self.visainstrument.query('READ? "defbuffer1", SOUR')
            
    def keithley_birthday(self) :
        a = 440
        ash = 466
        b = 493
        c = 523
        csh = 554
        d = 587
        dsh = 622
        e = 659
        f = 698
        fsh = 739
        g = 783
        gsh = 830

        notes = [c, c, d, c, f, e, c, c, d, c, g, f, c, c, c*2, a*2, f, e, d, ash*2, ash*2, a*2, f, g, f,]
        times = [3, 1, 4, 4, 4, 8, 3, 1, 4, 4, 4, 8, 3, 1, 4, 4, 4, 4, 10, 3, 1, 4, 4, 4, 8]
        
        i = 1  
        for n in range(25) : 
            self.visainstrument.write(":SYSTem:BEEPer {}, {}".format(notes[n], times[n]*0.1))
            if i == 1 : 
                self.visainstrument.write(":DISP:LIGH:STAT ON100")
            if i == -1 : 
                self.visainstrument.write(":DISP:LIGH:STAT ON25")
            i*= -1
            
