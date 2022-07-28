#!/usr/bin/env python

import rospy, cv2, numpy,cv_bridge

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class Cizgi:
    def __init__(self):
        self.bridge=cv_bridge.CvBridge()
        self.image_sub=rospy.Subscriber('camera/rgb/image_raw',Image,self.func)
        self.cmd_vel_pub=rospy.Publisher('cmd_vel',Twist,queue_size=1)
        self.twist=Twist()
    def func(self,img):
        rospy.loginfo("aa")
        image=self.bridge.imgmsg_to_cv2(img,'bgr8')
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 
        #yellow_lower=numpy.array([22,100,100]) sarı
        #yellow_upper=numpy.array([38,255,255]) sarı
        yellow_lower=numpy.array([0,100,100]) #turuncu
        yellow_upper=numpy.array([22,255,255])#turuncu
        #yellow_lower=numpy.array([10,10,10])
        #yellow_upper=numpy.array([255,255,250])
        mask=cv2.inRange(hsv,yellow_lower,yellow_upper)
        resize_mask=cv2.resize(mask,(300,300))
        cv2.namedWindow('maske',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('maske',300,300)
        cv2.imshow('maske',mask)
        
        h, w, d = image.shape
        search_top = 3*h/4
        search_bot = 3*h/4+70

        mask[0:int(search_top),0:w] = 0
        mask[int(search_bot):h, 0:w] = 0
        cv2.namedWindow('kirpilmis_maske',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('kirpilmis_maske',300,300)
        cv2.imshow('kirpilmis_maske',mask)
        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx= int(M['m10']/M['m00'])
            cy= int(M['m01']/M['m00'])
            cv2.circle(image, (cx,cy),50,(0,0,255),-1)
            err=cx-w/2
        self.twist.linear.x=0.0
        #self.twist.angular.z=-float(err)/100
        self.cmd_vel_pub.publish(self.twist)

        cv2.namedWindow('cizgi_izleme',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('cizgi_izleme',300,300)       
        cv2.imshow('cizgi_izleme',image)
        cv2.waitKey(3)


    
def shutdown():
    print("Kapatiliyor...")




if __name__=="__main__":
    rospy.init_node('followLine',anonymous=True)
    print("For exit CTRL+C")
    rospy.on_shutdown(shutdown)
    obje=Cizgi()
    rospy.spin()
