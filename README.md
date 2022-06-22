# gen_sub

json(자막) 파일 형식

sample.json 파일 참고

- subtitles
  - start: 자막이 들어갈 시작 시간
  - end: 자막이 끝나는 시간
  - subtitle: 자막 텍스트
  - font_type: 사용할 폰트
  - font_size: 자막 크기
  - font_color: 자막 색깔(RGB 값)
  - subtitle_xy: 자막 위치(좌표), 둘 다 0 혹은 없을 경우 정해진 기본 위치에 설정

---

- 참고사항
  - 구현된 코드는 한 프레임에 하나의 자막만 들어갈 수 있도록 구현
  - 자막의 시작 시간과 끝나는 시간이 겹치면 X