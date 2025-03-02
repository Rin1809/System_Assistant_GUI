from flask import Flask, render_template, request, session
import asyncio
import time
import os
import importlib
import json
import ctypes
import sys
from utils import cau_hinh
from core import chat
from utils.nhat_ky import log_error, log_info
from cac_plugin import *
from difflib import SequenceMatcher
import magic
from utils.cau_hinh import remove_ansi_escape_codes
import flask
import importlib.metadata
import re

print(importlib.metadata.version("flask"))
print(flask.__version__)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Khóa bí mật cho session

plugins = {}
memory = []
session_memory = []
plugin_instances = {}
monitoring_tasks = {}

async def setup_rin():
    global plugins, plugin_instances, memory, session_memory, monitoring_tasks
    plugins = load_plugins("cac_plugin")
    plugin_instances = {name: plugin_class() for name, plugin_class in plugins.items()}
    monitoring_tasks = {}
    memory = []
    session_memory = []
    await chat.setup_chat_session()

def load_plugins(plugin_dir):
    plugins_loaded = {}
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"cac_plugin.{module_name}")
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and name != "__init__":
                        if name == "XuLyFilePlugin":
                            plugins_loaded[name] = obj
                            log_info(f"Đã load plugin: {name}")
                            break
                        else:
                            if hasattr(obj, "thuc_thi"):
                                plugins_loaded[name] = obj
                                log_info(f"Đã load plugin: {name}")
            except Exception as e:
                log_error(f"Lỗi khi load plugin {filename}: {e}")
    return plugins_loaded

def ansi_to_html(text):
    """Convert ANSI escape codes to HTML tags for styling."""
    ansi_codes = {
        cau_hinh.PINK1:     '<span style="color: #FFC0CB;">',  # Pink
        cau_hinh.PLUM2:     '<span style="color: #DDA0DD;">',  # Plum2
        cau_hinh.RICH_PINK: '<span style="color: #FF69B4;">',  # Rich Pink
        cau_hinh.RED:       '<span style="color: red;">',
        cau_hinh.GREEN:     '<span style="color: green;">',
        cau_hinh.YELLOW:    '<span style="color: #EEE8AA;">', # LightGoldenrodYellow (similar to your yellow)
        cau_hinh.BLUE:      '<span style="color: blue;">',
        cau_hinh.ORANGE:    '<span style="color: #FF4500;">', # OrangeRed (similar to your orange/pink)
        cau_hinh.RESET:     '</span>',
        cau_hinh.BOLD:      '<strong>',
        cau_hinh.UNBOLD:    '</strong>',
        cau_hinh.RIN:       '<span style="color: #ADD8E6;">', # Light Blue (similar to your RIN color)
        cau_hinh.TIME:      '<span style="color: #F0F8FF;">', # AliceBlue (similar to your TIME color)
        cau_hinh.THISTLE1:  '<span style="color: #FFE1FF;">', # Thistle1
        cau_hinh.DARK_ORANGE:'<span style="color: #FF8C00;">', # DarkOrange
    }
    for code, html in ansi_codes.items():
        text = text.replace(code, html)
    return text

