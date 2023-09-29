#Language:Python
#Dependence:OpenCV&NumPy
#Code:utf-8
import cv2,os
Version=1.5
print("Welcome to Face Detect and Output System.")
print("System Version:",Version," Developed by Peppa Wang")
print("")
def get_folder_size(folder):
    size=0
    for root, dirs, files in os.walk(folder):
        for file in files:
            size+=os.path.getsize(os.path.join(root,file))
    return size
def enterformat(put):
    print(put,"picture format? Input'jpg','png','bmp',etc.")
    putpicformat=input('')
    while putpicformat!='jpg'and putpicformat!='JPG' and putpicformat!='png'and putpicformat!='PNG'and putpicformat!='bmp' and putpicformat!='BMP':
        print("You have entered an illegal format name, please re-enter it.")
        putpicformat=input('')
    return putpicformat
def entervalue(maxv,minv,name):
    print(name,"? Input a integal number range from ",minv," to ",maxv,".",sep='')
    value=float(input(''))
    while value>maxv or value<minv or value%1 != 0:
        print("You have entered an illegal numerical value, please re-enter it.")
        value=float(input(''))
    return value
def detect(imgread,scale,neighbors,minsz,read,frame):
    facenum=0
    img=cv2.cvtColor(imgread,cv2.COLOR_BGR2GRAY)
    faces=face.detectMultiScale(img,scaleFactor=scale,minNeighbors=neighbors,minSize=(minsz,minsz))
    for(x,y,w,h) in faces:
        facenum+=1
        f=str(facenum)
        framename=str(frame)
        if frame!=0:
            name="Output_"+read+"_"+framename+"_"+f+"."+outputpicformat
        else:
            name="Output_"+read+"_"+f+"."+outputpicformat
        out=imgread[y:y+w,x:x+w]
        cv2.imwrite(os.path.join(outpath,name),out)
    return facenum
total=0
framenum=0
face=cv2.CascadeClassifier("haarcascade_frontalface.xml")
current=os.path.dirname(os.path.abspath(__file__))
outpath=current +'\Output'
print("Detect mode? Please enter 1 or 2 to determine the detect mode.")
print("1-Picture detection    2-Camera video detection")
mode=int(input(''))
while mode != 1 and mode!= 2:
    print("You have entered an illegal mode, please re-enter it.")
    mode=int(input(''))
print("Output folder path:",outpath)

if mode==1:
    inpath=current + '\Input'
    print("Input folder path:",inpath)
    print('')
    print("Please put pending pictures into 'Input' folder!")
    os.startfile(inpath)
    print('')
    outputpicformat=enterformat('Output')
    speed=entervalue(10,0,"Detece speed")
    accuracy=entervalue(10,1,"Detece accuracy")
    scale=round(1.05+(speed)/100,2)
    neighbors=int(accuracy//3)+3
    minsz=int(accuracy*2)+10
    print("")
    print("Detect Factor: scaleFactor=",scale,", minNeighbors=",neighbors,", minSize= (",minsz,",",minsz,")",sep='')   
    print("If you have already confirmed the settings, please press 'Enter' key to start processing.")
    confirm=input()
    file_list=os.listdir(inpath)
    out_file_num=len(os.listdir(outpath))
    maxnum=len(file_list)
    print("Total file number:",maxnum)
    jpgnum=0
    bmpnum=0
    pngnum=0
    wrong_list=[]
    wrong_size=0
    if maxnum==0:
        print("")
        print("Done!")
        os.system("pause")
        exit()
    elif out_file_num!=0:
        print("")
        print("There are already some files located in the 'Output' folder!")
        print("To prevent data loss caused by overwriting, please empty all files in the 'Output' folder!")
        os.system("pause")
        exit()
    else:
        for name in file_list:
            extension = os.path.splitext(name)[-1]
            if extension==".jpg" or extension==".JPG" or extension==".jpeg" or extension==".JPEG":
                jpgnum+=1
            elif extension==".bmp" or extension==".BMP":
                bmpnum+=1
            elif extension==".png" or extension==".PNG":
                pngnum+=1
            else:
                print("The picture",name,"has the wrong format name,the program won't process it.")
                wrong_list.append(name)
                wrong_file=inpath+"\\"+name
                wrong_size+=os.path.getsize(wrong_file)
        print("Legal picture number:",maxnum-len(wrong_list))
        inputsize_byte=get_folder_size(inpath)-wrong_size    
        if inputsize_byte>1024:
            if inputsize_byte>1048576:
                print("Total size of input legal pictures:",round(inputsize_byte/1048576,2),"MB.")
            else:
                print("Total size of input legal pictures:",round(inputsize_byte/1024,2),"KB.")
        else:
            print("Total size of legal input pictures:",inputsize_byte,"Byte.")
        print("Picture format:")
        if jpgnum!=0:
            print("    JPG format picture number:",jpgnum)
        if pngnum!=0:
            print("    PNG format picture number:",pngnum)
        if bmpnum!=0:
            print("    BMP format picture number:",bmpnum)
        print("")
        print("Start Processing!")
        print("")
        for read in file_list:
            if read not in wrong_list:
                facenum=0
                print("Processing "+read+"...")
                imgread = cv2.imread(os.path.join(inpath,read))
                facenumber=detect(imgread,scale,neighbors,minsz,read,0)
                print("    Picture",read,":",facenumber,"Faces")
        print("")
if mode==2:
    outputpicformat=enterformat('Output')
    framerate=entervalue(60,1,"Frame rate")
    speed=entervalue(10,0,"Detece speed")
    accuracy=entervalue(10,1,"Detece accuracy")
    scale=round(1.05+(speed)/100,2)
    neighbors=int(accuracy//3)+3
    minsz=int(accuracy*2)+10
    print("")
    print("Detect Factor: scaleFactor=",scale,", minNeighbors=",neighbors,", minSize= (",minsz,",",minsz,")",sep='')
    out_file_num=len(os.listdir(outpath))
    if out_file_num!=0:
        print("")
        print("There are already some files located in the 'Output' folder!")
        print("To prevent data loss caused by overwriting, please empty all files in the 'Output' folder!")
        os.system("pause")
        exit()
    cam=cv2.VideoCapture(0)
    print("If you have already confirmed the settings, please press 'Enter' key to start processing.")
    confirm=input()
    while(cam.isOpened()):
        flag,frame=cam.read()
        framenum=framenum+1
        detect(frame,scale,neighbors,minsz,'Camera',framenum)
        cv2.imshow('Face-Detect-and-Output-System',frame)
        key=cv2.waitKey(int(1000/framerate))
        if key==27:
            break
    cam.release()
    cv2.destroyWindow('Face-Detect-and-Output-System')
print("Done!")
print("")
total=len(os.listdir(outpath))
print("Total number of output pictures:",total)
outputsize = round(get_folder_size(outpath)/1024,2)
print("Total size of output pictures:",outputsize,"KB.")
os.startfile(outpath)
print("")
print("Thank you for using Face Detect and Output System.")
os.system("pause")
