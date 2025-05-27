#!/usr/bin/env python3
from periphery import PWM
import time

# --- 请根据您的实际硬件配置修改以下PWM参数 ---
# 水平舵机 (Pan)
PWM_CHIP_PAN = "/sys/class/pwm/pwmchip0"  # Pan舵机连接的PWM控制器路径
PWM_CHANNEL_PAN = 0                     # Pan舵机连接的PWM通道号

# 垂直舵机 (Tilt)
PWM_CHIP_TILT = "/sys/class/pwm/pwmchip1" # Tilt舵机连接的PWM控制器路径
PWM_CHANNEL_TILT = 0                    # Tilt舵机连接的PWM通道号
# ----------------------------------------------

SERVO_FREQ = 50.0  # 舵机标准频率 50Hz

def set_angle(pwm_device, angle):
    """
    设置舵机角度 (0-180度).
    将角度转换为舵机所需的脉冲宽度 (1ms for 0°, 1.5ms for 90°, 2ms for 180°).
    """
    # 角度限幅，防止超出范围
    angle = max(0, min(180, angle))
    # 计算脉冲宽度 (单位: 秒)
    # 1ms + (angle / 180.0) * 1ms = (1 + angle / 180.0) * 1e-3
    pulse_width_s = (1.0 + angle / 180.0) * 1e-3
    
    try:
        pwm_device.duty_cycle = pulse_width_s
    except Exception as e:
        print(f"Error setting angle for {pwm_device}: {e}")

if __name__ == "__main__":
    try:
        # 初始化 Pan (水平) 舵机 PWM
        pan_pwm = PWM(PWM_CHIP_PAN, PWM_CHANNEL_PAN)
        pan_pwm.frequency = SERVO_FREQ
        pan_pwm.enable()
        print(f"Pan PWM ({PWM_CHIP_PAN}, channel {PWM_CHANNEL_PAN}) initialized and enabled.")

        # 初始化 Tilt (垂直) 舵机 PWM
        tilt_pwm = PWM(PWM_CHIP_TILT, PWM_CHANNEL_TILT)
        tilt_pwm.frequency = SERVO_FREQ
        tilt_pwm.enable()
        print(f"Tilt PWM ({PWM_CHIP_TILT}, channel {PWM_CHANNEL_TILT}) initialized and enabled.")

        # 将舵机设置到初始位置 (例如，中间位置90度)
        print("Setting servos to initial position (90 degrees)...")
        set_angle(pan_pwm, 90)
        set_angle(tilt_pwm, 90)
        time.sleep(1) # 等待舵机到达位置

        print("Starting pan scan...")
        # 示例：让云台水平扫描
        while True:
            # 从左到右扫描
            for angle in range(0, 181, 15): # 步长15度
                print(f"Setting pan angle to: {angle}°")
                set_angle(pan_pwm, angle)
                # tilt_pwm保持在90度，如果需要垂直扫描，可以类似修改
                # set_angle(tilt_pwm, 90) 
                time.sleep(0.3) # 每次转动后稍作停留
            
            time.sleep(0.5) # 在一端停留

            # 从右到左扫描
            for angle in range(180, -1, -15): # 步长15度
                print(f"Setting pan angle to: {angle}°")
                set_angle(pan_pwm, angle)
                time.sleep(0.3)
            
            time.sleep(0.5) # 在另一端停留

    except Exception as e:
        print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        # 清理：禁用PWM输出
        if 'pan_pwm' in locals() and pan_pwm.is_enabled:
            pan_pwm.disable()
            pan_pwm.close()
            print("Pan PWM disabled and closed.")
        if 'tilt_pwm' in locals() and tilt_pwm.is_enabled:
            tilt_pwm.disable()
            tilt_pwm.close()
            print("Tilt PWM disabled and closed.")
        print("Exiting program.")