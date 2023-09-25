# Part 1: Estimating Height with the Time of Flight Sensor

The time-of-flight (TOF) sensor on the drone outputs a distance
estimate.  ROS requires all distances to be in meters.  

## Questions

1. Look on the [data sheets](datasheets) for the TOF sensor on your drone. You will be using [the recommended Python library](https://docs.circuitpython.org/projects/vl53l0x/en/latest/) to read data from the TOF sensor. In what units does it output distances?
2. [This Adafruit product](https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/overview) uses the same TOF sensor as your drone. What are the minimum and maximum distances that the sensor can measure?
