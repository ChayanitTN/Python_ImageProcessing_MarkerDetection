from openpyxl import Workbook
import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from tkinter import * 
import cv2
import time
from tkinter.filedialog import *
from PIL import Image,ImageTk
import numpy as np
from matplotlib import pyplot as plt
import imageio
import PIL.Image, PIL.ImageTk
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
screen= Tk()
screen.title("GUI for Angle Detection")
screen.geometry("1315x460") #screen size >> 657x460
screen.configure(background='Gray11') #screen background
#####################################################################################################    VDO    ########
initial =[]
List = []    
#####################################################################################################   Contour   ######
def masking(vdo):
    ret,IMG = vdo.read()
    frame = cv2.GaussianBlur(IMG, (3,3), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_pink = np.array([154,100,100])
    upper_pink = np.array([174,255,255])
    lower_blue = np.array([36, 50, 70])
    upper_blue = np.array([89, 255, 255])
    mask1= cv2.inRange(hsv,lower_pink ,upper_pink)
    mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
    mask =  mask1 + mask2
    return mask
def Contour(IMG):
    frame = cv2.GaussianBlur(IMG, (3,3), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_pink = np.array([154,100,100])
    upper_pink = np.array([174,255,255])
    lower_blue = np.array([36, 50, 70])
    upper_blue = np.array([89, 255, 255])
    mask1= cv2.inRange(hsv,lower_pink ,upper_pink)
    mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
    mask =  mask1 + mask2
    img1 = IMG.copy()
    _, cont, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)    
    for cnts in cont:
        area = cv2.contourArea(cnts)
        if area >= 50 :
           cv2.drawContours(img1,cnts, -1, (255,0,0),2)
    return img1, cont
def open_file_Angle():
    screen.filename = askopenfilename(filetypes = [("mp4", "*.mp4")])
    file = screen.filename
    play_file_Angle(file)
    return file
def Angle_Finding(vdo):
    ret, IMG = vdo.read()
    IMG = cv2.resize(IMG,(600,320),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    count = 0
    track = {}
    track_id = 0
    center_ptPrev =[]
    center_ptCur = []
    trackframe = []
    leng = 0
    StartTime = time.time()
    #angular velocity
    anglearray = [0]
    curTime = [0]
    angularvelo = [0]
    row = 0
    column = 0 
    IMG,contours = Contour(IMG)
    for box in contours: #for every contour in the image
        area = cv2.contourArea(box)
        if area >= 40 :  #there should be 2 contours
            x,y,w,h = cv2.boundingRect(box)
            xp = int((x+x+w)/2) #finding coordinate of point in x and y 
            yp = int((y+y+h)/2)
            center_ptCur.append((xp,yp))  #add new coordinate of point   
            cv2.rectangle(IMG,(x,y),(x+w, y+h),(0,255,0),2) # draw the rectagle on the contour 
            for i in range(len(center_ptCur)): #there are only 2 markers therefore, 0 then 1 
                 cv2.line(IMG, center_ptCur[i-1], center_ptCur[i],(0,0,255),2 )
                 y = np.asarray(center_ptCur[i-1])-np.asarray(center_ptCur[i]) #still wondering what is y for because witout it the number is bizarre TT
                 C71 = center_ptCur[i-1]-y
                 tragus = center_ptCur[i]-y
                 
    
   
    if len(center_ptCur) == 2: #there always be two center point of two circle
        center_copy = center_ptCur.copy() #make a copy of point group 
        centerC7 = np.asarray(center_copy[0]) #one of the problem that can be solved later is the position of center_ptCur[0] and[1] can be switch and the variable C7 can be early assign which lead to the error and break out in system
        centerTragus = np.asarray(center_copy[1])
        sumsq = np.sum(np.square(centerC7-centerTragus))#finding distance between markers
        leng = np.sqrt(sumsq)
        xn3 = int(centerC7[0]) #point on the third that 90 degree
        yn3 = int(centerC7[1]-150) 
        pt =[]  
        pt.append(xn3)
        pt.append(yn3)
        point2 = (xn3,yn3) #collect out 
        cv2.line(IMG, tuple(centerC7), tuple(point2),(0,0,255),2 )
        xn32 = xn3-y[0]
        yn32 = yn3-y[1]
        pt1 = []
        pt1.append(xn32)
        pt1.append(yn32)
        d1 = pt1 - C71 #distance from 90degree point to C71 in x-y coordinate 
        d2 = tragus  - C71 #distance from tragus to C71 in x-y coordinate
        dot1 = (d1[0]*d2[0])+(d1[1]*d2[1])
        d11 = (d1[0]**2)
        d12 = (d1[1]**2)
        d21 = (d2[0]**2)
        d22 = (d2[1]**2)
        norm1 = (np.sqrt(d11+d12)*np.sqrt(d21+d22))
        angleR1 = dot1/norm1
        angle1 = np.arccos(angleR1)
        angle1 = round(angle1*(180/np.pi))
        initial.append(angle1)
        diff = centerTragus-point2
        
        if angle1 >= (int(initial[0])-5) and angle1 <= (int(initial[0])+5) :
             cv2.putText(IMG, str("Posture: Neutral"),(30,130),0,0.65,(255,255,50),2)
             cv2.putText(IMG, str("Angle (Degree):"),(30,70),0,0.65,(0,50,255),2)
             cv2.putText(IMG, str(angle1),(50,100),0,0.65,(0,50,255),2)
             print(angle1)   
        elif angle1 > int(initial[0])+5 and diff[0] <0 :
            if angle1 < int(initial[0])+ 15:
                cv2.putText(IMG, str("Posture: Flexion"),(30,130),0,0.65,(255,255,50),2)   
                cv2.putText(IMG, str("Angle (Degree):"),(30,70),0,0.65,(0,50,255),2)
                cv2.putText(IMG, str(angle1),(50,100),0,0.65,(0,50,255),2)
                print(angle1)  
            else :
                cv2.putText(IMG, str("Posture: HyperFlexion"),(30,130),0,0.65,(255,255,50),2)
                cv2.putText(IMG, str("Angle (Degree):"),(30,70),0,0.65,(0,50,255),2)
                cv2.putText(IMG, str(angle1),(50,100),0,0.65,(0,50,255),2)
                print(angle1)

        elif angle1 < int(initial[0])-5 :
            if angle1 > int(initial[0])-15 :
                if centerTragus[0] > point2[0] :
                    cv2.putText(IMG, str("Posture: Extension"),(30,130),0,0.65,(255,50,0),2)  
                    cv2.putText(IMG, str("Angle (Degree):"),(30,70),0,0.65,(0,50,255),2)
                    cv2.putText(IMG, str(-1*(angle1)),(50,100),0,0.65,(0,50,255),2)
                    print(-1*(angle1))   
                else: 
                    cv2.putText(IMG, str("Posture: Extension"),(30,130),0,0.65,(255,50,0),2)  
                    cv2.putText(IMG, str("Angle (Degree):"),(30,70),0,0.65,(0,50,255),2)
                    cv2.putText(IMG, str(angle1),(50,100),0,0.65,(0,50,255),2)
                    print(angle1)
            else: 
                if centerTragus[0] > point2[0] :
                    cv2.putText(IMG, str("Posture: HyperExtension"),(30,130),0,0.65,(255,50,0),2)  
                    cv2.putText(IMG, str("Angle (Degree):"),(30,70),0,0.65,(0,50,255),2)
                    cv2.putText(IMG, str(-1*(angle1)),(50,100),0,0.65,(0,50,255),2)
                    print(-1*(angle1))   
                else: 
                    cv2.putText(IMG, str("Posture: HyperExtension"),(30,130),0,0.65,(255,50,0),2)  
                    cv2.putText(IMG, str("Angle (Degree):"),(30,70),0,0.65,(0,50,255),2)
                    cv2.putText(IMG, str(angle1),(50,100),0,0.65,(0,50,255),2)
                    print(angle1)
        elif diff[0] > 0:
            cv2.putText(IMG, str("Posture: HyperExtension"),(30,130),0,0.65,(255,50,0),2)
            cv2.putText(IMG, str("Angle (Degree):"),(30,70),0,0.65,(0,50,255),2)
            cv2.putText(IMG, str(-1*(angle1)),(50,100),0,0.65,(0,50,255),2)
            print(-1*(angle1))
        List.append(angle1)  
        
    else:
        print('0') 
 
    return IMG

def LIST():
    wb = Workbook()
    ws = wb.active
    for row, i in enumerate(List):
        column_cell = 'A'
        ws[column_cell+str(row+2)] = str(i)
    wb.save("DEMO.xlsx")

def play_file_Angle(file):
    vdo = cv2.VideoCapture(file)
    ret,IMG = vdo.read()
    def streamCTUR(label):
        while ret == True :
            mask = masking(vdo) 
            mask = cv2.resize(mask,(600,320),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
            pic = ImageTk.PhotoImage(image=PIL.Image.fromarray(mask))
            label.config(image=pic)
            label.image = pic
        def __del__(self):
            if self.cap.isOpened():
                self.cap.release()
        thread.start()
    def streamANG(label):
        while ret == True :
            Angle = Angle_Finding(vdo)
            Angle = cv2.cvtColor(Angle, cv2.COLOR_BGR2RGB)
            pic = ImageTk.PhotoImage(image=PIL.Image.fromarray(Angle))
            label.config(image=pic)
            label.image = pic
        def __del__(self):
            if self.cap.isOpened():
                self.cap.release()
    if __name__ == "__main__":
        my_label = Label(VDO_Canvas)
        my_label.grid(padx=10, pady=10)
        thread = threading.Thread(target=streamANG, args=(my_label,))
        thread.start()
        screen.mainloop()
def open_file_Graph():
    screen.filename = askopenfilename(filetypes = [("mp4", "*.mp4")])
    print("Loading file please stand by...")
    file = screen.filename
    vdo = cv2.VideoCapture(file)
    ret,IMG = vdo.read()
    video = imageio.get_reader(file)
    #set necessary variables
    count = 0 # initialize the frame counter
    track = {} # track id 
    track_id = 0 
    center_ptPrev =[]
    trackframe = []
    leng = 0
    StartTime = time.time()
    #angular velocity
    anglearray = [0] #empty array to collect the angle 
    curTime = [0]
    angularvelo = [0]
    def markerContour1(hsv,max1, min1,max2, min2):
        # Threshold the HSV image to get only blue colors
        mask1= cv2.inRange(hsv,min1 ,max1)
        mask2 = cv2.inRange(hsv, min2, max2)
        mask =  mask1 + mask2 # this one has no problem 
        img1 = img.copy()
        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return img1,contours
    while True:
        ret,img = vdo.read()
        trackframe.append(count)
        count += 1
        center_ptCur = []
        if ret == True : 
            img_copy1 = img.copy()
            # define range of pink color in HSV
            lower_yellow = np.array([154,100,100])
            upper_yellow = np.array([174,255,255])
            #define range of green color in HSV 
            #gray coloe is closer 
            lower_blue = np.array([36, 50, 70])
            upper_blue = np.array([89, 255, 255])
            frame = cv2.GaussianBlur(img, (3,3), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            img, contours = markerContour1(hsv,upper_yellow,lower_yellow,upper_blue,lower_blue)
            contimg = img.copy()
            for box in contours: #for every contour that found in marker contour. 
                area = cv2.contourArea(box)
                if area >= 40 : # to classify the area that we want 
                    x,y,w,h = cv2.boundingRect(box) # detect rectangle box area around 
                    xp = int((x+x+w)/2)
                    yp = int((y+y+h)/2)
                    center_ptCur.append((xp,yp)) #collect all the centroid to calculate the line and angle later on 
                    cv2.rectangle(img,(x,y),(x+w, y+h),(0,255,0),2) #draw rectangle 
                    for i in range(len(center_ptCur)):
                        cv2.line(img, center_ptCur[i-1], center_ptCur[i],(0,0,255),2 )
                        y = np.asarray(center_ptCur[i-1])-np.asarray(center_ptCur[i]) #translation 
                        if np.all(y) == 0:
                            pass
                        else:
                            newpt1 = center_ptCur[i-1]-y # the C7 will move to tragus
                            newpt2 = center_ptCur[i]-y # the tragus point will move to new position      
            #calculating the angle 
            if len(center_ptCur) == 2:
                #get center point of the contour 
                center_copy = center_ptCur.copy() # Copy the set of array that were collected when find marker contour's centroids
                center = np.asarray(center_copy[0]) #C7 point
                center1 = np.asarray(center_copy[1]) #Tragus point
                sumsq = np.sum(np.square(center-center1))
                leng = np.sqrt(sumsq)
                #straight line up 
                xn3 = int(center[0])
                yn3 = int(center[1]-100)
                pt =[]   
                pt.append(xn3) #point on vertical 90 degree
                pt.append(yn3)
                point2 = (xn3,yn3)
                cv2.line(img, tuple(center), tuple(point2),(0,0,255),2 ) #vertical line on c7 as reference
                #Translation the point for getting the angle
                C71 = newpt1 # new reference point will move to tragus
                tragus = newpt2
                xn32 = xn3-y[0]
                yn32 = yn3-y[1]
                pt1 = []
                pt1.append(xn32) #point on vertical 90 degree
                pt1.append(yn32)
                d1 = pt1 - C71 # vertical line substract c7
                d2 = tragus - C71 # tragus substract c7
                #start calculate the angle
                dot1 = (d1[0]*d2[0])+(d1[1]*d2[1])
                d11 = (d1[0]**2)
                d12 = (d1[1]**2)
                d21 = (d2[0]**2)
                d22 = (d2[1]**2)
                norm1 = (np.sqrt(d11+d12)*np.sqrt(d21+d22))
                angleR1 = dot1/norm1 # using dot product between two vector 
                angle1 = np.arccos(angleR1)
                #testing the value
                angle1 = round(angle1*(180/np.pi)) 
                #initialize the neutral posture
                for i in range(count==1):
                    initialangle = []
                    #problem : need to get the initial angle to substract off
                    initialangle = np.append(initialangle,int(angle1))
                #try to calibrate the the line in order to measure the range of motion 
            else:
                pass
            #create angular velocity without using the loop 
            anglearray.append(angle1)
            curSec = time.time()
            Time = curSec-StartTime
            curTime.append(Time) 
            initialangle = int(anglearray[1])
            initialtime = int(curTime[1])
            if len(anglearray) <= 2:
                angledelta  = int(anglearray[-1])-initialangle
                Timedelta = 2*(curTime[-1]-initialtime)
                angularvelocity = angledelta / Timedelta
                angularvelo = np.append(angularvelo, angularvelocity)
            elif len(anglearray) > 2:
                angledelta = int(anglearray[-1])-int(anglearray[-3])
                Timedelta = 2*(curTime[-1] - curTime[-3])
                angularvelocity = angledelta / Timedelta
                angularvelo = np.append(angularvelo, angularvelocity)
            
            #starting the object tracking 
            if count <= 2:
                for pt1 in center_ptCur:
                    for pt2 in center_ptPrev:
                        distance =  math.hypot(pt2[0]-pt1[0], pt2[1]-pt1[1])
                        if distance < 5:
                            track[track_id] = pt1
                            track_id+=1 
            else: 
                track_copy = track.copy()
                center_ptCur_copy = center_ptCur.copy()
                for ids, pt1 in track_copy.items():
                    exist = False
                    for pt2 in center_ptCur_copy:
                        distance = math.hypot(pt1[0]-pt1[0], pt1[1]-pt2[1])
                        if distance < 5:
                            track[ids] = pt2
                            exists = True
                            if len(center_ptCur) > 0:
                                center_ptCur_copy.remove(pt2)
                            elif len(center_ptCur) ==  0:
                                pass
                            continue
                    if not exists:
                        track.pop(ids)
            
            # there are three window showing the videos : Masking, contours, angle finding 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # for real time graph use with this code
    curTimelist = iter(curTime)
    anglelist = iter(anglearray)
    angularlist = iter(angularvelo)
    fig = plt.Figure(figsize=(5.84,3.32), dpi=100)
    x1 = []
    y1 = []
    y2 = []

    FullGraph = FigureCanvasTkAgg(fig, Graph_canvas)
    FullGraph.get_tk_widget().grid(ipadx=21, pady=6, column=1, row =0)
    
    ax1 = fig.add_subplot()
    ax1.plot(curTime,anglearray)
    ax1.set_title('Cervical Angle over Time')
    ax1.set_ylabel('Degree')
    ax1.set_xlabel('sec')
    ax1.set_ylim([20, 100])
    fig.tight_layout()
#####################################################################################################   Frame   ########     
VDO_Frame = Frame(screen, bg='Gray21')
VDO_Frame.grid(padx=5, pady=5, row=0, column=0)
VDO_Canvas = Canvas(VDO_Frame, width=625, height=345 ,bg='Gray31', highlightthickness=0)
VDO_Canvas.grid(row=1, padx=10, pady=10)  
Label(VDO_Frame,text="Angle Frame ",font=(16),bg='Gray21', fg='white').grid(row=0,column=0, padx=5,pady=5)
#----------------------------------------------------------------------------------------------------------------------#
Angle_text = StringVar()
Angle_btn = Button(screen, textvariable = Angle_text, command = lambda: open_file_Angle(),font=(8) ,bg = "#155f49", fg = "white", height = 1, width = 58)
Angle_text.set("Import Video")
Angle_btn.grid(padx=5, column=0, row = 1)
#----------------------------------------------------------------------------------------------------------------------#
Graph_Frame = Frame(screen, bg='Gray21')
Graph_Frame.grid(padx=5, pady=5,  row=0, column=1)
Graph_canvas = Canvas(Graph_Frame,width=625, height=345 ,bg='Gray31',highlightthickness=0)
Graph_canvas.grid(row=1, column=1,padx=10, pady=10)
Label(Graph_Frame, text="Graph Frame",font=(16),bg='Gray21', fg='white').grid(row=0, column=1, padx=5, pady=5) 
#----------------------------------------------------------------------------------------------------------------------#
Graph_text = StringVar()
Graph_btn = Button(screen, textvariable = Graph_text, command = lambda: open_file_Graph(),font=(8) ,bg = "#155f49", fg = "white", height = 1, width = 20)
Graph_text.set("Angle Graph")
Graph_btn.grid(padx=5, column=1, row = 1)
#----------------------------------------------------------------------------------------------------------------------#
LIST_text = StringVar()
LIST_btn = Button(screen, textvariable = LIST_text, command = lambda: LIST(),font=(8) ,bg = "#155f49", fg = "white", height = 1, width = 20)
LIST_text.set("LIST")
LIST_btn.grid(padx=5, column=1, row = 2)
screen.mainloop() 