import cv2
import json
import numpy as np
from PIL import ImageFont, ImageDraw, Image

class Subtitle:
    __capture = ''
    __out = ''
    __fourcc = ''
    __fps = ''
    __size = ()
    __subtitles = {}

    def video_capture(self, file):
        self.__capture = cv2.VideoCapture(file)

    def __set_size(self):
        width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        return (width, height)

    def set_video_option(self, fourcc, fps, size=None):
        self.__fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.__fps = fps
        
        if size is None:
            self.__size = self.__set_size() # None is video default size
        
        else:
            self.__size = size #size = (width, height)

    def video_writer(self, file):
        self.__out = cv2.VideoWriter(file, self.__fourcc, self.__fps, self.__size)

    def load_subtitles(self, file):
        with open(file, 'r', encoding='UTF-8') as data:
            self.__subtitles =  json.load(data)
        self.__subtitles = self.__subtitles['subtitles']
    
    def __is_set_time(self, idx, time):
        if (idx >= len(self.__subtitles)):
            return False

        if (time >= self.__subtitles[idx]['start'] and time <= self.__subtitles[idx]['end']):
            return True
        
        else:
            return False
    
    def __is_end_time(self, idx, time):
        if (time == self.__subtitles[idx]['end'] and idx < len(self.__subtitles)):
            return True
        
        else:
            return False

    def __set_font(self, idx):
        font_type = self.__subtitles[idx]['font_type']
        font_size = self.__subtitles[idx]['font_size']
        
        return ImageFont.truetype('fonts/'+font_type, font_size) #폰트, 사이즈

    def __set_position(self, frame, t_size, t_xy):
        if (t_xy or (t_xy == 0 and t_xy == 0)): # x, y 둘 다 0으로 설정 시 기본 위치로 지정
            x = t_xy[0]
            y = t_xy[1]
        
        else:
            x = (frame.shape[1] - t_size[0]) / 2
            y = frame.shape[0] - frame.shape[0] / 10
        
        return (x,y)

    def __set_subtitle(self, frame, idx):
        font = self.__set_font(idx)
        font_color = tuple(self.__subtitles[idx]['font_color'])
        text = self.__subtitles[idx]['subtitle']
        sub_xy = self.__subtitles[idx]['subtitle_xy']

        pframe = Image.fromarray(frame) #cv2 -> pil 형식으로 변환
        draw = ImageDraw.Draw(pframe) #자막을 넣기 객체 생성
        position = self.__set_position(frame, draw.textsize(text, font), sub_xy)
        draw.text(position, text, font=font, fill=font_color) #자막 삽입
        
        return np.array(pframe) #다시 cv2로 사용해야 하기 때문에 numpy array 형식으로 반환

    def edit(self):
        cur_fps = 0 # 현재 fps
        time = 0 # 현재 영상 시간 100ms 기준
        idx = 0 # 딕셔너리 인덱스
        
        while self.__capture.isOpened():
            status, frame = self.__capture.read()
            if not status: # 프레임을 읽어오지 못할 경우 종료
                break   
            
            if (self.__is_set_time(idx, time)): #설정된 자막의 시간일 경우 True 반환
                frame = self.__set_subtitle(frame, idx) 
                if (self.__is_end_time(idx, time)): #설정중인 자막의 마지막 시간일 때 인덱스 증가 = 다음 자막 입력 진행
                    idx += 1
            
            # cv2.imshow('vdo', frame) # 따로 창으로 출력
            self.__out.write(frame)
                
            cur_fps += 1
            time = int(cur_fps / 6) * 100
            
            if cv2.waitKey(1) & 0xFF == ord('q'): # q 누르면 종료
                break

    def __del__(self):
        self.__capture.release()
        self.__out.release()
        cv2.destroyAllWindows()