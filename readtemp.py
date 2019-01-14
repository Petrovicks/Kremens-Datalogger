"""AF 2016"""

import subprocess
def readtemp():
   proc = subprocess.Popen(["/home/pi/Desktop/Lepton/LeptonModule-master/raspberrypi_video/foo"], stdout=subprocess.PIPE, shell=True)
   (t, err) = proc.communicate()
   #print "program output:", out

   f=t.split(':')
   str1=f[2]
   str2=f[3]

   temp1=int(str1.split(',')[0])
   temp2=int(str2.split(',')[0])

   #print temp1,temp2
   FPA_temp = (temp1*1.0)/100.0
   Aux_temp = (temp2*1.0)/100.0


#   print 'fpa', FPA_temp
#   print 'Aux', Aux_temp
   return FPA_temp, Aux_temp
