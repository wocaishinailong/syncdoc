#!/usr/bin/env python3
from periphery import PWM
import time

# ——— 硬件配置 ———
PWM_CHIP_PATH_PAN  = "/sys/class/pwm/pwmchip0"
PWM_CHANNEL_PAN    = 0
PWM_CHIP_PATH_TILT = "/sys/class/pwm/pwmchip1"
PWM_CHANNEL_TILT   = 0

SERVO_FREQ   = 50.0   # 50Hz → 周期 20ms
TEST_HIGH_MS = 3000   # 输出 100% 占空比时长（毫秒）

def set_angle(pwm, angle):
    """
    设置舵机角度 (0-180°)，
    先算脉冲宽度(1ms→2ms)，再除以 20ms 得到占空比比例(0.05→0.10)
    """
    angle = max(0, min(180, angle))
    pulse_s = 1e-3 + (angle / 180.0) * 1e-3
    duty_ratio = pulse_s * SERVO_FREQ
    pwm.duty_cycle = duty_ratio
    print(f"[DEBUG] angle={angle}°, pulse={pulse_s*1e3:.2f}ms, duty={duty_ratio*100:.1f}%")

def test_full_high(pwm, duration_ms):
    """把 PWM 输出设为 100% 占空比，duration_ms 毫秒后返回"""
    pwm.duty_cycle = 1.0
    print(f"[TEST] {pwm.chip}:{pwm.channel} → 100% 占空比 ({duration_ms}ms)")
    time.sleep(duration_ms / 1000.0)

if __name__ == "__main__":
    # ——— 初始化 PWM ———
    # 解析 chip number（可选）
    try:
        pan_chip = int(PWM_CHIP_PATH_PAN.split("pwmchip")[-1])
        tilt_chip = int(PWM_CHIP_PATH_TILT.split("pwmchip")[-1])
    except:
        pan_chip, tilt_chip = 0, 1

    pan = PWM(pan_chip, PWM_CHANNEL_PAN)
    tilt = PWM(tilt_chip, PWM_CHANNEL_TILT)
    for p in (pan, tilt):
        p.frequency = SERVO_FREQ
        p.enable()

    try:
        # 1) 全高测试，确保能量足够
        test_full_high(pan,  TEST_HIGH_MS)
        test_full_high(tilt, TEST_HIGH_MS)

        # 2) 回中并开始舵机扫描
        set_angle(pan,  90)
        set_angle(tilt, 90)
        time.sleep(1)

        print("开始水平扫描…")
        while True:
            for a in range(0, 181, 15):
                set_angle(pan, a)
                time.sleep(0.3)
            time.sleep(0.5)
            for a in range(180, -1, -15):
                set_angle(pan, a)
                time.sleep(0.3)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("用户中断")
    finally:
        for p in (pan, tilt):
            try:
                p.disable()
                p.close()
            except:
                pass
        print("退出程序")
