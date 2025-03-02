import time
import re
import importlib
import asyncio
import json
import psutil
import random
import threading
import os
from utils import cau_hinh
from core import chat
from utils.nhat_ky import log_error, log_info
from cac_plugin import *
from difflib import SequenceMatcher
from psutil import NoSuchProcess, AccessDenied, Process
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ctypes
import sys
from rich.style import Style
from rich.console import Console
from rich.console import Console
from core import chat
from utils.cau_hinh import remove_ansi_escape_codes
from utils.animation.hieu_ung import (
    hieu_ung_dang_suy_nghi,
    start_thinking_animation,
    stop_thinking_animation,
)
import magic

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["ABSL_LOGGING"] = "ERROR"

console = Console()
mau_hong = Style(color="pink1")
reset_mau = cau_hinh.RESET

thinking_task = None  # Biến toàn cục để lưu task animation

def rainbow_text_limited(text):
    colors = [
        "\033[38;2;255;225;255m",  # hong tim nhat (Mauve) - RGB 24-bit
        "\033[38;2;255;192;203m",  # hong nhat (Pink) - RGB 24-bit
        "\033[38;2;255;225;255m",  # hong tim nhat (rerun) (Mauve) - RGB 24-bit
        "\033[38;2;255;192;203m",  # hong nhat (rerun) (Pink) - RGB 24-bit
    ]
    reset = "\033[0m"
    segment_length = max(1, len(text) // len(colors))
    colored_text = "".join(
        colors[i % len(colors)] + text[i * segment_length : (i + 1) * segment_length] + reset
        for i in range(len(text) // segment_length + 1)
    )
    return colored_text

def load_random_file_content(folder_path):
    """Đọc ngẫu nhiên nội dung từ các file .txt trong thư mục."""
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    if not txt_files:
        return "Không tìm thấy file .txt nào."

    selected_file = random.choice(txt_files)
    file_path = os.path.join(folder_path, selected_file)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Lỗi khi đọc file {selected_file}: {e}"

# Thay doi duong dan neu muon
folder_path = "bieutuong"
text = load_random_file_content(folder_path)

# Nếu muốn thêm dòng "=))" vào đầu, hãy sử dụng text = r"""=))\n""" + text
colored_text = rainbow_text_limited(text)
print("[*]", "=" * 100)
print()
print(colored_text)

def load_plugins(plugin_dir):
    plugins = {}
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"cac_plugin.{module_name}")
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and name != "__init__":
                        if name == "XuLyFilePlugin":
                            plugins[name] = obj
                            log_info(f"Đã load plugin: {name}")
                            break
                        else:
                            if hasattr(obj, "thuc_thi"):
                                plugins[name] = obj
                                log_info(f"Đã load plugin: {name}")
            except Exception as e:
                log_error(f"Lỗi khi load plugin {filename}: {e}")
    return plugins

plugins = load_plugins("cac_plugin")

print()
print(f"{cau_hinh.RICH_PINK}!! Bấm số 0 để thoát...{cau_hinh.RESET}")
print(f"{cau_hinh.RICH_PINK}!! Bấm số 2 để ngắt tiến trình...{cau_hinh.RESET}")
print()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

danh_sach_tien_trinh_structure = {"type": "danh_sach_tien_trinh", "processes": []}
thong_tin_tien_trinh_structure = {"type": "thong_tin_tien_trinh", "process": {}}
ket_qua_tim_kiem_structure = {"type": "ket_qua_tim_kiem", "query": "", "results": []}
tom_tat_noi_dung_structure = {"type": "tom_tat_noi_dung", "url": "", "summary": ""}
kiem_tra_mang_structure = {"type": "kiem_tra_mang", "host": "", "result": ""}
traceroute_structure = {"type": "traceroute", "host": "", "result": ""}
dns_lookup_structure = {"type": "dns_lookup", "host": "", "dns_server": "", "result": ""}
giam_sat_file_structure = {
    "type": "giam_sat_file",
    "filepath": "",
    "algorithm": "",
    "interval": 0,
    "status": "",
}
trich_xuat_du_lieu_structure = {"type": "trich_xuat_du_lieu", "url": "", "data": []}
phan_tich_tai_nguyen_structure = {
    "type": "phan_tich_tai_nguyen",
    "cpu_usage": [],
    "avg_cpu_usage": 0.0,
    "memory_usage": [],
    "avg_memory_usage": 0.0,
    "disk_usage": [],
    "avg_disk_usage": 0.0,
    "network_stats": [],
}
thong_tin_o_dia_structure = {"type": "thong_tin_o_dia", "disk_info": []}
xu_ly_file_structure = {"type": "xu_ly_file", "filepath": "", "content": ""}
hanh_dong_structure = {"type": "thuc_thi_hanh_dong", "hanh_dong": "", "ket_qua": ""}

# Các hàm callback cho giám sát file
monitoring_tasks = {}  # Lưu trữ các task giám sát file

async def handle_file_change(filepath):
    """Xử lý khi file thay đổi."""
    message = f"File '{filepath}' đã bị thay đổi."
    await send_notification(message)
    print(message)

async def watch_file(filepath):
    """Giám sát file."""
    event_handler = FileChangeHandler(filepath, handle_file_change)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(filepath), recursive=False)
    observer.start()
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        observer.stop()
    observer.join()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filepath, callback):
        self.filepath = filepath
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.filepath:
            self.callback(self.filepath)

