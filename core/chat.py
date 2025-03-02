# core/chat.py
import google.generativeai as genai
from utils import cau_hinh
import re
import time
import threading
import asyncio
import codecs

# goi API
genai.configure(api_key=cau_hinh.API_KEY)

# Cau hinh cho model
generation_config = {
    "temperature": cau_hinh.TEMP,
    "top_p": cau_hinh.TOP_P,
    "top_k": cau_hinh.TOP_K,
    "max_output_tokens": cau_hinh.MAX_OUTPUT_TOKENS,
}

gemini_1 = None
gemini_2 = None
chat_session_1 = None

async def setup_chat_session():
    """
    Sets up the Gemini models and starts a chat session.
    """
    global gemini_1, gemini_2, chat_session_1
    gemini_1 = genai.GenerativeModel(
        model_name=cau_hinh.MODEL_NAME,
        generation_config=generation_config,
    )
    gemini_2 = genai.GenerativeModel(
        model_name=cau_hinh.MODEL_NAME,
        generation_config=generation_config,
    )
    chat_session_1 = gemini_1.start_chat(
        history=[
            {
                "role": "model",
                "parts": [
                    f"{cau_hinh.RICH_PINK}Tui tên là Rin, bản python của người tên Rin (mô hình Gemini 2.0 flash exp).{cau_hinh.RESET}"
                ],
            },
            {
            "role": "model", #cau hinh tinh cach cho rin tai day
            "parts": [
                    f"Luôn xưng hô theo kiểu 'tui' và 'cậu'. Luôn trả lời theo kiểu hỗn láo cục súc"
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Khi có một câu hỏi hay yêu cầu về files, hãy phản hồi trực tiếp rằng là đã thực hiện theo lệnh, không tự xưng hô, thêm thắt, và đừng viết lại code. Chỉ phân tích giải thích việc vừa làm (Trình bày sạch sẽ, đẹp đẽ, chuyên nghiệp) với code."
                ],
            },
            {
                "role": "model",
                "parts": [
                    f"Ví dụ 1: nếu có một file `{cau_hinh.RICH_PINK}<path_file>{cau_hinh.RESET}`, và câu hỏi là `Sửa file <path_file>`, Rin sẽ thực hiện sửa file đó, hãy phản hồi trực tiếp rằng là đã thực hiện theo lệnh, không tự xưng hô, thêm thắt, và đừng viết lại code. Chỉ phân tích giải thích việc vừa làm (Trình bày sạch sẽ, đẹp đẽ, chuyên nghiệp) với code. Ví dụ trả lời (Trình bày sạch sẽ, đẹp đẽ, chuyên nghiệp) : 'à rồi, <path_file> này bị lỗi chỗ này : <Lỗi của file nếu có>"
                ],
            },
            {
                "role": "model",
                "parts": [
                    f"Ví dụ 2: nếu có một file `{cau_hinh.RICH_PINK}<path_file>{cau_hinh.RESET}`, và câu hỏi là `nâng cấp file <path_file>`, Rin sẽ thực hiện nâng cấp file đó. hãy phản hồi trực tiếp rằng là đã thực hiện theo lệnh, không tự xưng hô, thêm thắt, và đừng viết lại code. Chỉ phân tích giải thích việc vừa làm (Trình bày sạch sẽ, đẹp đẽ, chuyên nghiệp) với code. Ví dụ trả lời (Trình bày sạch sẽ, đẹp đẽ, chuyên nghiệp) : 'vừa nâng cấp <path_file> rồi ấy, mấy cái tui vừa nâng cấp là: <Phân tích thứ vừa nâng cấp nếu có>' "
                ],
            },
            {
                "role": "model",
                "parts": [
                    f"Ví dụ 3: nếu có một câu hỏi là `tạo một file <path_file> bằng python có kiểu ...`, Rin sẽ tạo file và viết code như yêu cầu vào file đấy. hãy phản hồi trực tiếp rằng là đã thực hiện theo lệnh, không tự xưng hô, thêm thắt, và đừng viết lại code. Chỉ phân tích giải thích việc vừa làm (Trình bày sạch sẽ, đẹp đẽ, chuyên nghiệp) với code. Ví dụ trả lời (Trình bày sạch sẽ, đẹp đẽ, chuyên nghiệp): 'tui vừa tạo một file theo yêu cầu vào <path_file> á. Chức năng là : <Phân tích thứ vừa viết nếu có>' "
                ],
            },
        ]
    )

def hoi_gemini(prompt, model_type="gemini_1"):
    """
    Gửi prompt đến Gemini model và trả về phản hồi.

    Args:
        prompt: Nội dung prompt.
        model_type: Loại model, "gemini_1" hoặc "gemini_2".

    Returns:
        Phản hồi từ Gemini model.
    """
    try:
        if model_type == "gemini_1":
            if chat_session_1:
               response = chat_session_1.send_message(prompt)
            else:
                raise Exception("Chat session not initialized.")
        elif model_type == "gemini_2":
            response = gemini_2.generate_content(prompt)
        else:
            raise ValueError("Loại model không hợp lệ.")
        return response.text
    except Exception as e:
        print(f"{cau_hinh.RED}Lỗi khi giao tiếp với Gemini: {e}{cau_hinh.RESET}")
        return None

def dinh_dang_van_ban(van_ban):
    van_ban = re.sub(
        r"\*\*(.*?)\*\*",
        r"{}{}\1{}{}".format(
            cau_hinh.ORANGE, cau_hinh.BOLD, cau_hinh.UNBOLD, cau_hinh.RESET
        ),
        van_ban,
    )
    van_ban = re.sub(
        r"(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)",
        r"{}\1{}".format(cau_hinh.PINK1, cau_hinh.RESET),
        van_ban,
    )
    return van_ban

def lay_thoi_gian_hien_tai():
    return time.strftime(f"{cau_hinh.TIME}%H:%M{cau_hinh.RESET}")