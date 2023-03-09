# Your Robot's Sensors

Your drone is equipped with three sensors:

1. An inertial measurement unit (IMU)
1. A time-of-flight (ToF) sensor
1. A downward facing camera.

Thanks to these sensors, the drone is equipped with enough understanding of its environment to control its flight and fly autonomously. Each sensor is described below. By interfacing with each of these sensors, you will gain exposure to core robotics concepts including frame conversions, interpreting digital signals, and computer vision.


### Time-of-flight Sensor

A range sensor is any sensor that measures the distance to an
object. There are three main types that are used on quadcopters:
ultrasonic, infrared, and time-of-flight. For ultrasonic and infrared,
a wave is emitted from one element of the sensor and received by the
other. The time taken for the wave to be emitted, reflected, and be
absorbed by the second sensor allows the range to be
calculated. Infrared is more accurate, less noisy, and has a better
range than the ultrasonic range sensor.  The time-of-flight sensor
shines infrared light at the world and measures how long it takes to
bounce back.  Your drone uses the time-of-flight (TOF) sensor because
it accurately measures range and does not require an extra analog to
digital converter board as does the infrared sensor.


### Inertial Measurement Unit (IMU)

An IMU is a device that uses accelerometers and gyroscopes to measure
forces (via accelerations) and angular rates acting on a body. The IMU
on the Duckiedrone is a built-in component of the flight controller. Data
provided by the IMU are used by the state estimator, which you will be
implementing in the next project, to better understand its motion in
flight. In addition, the flight controller uses the IMU data to
stabilize the drone from small perturbations.

The IMU can be used to measure global orientation of roll and pitch, but **not** yaw.  This is because it measures acceleration due to gravity, so it can measure the downward pointing gravity
vector.  However, this information does not give a global yaw measurement.  Many
drones additionally include a magnetometer to measure global yaw
according to the Earth's magnetic field, but the Duckiedrone does not
have this sensor.

Note that IMUs do NOT measure position or linear velocity.  The
acceleration measurements can be integrated (added up over time) to
measure linear velocity, and these velocity estimates can be
integrated again to measure position.  However, without some absolute
measurement of position or velocity, these estimates will quickly
diverge.  To measures these properties of the drone, we need to use
the camera as described below.


### Camera

Each drone is equipped with a single Arducam 5 megapixel camera. The camera is used to measure motion in the planar
directions. This camera points down towards the ground to measure `x`, `y`,
and yaw velocities of the drone using optical flow vectors that are
extracted from the camera images. This is a lightweight task, meaning
that it does not require a lot of computational effort, because these vectors
are already calculated by the Raspberry Pi's image processor for h264 video
encoding. We also use the camera to estimate the relative position of
the drone by estimating the rigid transformations between two images.

```{tableofcontents}
```