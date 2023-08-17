import Camera_Function as cf
import Motor_Function as mf
from time import sleep


def measurement_sequence(vert_range, horiz_range, vert_overlap, horiz_overlap, vert_direction,exposure,iso,led,seq_num):
    global rotate_right 
    rotate_right = True

    if horiz_range == 0 and horiz_overlap == 0:
        for i in range(vert_range):
            cf.capture_measurements(led,exposure,iso,seq_num)
            sleep(2)
            if vert_direction == True:
                mf.move_vertical_UP(vert_overlap)
            else:
                mf.move_vertical_DOWN(vert_overlap)    
            sleep(2)
    elif vert_range == 0 and vert_overlap == 0:
        for i in range(horiz_range):
            cf.capture_measurements(led,exposure,iso,seq_num)
            sleep(2)
            if rotate_right == True: 
                mf.rotate_RIGHT(horiz_overlap)
                
            else:
                mf.rotate_LEFT(horiz_overlap)
            sleep(2) 
    else:
        for i in range(vert_range):
            cf.capture_measurements(led,exposure,iso,seq_num)
            sleep(3)
            for j in range(horiz_range):
                cf.capture_measurements(led,exposure,iso,seq_num)
                if rotate_right == True: 
                    mf.rotate_RIGHT(horiz_overlap)
                    sleep(2)
                else:
                    mf.rotate_LEFT(horiz_overlap)
                    sleep(2)
                rotate_right = not rotate_right

            if vert_direction == True:
                mf.move_vertical_UP(vert_overlap)
            else:
                mf.move_vertical_DOWN(vert_overlap)     

def move_to_initial_position(vert_range, horiz_range, vert_direction):
    
    if rotate_right == True:
        mf.rotate_RIGHT(horiz_range)
    else:
        mf.rotate_LEFT(horiz_range) 

    
    if vert_direction == True:
        mf.move_vertical_DOWN(vert_range)  # Move up
    else:
        mf.move_vertical_UP(vert_range)  # Move down

