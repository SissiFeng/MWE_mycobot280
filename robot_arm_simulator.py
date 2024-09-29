import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import time

class RobotArm:
    def __init__(self, base_pos, arm_lengths):
        self.base_pos = np.array(base_pos)
        self.arm_lengths = arm_lengths
        self.angles = [0, 0]  # 初始角度
        self.holding_bottle = False
        self.bottle = None

    def forward_kinematics(self):
        x = self.base_pos[0]
        y = self.base_pos[1]
        for length, angle in zip(self.arm_lengths, self.angles):
            x += length * np.cos(angle)
            y += length * np.sin(angle)
        return np.array([x, y])

    def move_to(self, target):
        # 简化的逆运动学，实际情况可能需要更复杂的算法
        dx = target[0] - self.base_pos[0]
        dy = target[1] - self.base_pos[1]
        distance = np.sqrt(dx**2 + dy**2)
        if distance > sum(self.arm_lengths):
            return False  # 目标超出范围

        angle = np.arctan2(dy, dx)
        cos_angle2 = (distance**2 - self.arm_lengths[0]**2 - self.arm_lengths[1]**2) / (2 * self.arm_lengths[0] * self.arm_lengths[1])
        angle2 = np.arccos(np.clip(cos_angle2, -1, 1))
        angle1 = angle - np.arctan2(self.arm_lengths[1] * np.sin(angle2), self.arm_lengths[0] + self.arm_lengths[1] * np.cos(angle2))

        self.angles = [angle1, angle2]
        return True

    def grab_bottle(self, bottle):
        if not self.holding_bottle and np.linalg.norm(self.forward_kinematics() - bottle.position) < 0.1:
            self.holding_bottle = True
            self.bottle = bottle
            return True
        return False

    def release_bottle(self):
        if self.holding_bottle:
            self.holding_bottle = False
            bottle = self.bottle
            self.bottle = None
            return bottle
        return None

class Bottle:
    def __init__(self, position):
        self.position = np.array(position)

class Station:
    def __init__(self, position, size):
        self.position = np.array(position)
        self.size = size

def draw_scene(ax, robot_arm, stations, bottles):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')

    # 绘制机械臂
    arm_pos = robot_arm.base_pos
    for length, angle in zip(robot_arm.arm_lengths, robot_arm.angles):
        next_pos = arm_pos + length * np.array([np.cos(angle), np.sin(angle)])
        ax.plot([arm_pos[0], next_pos[0]], [arm_pos[1], next_pos[1]], 'bo-')
        arm_pos = next_pos

    # 绘制工作站
    for station in stations:
        rect = Rectangle(station.position, station.size, station.size, fill=False)
        ax.add_patch(rect)

    # 绘制药瓶
    for bottle in bottles:
        circle = Circle(bottle.position, 0.1, fill=True, color='r')
        ax.add_patch(circle)

    if robot_arm.holding_bottle:
        circle = Circle(robot_arm.forward_kinematics(), 0.1, fill=True, color='g')
        ax.add_patch(circle)

def main():
    st.title("机械臂药瓶操作模拟器")

    robot_arm = RobotArm([5, 0], [3, 2])
    stations = [Station([1, 1], 2), Station([7, 1], 2), Station([4, 7], 2)]
    bottles = [Bottle([2, 2]), Bottle([8, 2]), Bottle([5, 8])]

    fig, ax = plt.subplots(figsize=(8, 8))
    plot_placeholder = st.empty()

    def update_plot():
        draw_scene(ax, robot_arm, stations, bottles)
        plot_placeholder.pyplot(fig)

    update_plot()

    st.sidebar.header("控制面板")
    target_x = st.sidebar.slider("目标 X 坐标", 0.0, 10.0, 5.0)
    target_y = st.sidebar.slider("目标 Y 坐标", 0.0, 10.0, 5.0)

    if st.sidebar.button("移动机械臂"):
        if robot_arm.move_to([target_x, target_y]):
            st.sidebar.success("机械臂已移动到目标位置")
        else:
            st.sidebar.error("目标位置超出机械臂范围")
        update_plot()

    if st.sidebar.button("抓取药瓶"):
        for bottle in bottles:
            if robot_arm.grab_bottle(bottle):
                bottles.remove(bottle)
                st.sidebar.success("成功抓取药瓶")
                break
        else:
            st.sidebar.error("附近没有可抓取的药瓶")
        update_plot()

    if st.sidebar.button("释放药瓶"):
        released_bottle = robot_arm.release_bottle()
        if released_bottle:
            released_bottle.position = robot_arm.forward_kinematics()
            bottles.append(released_bottle)
            st.sidebar.success("成功释放药瓶")
        else:
            st.sidebar.error("机械臂没有持有药瓶")
        update_plot()

    st.sidebar.header("任务")
    if st.sidebar.button("执行药瓶转移任务"):
        st.sidebar.info("开始执行药瓶转移任务...")
        for i, (start, end) in enumerate([([2, 2], [8, 2]), ([8, 2], [5, 8]), ([5, 8], [2, 2])]):
            st.sidebar.text(f"任务 {i+1}: 将药瓶从 {start} 移动到 {end}")
            robot_arm.move_to(start)
            update_plot()
            time.sleep(1)
            for bottle in bottles:
                if np.linalg.norm(bottle.position - np.array(start)) < 0.1:
                    robot_arm.grab_bottle(bottle)
                    bottles.remove(bottle)
                    break
            update_plot()
            time.sleep(1)
            robot_arm.move_to(end)
            update_plot()
            time.sleep(1)
            released_bottle = robot_arm.release_bottle()
            if released_bottle:
                released_bottle.position = np.array(end)
                bottles.append(released_bottle)
            update_plot()
            time.sleep(1)
        st.sidebar.success("药瓶转移任务完成！")

if __name__ == "__main__":
    main()
