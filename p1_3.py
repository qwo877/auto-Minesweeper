import cv2
import numpy as np
import mss
from collections import defaultdict

GRID_TOP_LEFT = (660, 357)
CELL_SIZE = 25
GRID_WIDTH = 24
GRID_HEIGHT = 20


def is_close(val, target, tol=3):
    return abs(val - target) <= tol


def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        shot = sct.grab(monitor)
        img = np.array(shot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def extract_grid(img):
    grid = []
    for y in range(GRID_HEIGHT):
        row = []
        for x in range(GRID_WIDTH):
            x1 = GRID_TOP_LEFT[0] + x * CELL_SIZE
            y1 = GRID_TOP_LEFT[1] + y * CELL_SIZE
            row.append(img[y1:y1+CELL_SIZE, x1:x1+CELL_SIZE])
        grid.append(row)
    return grid


def classify_cell(cell):
    core = cell[2:-2, 2:-2]
    b, g, r = np.mean(core, axis=(0,1))

    special_colors = {
        'h': [(170,215,81), (162,209,73)],
        'd': [(215,184,153), (229,194,159)],
        'f': [(189,167,59), (183,163,53)]
    }
    for label, targets in special_colors.items():
        if any(is_close(r, tr) and is_close(g, tg) and is_close(b, tb)
               for tr, tg, tb in targets):
            return label

    number_colors = {
        '1': [(194,177,159), (206,185,165)],
        '2': [(185,176,136), (197,184,141)],
        '3': [(226,167,139), (214,159,134)],
        '4': [(198,156,155), (210,164,160)]
    }
    for num, targets in number_colors.items():
        if any(is_close(r, tr) and is_close(g, tg) and is_close(b, tb)
               for tr, tg, tb in targets):
            return num

    return 'u' 


def get_board_state():
    img = capture_screen()
    grid = extract_grid(img)
    return [[classify_cell(cell) for cell in row] for row in grid]


def analyze_grid(board):
    cnt = defaultdict(int)
    for row in board:
        for c in row:
            cnt[c] += 1
    return cnt