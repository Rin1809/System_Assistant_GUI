# utils/cau_hinh.py
import threading
import sys
import codecs
import os
import re
from rich.console import Console
from rich.table import Table

# Khóa Rin
PRINT_LOCK = threading.Lock()

# Màu sắc
PINK1 = "\033[38;2;255;192;203m"
PLUM2 = "\033[38;2;221;160;221m"
RICH_PINK = "\033[38;2;255;105;180m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[38;5;226m"  # Nền vàng nhạt
BLUE = "\033[94m"
ORANGE = "\033[38;2;255;105;180m"
RESET = "\033[0m"
BOLD = "\033[1m"
UNBOLD = "\033[0m"
GREEN = "\033[38;5;154m"
RIN = "\033[38;5;159m"
TIME = "\033[38;5;231m"
THISTLE1 = "\033[38;2;255;225;255m"
DARK_ORANGE = "\033[38;2;255;140;0m"
MODEL_NAME = "gemini-2.0-flash-exp" # Thay doi model neu can
MODEL_NAME2 = "gemini-exp-1206"
TEMP = 0.7
TOP_P = 0.95
TOP_K = 40
MAX_OUTPUT_TOKENS = 8192 #giam xuon == nhanh hon
API_KEY = "Yourkey" #dat API key o day

SUCCESS = f"{GREEN}✔{RESET}"
FAIL = f"{RED}❌{RESET}"
ERROR = f"{RED}⚠{RESET}"

# path luu memory
MEMORY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory")

MEMORY_FILE_FORMAT = "Memory_%Y-%m-%d_%H-%M-%S.json"
SESSION_FILE_FORMAT = "Session_%Y-%m-%d_%H-%M-%S.json"

def remove_ansi_escape_codes(text):
    """Loại bỏ mã màu ANSI khỏi chuỗi."""
    return re.sub(r'\x1b\[[0-9;]*[mG]', '', text)

def format_output(plugin_name, message=None, execution_time=None, content=None, error=None, analysis=None, output=None, code=None, disk_info=None, detailed=True):
    """
    Formats the output for better readability.
    """
    console = Console()

    if not detailed:
        if execution_time is not None:
            console.print(f"[{plugin_name}] ✨ Hoàn tất ({execution_time:.2f}s) ✨")
        if message:
            console.print(f"✅ {message}")
        if error:
            console.print(f"❌ {error}")
        return

    table = Table(title=f"[{plugin_name}]")

    table.add_column("Trường", style="dim", width=20)
    table.add_column("Giá trị")

    if message:
        table.add_row("✅ Thông báo", message)
    if execution_time is not None:
        table.add_row("✨ Thời gian", f"{execution_time:.2f}s")
    if analysis:
        table.add_row("🔍 Phân tích", analysis)
    if output:
        table.add_row("➡️ Output", output)
    if content:
        table.add_row("📄 Nội dung", content)
    if code:
        table.add_row("💻 Code", code)
    if disk_info:
        table.add_row("💽 Thông tin ổ đĩa", "")
        for disk in disk_info:
            table.add_row("    - ➡️ Ổ đĩa", disk['caption'])
            table.add_row("      ➡️ Mô tả", disk['description'])
            table.add_row("      ➡️ Kích thước", f"{disk['size']} GB")
            table.add_row("      ➡️ Còn trống", f"{disk['free_space']} GB")
            table.add_row("      ➡️ Hệ thống File", disk['file_system'])
    if error:
        table.add_row("❌ Lỗi", error)

    console.print(table)
