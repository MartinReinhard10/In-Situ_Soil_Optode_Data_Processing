import Camera_Function as cf
import Motor_Function as mf


def measurement_sequence(vert_range, horiz_range, vert_overlap, horiz_overlap, vert_direction,exposure,iso,led,seq_num):
    rotate_right = True

    for i in range(vert_range):
        for j in range(horiz_range):
            cf.capture_measurements(led,exposure,iso,seq_num)
            if rotate_right == True: 
                mf.rotate_RIGHT(horiz_overlap)
            else:
                mf.rotate_LEFT(horiz_overlap)
        rotate_right = not rotate_right

        if vert_direction == True:
            mf.move_vertical_UP(vert_overlap)
        else:
            mf.move_vertical_DOWN(vert_overlap)     

