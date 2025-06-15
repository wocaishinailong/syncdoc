import cv2
import os
import time

# --- 配置 ---
CAMERA_DEVICE_INDEX = 21  # UVC摄像头对应的设备索引号

def main():
    """主函数，用于摄像头捕获、预览和截图。"""
    print("正在尝试初始化摄像头...")
    # 检查运行环境（仅提示权限）
    if os.name == 'posix':
        print(f"当前用户ID: {os.getuid()} (提示：如果非0，可能需要root权限)")

    # 初始化摄像头
    cap = cv2.VideoCapture(CAMERA_DEVICE_INDEX)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("\n错误：无法打开摄像头！")
        print(f"请尝试以下步骤排查：")
        print(f"1. 确认摄像头已正确连接到开发板的USB口。")
        print(f"2. 确认设备索引号(CAMERA_DEVICE_INDEX)为 {CAMERA_DEVICE_INDEX} 是否正确。")
        print(f"3. 尝试以root权限运行此脚本 (例如: sudo python3 camera_capture.py)。")
        return

    print("\n摄像头初始化成功！预览窗口已启动。")
    print("  - 按 [空格键] 进行拍照。")
    print("  - 按 [ESC] 键退出程序。")

    try:
        while True:
            # 读取一帧画面
            ret, frame = cap.read()
            if not ret:
                print("错误：无法获取视频流，程序即将退出。")
                break

            # 显示实时画面
            cv2.imshow('UVC Camera Preview (Press SPACE to capture, ESC to exit)', frame)

            # 等待按键事件
            key = cv2.waitKey(1) & 0xFF

            # 如果按下空格键，则保存截图
            if key == ord(' '):
                filename = f'capture_{int(time.time())}.jpg'
                cv2.imwrite(filename, frame)
                print(f"截图成功！已保存为 {filename}")

            # 如果按下ESC键，则退出循环
            elif key == 27:
                print("用户请求退出...")
                break
    finally:
        # 释放资源并关闭窗口
        print("正在释放摄像头资源并关闭窗口。")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()