def format_output_web(plugin_name, message=None, execution_time=None, content=None, error=None, analysis=None, output=None, code=None, disk_info=None, detailed=True):
    output_html = ""
    if not detailed:
        if execution_time is not None:
            output_html += f"<p>[{plugin_name}] ✨ Hoàn tất ({execution_time:.2f}s) ✨</p>"
        if message:
            output_html += f"<p>✅ {ansi_to_html(message)}</p>" # Apply ansi_to_html here
        if error:
            output_html += f"<p>❌ {ansi_to_html(error)}</p>" # Apply ansi_to_html here
        return output_html

    output_html += "<div class='output-section'>"
    output_html += f"<h3>[{plugin_name}]</h3>"
    output_html += "<hr>"
    if message:
        output_html += f"<p>✅ <strong>Thông báo:</strong> {ansi_to_html(message)}</p>" # Apply ansi_to_html here
    if execution_time is not None:
        output_html += f"<p>✨ <strong>Thời gian:</strong> {execution_time:.2f}s</p>"
    if analysis:
        # Use <pre> tag to preserve formatting
        output_html += f"<p>🔍 <strong>Phân tích:</strong> <pre style='white-space: pre-wrap;'><code>{ansi_to_html(analysis)}</code></pre></p>" # Apply ansi_to_html here
    if output:
        output_html += f"<p>➡️ <strong>Output:</strong> <pre><code class='output-code'>{ansi_to_html(output)}</code></pre></p>" # Apply ansi_to_html here
    if content:
        output_html += f"<p>📄 <strong>Nội dung:</strong> <pre><code class='content-code'>{ansi_to_html(content)}</code></pre></p>" # Apply ansi_to_html here
    if code:
        output_html += f"<p>💻 <strong>Code:</strong> <pre><code class='code-code'>{ansi_to_html(code)}</code></pre></p>" # Apply ansi_to_html here
    if disk_info:
        output_html += "<p>💽 <strong>Thông tin ổ đĩa:</strong></p>"
        output_html += "<ul>"
        for disk in disk_info:
            output_html += f"<li>➡️ Ổ đĩa: {disk['caption']}</li>"
            output_html += f"<ul>"
            output_html += f"<li>Mô tả: {disk['description']}</li>"
            output_html += f"<li>Kích thước: {disk['size']} GB</li>"
            output_html += f"<li>Còn trống: {disk['free_space']} GB</li>"
            output_html += f"<li>Hệ thống File: {disk['file_system']}</li>"
            output_html += f"</ul>"
        output_html += "</ul>"
    if error:
        output_html += f"<p>❌ <strong>Lỗi:</strong> {ansi_to_html(error)}</p>" # Apply ansi_to_html here
    output_html += "<hr>"
    output_html += "</div>"
    return output_html

