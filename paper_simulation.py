# -*- coding: utf-8 -*-
"""
@author: A.Ç.SEÇKİN
seckin.ac@gmail.com
"""

import numpy as np
import matplotlib.pyplot as plt
from PySpice.Unit import *
from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Spice.Netlist import Circuit

plt.close()
###############################################################################
circuit1 = Circuit('Coaxial Fabric 1')
circuit1.SinusoidalVoltageSource('input', 'in', circuit1.gnd, amplitude=5@u_V)
circuit1.R(1, 'in', 1, 10@u_kΩ)
circuit1.R(2, 1, circuit1.gnd, 3.3@u_kΩ)
circuit1.L(1, 1, 'out1', 20@u_mH)
circuit1.C(1, 'out1', circuit1.gnd, 1@u_pF)
circuit1.C(2, 'out1', circuit1.gnd, 62@u_pF)
circuit1.R(3, 'out1', circuit1.gnd, 1000@u_kΩ)
simulator1 = circuit1.simulator(temperature=25, nominal_temperature=25)
analysis1 = simulator1.ac(start_frequency=30@u_kHz, stop_frequency=10@u_MHz, number_of_points=300,  variation="dec")
frequency_v=np.array(analysis1.frequency)
gain_v=20*np.log10(np.absolute(analysis1['out1']))
print(frequency_v[np.argmax(gain_v)])
###############################################################################
figure, axes = plt.subplots(2, figsize=(20, 10))
plt.title("Bode Diagram")
bode_diagram(axes=axes,frequency=frequency_v,gain=gain_v,
                 phase=np.angle(analysis1['out1'], deg=False),

                 color='black',
                 linestyle='-')
