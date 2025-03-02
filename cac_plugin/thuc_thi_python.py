import subprocess
import sys
import re
import platform
import ctypes
import os
from utils import cau_hinh
from utils.nhat_ky import log_error, log_info
import json
import wmi
import traceback
import time
from core.chat import hoi_gemini
import threading
from core import chat

class ThucThiPython:
    def __init__(self):
        self.ten = "thực thi mã Python"

    def thuc_thi(self, cau_hoi, memory):
        if not cau_hoi.strip():
            return self._tra_ve_loi("Câu hỏi trống", "Nhập câu hỏi sau dấu $ ấy")

        he_dieu_hanh = platform.system()
        prompt = self._tao_prompt(cau_hoi, memory, he_dieu_hanh)

        try:
            phan_hoi_gemini = hoi_gemini(prompt)
            if not phan_hoi_gemini:
                return self._tra_ve_loi("Gemini không phản hồi", "Gemini không phản hồi.")

            ma_python = self._trich_xuat_code(phan_hoi_gemini)
            if not ma_python:
                return self._tra_ve_loi("Không tìm thấy mã Python", "Không tìm thấy mã Python trong phản hồi của Gemini.")

            ma_python = self._sua_loi_unicode(ma_python)

            start_time = time.time()
            ket_qua_thuc_thi = self._thuc_thi_lenh(ma_python)
            end_time = time.time()
            execution_time = end_time - start_time

            if re.search(r"(disk info|thông tin ổ đĩa|ổ đĩa)", cau_hoi, re.IGNORECASE):
                ket_qua_thuc_thi["disk_info"] = self._lay_thong_tin_o_dia()

            ket_qua_thuc_thi["gemini_2_validation"] = self._danh_gia_ket_qua(cau_hoi, ma_python, ket_qua_thuc_thi, memory)

            ket_qua_thuc_thi["execution_time"] = execution_time
            ket_qua_thuc_thi["plugin_name"] = "Thực thi Python"
            ket_qua_thuc_thi["code"] = ma_python
            return ket_qua_thuc_thi

        except Exception as e:
            log_error(f"Lỗi khi thực thi mã Python: {e}", detail=traceback.format_exc())
            return self._tra_ve_loi("Lỗi không xác định", f"Lỗi: {e}")

    def _tao_prompt(self, cau_hoi, memory, he_dieu_hanh):
        prompt = f"Tôi đang sử dụng hệ điều hành {he_dieu_hanh}. "
        if memory:
            prompt += "Thông tin từ memory:\n"
            for item in memory:
                prompt += json.dumps(item, ensure_ascii=False) + "\n"
        prompt += self._noi_dung_prompt(cau_hoi)
        return prompt

    def _noi_dung_prompt(self, cau_hoi):
        noi_dung = f"""
        DO ENGLISH
        PLEASE ONLY generate the Python code to fulfill the following request: {cau_hoi}. Only generate Python code, no further explanation is needed. Put the code in a pair of tags ```python\\n(code here)\\n```.
        When writing Python code, note that:
            - If you need to use the `print()` command to print Unicode strings (e.g. Vietnamese), put `import sys` and `sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())` at the beginning of the program to avoid the `UnicodeEncodeError` error.
            - **Example:**
                ```python
                import sys
                import codecs

                sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

                print("This is Vietnamese with diacritics.") # Use print normally, no need for encoding="utf-8"
                ```
            - **ABSOLUTELY DO NOT use `print(..., encoding='utf-8') or `print(..., file=sys.stdout, encoding="utf-8")`.**
            - **OPEN PROGRAM IS NOT JUST IN C://ab//xyz DISK AND CAN BE DIFFERENT NAME (ex: "unikey" BUT ACTUALLY IS "UnikeyNT"), YOU MUST BE CHECK HAVE CHECK ALL DISK AND ALL FOLDER OF THE COMPUTER TO FIND THE PROGRAM**
            - **"OPEN" IS NOT ALLWAY AN "APP"!!*
            - **ALWAYS MAKE THE CODE THAT SPORT FOR MY SYSTEM !!!!CAN 100% HAVE THE TRUE RESPONSE ABOUT MY SYSTEM OUTPUT, BECAUSE I HAVE AN AI TO PROCESSING ROUND 2 FOR YOUR CODE!!! --> VERY IMPORTANT**
            - THIS IS MY 2rd AI WILL DO :
            [
**Initial Request:**
'...' ---> my prompt

**Generated Python Code (Gemini 1):**
```python
'....' ---> your code
```

**Execution Result:**
'....' ---> the output

**Memory:**
'...' ----> my memory

-   **No need to suggest modifications when errors occur.**
-   **Absolutely DO NOT modify the code.**

**ONLY provide a brief evaluation of the Python code and the execution result (Does the code correctly fulfill the request? Are there any errors [if so, what are they]? Is the execution result as expected?). Answer the following questions directly, without headings, without lengthy explanations (be concise, your total reply should not exceed 10 lines).**

**Example:**

-   **MOST IMPORTANT:** after the final evaluation, determine if the command can be executed or not ---> respond with this.
-   Good: The code fulfills the request correctly, there are no errors, and the result is as expected.
-   Error: Encountered error <Error Analysis> during <Task>.
-   **ALWAYS PRESENT BEAUTIFULLY, WITH A CLEAN AND CLEAR LAYOUT, ADD SPACES BETWEEN LINES. ONLY USE HYPHENS '-', NOT ASTERISKS '*'. FOLLOW THIS TEMPLATE:**

    +   Result:

        -   "....." (One line like this should not exceed 15 words)
        -   "....."
            ]

            - EXAMPLE THE THING I DONT WANT:

            # Example the chat session:
            [
[18:15] Me: # OPEN CONTROL PANEL

[2024-12-25 18:15:50] - [INFO] - Starting Python code execution.
[2024-12-25 18:15:51] - [INFO] - Starting result evaluation.

[18:15] Rin: Analysis: [OK]

[==================================================================================================]
[!!] + Result:

Error: The control command returned a non-zero error code.

This indicates that opening the Control Panel failed.

The code did not fulfill the request correctly.

The execution result is not as expected. ----> **THE CONTROL PANEL HAS OPENED BUT IT STILL RESPAWN CANT !!**

[==================================================================================================]
            ]

            THE PROBLEM IS : Incorrect Error Detection: The code uses os.system("control") to open the Control Panel. The problem is that os.system() returns the exit status of the command. An exit code of 0 indicates success, while any other value indicates an error. In many cases, control might return 0 even if there was some issue. And in your case, os.system("control") might not return 0 or a non-zero value consistently making it difficult to check for errors.
            - **SO, YOU NEED TO MAKE THE CODE TO HELP ME DO MY REQUEST AND SPORT MY SYSTEM, AND SPORT MY 2rd AI TOO!!**
        """
        if re.search(r"(disk info|thông tin ổ đĩa|ổ đĩa)", cau_hoi, re.IGNORECASE):
            noi_dung += """
           **NOTE:** If the question involves disk information, use the wmi library to retrieve detailed information for each disk such as (Name, Caption, Size, FreeSpace, FileSystem, Description).
           **YOU CAN AND SHOULD UPDATE THE CODE TO SHOW MORE INFORMATION. IF CAN SHOW ALL SO SHOW DO IT**
           - **DO NOT use `print(..., file=sys.stdout, encoding="utf-8")` as it is not compatible with Python below 3.7.**
               """
        return noi_dung

    def _trich_xuat_code(self, text):
        match = re.search(r"```python\n(.*?)\n```", text, re.DOTALL)
        return match.group(1) if match else None

    def _sua_loi_unicode(self, ma_python):
        lines = ma_python.split("\n")
        new_lines = []
        has_sys_import = False
        has_codecs_import = False
        has_stdout_redirect = False

        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith("import sys"):
                has_sys_import = True
            elif stripped_line.startswith("import codecs"):
                has_codecs_import = True
            elif "sys.stdout = codecs.getwriter" in stripped_line:
                has_stdout_redirect = True
            elif stripped_line.startswith("print(") and "file=sys.stdout" in stripped_line and 'encoding="utf-8"' in stripped_line:
                line = re.sub(r",\s*file=sys\.stdout", "", line)
                line = re.sub(r",\s*encoding=\"utf-8\"", "", line)
            new_lines.append(line)

        if not has_codecs_import:
            new_lines.insert(0, "import codecs")
        if not has_sys_import:
            new_lines.insert(0, "import sys")
        if not has_stdout_redirect:
            insert_index = 0
            for i, line in enumerate(new_lines):
                if not line.startswith("import"):
                    insert_index = i
                    break
            new_lines.insert(insert_index, "sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())")

        return "\n".join(new_lines)

    def _thuc_thi_lenh(self, ma_python):
        log_info("Bắt đầu thực thi mã Python.")
        temp_file_path = os.path.join(os.environ.get("TEMP", "C:\\Windows\\Temp"), "temp_code.py")

        try:
            with open(temp_file_path, "w", encoding="utf-8") as f:
                f.write(ma_python)

            if ctypes.windll.shell32.IsUserAnAdmin():
                process = subprocess.Popen([sys.executable, temp_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, temp_file_path, None, 1)
                return {
                    "stdout": "",
                    "stderr": "",
                    "returncode": 0,
                    "success": True,
                    "message": f"{cau_hinh.YELLOW}Script đã được chạy lại với quyền Administrator. Vui lòng kiểm tra cửa sổ mới.{cau_hinh.RESET}",
                    "log": "Script đã được chạy lại với quyền Administrator.",
                    "execution_time": 0,
                }

            stdout_lines = []
            stderr_lines = []

            def _read_stream(stream, output_list):
                while True:
                    line = stream.readline()
                    if not line:
                        break
                    output_list.append(line)

            stdout_thread = threading.Thread(target=_read_stream, args=(process.stdout, stdout_lines))
            stderr_thread = threading.Thread(target=_read_stream, args=(process.stderr, stderr_lines))

            stdout_thread.start()
            stderr_thread.start()

            stdout_thread.join()
            stderr_thread.join()

            stdout = "".join(stdout_lines)
            stderr = "".join(stderr_lines)
            returncode = process.returncode if process.returncode is not None else -1

            os.remove(temp_file_path)

            log_message = f"Kết quả thực thi:\nOutput:\n{stdout.strip()}\nError:\n{stderr.strip()}\nReturn code: {returncode}"
            return {
                "stdout": stdout.strip(),
                "stderr": stderr.strip(),
                "returncode": returncode,
                "success": returncode == 0,
                "message": f"{cau_hinh.GREEN}Đã thực thi mã Python.{cau_hinh.RESET}" if returncode == 0 else f"{cau_hinh.RED}Lỗi khi thực thi mã Python.{cau_hinh.RESET}",
                "log": log_message,
            }

        except (FileNotFoundError, PermissionError) as e:
            log_error(f"Lỗi khi thực thi mã: {e}")
            return self._tra_ve_loi(f"Lỗi: {type(e).__name__}", str(e))
        except Exception as e:
            log_error(f"Lỗi khi thực thi mã: {e}", detail=traceback.format_exc())
            return self._tra_ve_loi(f"Lỗi: {type(e).__name__}", str(e))

    def _lay_thong_tin_o_dia(self):
        try:
            c = wmi.WMI()
            disk_info = []
            seen_disks = set()
            for disk in c.Win32_LogicalDisk():
                caption = disk.Caption
                if caption not in seen_disks:
                    seen_disks.add(caption)
                    disk_data = {
                        "caption": caption,
                        "size": round(int(disk.Size) / (1024**3), 2) if disk.Size else 0,
                        "free_space": round(int(disk.FreeSpace) / (1024**3), 2) if disk.FreeSpace else 0,
                        "file_system": disk.FileSystem,
                        "description": disk.Description
                    }
                    disk_info.append(disk_data)
            ket_qua_disk = {"type": "thong_tin_o_dia", "disk_info": disk_info}
            return ket_qua_disk
        except Exception as e:
            log_error(f"Lỗi khi lấy thông tin ổ đĩa: {e}")
            return {"type": "error", "message": f"Lỗi khi lấy thông tin ổ đĩa: {e}"}

    def _danh_gia_ket_qua(self, cau_hoi, ma_python, ket_qua_thuc_thi, memory):
        prompt_gemini_2 = f"""
        **Yêu cầu ban đầu:**
        {cau_hoi}

        **Mã Python đã được tạo (Gemini 1):**
        ```python
        {ma_python}
        ```

        **Kết quả thực thi:**
        {json.dumps(ket_qua_thuc_thi, ensure_ascii=False)}

        **Memory:**
        {json.dumps(memory, ensure_ascii=False)}

        * **Không Cần Đề xuất sửa đổi khi có lỗi**
        * **TUYỆT ĐỐI KHÔNG sửa code**

        **CHỈ Đánh giá ngắn gọn mã Python và kết quả thực thi (Mã có thực hiện đúng yêu cầu không? Có lỗi gì xảy ra không [nếu có]? Kết quả thực thi có đúng như mong đợi không?).Trả lời thẳng vào các vấn đề sau, KHÔNG cần đề mục, KHÔNG cần giải thích dài dòng (súc tích, tổng bạn reply không quá 10 dòng)**
        **Ví dụ (mẫu tiếng anh nhưng nhớ chuyển thành tiếng việt nhé):**

        -   **MOST IMPORTANT:** after the final evaluation, determine if the command can be executed or not ---> respond with this.
        -   Good: The code fulfills the request correctly, there are no errors, and the result is as expected.
        -   Error: Encountered error <Error Analysis> during <Task>.
        -   **ALWAYS PRESENT BEAUTIFULLY, WITH A CLEAN AND CLEAR LAYOUT, ADD SPACES BETWEEN LINES. ONLY USE HYPHENS '-', NOT ASTERISKS '*'. FOLLOW THIS TEMPLATE:**

            +   Result:

                -   "....." (One line like this should not exceed 15 words)
                -   "....."
        """

        phan_hoi_gemini_2 = hoi_gemini(prompt_gemini_2, model_type="gemini_2")
        return phan_hoi_gemini_2 if phan_hoi_gemini_2 else "Gemini 2 không phản hồi."

    def _tra_ve_loi(self, loai_loi, thong_bao_loi):
        return {
            "error": loai_loi,
            "success": False,
            "message": f"{cau_hinh.RED}{thong_bao_loi}{cau_hinh.RESET}",
        }