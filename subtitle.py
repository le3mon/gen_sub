from pprint import pformat
import cv2
import json
import numpy as np
from PIL import ImageFont, ImageDraw, Image

class Subtitle:
    __capture = ''
    __out = ''
    __fourcc = ''
    __fps = ''
    __size = ''
    __subtitles = {}
    # def __init__(self):
    
    def video_capture(self, file):
        self.__capture = cv2.VideoCapture(file)

    def __get_size(self):
        width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)
    
    def set_video_option(self, fourcc, fps, size=None):
        self.__fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.__fps = fps
        if size is None:
            self.__size = self.__get_size() # None is default size
        else:
            self.__size = size

    def video_writer(self, file):
        self.__out = cv2.VideoWriter(file, self.__fourcc, self.__fps, self.__size)

    def set_subtitles(self, file):
        with open(file, 'r', encoding='UTF-8') as data:
            self.__subtitles =  json.load(data)
        self.__subtitles = self.__subtitles['subtitles']

    def edit(self):
        cur_fps = 0 # 현재 fps
        time = 0 # 현재 영상 시간 100ms 기준
        idx = 0
        font = ImageFont.truetype('fonts/NanumSquareB.ttf', 20) #폰트, 사이즈
        
        while self.__capture.isOpened():
            status, frame = self.__capture.read()
            if not status: # 프레임을 읽어오지 못할 경우
                break   
            
            if (self.__subtitles[idx]['start'] <= time and self.__subtitles[idx]['end'] >= time):
                pframe = Image.fromarray(frame)
                draw = ImageDraw.Draw(pframe)
                draw.text((30, 50), "가나다라", font=font, fill=(0, 0, 0))
                frame = np.array(pframe)
                # cv2.putText(frame, self.__subtitles[idx]['subtitle'], (400,400), cv2.FONT_HERSHEY_COMPLEX_SMALL, 5, (255, 255, 255))
            
            elif (idx+1 == len(self.__subtitles)):
                None

            elif (self.__subtitles[idx+1]['start'] <= time and self.__subtitles[idx+1]['end'] >= time):
                cv2.putText(frame, self.__subtitles[idx+1]['subtitle'], (400,400), cv2.FONT_HERSHEY_COMPLEX_SMALL, 5, (255, 255, 255))
                if (idx < len(self.__subtitles)-1):
                    idx = idx + 1
            
            # cv2.imshow('vdo', frame) # 따로 창으로 출력
            self.__out.write(frame)
                
            cur_fps = cur_fps + 1
            time = int(cur_fps / 6) * 100
            
            if cv2.waitKey(1) & 0xFF == ord('q'): # q 누르면 종료
                break

    def __del__(self):
        self.__capture.release()
        self.__out.release()
        cv2.destroyAllWindows()