import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    velocity_threshold = 0.2

    # Rover sees navigable terrain pixels
    if Rover.nav_angles is not None:

        # Rover in moving mode
        if Rover.mode == 'forward': 

            # If enough navigable terrain, continue forward
            if len(Rover.nav_angles) >= Rover.stop_forward:
                if Rover.vel < Rover.max_vel:
                    Rover.throttle = Rover.throttle_set  # Max throttle
                else:
                    Rover.throttle = 0  # Coast
                Rover.brake = 0
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180 / np.pi), -15, 15)  # Clipped mean

            # If not enough navigable terrain, stop
            else:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
                Rover.mode = 'stop'

        # Rover in stopped mode
        elif Rover.mode == 'stop':

            # If still moving, keep breaking
            if Rover.vel > velocity_threshold:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0

            # Rover not moving
            else:

                # If enough navigable terrain, start forward
                if len(Rover.nav_angles) >= Rover.go_forward:
                    Rover.throttle = Rover.throttle_set
                    Rover.brake = 0
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180 / np.pi), -15, 15)
                    Rover.mode = 'forward'

                # If not enough navigable terrain, 4-wheel turn in direction of navigable terrain
                else:
                    Rover.throttle = 0
                    Rover.brake = 0
                    Rover.steer = -15 if np.clip(np.mean(Rover.nav_angles * 180 / np.pi), -15, 15) < 0 else 15

    # No navigable terrain pixels
    else:

        # If Rover moving, stop it
        if Rover.mode == 'forward':
            Rover.throttle = 0
            Rover.brake = Rover.brake_set
            Rover.steer = 0
            Rover.mode = 'stop'

        # If Rover already stopped, look around for new direction
        elif Rover.mode == 'stop':
            Rover.throttle = 0
            Rover.brake = 0
            Rover.steer = -15

    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover
