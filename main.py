import cv2

#시간할 경우 소수점 두자리 까지 -> 가능하다면? 00:00:00 형식으로 사용?
cap = cv2.VideoCapture('sample2.mp4')

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter('output.mp4', fourcc, 60.0, (width, height)) # 파일 이름, fourcc, 프레임, (너비, 높이)

i = 0
sub_list = ["1", "2", "3", "4", "5"]
while cap.isOpened():
    status, frame = cap.read()
    if not status:
        break   
    # frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
    cv2.putText(frame, str(i), (500,500), cv2.FONT_HERSHEY_COMPLEX_SMALL, 10, (0, 0, 0)) #이미지, 텍스트, 위치, 폰트, 폰트크기, 폰트색
    
    cv2.imshow('vdo', frame) # 따로 창으로 출력
    out.write(frame)
        
    i = i + 1
    if cv2.waitKey(1) & 0xFF == ord('q'): # q 누르면 종료
        break
cap.release()
out.release()
cv2.destroyAllWindows()