@app.route("/", methods=['GET', 'POST'])
async def index():
    global memory, session_memory, plugin_instances
    output_text = ""
    user_input = ""

    if request.method == 'POST':
        user_input = request.form['user_input']
        session_memory_temp = session.get('session_memory', [])
        memory_temp = session.get('memory', [])

        cau_hoi = user_input.strip()
        if not cau_hoi:
            output_text = "<p class='error-message'>Vui lòng nhập câu hỏi.</p>"
        else:
            output_text = ""
            plugin_executed = False

            if cau_hoi.startswith("#"):
                cau_hoi_moi = cau_hoi[1:].strip()
                if "XuLyFilePlugin" in plugin_instances:
                    xu_ly_file_instance = plugin_instances["XuLyFilePlugin"]
                    ket_qua_xu_ly = None
                    filepath = None

                    parts = cau_hoi_moi.split()
                    filepaths = [part.strip('"\'') for part in parts if os.path.isfile(part.strip('"\''))]

                    if filepaths:
                        filepath = filepaths[0]
                        mime_type = magic.from_file(filepath, mime=True)

                        if 'text' in mime_type or 'application/json' in mime_type:
                            prompt = f"""
                            Người dùng đang muốn thao tác với file: {filepath}
                            Loại file: {mime_type}
                            Câu hỏi/yêu cầu của người dùng: {cau_hoi_moi}
                            ... (giữ nguyên prompt như trước) ...
                            """
                            hanh_dong = chat.hoi_gemini(prompt, model_type="gemini_2")
                            hanh_dong = hanh_dong.strip().lower() if hanh_dong else ""

                            if hanh_dong == "tao_code":
                                ket_qua_xu_ly = xu_ly_file_instance.xu_ly_tao_code(
                                    filepath, cau_hoi_moi, memory_temp
                                )
                            elif hanh_dong == "fix_code":
                                ket_qua_xu_ly = xu_ly_file_instance.fix_code(
                                    filepath, cau_hoi_moi, memory_temp
                                )
                            elif hanh_dong == "nang_cap_code":
                                ket_qua_xu_ly = xu_ly_file_instance.nang_cap_code(
                                    filepath, cau_hoi_moi, memory_temp
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
                                    filepath, cau_hoi_moi, memory_temp
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
                        session_memory_temp.append({"role": "user", "content": cau_hoi})
                        session_memory_temp.append(
                            {
                                "role": "system",
                                "content": f"[PLUGIN: XuLyFile] Bắt đầu xử lý file: {filepath}. Câu hỏi: {cau_hoi_moi}",
                            }
                        )
                        start_time = time.time()
                        end_time = time.time()
                        execution_time = end_time - start_time

                        if ket_qua_xu_ly["type"] == "xu_ly_file":
                            formatted_result = format_output_web( # Vẫn dùng format_output_web cho XuLyFile
                                plugin_name="XuLyFile",
                                message=ket_qua_xu_ly["message"],
                                content=ket_qua_xu_ly["content"],
                                execution_time=execution_time
                            )
                            output_text += formatted_result

                            memory_temp.append(ket_qua_xu_ly)
                            session_memory_temp.append({"role": "model", "content": ket_qua_xu_ly["message"]})
                            if ket_qua_xu_ly["content"]:
                                session_memory_temp.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: XuLyFile] Nội dung:\n{ket_qua_xu_ly['content']}",
                                    }
                                )
                        elif ket_qua_xu_ly["type"] == "thay_doi":
                            formatted_result = format_output_web( # Vẫn dùng format_output_web cho XuLyFile
                                plugin_name="XuLyFile",
                                message=thong_bao,
                                analysis=danh_gia,
                                content=noi_dung,
                                execution_time=execution_time
                            )
                            output_text += formatted_result

                            memory_temp.append(ket_qua_xu_ly)
                            session_memory_temp.append({"role": "model", "content": ket_qua_xu_ly["message"]})
                            if noi_dung:
                                session_memory_temp.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: XuLyFile] Các thay đổi:\n{noi_dung}",
                                    }
                                )
                            elif thong_bao:
                                session_memory_temp.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: XuLyFile] Thông báo:\n{thong_bao}",
                                    }
                                )
                        elif ket_qua_xu_ly["type"] == "error":
                            formatted_result = format_output_web( # Vẫn dùng format_output_web cho XuLyFile
                                plugin_name="XuLyFile",
                                error=ket_qua_xu_ly["message"],
                                execution_time=execution_time
                            )
                            output_text += formatted_result

                            session_memory_temp.append({"role": "model", "content": ket_qua_xu_ly["message"]})

                        plugin_executed = True
                        end_time = time.time()
                        execution_time = end_time - start_time
                        session_memory_temp.append(
                            {
                                "role": "system",
                                "content": f"[PLUGIN: XuLyFile] Thời gian xử lý: {execution_time:.4f} giây",
                            }
                        )
                    else:
                        output_text += f"<p class='error-message'>Không tìm thấy file hoặc không hỗ trợ định dạng file.</p>"
                        session_memory_temp.append(
                            {"role": "model", "content": "Không tìm thấy file hoặc không hỗ trợ định dạng file."}
                        )
                else:
                    output_text += f"<p class='error-message'>Lỗi: Không tìm thấy plugin 'XuLyFilePlugin'.</p>"
                    session_memory_temp.append(
                        {"role": "model", "content": "Lỗi: Không tìm thấy plugin 'XuLyFilePlugin'."}
                    )
                session_memory_temp.append({"role": "system", "content": "--- Kết thúc xử lý câu lệnh ---"})


            file_messages = []
            xu_ly_cau_hoi_tiep_theo = True
            hanh_dong_duoc_thuc_hien = False
            plugin_executed = False

            if cau_hoi.startswith("@") and "ThucThiLenhHeThong" in plugin_instances:
                plugin_executed = True
                thuc_thi_lenh_he_thong_plugin = plugin_instances["ThucThiLenhHeThong"]
                try:
                    cau_hoi_moi = cau_hoi[1:].strip()
                    session_memory_temp.append({"role": "user", "content": cau_hoi})
                    session_memory_temp.append(
                        {
                            "role": "system",
                            "content": f"[PLUGIN: ThucThiLenhHeThong] Bắt đầu thực thi. Câu hỏi: {cau_hoi_moi}",
                        }
                    )

                    start_time = time.time()
                    ket_qua_thuc_thi = await thuc_thi_lenh_he_thong_plugin.thuc_thi(
                        cau_hoi_moi, memory_temp
                    )
                    end_time = time.time()
                    execution_time = end_time - start_time

                    if ket_qua_thuc_thi:
                        formatted_result = format_output_web( # Use format_output_web
                            plugin_name="ThucThiLenhHeThong",
                            message=ket_qua_thuc_thi.get("message"),
                            analysis=ket_qua_thuc_thi.get("gemini_2_validation"),
                            output=ket_qua_thuc_thi.get("stdout"),
                            error=ket_qua_thuc_thi.get("error"),
                            execution_time=execution_time,
                            detailed=True
                        )
                        output_text += formatted_result

                        session_memory_temp.append(
                            {
                                "role": "system",
                                "content": f"[PLUGIN: ThucThiLenhHeThong] Thời gian thực thi: {execution_time:.4f} giây",
                            }
                        )
                        if ket_qua_thuc_thi.get("success"):
                            if "message" in ket_qua_thuc_thi:
                                session_memory_temp.append(
                                    {"role": "model", "content": ket_qua_thuc_thi["message"]}
                                )
                            if "gemini_2_validation" in ket_qua_thuc_thi:
                                session_memory_temp.append(
                                    {
                                        "role": "model",
                                        "content": f"Phân tích: [OK]\n\n[==================================================================================================]\n[!!] {ket_qua_thuc_thi['gemini_2_validation']}\n[==================================================================================================]",
                                    }
                                )
                            if "output" in ket_qua_thuc_thi and ket_qua_thuc_thi["output"]:
                                session_memory_temp.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: ThucThiLenhHeThong] Output:\n\n{ket_qua_thuc_thi['output']}",
                                    }
                                )
                        else:
                            if "message" in ket_qua_thuc_thi:
                                session_memory_temp.append(
                                    {"role": "model", "content": ket_qua_thuc_thi["message"]}
                                )
                            if "gemini_2_validation" in ket_qua_thuc_thi:
                                session_memory_temp.append(
                                    {
                                        "role": "model",
                                        "content": f"Phân tích: [OK]\n\n[==================================================================================================]\n[!!] {ket_qua_thuc_thi['gemini_2_validation']}\n[==================================================================================================]",
                                    }
                                )
                            if "output" in ket_qua_thuc_thi and ket_qua_thuc_thi["output"]:
                                session_memory_temp.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: ThucThiLenhHeThong] Output:\n\n{ket_qua_thuc_thi['output']}",
                                    }
                                )
                            if "error" in ket_qua_thuc_thi and ket_qua_thuc_thi["error"]:
                                session_memory_temp.append(
                                    {
                                        "role": "system",
                                        "content": f"[PLUGIN: ThucThiLenhHeThong] Error: {ket_qua_thuc_thi['error']}",
                                    }
                                )
                    else:
                        output_text += f"<p class='error-message'>Lỗi: Không nhận được kết quả thực thi lệnh hệ thống.</p>"
                        session_memory_temp.append(
                            {
                                "role": "system",
                                "content": "[ERROR] Không nhận được kết quả thực thi lệnh hệ thống.",
                            }
                        )

                except Exception as e:
                    output_text += f"<p class='error-message'>Lỗi khi gọi plugin thực thi lệnh hệ thống: {e}</p>"
                    session_memory_temp.append(
                        {
                            "role": "system",
                            "content": f"[ERROR] Lỗi khi gọi plugin ThucThiLenhHeThong: {e}",
                        }
                    )
                finally:
                    pass
                session_memory_temp.append({"role": "system", "content": "--- Kết thúc xử lý câu lệnh ---"})
                plugin_executed = False
            elif cau_hoi.startswith("$") and "ThucThiPython" in plugin_instances:
                plugin_executed = True
                thuc_thi_plugin = plugin_instances["ThucThiPython"]
                try:
                    cau_hoi_moi = cau_hoi[1:].strip()
                    session_memory_temp.append({"role": "user", "content": cau_hoi})
                    session_memory_temp.append(
                        {
                            "role": "system",
                            "content": f"[PLUGIN: ThucThiPython] Bắt đầu thực thi. Câu hỏi: {cau_hoi_moi}",
                        }
                    )

                    start_time = time.time()
                    ket_qua_thuc_thi = thuc_thi_plugin.thuc_thi(cau_hoi_moi, memory_temp)
                    end_time = time.time()
                    execution_time = end_time - start_time

                    if ket_qua_thuc_thi:
                        formatted_result = format_output_web( # Use format_output_web
                            plugin_name="ThucThiPython",
                            message=ket_qua_thuc_thi["message"],
                            analysis=ket_qua_thuc_thi["gemini_2_validation"],
                            output=ket_qua_thuc_thi.get("stdout"),
                            error=ket_qua_thuc_thi.get("stderr"),
                            disk_info=ket_qua_thuc_thi.get("disk_info", {}).get("disk_info"),
                            code=ket_qua_thuc_thi.get("code"),
                            execution_time=execution_time,
                            detailed=True
                        )
                        output_text += formatted_result

                        session_memory_temp.append(
                            {
                                "role": "system",
                                "content": f"[PLUGIN: ThucThiPython] Thời gian thực thi: {execution_time:.4f} giây",
                            }
                        )
                        if ket_qua_thuc_thi["success"]:
                            session_memory_temp.append({"role": "model", "content": ket_qua_thuc_thi["message"]})
                            session_memory_temp.append({"role": "system", "content": f"[PLUGIN: ThucThiPython] Command executed successfully. Analysis: {ket_qua_thuc_thi.get('gemini_2_validation', 'No analysis').split('.')[0]}" })
                        else:
                            session_memory_temp.append({"role": "model", "content": ket_qua_thuc_thi["message"]})
                            session_memory_temp.append({"role": "system", "content": f"[PLUGIN: ThucThiPython] Command failed. Error: {ket_qua_thuc_thi.get('error', 'Unknown error')}"})

                except Exception as e:
                    output_text += f"<p class='error-message'>Lỗi khi gọi plugin thực thi Python: {e}</p>"
                    session_memory_temp.append(
                        {
                            "role": "system",
                            "content": f"[ERROR] Lỗi khi gọi plugin ThucThiPython: {e}",
                        }
                    )
                finally:
                    pass
                session_memory_temp.append({"role": "system", "content": "--- Kết thúc xử lý câu lệnh ---"})
                plugin_executed = False
            elif not plugin_executed:
                prompt_parts = []
                prompt_parts.append(f"Câu hỏi hiện tại: {cau_hoi}")
                prompt_moi = "\n".join(prompt_parts)

                try:
                    phan_hoi = chat.hoi_gemini(prompt_moi)
                    if phan_hoi:
                        phan_hoi_da_dinh_dang = chat.dinh_dang_van_ban(phan_hoi)
                        session_memory_temp.append({"role": "user", "content": cau_hoi})
                        session_memory_temp.append({"role": "model", "content": phan_hoi_da_dinh_dang})
                        output_text += f"<div class='rin-response'><p><strong>Rin:</strong> {ansi_to_html(phan_hoi_da_dinh_dang)}</p></div>" # Apply ansi_to_html here
                    else:
                        output_text += "<p class='error-message'>Hmm... Có vẻ tui đang gặp chút vấn đề (Không nhận được phản hồi từ Gemini).</p>"
                except Exception as e:
                    output_text += f"<p class='error-message'>Lỗi: {e}</p>"

            session['session_memory'] = session_memory_temp
            session['memory'] = memory_temp

    session_memory_display = session.get('session_memory', [])
    return render_template('index.html', output_text=output_text, session_memory=session_memory_display, user_input=user_input)

first_request_done = False

@app.before_request
async def before_request_func():
    global first_request_done
    if not first_request_done:
        await setup_rin()
        first_request_done = True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)