import cv2
import numpy as np
import mss
import keyboard
from collections import defaultdict
import pyautogui #pip install pyautogui


GRID_TOP_LEFT = (660, 357)
CELL_SIZE = 25
GRID_WIDTH = 24
GRID_HEIGHT = 20

def is_close(val, target, tol=3):
    return abs(val - target) <= tol

def capture_screen():
    pyautogui.moveTo(0, 0)
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def extract_grid(img):
    grid = []
    for y in range(GRID_HEIGHT):
        row = []
        for x in range(GRID_WIDTH):
            x1 = GRID_TOP_LEFT[0] + x * CELL_SIZE
            y1 = GRID_TOP_LEFT[1] + y * CELL_SIZE
            cell_img = img[y1:y1 + CELL_SIZE, x1:x1 + CELL_SIZE]
            row.append(cell_img)
        grid.append(row)
    return grid

def classify_cell(cell):
    margin = 2
    h, w = cell.shape[:2]
    center = cell[margin:h - margin, margin:w - margin]
    avg_color = np.mean(center, axis=(0, 1))
    b, g, r = avg_color
    # print(r,g,b)
    if (is_close(r, 170) and is_close(g, 215) and is_close(b, 81)) \
       or (is_close(r, 162) and is_close(g, 209) and is_close(b, 73)):
        return 'h'  #草

    if (is_close(r, 215) and is_close(g, 184) and is_close(b, 153)) \
       or (is_close(r, 229) and is_close(g, 194) and is_close(b, 159)):
        return 'd'  # 空

    if (is_close(r, 194) and is_close(g, 177) and is_close(b, 159)) \
       or (is_close(r, 206) and is_close(g, 185) and is_close(b, 165)):
        return '1'

    if (is_close(r, 185) and is_close(g, 176) and is_close(b, 136)) \
       or (is_close(r, 197) and is_close(g, 184) and is_close(b, 141)):
        return '2'

    if (is_close(r, 226) and is_close(g, 167) and is_close(b, 139)) \
       or (is_close(r, 214) and is_close(g, 159) and is_close(b, 134)):
        return '3'

    if (is_close(r, 198) and is_close(g, 156) and is_close(b, 155)) \
       or (is_close(r, 210) and is_close(g, 164) and is_close(b, 160)):
        return '4'
    if (is_close(r, 189) and is_close(g, 167) and is_close(b, 59)) \
       or (is_close(r, 183) and is_close(g, 163) and is_close(b, 53)):
        return 'f' #旗子

    return 'u'  # 無法識別

def analyze_grid(grid):
    counter = defaultdict(int)
    for row in grid:
        for cell in row:
            label = classify_cell(cell)
            counter[label] += 1
    return counter

def debug_visualize(img, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            label = classify_cell(cell)
            x1 = GRID_TOP_LEFT[0] + x * CELL_SIZE
            y1 = GRID_TOP_LEFT[1] + y * CELL_SIZE
            cv2.putText(img, label, (x1 + 2, y1 + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
    cv2.imshow("分類結果", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    img = capture_screen()
    grid = extract_grid(img)
    result = analyze_grid(grid)

    print("=== 盤面狀態統計 ===")
    for label, count in sorted(result.items()):
        print(f"{label}: {count}")

    debug_visualize(img.copy(), grid)

print("請按下 Q 開始")
while True:
    keyboard.wait('q')
    print("開始擷取與分析...")
    main()
    print("等待下一次觸發...\n")
