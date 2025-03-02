import asyncio
import time
import random
from utils import cau_hinh

async def hieu_ung_dang_suy_nghi(text=None, animation=None, delay=None):
    all_animations = {
        "default": ["-", "\\", "|", "/"],
        "circle": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        "bengali": [" অপেক্ষা করুন ", " অপেক্ষা করুন.", " অপেক্ষা করুন..", " অপেক্ষা করুন..."],
        "dots": [".", "..", "...", "...."],
        "loading_bar": ["-", "=", "#", "█"],
        "tim_dap": ["❤️ ", "💓 ", "💗 "],
    }

    default_messages = [
        "Chờ xíu...",
        "Đang xử lý...",
        "Đang tải...",
        "Vui lòng chờ...",
        "Suy nghĩ...",
        "Hmm...",
    ]

    animation = (
        all_animations.get(animation, all_animations["tim_dap"])
        if isinstance(animation, str)
        else (animation or all_animations["tim_dap"])
    )
    text = text or random.choice(default_messages)
    delay = delay or 0.1

    idx = 0
    colors = [
        cau_hinh.PINK1,
        cau_hinh.RICH_PINK,
        cau_hinh.THISTLE1,
    ]

    random_color = random.choice(colors)


    random_animation_color = random.choice(colors)

    while True:  
        frame = animation[idx % len(animation)]

        colored_frame = f"{random_animation_color}{frame}{cau_hinh.RESET}"

    
        print_text = (
            f"  {cau_hinh.RIN}Rin{cau_hinh.RESET}: {random_color}{text}{cau_hinh.RESET}{colored_frame}   "
        )
        print(print_text, end="\r", flush=True)
        idx += 1
        try:
            await asyncio.sleep(delay)
        except asyncio.CancelledError:
            break  

async def start_thinking_animation(text=None, animation_style=None, delay=None):

    task = asyncio.create_task(hieu_ung_dang_suy_nghi(text, animation_style, delay))
    return task

def stop_thinking_animation():

    print(end="\r", flush=True)