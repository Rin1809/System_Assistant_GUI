import subprocess
import platform
from utils import cau_hinh
from utils.nhat_ky import log_info, log_error
from core.chat import hoi_gemini
import time
import json
import re
import asyncio
import sys
from core import chat

class ThucThiLenhHeThong:
    def __init__(self):
        self.ten = "thực thi lệnh hệ thống"

    def _chay_lenh(self, command):
        """
        Chạy lệnh hệ thống (nội bộ, không phải API).
        """
        try:
            # thu thi tren win == powershell
            process = subprocess.Popen(
                ["powershell.exe", "-Command", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            stdout, stderr = process.communicate()
            returncode = process.returncode
            return {
                "stdout": stdout.strip(),
                "stderr": stderr.strip(),
                "returncode": returncode
            }
        except Exception as e:
            log_error(f"Lỗi khi thực thi lệnh: {command} - {e}")
            return {
                "stdout": "",
                "stderr": f"Lỗi: {e}",
                "returncode": -1
            }

    async def thuc_thi(self, cau_hoi, memory):
        """
        API để thực thi lệnh hệ thống (sử dụng Gemini để tạo lệnh).
        """
        log_info(f"Thực thi lệnh hệ thống: {cau_hoi}")

        system = platform.system()
        version = sys.getwindowsversion()
        version_str = f"{version.build}.{version.major}.{version.minor}-{version.service_pack}"
        prompt = self._tao_prompt(cau_hoi, memory, system, version_str)

        # gui promt toi model 1
        phan_hoi = hoi_gemini(prompt)
        if not phan_hoi:
            return self._tra_ve_loi("Gemini không phản hồi", "Gemini không phản hồi.")

        command = self._phan_tich_phan_hoi(phan_hoi)
        # Kiểm tra lệnh rỗng
        if not command:
            return self._tra_ve_loi("Lệnh rỗng", "Không thể tạo ra lệnh từ yêu cầu.")

        start_time = time.time()  # Bắt đầu tính thời gian
        ket_qua = self._chay_lenh(command)
        end_time = time.time()  # Kết thúc tính thời gian
        execution_time = end_time - start_time  # Tính thời gian thực thi

        # comment cua model 2
        ket_qua["gemini_2_validation"] = self._danh_gia_ket_qua(cau_hoi, command, ket_qua, memory)
        self._luu_memory(cau_hoi, command, ket_qua, memory)
        ket_qua_tra_ve = self._tao_ket_qua_tra_ve(ket_qua)

        ket_qua_tra_ve["execution_time"] = execution_time
        ket_qua_tra_ve["plugin_name"] = "Thực thi lệnh hệ thống"
        return ket_qua_tra_ve


    def _tao_prompt(self, cau_hoi, memory, system, version_str):
        prompt = f"""
        You are a command line expert on the {system} operating system, version {version_str}.
        Please generate only one PowerShell command line to fulfill the following request: {cau_hoi}.
        Don't explain, just generate a PowerShell command line that can be executed directly.
        Note that:
        - **"OPEN" IS NOT ALLWAY AN "APP"!!*
        - **OPEN PROGRAM IS NOT JUST IN C:\\ DISK AND CAN BE DIFFERENT NAME (ex: "unikey" BUT ACTUALLY IS "UnikeyNT" so you should find the different name of that project too), YOU MUST BE CHECK HAVE CHECK ALL DISK IN COMPUTER**
        - **IF OPEN OR EXECUTE A PROGRAM, DONT NEED TO WRITE `Start-Process`**
        - **DONT NEED TO WRITE A COMMENT IN OUTPUT!**
        - **IF SEE A '{cau_hinh.RICH_PINK}vietnamese{cau_hinh.RESET}', YOU NEED TO TRANSLATE TO ENGLISH BEFORE RESPONSE**
        - **OUTPUT IS POWERSHELL (ADMINISTRATOR) NOT BATCH OR COMMAND PROMT**
        - **REMEMBER USE START-PROCESS WITH -FILEPATH**
        - **Here are some examples of PowerShell commands related to system administration:**
          - Get information about a process: `Get-Process -Name <process_name>`
          - Stop a process: `Stop-Process -Name <process_name> -Force`
          - Get Windows services: `Get-Service`
          - Start a service: `Start-Service -Name <service_name>`
          - Stop a service: `Stop-Service -Name <service_name>`
          - Get disk information: `Get-Partition | Select-Object DiskNumber, PartitionNumber, Size, Type`
          - Get network adapter information: `Get-NetAdapter | Select-Object Name, Status, LinkSpeed`
          - Get firewall status: `Get-NetFirewallProfile | Select-Object Name, Enabled`
          - Open Event Viewer: `Start-Process -FilePath eventvwr.msc`
          - Open Disk Management: `Start-Process -FilePath diskmgmt.msc`
          - Open Task Scheduler: `Start-Process -FilePath taskschd.msc`
          - **To open PowerShell, use the command: `Start-Process powershell`**

        Please generate a PowerShell command that is relevant to the user's request and can run on {system} {version_str}.
        **DO NOT ADD THE COMMAND INTO THE:
        [
        ```power
        <command>
        ```
        ]
        **Response with just the command with no any character else!!**
        """
        if memory:
            prompt += f"\nThe memory from the previous command, you can use these to make command better: {json.dumps(memory, ensure_ascii=False)}"
        return prompt

    def _phan_tich_phan_hoi(self, phan_hoi):
        command = phan_hoi.replace("```", "").replace("powershell", "").strip()
        log_info(f"Lệnh được tạo: {command}")
        return command

    def _danh_gia_ket_qua(self, cau_hoi, command, ket_qua, memory):
        prompt_gemini_2 = f"""
        **Yêu cầu ban đầu (User):**
        {cau_hoi}

        **Lệnh PowerShell đã tạo ra (Gemini 1):**
        `{command}`

        **Kết quả thực thi:**
        {json.dumps(ket_qua, ensure_ascii=False)}

        **Memory:**
        {json.dumps(memory, ensure_ascii=False)}

        **Đánh giá kết quả và phân tích lỗi (nếu có, response bằng tiếng việt, đánh giá kết quả cuối cùng bằng tiếng việt luôn).**
        -   **MOST IMPORTANT:** after the final evaluation, determine if the command can be executed or not ---> respond with this.
        -   Good: The code fulfills the request correctly, there are no errors, and the result is as expected.
        -   Error: Encountered error <Error Analysis> during <Task>.
        -   **ALWAYS PRESENT BEAUTIFULLY, WITH A CLEAN AND CLEAR LAYOUT, ADD SPACES BETWEEN LINES. ONLY USE HYPHENS '-', NOT ASTERISKS '*'. FOLLOW THIS TEMPLATE:**

            +   Result:

                -   "....." (One line like this should not exceed 15 words)
                -   "....."
        * ** và nếu có như này:
        [

        ```powershell
        abcxyz....
        ```
        ]

        hoặc:
        [
        `power`
        ]
         thì cứ bỏ qua, nó không phải lỗi đâu...
        """
        phan_hoi_gemini_2 = hoi_gemini(prompt_gemini_2, model_type="gemini_2")
        return phan_hoi_gemini_2 if phan_hoi_gemini_2 else "Gemini 2 không phản hồi."

    def _luu_memory(self, cau_hoi, command, ket_qua, memory):
        memory_item = {
            "loại": "lệnh hệ thống",
            "câu hỏi": cau_hoi,
            "lệnh": command,
            "kết quả": ket_qua,
        }
        memory.append(memory_item)

    def _tao_ket_qua_tra_ve(self, ket_qua):
        if ket_qua["returncode"] == 0:
            message = f"{cau_hinh.GREEN}Thực thi thành công{cau_hinh.RESET}"
        else:
            if ket_qua['stderr']:
                message = f"{cau_hinh.ERROR}Lỗi: {ket_qua['stderr']}"
            else:
                message = f"{cau_hinh.ERROR}Lỗi: Lệnh thực thi không thành công với mã lỗi {ket_qua['returncode']}"

        ket_qua["message"] = message
        ket_qua["gemini_2_validation"] = ket_qua.get("gemini_2_validation", "Không có đánh giá.")
        return ket_qua

    def _tra_ve_loi(self, loai_loi, thong_bao_loi):
        return {
            "success": False,
            "message": f"{cau_hinh.ERROR}{thong_bao_loi}{cau_hinh.RESET}",
            "output": "",
            "error": loai_loi,
            "gemini_2_validation": "Không có đánh giá.",
        }