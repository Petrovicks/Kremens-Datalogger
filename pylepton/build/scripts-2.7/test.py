#!/usr/bin/python

import sys
import numpy as np
import cv2
import cv
from pylepton import Lepton

def capture(flip_v = False, device = "/dev/spidev0.1"):
  with Lepton(device) as l:
    a,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
  cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(a, 8, a)
  return np.uint8(a)

if __name__ == '__main__':
  from optparse import OptionParser

  usage = "usage: %prog [options] output_file[.format]"
  parser = OptionParser(usage=usage)

  parser.add_option("-f", "--flip-vertical",
                    action="store_true", dest="flip_v", default=False,
                    help="flip the output image vertically")

  parser.add_option("-d", "--device",
                    dest="device", default="/dev/spidev0.1",
                    help="specify the spi device node (might be /dev/spidev0.1 on a newer device)")

  (options, args) = parser.parse_args()

  if len(args) < 1:
    print "You must specify an output filename"
    sys.exit(1)

  videoFilename = 'test_vid'
  y = 60
  x = 80
  frameShape = (x,y)
  codec = cv.CV_FOURCC('M','J','P','G')
  writer = cv2.VideoWriter(videoFilename,codec,30,frameShape,False)


  count = 0
  end = 10
  for i in range(end):

    image = capture(flip_v = options.flip_v, device = options.device)
    writer.write(image)
    
    cv2.imwrite('image_%04d.png'%(count), image)
    
    cv2.waitKey(end)
    ''' 
    if i == end:
       writer.release()
       print 'count',count
       break
    if count == end:
       writer.release()
       break
    '''
    count = count +1

