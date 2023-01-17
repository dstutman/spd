from frankx import Robot, LinearMotion, Affine

robot = Robot("172.16.0.2")
robot.recover_from_errors()

robot.set_dynamic_rel(0.1)
robot.jerk_rel = 0.01
robot.acceleration_rel = 0.01

robot.move(LinearMotion(Affine(0.25, 0.25, 0.25)))