import cv2

# 初始化USB摄像头设备
cap = cv2.VideoCapture(0)  # 设备索引根据实际连接情况调整

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法获取视频流")
            break

        # 显示实时画面
        cv2.imshow('ELF2 Camera Preview', frame)

        # 空格键触发截图
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.imwrite(f'capture_{int(time.time())}.jpg', frame)
            print("截图已保存")

        # ESC键退出
        if cv2.waitKey(1) == 27:
            break
finally:
    cap.release()
    cv2.destroyAllWindows()