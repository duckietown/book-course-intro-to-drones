# Assignment 3: Linux and Networking


The networking component of this assignment will help you understand
how to communicate with your drone. Fundamentally, robots are
computers that are linked through networks. In robotics, accounting
for networking allows both more robust and more efficient design. The
networking part of this assignment describes how to use basic
networking with a focus on concepts most useful to robotics.

Networking may not seem like a topic in robotics, but it is one of the
most common reasons robots fail to work.  If you cannot connect your
base station to the robot, you cannot see the robot's status; you
cannot see sensor output; you cannot send actuation commands. Moreover
networks in the wild can be set up in a variety of diverse ways that
may or may not allow your base station to connect to your robot.  For
example, Brown's default guest network does not allow peer-to-peer
connections, so even if you get your base station and the robot
connected on that network, you still cannot talk to the robot.

As a result, it is essential to be familiar with basic networking
concepts in order to make your drone, or any robot, work.  This unit
asks you to think and learn about some networking concepts. We also
cover helpful linux commands.


This assignment is comprised of two parts: Introduction to Linux (Part
1), Networking (Part 2). Please complete all parts of this assignment.
You can do this assignment in the vscode shell on your drone, or on
any machine with Python and the requisite shell commands.  
