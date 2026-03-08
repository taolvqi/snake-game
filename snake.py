#!/usr/bin/env python3
"""
🐍 贪吃蛇小游戏 - Snake Game
用 Python + curses 实现，支持中文界面
"""

import curses
import random
import time

# 游戏配置
WIDTH = 40
HEIGHT = 20
SNAKE_HEAD = '●'  # 蛇头
SNAKE_BODY = '○'  # 蛇身
FOOD_CHAR = '★'
WALL_CHAR = '█'


class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.score = 0
        self.game_over = False
        self.paused = False
        self.direction = 'RIGHT'  # UP, DOWN, LEFT, RIGHT
        self.paused_direction = None  # 暂停时的方向
        
        # 蛇的初始位置（中心）
        self.snake = [
            [HEIGHT // 2, WIDTH // 2],
            [HEIGHT // 2, WIDTH // 2 - 1],
            [HEIGHT // 2, WIDTH // 2 - 2]
        ]
        
        # 食物位置
        self.food = self.spawn_food()
        
        # 游戏速度（毫秒）
        self.speed = 150
        
    def spawn_food(self):
        """生成随机食物"""
        while True:
            food = [
                random.randint(1, HEIGHT - 2),
                random.randint(1, WIDTH - 2)
            ]
            # 使用集合检查，提高性能
            snake_set = set(tuple(x) for x in self.snake)
            if tuple(food) not in snake_set:
                return food
    
    def handle_input(self):
        """处理键盘输入"""
        try:
            key = self.stdscr.getch()
            
            # 暂停/继续
            if key == ord(' '):
                self.paused = not self.paused
                if self.paused:
                    self.paused_direction = self.direction
                else:
                    self.direction = self.paused_direction
                return
            
            if self.paused:
                return
            
            # 方向控制 - 防止直接反向移动
            if key == curses.KEY_UP and self.direction != 'DOWN':
                self.direction = 'UP'
            elif key == curses.KEY_DOWN and self.direction != 'UP':
                self.direction = 'DOWN'
            elif key == curses.KEY_LEFT and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            elif key == curses.KEY_RIGHT and self.direction != 'LEFT':
                self.direction = 'RIGHT'
            elif key == 27:  # ESC 退出
                self.game_over = True
        except:
            pass
    
    def update(self):
        """更新蛇的位置"""
        if self.paused or self.game_over:
            return
            
        head = self.snake[0].copy()
        
        if self.direction == 'UP':
            head[0] -= 1
        elif self.direction == 'DOWN':
            head[0] += 1
        elif self.direction == 'LEFT':
            head[1] -= 1
        elif self.direction == 'RIGHT':
            head[1] += 1
        
        # 检查撞墙
        if head[0] <= 0 or head[0] >= HEIGHT - 1 or head[1] <= 0 or head[1] >= WIDTH - 1:
            self.game_over = True
            return
        
        # 检查撞到自己
        if head in self.snake:
            self.game_over = True
            return
        
        # 移动蛇
        self.snake.insert(0, head)
        
        # 检查吃到食物
        if head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            # 每吃5个食物加速
            if self.score % 50 == 0 and self.speed > 50:
                self.speed -= 10
        else:
            self.snake.pop()
    
    def draw(self):
        """绘制游戏界面"""
        self.stdscr.clear()
        
        # 绘制边框
        for i in range(WIDTH):
            self.stdscr.addstr(0, i, WALL_CHAR)
            self.stdscr.addstr(HEIGHT - 1, i, WALL_CHAR)
        for i in range(HEIGHT):
            self.stdscr.addstr(i, 0, WALL_CHAR)
            self.stdscr.addstr(i, WIDTH - 1, WALL_CHAR)
        
        # 绘制蛇 - 区分蛇头和蛇身
        for i, segment in enumerate(self.snake):
            if i == 0:
                char = SNAKE_HEAD
                color = curses.color_pair(1)  # 绿色显示蛇头
            else:
                char = SNAKE_BODY
                color = curses.color_pair(1) | curses.A_DIM  # 稍暗的颜色
            try:
                self.stdscr.addstr(segment[0], segment[1], char, color)
            except:
                pass
        
        # 绘制食物 - 使用红色
        try:
            self.stdscr.addstr(self.food[0], self.food[1], FOOD_CHAR, curses.color_pair(2))
        except:
            pass
        
        # 显示分数
        score_text = f" 分数: {self.score} "
        self.stdscr.addstr(HEIGHT - 1, WIDTH // 2 - len(score_text) // 2, score_text)
        
        # 显示信息
        if self.paused:
            info = "已暂停 | ↑↓←→ 控制 | 空格暂停 | ESC 退出"
            # 显示暂停提示
            pause_msg = "|| 暂停中 ||"
            self.stdscr.addstr(HEIGHT // 2, WIDTH // 2 - len(pause_msg) // 2, pause_msg, curses.color_pair(3))
        else:
            info = "↑↓←→ 控制 | 空格暂停 | ESC 退出"
        self.stdscr.addstr(HEIGHT, 0, info)
        
        self.stdscr.refresh()
    
    def run(self):
        """主游戏循环"""
        try:
            curses.curs_set(0)
        except:
            pass  # 无终端环境下忽略
        self.stdscr.nodelay(True)
        
        while not self.game_over:
            self.handle_input()
            self.update()
            self.draw()
            curses.napms(self.speed)
        
        return self.score


def select_difficulty(stdscr):
    """选择难度"""
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    try:
        curses.curs_set(0)
    except:
        pass  # 无终端环境下忽略
    stdscr.nodelay(False)  # 阻塞等待输入
    
    title = "🐍 贪吃蛇 - 选择难度"
    opts = [
        ("1", "简单 - 速度 200ms", 200),
        ("2", "普通 - 速度 150ms", 150),
        ("3", "困难 - 速度 100ms", 100),
    ]
    
    stdscr.addstr(h//2 - 4, w//2 - len(title)//2, title)
    for i, (key, desc, _) in enumerate(opts):
        stdscr.addstr(h//2 - 1 + i, w//2 - len(desc)//2, f"{desc}")
    
    stdscr.addstr(h//2 + 3, w//2 - 15, "按 1/2/3 选择难度...")
    stdscr.refresh()
    
    while True:
        key = stdscr.getch()
        if key == -1:
            continue  # 忽略无输入
        if key in [ord('1'), ord('2'), ord('3')]:
            idx = ord(key) - ord('1')
            return opts[idx][2]
        elif key in [curses.KEY_EXIT, 27]:  # ESC 或 q 退出
            return 150  # 默认普通难度


def show_start_screen(stdscr):
    """显示开始界面"""
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    try:
        curses.curs_set(0)
    except:
        pass  # 无终端环境下忽略
    stdscr.nodelay(False)  # 阻塞等待输入
    
    title = "🐍 贪吃蛇 Snake Game"
    desc = "用方向键控制蛇吃到食物"
    tips = "按任意键开始游戏..."
    
    stdscr.addstr(h//2 - 2, w//2 - len(title)//2, title)
    stdscr.addstr(h//2, w//2 - len(desc)//2, desc)
    stdscr.addstr(h//2 + 2, w//2 - len(tips)//2, tips, curses.A_BLINK)
    stdscr.refresh()
    
    # 等待按键，忽略 -1
    while True:
        key = stdscr.getch()
        if key != -1:
            break


def main(stdscr):
    # 初始化颜色
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # 蛇 - 绿色
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # 食物 - 红色
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # 暂停提示 - 青色
    
    try:
        curses.curs_set(0)
    except:
        pass  # 无终端环境下忽略
    
    # 显示开始界面
    show_start_screen(stdscr)
    
    # 选择难度
    speed = select_difficulty(stdscr)
    
    # 初始化游戏
    game = SnakeGame(stdscr)
    game.speed = speed  # 应用选择的难度
    
    final_score = game.run()
    
    # 显示游戏结束画面
    stdscr.nodelay(False)
    stdscr.clear()
    msg1 = "游戏结束!"
    msg2 = f"最终得分: {final_score}"
    msg3 = "按任意键退出..."
    
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h//2 - 1, w//2 - len(msg1)//2, msg1)
    stdscr.addstr(h//2, w//2 - len(msg2)//2, msg2)
    stdscr.addstr(h//2 + 1, w//2 - len(msg3)//2, msg3)
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