async def send_notification(message):
    if chat.chat_session_1:
        try:
            phan_hoi = await chat.chat_session_1.send_message_async(message)
            if phan_hoi and phan_hoi.text:
                phan_hoi_da_dinh_dang = chat.dinh_dang_van_ban(phan_hoi.text)
                print(
                    f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.PINK1}{phan_hoi_da_dinh_dang}{cau_hinh.RESET}"
                )
            else:
                print(
                    f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.RED}Có lỗi xảy ra khi gửi thông báo.{cau_hinh.RESET}"
                )
        except Exception as e:
            print(
                f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.RED}Lỗi: {e}{cau_hinh.RESET}"
            )

async def cancel_thinking_task():
    global thinking_task
    if thinking_task:
        thinking_task.cancel()
        try:
            await thinking_task
        except asyncio.CancelledError:
            pass
        finally:
            thinking_task = None

async def start_thinking_animation_wrapper(text=None):
    global thinking_task
    await cancel_thinking_task()  # Hủy task cũ nếu có
    thinking_task = asyncio.create_task(start_thinking_animation(text=text))

async def stop_thinking_animation_wrapper():
    global thinking_task
    if thinking_task:
        stop_thinking_animation()
        await cancel_thinking_task()
        
def format_output(message, execution_time=None, content=None, error=None, analysis=None, code=None):
    """
    Formats the output for better readability.
    """
    output = ""
    if execution_time is not None:
        output += f"[Xử lý file] ✨ Hoàn tất ({execution_time:.2f}s) ✨\n"
    else:
        output += "[Xử lý file]\n"
    output += "────────────────────────────────────────────────────────────────────────\n"
    if message:
        output += f"✅ {message}\n"
    if content:
        output += "    Nội dung:\n"
        output += "    ----------------------------------------\n"
        output += f"    {content}\n"
        output += "    ----------------------------------------\n"
    if error:
        output += f"❌ {error}\n"
    if analysis:
        output += f"🔍  Phân tích:\n    -  {analysis}\n"
    if code:
        output += f"    Code:\n"
        output += "    ----------------------------------------\n"
        output += f"    {code}\n"
        output += "    ----------------------------------------\n"

    output += "────────────────────────────────────────────────────────────────────────\n"
    return output

