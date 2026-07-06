"""
เกมหนูหาชีสในเขาวงกต - เวอร์ชัน matplotlib (แสดงเป็นรูปภาพ)
=============================================================
ขั้นตอนนี้ทำแค่ 3 อย่าง (เหมือนเวอร์ชัน terminal ทุกอย่าง แค่เปลี่ยนวิธีแสดงผล):
1. สร้างแผนที่เขาวงกต
2. วางหนู (M) ไว้ที่จุดเริ่มต้น และทางออก/ชีส (C) ไว้ที่จุดจบ
3. แสดงผลเป็น "รูปภาพ" ด้วย matplotlib แทนการ print ตัวอักษร

ยังไม่มี AI ของหนู ยังไม่มีอัลกอริทึมการเดินใดๆ ทั้งสิ้น
"""

import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ----------------------------------------------------------
# ค่าตั้งต้นของสนาม (เหมือนเดิมทุกอย่าง)
# ----------------------------------------------------------
GRID_SIZE = 30        # เขาวงกต 30x30 ช่อง
CELL_SIZE_CM = 16     # แต่ละช่องขนาด 16 cm

DIRS = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0),
}
OPPOSITE = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}


class Cell:
    """แต่ละช่องในเขาวงกต เก็บว่ามีกำแพงด้านไหนบ้าง (เริ่มต้น = ปิดล้อมรอบหมด)"""
    def __init__(self):
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False


def generate_maze(width, height):
    """
    สร้างเขาวงกตด้วยวิธี Recursive Backtracker (DFS แบบใช้ stack)
    (นี่คืออัลกอริทึมสร้าง 'แผนที่' เท่านั้น ไม่ใช่อัลกอริทึมของหนู)
    """
    grid = [[Cell() for _ in range(height)] for _ in range(width)]
    stack = []

    start_x, start_y = 0, 0
    grid[start_x][start_y].visited = True
    stack.append((start_x, start_y))

    while stack:
        x, y = stack[-1]
        neighbors = []
        for direction, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not grid[nx][ny].visited:
                neighbors.append((direction, nx, ny))

        if neighbors:
            direction, nx, ny = random.choice(neighbors)
            grid[x][y].walls[direction] = False
            grid[nx][ny].walls[OPPOSITE[direction]] = False
            grid[nx][ny].visited = True
            stack.append((nx, ny))
        else:
            stack.pop()

    return grid


def count_junctions(grid, width, height):
    """นับจำนวนทางแยก (ช่องที่เปิดทางเดินได้ >= 3 ทิศ)"""
    junctions = 0
    for x in range(width):
        for y in range(height):
            open_paths = sum(1 for d in DIRS if not grid[x][y].walls[d])
            if open_paths >= 3:
                junctions += 1
    return junctions


def generate_valid_maze(width, height, min_junctions=5, max_attempts=50):
    """สร้างเขาวงกตซ้ำจนกว่าจะมีทางแยกอย่างน้อย min_junctions จุด"""
    for attempt in range(1, max_attempts + 1):
        grid = generate_maze(width, height)
        junctions = count_junctions(grid, width, height)
        if junctions >= min_junctions:
            print(f"[สร้างเขาวงกตสำเร็จ] ลองครั้งที่ {attempt} -> พบทางแยก {junctions} จุด")
            return grid

    print(f"[คำเตือน] ลองครบ {max_attempts} ครั้งแล้ว ใช้ผลลัพธ์ล่าสุด")
    return grid


# ----------------------------------------------------------
# ส่วนแสดงผลเป็น "รูปภาพ" ด้วย matplotlib (ส่วนใหม่ของวันนี้)
# ----------------------------------------------------------
def draw_maze(grid, width, height, mouse_pos, exit_pos, save_path="E:\\งาน\\401\\map.png"):
    """
    วาดเขาวงกตด้วย matplotlib ทีละกำแพง แล้ววางหนู + ทางออกทับลงไป

    วิธีคิดพิกัด: แต่ละช่อง (x, y) ในเขาวงกต จะกินพื้นที่ 1x1 หน่วยในภาพ
    ตั้งแต่มุม (x, y) ถึง (x+1, y+1)
    เราจะกลับแกน y ตอนวาด (py = height-1-y) เพื่อให้ช่อง (0,0)
    ไปอยู่ 'มุมบนซ้าย' ของภาพ เหมือนกับที่เราอ่าน grid ทั่วไป
    """
    fig, ax = plt.subplots(figsize=(9, 9))

    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            px, py = x, height - 1 - y  # กลับแกน y

            # วาดกำแพงแต่ละด้าน ถ้ามีอยู่จริง (walls[...] == True)
            if cell.walls['N']:
                ax.plot([px, px + 1], [py + 1, py + 1], color='black', linewidth=1.5)
            if cell.walls['S']:
                ax.plot([px, px + 1], [py, py], color='black', linewidth=1.5)
            if cell.walls['E']:
                ax.plot([px + 1, px + 1], [py, py + 1], color='black', linewidth=1.5)
            if cell.walls['W']:
                ax.plot([px, px], [py, py + 1], color='black', linewidth=1.5)

    # วาดตำแหน่งหนู (จุดเริ่มต้น) เป็นวงกลมสีเทา
    mx, my = mouse_pos
    mpx, mpy = mx + 0.5, height - 1 - my + 0.5
    ax.add_patch(patches.Circle((mpx, mpy), 0.35, color='dimgray', zorder=5))
    ax.text(mpx, mpy, 'M', ha='center', va='center', fontsize=12, color='white', fontweight='bold')

    # วาดตำแหน่งทางออก/ชีส เป็นวงกลมสีทอง
    ex, ey = exit_pos
    epx, epy = ex + 0.5, height - 1 - ey + 0.5
    ax.add_patch(patches.Circle((epx, epy), 0.35, color='gold', zorder=4))
    ax.text(epx, epy, 'C', ha='center', va='center', fontsize=12, color='black', fontweight='bold')

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')   # ทำให้ 1 หน่วยแกน x เท่ากับ 1 หน่วยแกน y (ช่องจะได้เป็นสี่เหลี่ยมจัตุรัสจริง)
    ax.axis('off')           # ซ่อนเส้นแกน x/y ที่ matplotlib ใส่มาให้อัตโนมัติ (ไม่ต้องใช้)
    ax.set_title(
        f"Maze {width}x{height} cells ({CELL_SIZE_CM} cm/cell)\n"
        f"M = Mouse (start), C = Exit / Cheese (finish)"
    )

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"[บันทึกรูปภาพ] เขาวงกตถูกบันทึกไว้ที่: {save_path}")
    plt.show()


# ----------------------------------------------------------
# ส่วนรันโปรแกรมหลัก
# ----------------------------------------------------------
if __name__ == "__main__":
    START = (0, 0)
    EXIT = (GRID_SIZE - 1, GRID_SIZE - 1)

    print(f"กำลังสร้างเขาวงกตขนาด {GRID_SIZE}x{GRID_SIZE} ช่อง (ช่องละ {CELL_SIZE_CM} cm)...")
    maze = generate_valid_maze(GRID_SIZE, GRID_SIZE, min_junctions=5)

    print(f"จุดเริ่มต้น (หนู M) : {START}")
    print(f"จุดทางออก (C)      : {EXIT}")

    draw_maze(maze, GRID_SIZE, GRID_SIZE, START, EXIT)