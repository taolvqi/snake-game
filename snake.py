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
SNAKE_CHAR = '●'
FOOD_CHAR = '★'
WALL_CHAR = '█'

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.score = 0
        self.game_over = False
        self.direction = 'RIGHT'  # UP, DOWN, LEFT, RIGHT
        
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
            if food not in self.snake:
                return food
    
    def handle_input(self):
        """处理键盘输入"""
        try:
            key = self.stdscr.getch()
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
        
        # 绘制蛇
        for i, segment in enumerate(self.snake):
            char = SNAKE_CHAR
            self.stdscr.addstr(segment[0], segment[1], char)
        
        # 绘制食物
        self.stdscr.addstr(self.food[0], self.food[1], FOOD_CHAR)
        
        # 显示分数
        score_text = f" 分数: {self.score} "
        self.stdscr.addstr(HEIGHT - 1, WIDTH // 2 - len(score_text) // 2, score_text)
        
        # 显示信息
        info = "↑↓←→ 控制方向 | ESC 退出"
        self.stdscr.addstr(HEIGHT, 0, info)
        
        self.stdscr.refresh()
    
    def run(self):
        """主游戏循环"""
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        
        while not self.game_over:
            self.handle_input()
            self.update()
            self.draw()
            curses.napms(self.speed)
        
        return self.score


def main(stdscr):
    # 初始化颜色
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    game = SnakeGame(stdscr)
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
