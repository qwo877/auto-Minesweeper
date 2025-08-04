import keyboard
from p1_3 import get_board_state, analyze_grid
from collections import deque


def is_opened_number(cell):
    return cell in {'1','2','3','4'}


def get_neighbors(x, y, w=24, h=20):
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            yield nx, ny


def solve():
    board = get_board_state()
    stats = analyze_grid(board)
    print("=== 盤面統計 ===")
    for label in sorted(stats.keys()):
        print(f"{label}: {stats[label]}")




if __name__ == '__main__':
    print("請按下 Q 鍵開始擷取與分析...")
    while True:
        keyboard.wait('q')
        print("開始擷取與分析...")
        solve()
        print("等待下一次觸發...")