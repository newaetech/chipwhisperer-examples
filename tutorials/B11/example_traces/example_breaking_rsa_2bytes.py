#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, NewAE Technology Inc.
# All rights reserved.
#
# Find this and more at ChipWhisperer.com
#
#    This file is part of chipwhisperer.
#
#    chipwhisperer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    chipwhisperer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with chipwhisperer.  If not, see <http://www.gnu.org/licenses/>.
#=================================================

from chipwhisperer.common.api.CWCoreAPI import CWCoreAPI
from matplotlib.pylab import *
import numpy as np

cwapi = CWCoreAPI()
#You may need to specify the full path for this to work
cwapi.openProject(r'rsa_test_2bytes.cwp')

tm = cwapi.project().traceManager()
ntraces = tm.numTraces()

#Reference trace
trace_ref = tm.getTrace(0)

#plot(trace_ref)

#The target trace we will attack
#If following tutorial:
#0/1 = 80 00
#2/3 = 81 40
#4/5 = AB E2
#6/7 = AB E3 (this won't work as we don't detect the last 1)
target_trace_number = 4

start = 3600
rsa_one = trace_ref[start:(start+500)]
        
diffs = []

for i in range(0, 23499):
    
    diff = tm.getTrace(target_trace_number)[i:(i+len(rsa_one))] - rsa_one    
    diffs.append(np.sum(abs(diff)))
#plot(diffs)
    
recovered_key = 0x0000
bitnum = 17

last_t = -1
for t,d in enumerate(diffs):
    
    if d < 10:        
        bitnum -= 1
        if last_t > 0:
            delta = t-last_t
            
            print delta
            
            if delta > 1300:
                recovered_key |= 1<<bitnum
                

        last_t = t
    
print("Key = %04x"%recovered_key)