async def main():
    global monitoring_tasks
    global memory
    memory = []
    session_memory = []
    plugin_executed = False

    await chat.setup_chat_session()

    if os.name == "nt" and not ctypes.windll.shell32.IsUserAnAdmin():
        print(f"{cau_hinh.GREEN}Đang không chạy bằng quyền admin, tự chạy lại!{cau_hinh.RESET}")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 5)
        return

    plugin_instances = {name: plugin_class() for name, plugin_class in plugins.items()}
    monitoring_tasks = {}

    if not os.path.exists(cau_hinh.MEMORY_DIR):
        os.makedirs(cau_hinh.MEMORY_DIR)

    session_filename = time.strftime(cau_hinh.SESSION_FILE_FORMAT)
    session_file_path = os.path.join(cau_hinh.MEMORY_DIR, session_filename)

    try:
        while True:
            print()
            cau_hoi = input(f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Tôi: {cau_hinh.RESET} ")
            print()

            if not cau_hoi.strip(): 
                print(f"{cau_hinh.RED}Vui lòng nhập câu hỏi.{cau_hinh.RESET}")
                continue

            if cau_hoi == "0":
                print(
                    f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.PINK1}Bai Bai...!{cau_hinh.RESET}"
                )
                break

            if cau_hoi.startswith("!"):
                memory_file = cau_hoi[1:].strip().strip('"')
                memory_file_path = os.path.join(cau_hinh.MEMORY_DIR, memory_file)
                if os.path.exists(memory_file_path):
                    try:
                        with open(memory_file_path, "r", encoding="utf-8") as f:
                            memory = json.load(f)
                        print(
                            f"{cau_hinh.GREEN}Đã load memory từ file: {memory_file}{cau_hinh.RESET}"
                        )
                    except json.JSONDecodeError:
                        print(f"{cau_hinh.RED}Lỗi: File memory bị lỗi định dạng.{cau_hinh.RESET}")
                else:
                    print(
                        f"{cau_hinh.RED}Lỗi: Không tìm thấy file memory: {memory_file}{cau_hinh.RESET}"
                    )
                continue

            

            if cau_hoi == "2":
                for task in monitoring_tasks.values():
                    task.cancel()
                if "chat_task" in locals() and not chat_task.done():
                    chat_task.cancel()
                    print(
                        f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.YELLOW}Đã hủy thao tác đang chờ.{cau_hinh.RESET}"
                    )
                await cancel_thinking_task() # Thêm dòng này để hủy thinking_task
                await stop_thinking_animation_wrapper()
                continue
  
            # Xử lý các câu lệnh bắt đầu bằng '#'
            if cau_hoi.startswith("#"):
                await start_thinking_animation_wrapper(text="Đợi xíu...")
                cau_hoi_moi = cau_hoi[1:].strip()
                if "XuLyFilePlugin" in plugin_instances:
                    xu_ly_file_instance = plugin_instances["XuLyFilePlugin"]
                    ket_qua_xu_ly = None
                    filepath = None  # Khởi tạo biến filepath

                    # Tách các đường dẫn file
                    parts = cau_hoi_moi.split()
                    filepaths = [part.strip('"\'') for part in parts if os.path.isfile(part.strip('"\''))]
                    
                    if filepaths:
                        filepath = filepaths[0]  # Giả sử chỉ xử lý file đầu tiên
                        mime_type = magic.from_file(filepath, mime=True)
                        
                        # Xác định loại file dựa trên mimetype thay vì đuôi file
                        if 'text' in mime_type or 'application/json' in mime_type:
                            # Sử dụng Gemini để phân tích ý định của người dùng
                            prompt = f"""
                            Người dùng đang muốn thao tác với file: {filepath}
                            Loại file: {mime_type}
                            Câu hỏi/yêu cầu của người dùng: {cau_hoi_moi}

                            Hãy xác định hành động mà người dùng muốn thực hiện với file này.

                            **Phân biệt rõ ràng giữa "sửa", "nâng cấp" và "chỉnh sửa":**
                            - **sửa (fix_code)**: Sửa lỗi code trong file.
                            - **nâng cấp (nang_cap_code)**: Thêm tính năng mới, cải thiện cấu trúc code, tối ưu hóa code.
                            - **chỉnh sửa (chinh_sua_file)**: Thay đổi nội dung text trong file (thay thế, xóa, thêm text).

                            **Ví dụ:**
                            - **sửa**: "sửa file test.py" -> hành động: `fix_code`
                            - **nâng cấp**: "nâng cấp file test.py" -> hành động: `nang_cap_code`
                            - **chỉnh sửa**: "sửa file test.txt, thay thế 'xin chào' bằng 'hello'" -> hành động: `chinh_sua_file`
                            - **chỉnh sửa**: "sửa file test.py, xóa dòng 'import os'" -> hành động: `chinh_sua_file`
                            - **chỉnh sửa**: "sửa file test.py, thêm 'print("hello")' vào cuối file" -> hành động: `chinh_sua_file`
                            - **ghi đè**: "ghi file test.txt với nội dung 'abc'" -> hành động: `ghi_file`
                            - **tạo code**: "tạo file test.py với nội dung là code tính tổng 2 số" -> hành động: `tao_code`

                            **Lưu ý:**
                            - Ưu tiên `fix_code` hoặc `nang_cap_code` nếu file là code và yêu cầu là "sửa" hoặc "nâng cấp".
                            - Chỉ dùng `chinh_sua_file` khi yêu cầu rõ ràng là chỉnh sửa text.

                            Các hành động có thể là:
                            - 'doc_file': Đọc nội dung file.
                            - 'chinh_sua_file': Chỉnh sửa nội dung file (thay thế, xóa, thêm).
                            - 'ghi_file': Ghi nội dung mới vào file.
                            - 'tao_code': Tạo code mới và lưu vào file.
                            - 'fix_code': Sửa lỗi code trong file.
                            - 'nang_cap_code': Nâng cấp code trong file (thêm tính năng, cải thiện cấu trúc, tối ưu hóa).

                            Trả về duy nhất tên hành động. Không giải thích, không cần đầu ra khác.
                            """
                            hanh_dong = chat.hoi_gemini(prompt, model_type="gemini_2") # Sử dụng model_type="gemini_2" để phân tích
                            hanh_dong = hanh_dong.strip().lower() if hanh_dong else ""
                            
                            if hanh_dong == "tao_code":
                                ket_qua_xu_ly = xu_ly_file_instance.xu_ly_tao_code(
                                    filepath, cau_hoi_moi, memory
                                )
                            elif hanh_dong == "fix_code":
                                ket_qua_xu_ly = xu_ly_file_instance.fix_code(
                                    filepath, cau_hoi_moi, memory
                                )
                            elif hanh_dong == "nang_cap_code":
                                ket_qua_xu_ly = xu_ly_file_instance.nang_cap_code(
                                    filepath, cau_hoi_moi, memory
                                )
                            elif hanh_dong == "chinh_sua_file":
                                ket_qua_xu_ly = xu_ly_file_instance.chinh_sua_file(
                                    filepath, cau_hoi_moi
                                )
                            elif hanh_dong == "ghi_file":
                                noi_dung = re.search(
                                    r'với nội dung\s*"(.*?)"', cau_hoi_moi, re.IGNORECASE
                                )
                                if noi_dung:
                                    noi_dung = noi_dung.group(1)
                                    ket_qua_xu_ly = xu_ly_file_instance.ghi_file(
                                        filepath, noi_dung
                                    )
                                else:
                                    ket_qua_xu_ly = {
                                        "type": "error",
                                        "message": "Thiếu nội dung cần ghi vào file."
                                    }
                            elif hanh_dong == "doc_file":
                                ket_qua_xu_ly = xu_ly_file_instance.xu_ly_file(
                                    filepath, cau_hoi_moi, memory
                                )
                            else:
                                ket_qua_xu_ly = {
                                    "type": "error",
                                    "message": "Không xác định được hành động hoặc hành động không được hỗ trợ."
                                }
                        else:
                            ket_qua_xu_ly = {
                                "type": "error",
                                "message": "File không được hỗ trợ."
                            }
                    else:
                        ket_qua_xu_ly = {
                            "type": "error",
                            "message": "Không tìm thấy file."
                        }

                    if ket_qua_xu_ly:
                        session_memory.append({"role": "user", "content": cau_hoi})
                        session_memory.append(
                            {
                                "role": "system",
                                "content": f"[PLUGIN: XuLyFile] Bắt đầu xử lý file: {filepath}. Câu hỏi: {cau_hoi_moi}",
                            }
                        )
                        start_time = time.time()
                        end_time = time.time()
                        execution_time = end_time - start_time

                        if ket_qua_xu_ly["type"] == "xu_ly_file":
                            # Sử dụng hàm format_output để in kết quả
                            formatted_result = format_output(
                                message=ket_qua_xu_ly["message"],
                                content=ket_qua_xu_ly["content"],
                                execution_time=execution_time
                            )
                            print(
                                f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {formatted_result}"
                            )

                            
                            memory.append(ket_qua_xu_ly)
                            session_memory.append({"role": "model", "content": ket_qua_xu_ly["message"]})
                            if ket_qua_xu_ly["content"]:
                                session_memory.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: XuLyFile] Nội dung:\n{ket_qua_xu_ly['content']}",
                                    }
                                )
                        elif ket_qua_xu_ly["type"] == "thay_doi":
                            # Sử dụng hàm format_output để in kết quả
                            danh_gia = ""
                            noi_dung = None

                            if hanh_dong == "fix_code":
                                danh_gia = "Sửa lỗi code"
                            elif hanh_dong == "nang_cap_code":
                                danh_gia = "Nâng cấp code"
                            elif hanh_dong == "chinh_sua_file":
                                danh_gia = "Chỉnh sửa nội dung"

                            if 'content' in ket_qua_xu_ly:
                                noi_dung = ket_qua_xu_ly['content']
                                
                            thong_bao = f"{danh_gia} thành công!" if danh_gia else ket_qua_xu_ly['message']

                            formatted_result = format_output(
                                message=thong_bao,
                                analysis=danh_gia,
                                content=noi_dung,
                                execution_time=execution_time
                            )
                            
                            print(
                                f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {formatted_result}"
                            )
                            
                            memory.append(ket_qua_xu_ly)
                            session_memory.append({"role": "model", "content": ket_qua_xu_ly["message"]})
                            if noi_dung:
                                session_memory.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: XuLyFile] Các thay đổi:\n{noi_dung}",
                                    }
                                )
                            elif thong_bao:
                                session_memory.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: XuLyFile] Thông báo:\n{thong_bao}",
                                    }
                                )
                        elif ket_qua_xu_ly["type"] == "error":
                            formatted_result = format_output(
                                error=ket_qua_xu_ly["message"],
                                execution_time=execution_time
                            )
                            print(
                                f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {formatted_result}"
                            )
                            
                            session_memory.append({"role": "model", "content": ket_qua_xu_ly["message"]})

                        plugin_executed = True  # Thêm
                        end_time = time.time()
                        execution_time = end_time - start_time
                        session_memory.append(
                            {
                                "role": "system",
                                "content": f"[PLUGIN: XuLyFile] Thời gian xử lý: {execution_time:.4f} giây",
                            }
                        )
                    else:
                        print(
                            f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.RED}Không tìm thấy file hoặc không hỗ trợ định dạng file.{cau_hinh.RESET}"
                        )
                        session_memory.append(
                            {"role": "model", "content": "Không tìm thấy file hoặc không hỗ trợ định dạng file."}
                        )
                else:
                    print(
                        f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.RED}Lỗi: Không tìm thấy plugin 'XuLyFilePlugin'.{cau_hinh.RESET}"
                    )
                    session_memory.append(
                        {"role": "model", "content": "Lỗi: Không tìm thấy plugin 'XuLyFilePlugin'."}
                    )
                session_memory.append({"role": "system", "content": "--- Kết thúc xử lý câu lệnh ---"})
                await stop_thinking_animation_wrapper()
                continue

            file_messages = []
            xu_ly_cau_hoi_tiep_theo = True
            hanh_dong_duoc_thuc_hien = False
            plugin_executed = False

            # Nếu không phải là lệnh đặc biệt, xử lý như một câu hỏi thông thường
            if cau_hoi.startswith("@") and "ThucThiLenhHeThong" in plugin_instances:
                plugin_executed = True
                thuc_thi_lenh_he_thong_plugin = plugin_instances["ThucThiLenhHeThong"]
                try:
                    cau_hoi_moi = cau_hoi[1:].strip()
                    session_memory.append({"role": "user", "content": cau_hoi})
                    session_memory.append(
                        {
                            "role": "system",
                            "content": f"[PLUGIN: ThucThiLenhHeThong] Bắt đầu thực thi. Câu hỏi: {cau_hoi_moi}",
                        }
                    )

                    start_time = time.time()
                    ket_qua_thuc_thi = await thuc_thi_lenh_he_thong_plugin.thuc_thi(
                        cau_hoi_moi, memory
                    )
                    end_time = time.time()
                    execution_time = end_time - start_time

                    if ket_qua_thuc_thi:
                        print(ket_qua_thuc_thi)  # <--- THÊM DÒNG NÀY ĐỂ DEBUG
                        formatted_result = cau_hinh.format_output(
                            plugin_name="Thực thi lệnh hệ thống",
                            message=ket_qua_thuc_thi.get("message"), # Nên dùng .get() để an toàn hơn
                            analysis=ket_qua_thuc_thi.get("gemini_2_validation"), # Nên dùng .get() để an toàn hơn
                            output=ket_qua_thuc_thi.get("output"), # Nên dùng .get() để an toàn hơn
                            error=ket_qua_thuc_thi.get("error"), # Nên dùng .get() để an toàn hơn
                            execution_time=execution_time,
                            detailed=True
                        )
                        session_memory.append(
                            {
                                "role": "system",
                                "content": f"[PLUGIN: ThucThiLenhHeThong] Thời gian thực thi: {execution_time:.4f} giây",
                            }
                        )
                        if ket_qua_thuc_thi.get("success"): # Sử dụng .get() để tránh KeyError
                            if "message" in ket_qua_thuc_thi:
                                session_memory.append(
                                    {"role": "model", "content": ket_qua_thuc_thi["message"]}
                                )

                            if "gemini_2_validation" in ket_qua_thuc_thi:
                                session_memory.append(
                                    {
                                        "role": "model",
                                        "content": f"Phân tích: [OK]\n\n[==================================================================================================]\n[!!] {ket_qua_thuc_thi['gemini_2_validation']}\n[==================================================================================================]",
                                    }
                                )

                            if "output" in ket_qua_thuc_thi and ket_qua_thuc_thi["output"]:
                                session_memory.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: ThucThiLenhHeThong] Output:\n\n{ket_qua_thuc_thi['output']}",
                                    }
                                )
                        else:
                            if "message" in ket_qua_thuc_thi:
                                session_memory.append(
                                    {"role": "model", "content": ket_qua_thuc_thi["message"]}
                                )

                            if "gemini_2_validation" in ket_qua_thuc_thi:
                                session_memory.append(
                                    {
                                        "role": "model",
                                        "content": f"Phân tích: [OK]\n\n[==================================================================================================]\n[!!] {ket_qua_thuc_thi['gemini_2_validation']}\n[==================================================================================================]",
                                    }
                                )
                            if "output" in ket_qua_thuc_thi and ket_qua_thuc_thi["output"]:
                                session_memory.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: ThucThiLenhHeThong] Output:\n\n{ket_qua_thuc_thi['output']}",
                                    }
                                )
                            if "error" in ket_qua_thuc_thi and ket_qua_thuc_thi["error"]:
                                session_memory.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: ThucThiLenhHeThong] {cau_hinh.RED}Error: {ket_qua_thuc_thi['error']}{cau_hinh.RESET}",
                                    }
                                )
                    else: # Thêm khối else để xử lý trường hợp ket_qua_thuc_thi là None
                        print(f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.RED}Lỗi: Không nhận được kết quả thực thi lệnh hệ thống.{cau_hinh.RESET}")
                        session_memory.append(
                            {
                                "role": "system",
                                "content": "[ERROR] Không nhận được kết quả thực thi lệnh hệ thống.",
                            }
                        )


                except Exception as e:
                    print(
                        f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.RED}Lỗi khi gọi plugin thực thi lệnh hệ thống: {e}{cau_hinh.RESET}"
                    )
                    session_memory.append(
                        {
                            "role": "system",
                            "content": f"[ERROR] Lỗi khi gọi plugin ThucThiLenhHeThong: {e}",
                        }
                    )
                finally:
                    #await stop_thinking_animation_wrapper()  # Sử dụng hàm wrapper
                    pass
                session_memory.append({"role": "system", "content": "--- Kết thúc xử lý câu lệnh ---"})
                await stop_thinking_animation_wrapper()
                plugin_executed = False
            elif cau_hoi.startswith("$") and "ThucThiPython" in plugin_instances:
                plugin_executed = True
                thuc_thi_plugin = plugin_instances["ThucThiPython"]
                try:
                    cau_hoi_moi = cau_hoi[1:].strip()
                    session_memory.append({"role": "user", "content": cau_hoi})
                    session_memory.append(
                        {
                            "role": "system",
                            "content": f"[PLUGIN: ThucThiPython] Bắt đầu thực thi. Câu hỏi: {cau_hoi_moi}",
                        }
                    )

                    start_time = time.time()
                    ket_qua_thuc_thi = thuc_thi_plugin.thuc_thi(cau_hoi_moi, memory)
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    
                    if ket_qua_thuc_thi:
                        # In kết quả thông qua hàm format_output từ cau_hinh.py
                        formatted_result = cau_hinh.format_output(
                            plugin_name="Thực thi Python",
                            message=ket_qua_thuc_thi["message"],
                            analysis=ket_qua_thuc_thi["gemini_2_validation"],
                            output=ket_qua_thuc_thi.get("stdout"), # Sử dụng .get() để tránh lỗi KeyError
                            error=ket_qua_thuc_thi.get("stderr"), # Sử dụng .get() để tránh lỗi KeyError
                            disk_info=ket_qua_thuc_thi.get("disk_info", {}).get("disk_info"),
                            code=None,
                            execution_time=execution_time,
                            detailed=True
                        )
                        print(f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}:")
                        
                        session_memory.append(
                            {
                                "role": "system",
                                "content": f"[PLUGIN:                        ThucThiPython] Thời gian thực thi: {execution_time:.4f} giây",
                            }
                        )
                        if ket_qua_thuc_thi["success"]:
                            session_memory.append({"role": "model", "content": ket_qua_thuc_thi["message"]})
                            session_memory.append({"role": "system", "content": f"[PLUGIN: ThucThiPython] Command executed successfully. Analysis: {ket_qua_thuc_thi.get('gemini_2_validation', 'No analysis').split('.')[0]}" })
                        else:
                            session_memory.append({"role": "model", "content": ket_qua_thuc_thi["message"]})
                            session_memory.append({"role": "system", "content": f"[PLUGIN: ThucThiPython] Command failed. Error: {ket_qua_thuc_thi.get('error', 'Unknown error')}"})


                except Exception as e:
                    print(
                        f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.RED}Lỗi khi gọi plugin thực thi tự do: {e}{cau_hinh.RESET}"
                    )
                    session_memory.append(
                        {
                            "role": "system",
                            "content": f"[ERROR] Lỗi khi gọi plugin ThucThiPython: {e}",
                        }
                    )
                finally:
                    #await stop_thinking_animation_wrapper()  # Sử dụng hàm wrapper
                    pass
                session_memory.append({"role": "system", "content": "--- Kết thúc xử lý câu lệnh ---"})
                await stop_thinking_animation_wrapper()
                plugin_executed = False
            elif not plugin_executed:
                # Nếu không có plugin nào được gọi, gửi câu hỏi trực tiếp đến Gemini
                if cau_hoi.strip().lower() == "rin":
                    print(f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.PINK1}Dạ, có tui đây{cau_hinh.RESET}")
                    await stop_thinking_animation_wrapper()
                    continue

                # Không cần xử lý memory ở đây nữa, để prompt của Gemini tự nhiên hơn
                prompt_parts = []
                prompt_parts.append(f"Câu hỏi hiện tại: {cau_hoi}")
                prompt_moi = "\n".join(prompt_parts)

                try:
                    # Tăng timeout lên 120 giây
                    chat_task = asyncio.create_task(chat.chat_session_1.send_message_async(prompt_moi))
                    await asyncio.sleep(0)  # Nhường quyền cho task khác
                    phan_hoi = await asyncio.wait_for(chat_task, timeout=120)
                    if phan_hoi and phan_hoi.text:
                        phan_hoi_da_dinh_dang = chat.dinh_dang_van_ban(phan_hoi.text)
                        # memory.append({"role": "user", "content": cau_hoi})
                        # memory.append({"role": "model", "content": phan_hoi_da_dinh_dang})
                        session_memory.append({"role": "user", "content": cau_hoi})
                        session_memory.append({"role": "model", "content": phan_hoi_da_dinh_dang})

                        print(
                            f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.PINK1}{phan_hoi_da_dinh_dang}{cau_hinh.RESET}"
                        )
                    else:
                        print(
                            f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.RED}Hmm... Có vẻ tui đang gặp chút vấn đề (Không nhận được phản hồi từ Gemini).{cau_hinh.RESET}"
                        )
                    await stop_thinking_animation_wrapper()  # Sử dụng hàm wrapper
                except asyncio.TimeoutError:
                    chat_task.cancel()
                    try:
                        await chat_task
                    except asyncio.CancelledError:
                        print(
                            f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.YELLOW}Đã hủy thao tác của Gemini (timeout).{cau_hinh.RESET}"
                        )
                    finally:
                        await stop_thinking_animation_wrapper()  # Sử dụng hàm wrapper
                except Exception as e:
                    print(
                        f"[{chat.lay_thoi_gian_hien_tai()}] {cau_hinh.RIN}Rin{cau_hinh.RESET}: {cau_hinh.RED}Lỗi: {e}{cau_hinh.RESET}"
                    )
                    await stop_thinking_animation_wrapper()  # Sử dụng hàm wrapper

            for file_message in file_messages:
                if isinstance(file_message, dict) and file_message.get("type") == "error":
                    print(
                        f"{cau_hinh.RED}>> {file_message.get('message', 'Lỗi không xác định.')}{cau_hinh.RESET}"
                    )
                elif isinstance(file_message, str):
                    print(file_message)

            with open(session_file_path, "w", encoding="utf-8") as f:
                json.dump(session_memory, f, ensure_ascii=False, indent=4)

    except KeyboardInterrupt:
        print(f"{cau_hinh.RED}Chương trình bị dừng bởi người dùng.{cau_hinh.RESET}")
    finally:
        for task in monitoring_tasks.values():
            task.cancel()
        await asyncio.gather(*monitoring_tasks.values(), return_exceptions=True)

if __name__ == "__main__":
    async def run_all_tasks():
        main_task = asyncio.create_task(main())
        await main_task

    asyncio.run(run_all_tasks())