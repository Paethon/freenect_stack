"""
Since the MATLAB wrapper for ROS is not able to call services and also
does not support all messages, we listen to a topic for Point messages
and use the value of the x- and y-coordinates to decide whether we
should start/stop the depth stream and lock/unlock autoexposure
"""

import rospy
from geometry_msgs.msg import Point
from freenect_camera.srv import setAutoExposure, activeDepthStream

set_auto_exposure = lambda(x): False
active_depth_stream = lambda(x): False


def callback(point):
    if(point.x < 1):
        print 'Locking exposure'
        set_auto_exposure(False)
    else:
        print 'Unlocking exposure'
        set_auto_exposure(True)

    if(point.y < 1):
        print 'Stopping depth stream'
        active_depth_stream(False)
    else:
        print 'Starting depth stream'
        active_depth_stream(True)


def main():
    global set_auto_exposure, active_depth_stream
    # Wait until the services are actually available
    print 'Waiting for services to become available'
    rospy.wait_for_service('/camera/driver/setAutoExposure')
    print 'setAutoExposure found'
    rospy.wait_for_service('/camera/driver/activeDepthStream')
    print 'activeDepthStream found'
    # Make the services available as functions
    set_auto_exposure = rospy.ServiceProxy('/camera/driver/setAutoExposure',
                                           setAutoExposure)
    active_depth_stream = rospy.ServiceProxy(
        '/camera/driver/activeDepthStream',
        activeDepthStream)
    # Then subscribe to the control message topic from MATLAB
    rospy.init_node('matlab_controll_wrapper')
    rospy.Subscriber('/matlab/kinect_control', Point, callback)
    # Spinspin
    rospy.spin()

if __name__ == '__main__':
    main()
