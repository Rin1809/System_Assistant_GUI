# System_Assistant_GUI - Trợ lý Ảo Cá Nhân Giao Diện Web ᓚᘏᗢ

## I want to know how many user that my computer have, but i forgot the command or where can i check it, ưhat should do?
![image](https://github.com/user-attachments/assets/d141d003-1d1b-4244-b795-a1f1f141f46e)


<details>
<summary>🇻🇳 Tiếng Việt</summary>

## 1. Giới thiệu

**System_Assistant_GUI** (tên mã **Rin Web**) là phiên bản giao diện người dùng đồ họa (GUI) trên nền web của dự án **Assistant**. Dự án này vẫn giữ nguyên sức mạnh cốt lõi của trợ lý ảo Rin, sử dụng mô hình ngôn ngữ lớn Gemini, nhưng cung cấp một giao diện web trực quan và dễ tương tác hơn, cho phép người dùng điều khiển và làm việc với Rin thông qua trình duyệt web.

**Mục tiêu chính của System_Assistant_GUI (Rin Web):**

- **Trải nghiệm người dùng thân thiện:** Mang đến trải nghiệm tương tác trợ lý ảo mượt mà và trực quan thông qua giao diện web, thay vì dòng lệnh thuần túy.
- **Dễ dàng truy cập:** Cho phép truy cập trợ lý ảo Rin từ bất kỳ thiết bị nào có trình duyệt web, mở rộng khả năng sử dụng và tính linh hoạt.
- **Giữ nguyên sức mạnh cốt lõi:** Bảo toàn toàn bộ tính năng mạnh mẽ của phiên bản dòng lệnh (CLI), bao gồm thực thi lệnh hệ thống, chạy mã Python, xử lý file, và tích hợp Gemini AI.
- **Tùy biến và Mở rộng:**  Tiếp tục hỗ trợ kiến trúc plugin, cho phép mở rộng và tùy chỉnh chức năng dễ dàng.

**System_Assistant_GUI (Rin Web) dành cho:**

- **Người dùng ưa thích giao diện đồ họa:** Mong muốn tương tác với trợ lý ảo qua giao diện web trực quan thay vì dòng lệnh.
- **Người dùng cần truy cập đa nền tảng:** Muốn sử dụng trợ lý ảo Rin trên nhiều thiết bị (máy tính, máy tính bảng, điện thoại) thông qua trình duyệt web.
- **Người dùng mới bắt đầu:** Giao diện web có thể giúp người dùng mới làm quen và sử dụng các tính năng của Rin dễ dàng hơn.

## 2. Tính năng

**System_Assistant_GUI (Rin Web)** kế thừa và mở rộng các tính năng của phiên bản dòng lệnh, với giao diện web tập trung vào trải nghiệm người dùng:

- **Giao diện Web Trực quan:** Giao diện web đơn giản, dễ sử dụng, cho phép nhập lệnh và xem kết quả trực tiếp trên trình duyệt.
- **Thực thi lệnh hệ thống (@):** Chạy lệnh PowerShell (Windows) thông qua ô nhập lệnh web.
- **Thực thi mã Python ($):** Tạo và chạy mã Python trực tiếp từ giao diện web.
- **Xử lý file nâng cao (#):** Tương tác và xử lý file (đọc, ghi, sửa...) thông qua lệnh web.
- **Hiển thị Kết quả Chi tiết:** Kết quả trả về được định dạng rõ ràng, phân chia theo các phần (thông báo, phân tích, output, lỗi, code...), dễ đọc và dễ hiểu trên giao diện web.
- **Lịch sử Phiên Chat:** Lưu trữ và hiển thị lịch sử tương tác trong phiên làm việc, giúp theo dõi và xem lại các lệnh và phản hồi trước đó.
- **Tích hợp Gemini (Google AI):** Sử dụng Gemini để xử lý ngôn ngữ tự nhiên và thực hiện các tác vụ thông minh.
- **Hỗ trợ Memory:**  Duy trì memory phiên làm việc, cải thiện khả năng tương tác và hiểu ngữ cảnh của trợ lý ảo.
- **Plugin Kiến trúc:** Hỗ trợ plugin tương tự phiên bản CLI, dễ dàng mở rộng chức năng.
- **Giao diện Tùy biến:** Cho phép tùy chỉnh giao diện web qua file CSS (`static/style.css`).
- **Thông báo Lỗi và Phân tích:** Hiển thị thông báo lỗi chi tiết và phân tích kết quả (từ Gemini 2) ngay trên giao diện web.

## 3. Cấu trúc Dự án

```
System_Assistant_GUI/
├── .git/             (Thư mục Git - không liệt kê khi tạo tài liệu)
├── .gitignore        (File chỉ định các tệp/thư mục Git bỏ qua)
├── bieutuong/         (Thư mục chứa biểu tượng, hình ảnh - không liệt kê)
├── cac_plugin/       (Thư mục plugin chức năng)
│   ├── thuc_thi_lenh_he_thong.py (Plugin lệnh hệ thống PowerShell)
│   ├── thuc_thi_python.py     (Plugin mã Python)
│   ├── xu_ly_file_plugin.py   (Plugin xử lý file nâng cao)
│   ├── __init__.py
│   └── __pycache__/         (Thư mục cache Python - không liệt kê)
├── core/              (Thư mục mã nguồn core)
│   ├── chat.py         (Module giao tiếp Gemini)
│   ├── __init__.py
│   └── __pycache__/         (Thư mục cache Python - không liệt kê)
├── memory/            (Thư mục lưu trữ memory - không liệt kê)
├── moitruongao/       (Thư mục môi trường ảo Python - không liệt kê)
├── rin.py             (File dòng lệnh, vẫn tồn tại để tham khảo)
├── run.bat            (Batch script chạy CLI - không dùng cho GUI)
├── static/            (Thư mục chứa file tĩnh cho web)
│   ├── style.css      (File CSS tùy chỉnh giao diện web)
├── templates/         (Thư mục chứa template HTML)
│   ├── index.html     (Template HTML chính cho giao diện web)
├── utils/             (Thư mục tiện ích)
│   ├── animation/      (Thư mục hiệu ứng động)
│   │   ├── hieu_ung.py  (Module hiệu ứng động)
│   │   └── __init__.py
│   │   └── __pycache__/     (Thư mục cache Python - không liệt kê)
│   ├── cau_hinh.py     (File cấu hình)
│   ├── nhat_ky.py      (Module nhật ký)
│   ├── rin.bat        (Batch script phụ trợ)
│   ├── __init__.py
│   └── __pycache__/     (Thư mục cache Python - không liệt kê)
├── web_rin.py         (File mã nguồn chính cho giao diện web Flask)
├── __init__.py
```

- **`.git/`, `.gitignore`, `bieutuong/`, `cac_plugin/`, `core/`, `memory/`, `moitruongao/`, `utils/__pycache__/`, `rin.py`, `run.bat`, `utils/rin.bat`, `utils/__init__.py`, `__init__.py` (cac_plugin), `core/__init__.py`**: Tương tự như cấu trúc của dự án **Assistant** CLI.
- **`static/`**: Thư mục chứa các file tĩnh phục vụ cho giao diện web, ví dụ:
    - **`style.css`**: File CSS để tùy chỉnh giao diện (màu sắc, bố cục...) của trang web.
- **`templates/`**: Thư mục chứa các template HTML:
    - **`index.html`**: File HTML template chính cho giao diện trang web của trợ lý ảo Rin. Sử dụng Jinja2 template engine để hiển thị dữ liệu động từ Python.
- **`web_rin.py`**: File Python chính để khởi chạy ứng dụng web Flask. File này xử lý routing, logic giao diện web, và tích hợp các plugin chức năng giống như `rin.py` ở phiên bản CLI.

## 4. Cài đặt

### Điều kiện tiên quyết

Tương tự như phiên bản dòng lệnh, bạn cần đảm bảo:

1.  **Python:** Python 3.8+. [https://www.python.org/downloads/](https://www.python.org/downloads/)
2.  **pip:** (Đi kèm Python).
3.  **Gemini API Key:**  Cần có API key Gemini, đặt vào `utils/cau_hinh.py`.

### Các bước cài đặt

1. **Tải Dự án:** Tải mã nguồn dự án **System_Assistant_GUI** từ GitHub.

   ```bash
   git clone https://github.com/Rin1809/System_Assistant_GUI/
   cd System_Assistant_GUI
   ```

2. **Tạo và Kích hoạt Môi trường Ảo:** Tương tự phiên bản CLI, tạo và kích hoạt môi trường ảo `moitruongao`. Xem lại hướng dẫn chi tiết ở phần Cài đặt của file `README.md` cho dự án **Assistant** (phiên bản CLI).

3. **Cài đặt Thư viện:** Cài đặt thư viện cần thiết, bao gồm cả Flask (cho giao diện web) và các thư viện core của Rin:

   ```bash
   pip install -r requirements.txt # Nếu có file requirements.txt

   # Hoặc cài thủ công nếu không có file:
   pip install flask google-generativeai pygments python-magic python-docx openpyxl rich psutil watchdog wmi
   ```

4. **Cấu hình API Key:** Tương tự phiên bản CLI, mở `utils/cau_hinh.py` và điền API key Gemini vào biến `API_KEY`.

5. **Chạy Ứng dụng Web:**

   - **Windows (khuyến khích):** Chạy file `run.bat`. File này sẽ kích hoạt môi trường ảo và khởi chạy ứng dụng web Rin.

   - **Mọi hệ điều hành (sau kích hoạt môi trường ảo):** Chạy lệnh:

     ```bash
     python web_rin.py
     ```

     Ứng dụng web Rin sẽ chạy. Mở trình duyệt và truy cập địa chỉ hiển thị trên dòng lệnh (thường là `http://127.0.0.1:5000/` hoặc `http://0.0.0.0:5000/`).

## 5. Cách Sử dụng

**Giao diện Web của Assistant (Rin Web):**

Sau khi chạy `web_rin.py` hoặc `run.bat`, mở trình duyệt và truy cập địa chỉ được cung cấp. Bạn sẽ thấy giao diện web của Rin:

Giao diện web bao gồm:

1. **Ô Nhập Lệnh/Câu Hỏi:**  Textbox lớn ở đầu trang để bạn nhập các lệnh hoặc câu hỏi cho Rin. Sử dụng các tiền tố `@`, `$`, `#` tương tự như phiên bản CLI (mô tả ở phần Cách Sử dụng của README CLI).

2. **Nút "Gửi":** Nút để gửi lệnh/câu hỏi sau khi đã nhập vào textbox.

3. **Khu vực Hiển thị Output:** Phần lớn dưới ô nhập lệnh, hiển thị kết quả phản hồi từ Rin. Output được định dạng rõ ràng với các section (Thông báo, Phân tích, Output, Code, v.v.) để dễ đọc.

4. **Lịch sử Phiên Chat:** Khu vực ở cuối trang, hiển thị lịch sử các tương tác trong phiên làm việc hiện tại, giúp bạn xem lại các lệnh và phản hồi trước đó.

**Quy trình sử dụng:**

1. **Nhập lệnh/câu hỏi:**  Gõ câu hỏi hoặc lệnh của bạn vào ô textbox. Nhớ sử dụng các tiền tố `@`, `$`, `#` để gọi các plugin chức năng cụ thể (nếu muốn).
2. **Nhấn "Gửi":** Nhấn nút "Gửi" hoặc phím Enter để gửi lệnh/câu hỏi đến Rin.
3. **Xem Kết quả:**  Kết quả phản hồi từ Rin sẽ được hiển thị trong khu vực "output-area" phía dưới, và lịch sử phiên chat sẽ được cập nhật ở cuối trang.
4. **Lặp lại:** Tiếp tục nhập lệnh mới và tương tác với Rin.
5. **Đóng Trình duyệt:** Đóng tab hoặc cửa sổ trình duyệt để kết thúc phiên làm việc (ứng dụng web Rin vẫn chạy ở server cho đến khi bạn tắt tiến trình Python).

**Lưu ý:**

- Giao diện web có thể được tùy chỉnh bằng cách chỉnh sửa file `static/style.css`.
- Cách sử dụng các lệnh (tiền tố `@`, `$`, `#`, cú pháp, v.v.) tương tự như phiên bản CLI. Tham khảo phần "Cách Sử dụng" của `README.md` cho dự án **Assistant** (phiên bản dòng lệnh) để biết chi tiết.
- Để thoát hoàn toàn ứng dụng web Rin (tắt server Flask), bạn cần dừng tiến trình Python `web_rin.py` trong dòng lệnh (ví dụ, bằng Ctrl+C).

## 6. Ví dụ Sử dụng

Các ví dụ sau minh họa cách tương tác với **System_Assistant_GUI (Rin Web)** qua giao diện trình duyệt:

**(Lưu ý: Các ví dụ này tương tự về lệnh với phiên bản CLI, chỉ khác về giao diện tương tác là web.)**

**Ví dụ 1: Hỏi thông tin thời tiết:**

- Nhập vào ô textbox: `thời tiết Hà Nội ngày mai thế nào?`
- Nhấn "Gửi".
- Kết quả hiển thị trong khu vực "output-area":  Rin sẽ trả lời thông tin thời tiết dự báo cho Hà Nội, với định dạng web đẹp mắt.

**Ví dụ 2: Mở ứng dụng bằng lệnh hệ thống:**

- Nhập: `@mở máy tính`
- Nhấn "Gửi".
- Kết quả hiển thị:  Rin thông báo thực thi lệnh thành công, và File Explorer (This PC) sẽ được mở trên máy tính. Thông tin chi tiết (phân tích, output...) cũng hiển thị trên web.

**Ví dụ 3: Lấy thông tin ổ đĩa bằng Python:**

- Nhập: `$viết code python in ra dung lượng ổ đĩa C và D`
- Nhấn "Gửi".
- Kết quả hiển thị: Rin sẽ chạy code Python, và hiển thị thông tin dung lượng ổ đĩa C và D (kích thước, dung lượng trống...) dưới dạng bảng hoặc danh sách trên web.

**Ví dụ 4: Đọc nội dung file code Python:**

- Nhập: `#đọc file "core/chat.py"`
- Nhấn "Gửi".
- Kết quả hiển thị: Nội dung file `core/chat.py` (mã Python) sẽ được hiển thị trong khu vực output, có thể kèm syntax highlighting (tùy thuộc vào khả năng của thư viện highlight code trên web - hiện tại ví dụ không có highlight syntax).

**Ví dụ 5: Chỉnh sửa file text:**

- Nhập: `#sửa file "example_web.txt" thêm "--- Thêm dòng mới từ giao diện web ---" vào cuối`
- Nhấn "Gửi".
- Kết quả hiển thị: Thông báo chỉnh sửa file thành công, file `example_web.txt` (trong thư mục dự án) sẽ được cập nhật với dòng text mới thêm vào cuối.

**Khám phá thêm:**

Thử nghiệm với các lệnh khác nhau qua giao diện web, tận dụng các plugin, và tùy chỉnh giao diện để trải nghiệm toàn bộ tiềm năng của **System_Assistant_GUI (Rin Web)**.

## 7. Cấu hình Nâng cao

- **File cấu hình `utils/cau_hinh.py`:**  Tương tự phiên bản CLI, file này cấu hình API Key Gemini, model, nhiệt độ, các tham số Gemini, màu sắc, v.v. Các cấu hình này ảnh hưởng đến cả phiên bản web và CLI.

- **Tùy chỉnh giao diện web (`static/style.css`):** Bạn có thể tùy chỉnh hoàn toàn giao diện web của Rin bằng cách chỉnh sửa file CSS `static/style.css`. Thay đổi màu sắc, font chữ, bố cục, v.v. để tạo giao diện theo ý muốn.

- **Plugin kiến trúc (`cac_plugin/`):**  Phiên bản web **System_Assistant_GUI** sử dụng lại hệ thống plugin giống như bản CLI. Bạn có thể phát triển thêm plugin mới trong thư mục `cac_plugin/` để mở rộng chức năng (xem các plugin mẫu). Các plugin này sẽ hoạt động trên cả giao diện web và CLI.

- **Chạy trên Port và Host khác (web_rin.py):**  Nếu muốn chạy ứng dụng web trên port hoặc host khác (ví dụ, để truy cập từ xa), bạn có thể chỉnh sửa dòng `app.run(debug=True, host='0.0.0.0', port=5000)` trong file `web_rin.py`. Thay đổi `host` và `port` theo nhu cầu. `host='0.0.0.0'` cho phép truy cập từ bên ngoài (mạng LAN), `host='127.0.0.1'` (hoặc `'localhost'`) chỉ cho phép truy cập từ máy cục bộ.

</details>

<details>
<summary>🇬🇧 English</summary>

## 1. Introduction

**System_Assistant_GUI** (codename **Rin Web**) is the web-based Graphical User Interface (GUI) version of the **Assistant** project. This project retains the core power of the Rin virtual assistant, utilizing the Gemini large language model, but provides a more intuitive and user-friendly web interface, allowing users to control and interact with Rin through a web browser.

**The main goals of System_Assistant_GUI (Rin Web):**

- **User-Friendly Experience:** Deliver a smooth and intuitive virtual assistant interaction experience through a web interface, instead of a pure command line.
- **Easy Access:** Allow access to Rin virtual assistant from any device with a web browser, expanding usability and flexibility.
- **Retain Core Power:** Preserve all the powerful features of the Command-Line Interface (CLI) version, including system command execution, Python code execution, file processing, and Gemini AI integration.
- **Customizable and Extensible:** Continue to support plugin architecture, allowing for easy function expansion and customization.

**System_Assistant_GUI (Rin Web) is intended for:**

- **Users Preferring Graphical Interfaces:** Who desire to interact with a virtual assistant via an intuitive web interface instead of a command line.
- **Users Needing Cross-Platform Access:** Who want to use Rin virtual assistant on multiple devices (computers, tablets, phones) through a web browser.
- **Beginner Users:** The web interface can help new users get acquainted with and use Rin's features more easily.

## 2. Features

**System_Assistant_GUI (Rin Web)** inherits and extends the features of the command-line version, with the web interface focusing on user experience:

- **Intuitive Web Interface:** Simple, easy-to-use web interface allows for entering commands and viewing results directly in the browser.
- **System Command Execution (@):** Run PowerShell commands (Windows) via the web command input box.
- **Python Code Execution ($):** Create and run Python code snippets directly from the web interface.
- **Advanced File Processing (#):** Interact with and process files (read, write, edit...) via web commands.
- **Detailed Result Display:**  Return results are clearly formatted, divided into sections (message, analysis, output, error, code...), easy to read and understand on the web interface.
- **Session History:** Stores and displays interaction history within the current session, helping to track and review previous commands and responses.
- **Gemini Integration (Google AI):** Uses the power of Gemini to understand natural language and perform intelligent tasks.
- **Memory Support:**  Maintains session memory, improving the virtual assistant's interaction ability and context understanding.
- **Plugin Architecture:** Plugin support similar to the CLI version, easily adding new functionalities and extensions.
- **Customizable Interface:** Allows for customizing the web interface via CSS file (`static/style.css`).
- **Error Notifications and Analysis:** Display detailed error messages and result analysis (from Gemini 2) directly on the web interface.

## 3. Project Structure

```
System_Assistant_GUI/
├── .git/             (Git Directory - not listed in documentation)
├── .gitignore        (File specifying files/directories Git should ignore)
├── bieutuong/         (Directory containing icons, images - not listed)
├── cac_plugin/       (Directory of function plugins)
│   ├── thuc_thi_lenh_he_thong.py (PowerShell system command plugin)
│   ├── thuc_thi_python.py     (Python code plugin)
│   ├── xu_ly_file_plugin.py   (Advanced file processing plugin)
│   ├── __init__.py
│   └── __pycache__/         (Python cache directory - not listed)
├── core/              (Core source code directory)
│   ├── chat.py         (Gemini communication module)
│   ├── __init__.py
│   └── __pycache__/         (Python cache directory - not listed)
├── memory/            (Memory storage directory - not listed)
├── moitruongao/       (Python virtual environment directory - not listed)
├── rin.py             (Command-line file, still present for reference)
├── run.bat            (Batch script to run CLI - not used for GUI)
├── static/            (Directory for static web files)
│   ├── style.css      (CSS file to customize web interface)
├── templates/         (Directory for HTML templates)
│   ├── index.html     (Main HTML template for web UI)
├── utils/             (Utility directory)
│   ├── animation/      (Directory for dynamic effects)
│   │   ├── hieu_ung.py  (Dynamic effects module)
│   │   └── __init__.py
│   │   └── __pycache__/     (Python cache directory - not listed)
│   ├── cau_hinh.py     (Configuration file)
│   ├── nhat_ky.py      (Logging module)
│   ├── rin.bat        (Auxiliary batch script)
│   ├── __init__.py
│   └── __pycache__/     (Python cache directory - not listed)
├── web_rin.py         (Main source file for Flask web interface)
├── __init__.py
```

- **`.git/`, `.gitignore`, `bieutuong/`, `cac_plugin/`, `core/`, `memory/`, `moitruongao/`, `utils/__pycache__/`, `rin.py`, `run.bat`, `utils/rin.bat`, `utils/__init__.py`, `__init__.py` (cac_plugin), `core/__init__.py`**: Similar to **Assistant** CLI project structure.
- **`static/`**: Directory for static files serving web interface, e.g.:
    - **`style.css`**: CSS file to customize the look and feel of the web page.
- **`templates/`**: Directory containing HTML templates:
    - **`index.html`**: Main HTML template for Rin web assistant UI. Uses Jinja2 template engine to render dynamic data from Python.
- **`web_rin.py`**: Main Python file to start Flask web application. This file handles routing, web UI logic, and integrates function plugins like `rin.py` in CLI version.

## 4. Installation

### Prerequisites

Similar to CLI version, ensure you have:

1.  **Python:** Python 3.8+. [https://www.python.org/downloads/](https://www.python.org/downloads/)
2.  **pip:** (Included with Python).
3.  **Gemini API Key:**  Gemini API key is required, put it in `utils/cau_hinh.py`.

### Installation Steps

1. **Download Project:** Download **System_Assistant_GUI** project source code from GitHub (or source).

   ```bash
   git clone https://github.com/Rin1809/System_Assistant_GUI/
   cd System_Assistant_GUI
   ```

2. **Create and Activate Virtual Environment:** Same as CLI version, create and activate `moitruongao` virtual environment. Refer to detailed instruction in "Installation" section of `README.md` for **Assistant** (CLI version).

3. **Install Libraries:** Install needed Python libraries, including Flask (for web UI) and core Rin libraries:

   ```bash
   pip install -r requirements.txt # If requirements.txt file exists

   # Or manual install if file is missing:
   pip install flask google-generativeai pygments python-magic python-docx openpyxl rich psutil watchdog wmi
   ```

4. **Configure API Key:** Same as CLI, open `utils/cau_hinh.py` and fill in Gemini API key into `API_KEY` variable.

5. **Run Web Application:**

   - **Windows (Recommended):** Run `run.bat` file. This activates virtual environment and starts Rin web app.

   - **Any OS (after activating virtual environment):** Run command:

     ```bash
     python web_rin.py
     ```

     Rin web app will run. Open browser and access the address shown in command line (usually `http://127.0.0.1:5000/` or `http://0.0.0.0:5000/`).

## 5. Usage

**Web Interface of Assistant (Rin Web):**

After running `web_rin.py` or `run.bat`, open a browser and navigate to provided address. You'll see Rin web UI:

Web interface includes:

1. **Command/Question Input Box:** Large textbox at the top for you to enter commands or questions for Rin. Use prefixes `@`, `$`, `#` same as CLI version (described in "Usage" of CLI README).

2. **"Send" Button:** Button to submit command/question after entering into textbox.

3. **Output Display Area:** Large section below input box, displaying Rin's response results. Output is neatly formatted into sections (Message, Analysis, Output, Code, etc.) for readability.

4. **Session History:** Section at the bottom, showing history of interactions in current session, helping you to track and review previous commands and responses.

**Usage Procedure:**

1. **Enter command/question:**  Type your question or command into the textbox. Remember to use prefixes `@`, `$`, `#` to invoke specific plugin functions (if desired).
2. **Click "Send":** Press "Send" button or Enter key to send command/question to Rin.
3. **View Results:**  Rin's response will be shown in "output-area" below, and session history will be updated at bottom of page.
4. **Repeat:** Continue entering new commands and interact with Rin.
5. **Close Browser:** Close browser tab or window to end session (Rin web app still runs on server until you terminate Python process).

**Note:**

- Web UI can be customized by editing `static/style.css` file.
- Command usages (prefixes `@`, `$`, `#`, syntax etc.) are similar to CLI version. Refer to "Usage" section of `README.md` for **Assistant** (CLI version) for details.
- To completely exit Rin web app (stop Flask server), you need to terminate `web_rin.py` Python process in command line (e.g., using Ctrl+C).

## 6. Usage Examples

Following examples show how to interact with **System_Assistant_GUI (Rin Web)** through web UI:

**(Note: These examples are similar in commands to CLI version, only difference is web-based interaction.)**

**Example 1: Asking weather information:**

- Enter in textbox: `how is Hanoi weather tomorrow?`
- Click "Send".
- Result in "output-area": Rin will respond with weather forecast information for Hanoi, web-formatted nicely.

**Example 2: Open application using system command:**

- Enter: `@open calculator`
- Click "Send".
- Result shown: Rin confirms command execution successful, and Calculator app should open on computer. Details (analysis, output...) are also shown on web UI.

**Example 3: Get disk information using Python:**

- Enter: `$write python code to print disk space on C and D drives`
- Click "Send".
- Result shown: Rin will run Python code and display disk space info for C and D drives (size, free space...) in a table or list on the web page.

**Example 4: Read content of Python code file:**

- Enter: `#read file "core/chat.py"`
- Click "Send".
- Result shown: Content of `core/chat.py` (Python code) will be displayed in output area, possibly with syntax highlighting (syntax highlighting in example might not be present).

**Example 5: Edit text file:**

- Enter: `#edit file "example_web.txt" append "--- New line added from web UI ---" to end`
- Click "Send".
- Result shown: Confirmation of successful file editing, `example_web.txt` file (in project directory) will be updated with the new line appended to the end.

**Explore Further:**

Experiment with different commands through web UI, utilize plugins, and customize interface to experience full potential of **System_Assistant_GUI (Rin Web)**.

## 7. Advanced Configuration

- **Configuration file `utils/cau_hinh.py`:**  Same as CLI version, this file configures Gemini API Key, model, temperature, Gemini parameters, colors, etc. These configurations affect both web and CLI versions.

- **Customize web interface (`static/style.css`):** You can fully customize Rin web UI by editing CSS file `static/style.css`. Change colors, fonts, layout, etc. to create desired look and feel.

- **Plugin Architecture (`cac_plugin/`):**  Web version **System_Assistant_GUI** reuses plugin system like CLI. You can develop new plugins in `cac_plugin/` directory to extend functionality (see sample plugins). These plugins will work on both web and CLI interfaces.

- **Run on different Port and Host (web_rin.py):**  If you want to run web app on a different port or host (e.g., for remote access), you can edit line `app.run(debug=True, host='0.0.0.0', port=5000)` in `web_rin.py` file. Change `host` and `port` as needed. `host='0.0.0.0'` allows access from outside (LAN), `host='127.0.0.1'` (or `'localhost'`) allows local access only.

</details>

<details>
<summary>🇯🇵 日本語</summary>

## 1. はじめに

**System_Assistant_GUI**（コード名 **Rin Web**）は、**Assistant** プロジェクトの Web ベースのグラフィカルユーザーインターフェース（GUI）バージョンです。このプロジェクトは、Gemini 大規模言語モデルを利用した仮想アシスタント Rin のコアパワーを維持しつつ、より直感的でユーザーフレンドリーな Web インターフェースを提供し、ユーザーが Web ブラウザーを介して Rin を制御および操作できるようにします。

**System_Assistant_GUI（Rin Web）の主な目標:**

- **ユーザーフレンドリーなエクスペリエンス:** 純粋なコマンドラインではなく、Web インターフェースを通じて、スムーズで直感的な仮想アシスタントインタラクションエクスペリエンスを提供します。
- **簡単なアクセス:** Web ブラウザーを備えた任意のデバイスからの Rin 仮想アシスタントへのアクセスを可能にし、ユーザビリティと柔軟性を拡張します。
- **コアパワーの維持:** システムコマンドの実行、Python コードの実行、ファイル処理、Gemini AI 統合など、コマンドラインインターフェース（CLI）バージョンのすべての強力な機能を保持します。
- **カスタマイズと拡張性:** プラグインアーキテクチャのサポートを継続し、新しい機能の追加や、必要に応じた仮想アシスタントの開発を容易にします。

**System_Assistant_GUI（Rin Web）の対象ユーザー:**

- **グラフィカルインターフェースを好むユーザー:** コマンドラインではなく、直感的な Web インターフェースを介して仮想アシスタントと対話したいユーザー。
- **クロスプラットフォームアクセスを必要とするユーザー:** Web ブラウザーを介して、複数のデバイス（コンピューター、タブレット、電話）で Rin 仮想アシスタントを使用したいユーザー。
- **初心者ユーザー:** Web インターフェースは、新しいユーザーが Rin の機能をより簡単に習得して使用するのに役立ちます。

## 2. 機能

**System_Assistant_GUI（Rin Web）** は、Web インターフェースでユーザーエクスペリエンスに焦点を当てた、コマンドラインバージョンの機能を継承および拡張します。

- **直感的な Web インターフェース:** シンプルで使いやすい Web インターフェースにより、コマンドの入力と結果のブラウザーでの直接表示が可能です。
- **システムコマンドの実行（@）:** Web コマンド入力ボックスを介して PowerShell コマンド（Windows）を実行します。
- **Python コードの実行（$）:** Web インターフェースから直接 Python コードスニペットを作成および実行します。
- **高度なファイル処理（#）:** Web コマンドを介してファイルを操作および処理（読み取り、書き込み、編集など）します。
- **詳細な結果表示:** 戻り値の結果は明確にフォーマットされ、セクション（メッセージ、分析、出力、エラー、コードなど）に分割され、Web インターフェース上で読みやすく理解しやすくなっています。
- **セッション履歴:** 現在のセッションでのインタラクション履歴を保存および表示し、以前のコマンドと応答を追跡および確認するのに役立ちます。
- **Gemini 統合 (Google AI):** 自然言語を理解し、インテリジェントなタスクを実行するために Gemini の能力を活用します。
- **メモリサポート:** セッションメモリを維持し、仮想アシスタントの対話能力とコンテキストの理解を向上させます。
- **プラグインアーキテクチャ:** CLI バージョンと同様のプラグインサポート。新しい機能の追加や拡張が容易です。
- **カスタマイズ可能なインターフェース:** CSS ファイル (`static/style.css`) を介して Web インターフェースをカスタマイズできます。
- **エラー通知と分析:** 詳細なエラーメッセージと結果分析（Gemini 2 から）を Web インターフェース上に直接表示します。

## 3. プロジェクト構造

```
System_Assistant_GUI/
├── .git/             (Git ディレクトリ - ドキュメントにリストされていません)
├── .gitignore        (Git が無視するファイル/ディレクトリを指定するファイル)
├── bieutuong/         (アイコン、画像を含むディレクトリ - リストされていません)
├── cac_plugin/       (機能プラグインのディレクトリ)
│   ├── thuc_thi_lenh_he_thong.py (PowerShell システムコマンドプラグイン)
│   ├── thuc_thi_python.py     (Python コードプラグイン)
│   ├── xu_ly_file_plugin.py   (高度なファイル処理プラグイン)
│   ├── __init__.py
│   └── __pycache__/         (Python キャッシュディレクトリ - リストされていません)
├── core/              (コアソースコードディレクトリ)
│   ├── chat.py         (Gemini 通信モジュール)
│   ├── __init__.py
│   └── __pycache__/         (Python キャッシュディレクトリ - リストされていません)
├── memory/            (メモリストレージディレクトリ - リストされていません)
├── moitruongao/       (Python 仮想環境ディレクトリ - リストされていません)
├── rin.py             (コマンドラインファイル、参照用にまだ存在)
├── run.bat            (CLI を実行するバッチスクリプト - GUI には使用しません)
├── static/            (静的 Web ファイルのディレクトリ)
│   ├── style.css      (Web インターフェースをカスタマイズする CSS ファイル)
├── templates/         (HTML テンプレートのディレクトリ)
│   ├── index.html     (Web UI のメイン HTML テンプレート)
├── utils/             (ユーティリティディレクトリ)
│   ├── animation/      (動的エフェクトのディレクトリ)
│   │   ├── hieu_ung.py  (動的エフェクトモジュール)
│   │   └── __init__.py
│   │   └── __pycache__/     (Python キャッシュディレクトリ - リストされていません)
│   ├── cau_hinh.py     (構成ファイル)
│   ├── nhat_ky.py      (ロギングモジュール)
│   ├── rin.bat        (補助バッチスクリプト)
│   ├── __init__.py
│   └── __pycache__/     (Python キャッシュディレクトリ - リストされていません)
├── web_rin.py         (Flask Web インターフェース用のメインソースファイル)
├── __init__.py
```

- **`.git/`、`.gitignore`、`.bieutuong/`、`.cac_plugin/`、`.core/`、`.memory/`、`.moitruongao/`、`.utils/__pycache__/`、`.rin.py`、`.run.bat`、`.utils/rin.bat`、`.utils/__init__.py`、`.__init__.py` (cac_plugin)、`core/__init__.py`**: **Assistant** CLI プロジェクト構造と同様です。
- **`static/`**: Web インターフェースを提供する静的ファイル用のディレクトリ。例:
    - **`style.css`**: Web ページのルックアンドフィールをカスタマイズする CSS ファイル。
- **`templates/`**: HTML テンプレートを含むディレクトリ:
    - **`index.html`**: Rin Web アシスタント UI のメイン HTML テンプレート。Jinja2 テンプレートエンジンを使用して、Python からの動的データをレンダリングします。
- **`web_rin.py`**: Flask Web アプリケーションを起動するメイン Python ファイル。このファイルはルーティング、Web UI ロジックを処理し、CLI バージョンの `rin.py` のように機能プラグインを統合します。

## 4. インストール

### 前提条件

CLI バージョンと同様に、以下があることを確認してください。

1.  **Python:** Python 3.8 以降。[https://www.python.org/downloads/](https://www.python.org/downloads/) からダウンロードできます。
2.  **pip:** (Python に付属).
3.  **Gemini API キー:**  Gemini API キーが必要です。`utils/cau_hinh.py` に入力してください。

### インストール手順

1. **プロジェクトのダウンロード:** **System_Assistant_GUI** プロジェクトのソースコードを GitHub (またはその他のソース) からダウンロードします。

   ```bash
   git clone https://github.com/Rin1809/System_Assistant_GUI/
   cd System_Assistant_GUI
   ```

2. **仮想環境の作成とアクティブ化 (推奨):** CLI バージョンと同様に、`moitruongao` 仮想環境を作成してアクティブ化します。**Assistant**（CLI バージョン）の `README.md` の「インストール」セクションで詳細な手順を参照してください。

3. **ライブラリのインストール:** Flask（Web UI 用）と Rin コアライブラリを含む、必要な Python ライブラリをインストールします。

   ```bash
   pip install -r requirements.txt  # requirements.txt ファイルが存在する場合

   # または requirements.txt が存在しない場合は手動でインストール:
   pip install flask google-generativeai pygments python-magic python-docx openpyxl rich psutil watchdog wmi
   ```

4. **API キーの設定:** CLI と同様に、`utils/cau_hinh.py` を開き、`API_KEY = "YOUR_API_KEY_HERE"` 変数に Gemini API キーを入力します。

5. **アプリケーションの実行:**

   - **Windows（推奨）:** `run.bat` ファイルを実行します。これにより、仮想環境がアクティブになり、Rin Web アプリケーションが起動します。

   - **任意の OS (仮想環境をアクティブ化した後):** 次のコマンドを実行します。

     ```bash
     python web_rin.py
     ```

     Rin Web アプリケーションが実行されます。ブラウザを開き、コマンドラインに表示されているアドレス (通常は `http://127.0.0.1:5000/` または `http://0.0.0.0:5000/`) にアクセスします。

## 6. 使用方法

**Assistant (Rin Web) の Web インターフェース:**

`web_rin.py` または `run.bat` を実行した後、ブラウザを開き、提供されたアドレスに移動します。Rin Web UI が表示されます。

Web インターフェースには以下が含まれます。

1. **コマンド/質問入力ボックス:** 最上部にある大きなテキストボックス。ここに Rin へのコマンドまたは質問を入力します。CLI バージョンと同じように、プレフィックス `@`、`$`、`#` を使用します (CLI README の「使用法」を参照)。

2. **[送信] ボタン:** テキストボックスに入力後、コマンド/質問を送信するためのボタン。

3. **出力表示エリア:** 入力ボックスの下にある大きなセクション。Rin からの応答結果を表示します。出力は、Web インターフェース上で読みやすく理解しやすいように、セクション（メッセージ、分析、出力、コードなど）にきちんとフォーマットされています。

4. **セッション履歴:** 下部にあるセクション。現在のセッションでの対話履歴が表示され、以前のコマンドと応答を追跡および確認できます。

**使用手順:**

1. **コマンド/質問を入力:** テキストボックスに質問またはコマンドを入力します。特定のプラグイン機能を呼び出すには、プレフィックス `@`、`$`、`#` を使用してください（必要に応じて）。
2. **[送信] をクリック:** [送信] ボタンまたは Enter キーをクリックして、コマンド/質問を Rin に送信します。
3. **結果の確認:** Rin からの応答結果が下の「出力エリア」に表示され、セッション履歴がページ下部に更新されます。
4. **繰り返す:** 新しいコマンドの入力を継続し、Rin と対話します。
5. **ブラウザを閉じる:** セッションを終了するには、ブラウザータブまたはウィンドウを閉じます（Rin Web アプリは、Python プロセスを終了するまでサーバー上で実行され続けます）。

**注:**

- Web UI は `static/style.css` ファイルを編集することでカスタマイズできます。
- コマンドの使用法 (プレフィックス `@`、`$`、`#`、構文など) は CLI バージョンと同様です。詳細については、**Assistant** (CLI バージョン) の `README.md` の「使用法」セクションを参照してください。
- Rin Web アプリケーションを完全に終了する (Flask サーバーを停止する) には、コマンドラインで `web_rin.py` Python プロセスを停止する必要があります (たとえば、Ctrl + C を使用)。

## 6. 使用例

以下の使用例は、Web インターフェースを介して **System_Assistant_GUI (Rin Web)** と対話する方法を示しています。

**(注: これらの例はコマンドに関して CLI バージョンと似ていますが、対話型インターフェースが Web ベースである点が異なります。)**

**例 1: 天気情報を尋ねる:**

- テキストボックスに入力: `明日のハノイの天気は？`
- [送信] をクリックします。
- 結果は「出力エリア」に表示されます: Rin はハノイの天気予報情報を、Web 形式で美しく返答します。

**例 2: システムコマンドを使用してアプリケーションを開く:**

- 入力: `@電卓を開く`
- [送信] をクリックします。
- 結果表示: Rin はコマンドの実行成功を確認し、電卓アプリがコンピュータ上で開かれます。詳細情報（分析、出力など）も Web UI に表示されます。

**例 3: Python を使用してディスク情報を取得する:**

- 入力: `$C ドライブと D ドライブのディスク容量を印刷する python コードを記述`
- [送信] をクリックします。
- 結果表示: Rin は Python コードを実行し、C ドライブと D ドライブのディスク容量情報（サイズ、空き容量など）を Web ページ上の表またはリスト形式で表示します。

**例 4: Python コードファイルの内容を読み取る:**

- 入力: `#ファイル "core/chat.py" を読み取り`
- [送信] をクリックします。
- 結果表示: `core/chat.py` ファイルの内容 (Python コード) が出力エリアに表示され、シンタックスハイライト表示される場合があります (現在の例ではシンタックスハイライトは表示されません)。

**例 5: テキストファイルを編集する:**

- 入力: `#ファイル "example_web.txt" を編集し、"--- Web UI から新しい行を追加 ---" を末尾に追加`
- [送信] をクリックします。
- 結果表示: ファイル編集成功の確認メッセージが表示され、`example_web.txt` ファイル (プロジェクトディレクトリ内) が末尾に新しく追加されたテキスト行で更新されます。

**さらに詳しく調べる:**

Web UI 経由でさまざまなコマンドを試したり、プラグインを活用したり、インターフェースをカスタマイズしたりして、**System_Assistant_GUI (Rin Web)** のすべての可能性を探求してください。

## 7. 高度な設定

- **構成ファイル `utils/cau_hinh.py`:**  CLI バージョンと同様に、このファイルは Gemini API キー、モデル、温度、Gemini パラメータ、色などを構成します。これらの構成は、Web バージョンと CLI バージョンの両方に影響します。

- **Web インターフェースのカスタマイズ (`static/style.css`):** CSS ファイル `static/style.css` を編集することで、Rin の Web UI を完全にカスタマイズできます。色、フォント、レイアウトなどを変更して、目的のルックアンドフィールを作成します。

- **プラグインアーキテクチャ (`cac_plugin/`):**  Web バージョン **System_Assistant_GUI** は、CLI バージョンと同じプラグインシステムを再利用します。`cac_plugin/` ディレクトリに新しいプラグインを開発して機能を拡張できます (サンプルプラグインを参照)。これらのプラグインは、Web インターフェースと CLI インターフェースの両方で動作します。

- **別のポートとホストで実行する (web_rin.py):**  Web アプリケーションを別のポートまたはホスト (たとえば、リモートアクセス用) で実行する場合は、`web_rin.py` ファイルの `app.run(debug=True, host='0.0.0.0', port=5000)` 行を編集できます。必要に応じて `host` と `port` を変更します。`host='0.0.0.0'` は外部 (LAN) からのアクセスを許可し、`host='127.0.0.1'` (または `'localhost'`) はローカルマシンからのアクセスのみを許可します。

</details>
