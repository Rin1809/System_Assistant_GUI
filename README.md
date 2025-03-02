# Assistant  (Testing - Got bug) ᓚᘏᗢ


<!-- Vietnamese -->
<details>
  <summary>🇻🇳 Tiếng Việt</summary>

## Giới thiệu

**Assistant - Rin** là một trợ lý ảo mạnh mẽ được xây dựng bằng Python, tận dụng sức mạnh của mô hình ngôn ngữ lớn (LLM) Gemini từ Google AI.  Rin được thiết kế để thực hiện một loạt các tác vụ đa dạng, bao gồm thực thi mã Python, thực thi các lệnh hệ thống Windows, Linux, xử lý các loại tệp tin khác nhau, và tương tác tự nhiên với người dùng thông qua giao diện dòng lệnh.  Điểm nổi bật của Rin là khả năng **tự đánh giá và cải thiện** kết quả thực thi bằng cách sử dụng một mô hình Gemini thứ hai để kiểm tra chéo (cross-checking) và xác thực kết quả.

## Tính năng chính

*   **Thực thi mã Python linh hoạt:** Rin cho phép người dùng yêu cầu thực thi các đoạn mã Python một cách trực tiếp.  Trợ lý sẽ tự động tạo mã, thực thi mã, và trả về kết quả chi tiết, bao gồm đầu ra (stdout), lỗi (stderr), thời gian thực thi, và mã Python đã thực thi.
*   **EX: Thực thi lệnh hệ thống Windows (PowerShell):** Rin có thể thực thi các lệnh PowerShell trên hệ điều hành Windows.  Trợ lý sử dụng Gemini để tạo lệnh PowerShell dựa trên yêu cầu của người dùng, thực thi lệnh, và trả về kết quả đầy đủ, bao gồm đầu ra, lỗi, mã trả về (return code), và quan trọng nhất là **đánh giá và xác thực từ mô hình Gemini thứ hai**.
*   **Xử lý tệp tin đa năng:** Rin cung cấp một loạt các chức năng xử lý tệp tin mạnh mẽ, bao gồm:
    *   Đọc nội dung từ nhiều định dạng tệp tin (text, JSON, CSV, DOCX, XLSX).
    *   Ghi nội dung vào tệp tin.
    *   Chỉnh sửa nội dung tệp tin: thay thế, xóa, và thêm văn bản.
    *   Tạo mã Python mới và lưu vào tệp tin.
    *   Sửa lỗi cú pháp và logic trong mã Python hiện có.
    *   Nâng cấp và cải tiến mã Python.
*   **Tương tác trực tiếp với Gemini:** Người dùng có thể đặt câu hỏi trực tiếp cho mô hình Gemini để nhận được câu trả lời cho các vấn đề chung, không liên quan đến các plugin cụ thể.
*   **Bộ nhớ (Memory):** Rin có khả năng lưu trữ lịch sử các tương tác, các lệnh đã thực thi, và kết quả vào các tệp tin "memory".  Điều này cho phép người dùng tải lại và sử dụng thông tin từ các phiên làm việc trước đó, giúp tiết kiệm thời gian và tăng tính liên tục.
*   **Giám sát tệp tin (File Monitoring - Tính năng thử nghiệm):**  Rin có khả năng giám sát sự thay đổi của các tệp tin được chỉ định và thông báo cho người dùng khi có thay đổi.
*   **Giao diện dòng lệnh thân thiện:**  Tương tác với Rin được thực hiện thông qua giao diện dòng lệnh (command-line interface - CLI) trực quan, với màu sắc và hiệu ứng động (animation) để nâng cao trải nghiệm người dùng.

## Cài đặt

1.  **Yêu cầu hệ thống:**
    *   Python 3.7 trở lên.
    *   Các thư viện Python (chi tiết trong file `requirements.txt`):
        *   `google-generativeai`
        *   `python-magic`
        *   `psutil`
        *   `watchdog`
        *   `pygments`
        *   `docx` (python-docx)
        *   `openpyxl`
        *   `wmi`
        *   `ctypes`
        *   `rich`
        * `Flask`

2.  **Các bước cài đặt:**

    Mở terminal (hoặc Command Prompt trên Windows) và thực hiện các lệnh sau:

    ```bash
    git clone https://github.comRin1809/System_Assistant_GUI.git 
    cd "Name folder"
    python -m venv moitruongao
    moitruongao\Scripts\activate  # Trên Windows.  Hoặc: source moitruongao/bin/activate (trên Linux/macOS)
    pip install -r requirements.txt
    ```


3.  **Chạy ứng dụng:**
    *  Cách 1: Chạy file `run.bat` (cách này đã bao gồm các bước tạo và kích hoạt môi trường ảo, cài thư viện)
    ```bash
    run.bat
    ```
    *  Cách 2: Chạy trực tiếp file `web_rin.py`:
    ```bash
    python web_rin.py
    ```
4.  **Cấu hình:**

    *   Mở file `utils/cau_hinh.py` và cấu hình các thông số sau:
        *   **`API_KEY`:** Thay thế bằng API key Gemini của bạn (bắt buộc).  Bạn có thể lấy API key từ Google AI Studio.
        *   **`MODEL_NAME`:** Tên mô hình Gemini bạn muốn sử dụng (mặc định: `gemini-2.0-flash-exp`).  Bạn có thể thay đổi nếu cần.
        *    Các tham số khác bạn có thể giữ nguyên hoặc điều chỉnh theo nhu cầu.

## Hướng dẫn sử dụng chi tiết

*   **Tương tác chung:**  Nhập trực tiếp câu hỏi hoặc yêu cầu vào giao diện dòng lệnh và nhấn Enter.  Rin sẽ cố gắng hiểu và trả lời.

*   **Thực thi mã Python (`$`):**  Để yêu cầu Rin thực thi mã Python, hãy bắt đầu câu hỏi bằng ký tự `$`, theo sau là mã Python hoặc yêu cầu viết mã Python.

    *   **Ví dụ:**
        *   `$ print("Xin chào, thế giới!")`  (Thực thi trực tiếp mã Python)
        *   `$ viết code python để tính tổng của hai số a và b` (Yêu cầu viết mã Python)

*   **Thực thi lệnh hệ thống Windows - PowerShell (`@`):** Để yêu cầu Rin thực thi lệnh PowerShell, hãy bắt đầu câu hỏi bằng ký tự `@`, theo sau là lệnh PowerShell hoặc yêu cầu viết lệnh PowerShell.

    *   **Ví dụ:**
        *   `@ Get-Process` (Thực thi trực tiếp lệnh PowerShell)
        *   `@ lệnh powershell để liệt kê các file trong thư mục hiện tại` (Yêu cầu viết lệnh PowerShell)

*   **Xử lý tệp tin (`#`):**  Để thao tác với tệp tin, hãy bắt đầu câu hỏi bằng ký tự `#`, theo sau là đường dẫn đầy đủ đến tệp tin (đặt trong dấu nháy kép nếu đường dẫn có khoảng trắng) và yêu cầu cụ thể.

    *   **Cú pháp:** `# "<đường_dẫn_tệp_tin>" <hành_động> [tham_số]`

    *   **Các hành động được hỗ trợ:**
        *   **`read file`:**  Đọc nội dung của tệp tin.
            *   **Ví dụ:** `# "C:\Users\MyUser\Documents\test.txt" read file`
        *   **`edit file`:** Chỉnh sửa nội dung tệp tin, hỗ trợ các thao tác:
            *   `thay thế "<chuỗi_cũ>" bằng "<chuỗi_mới>"`
            *   `xóa "<chuỗi_cần_xóa>"`
            *   `thêm "<chuỗi_cần_thêm>" vào cuối`
            *   **Ví dụ:** `# "C:\data.txt" edit file, thay thế "apple" bằng "orange", xóa "banana", thêm "grape" vào cuối`
        *   **`write file`:**  Ghi (hoặc ghi đè) nội dung vào tệp tin.
            *   **Ví dụ:** `# "C:\output.txt" write file với nội dung "This is the new content."`
        *   **`create code`:**  Tạo mã Python theo yêu cầu và lưu vào tệp tin.
             *    **Ví dụ:** `# "C:\my_script.py" create code: Viết hàm Python tính giai thừa của một số.`
        *   **`fix_code`:** Sửa lỗi trong mã Python (nếu có) của file.
             * **Ví dụ:** `# "C:\broken_code.py" fix_code`
        *  **`upgrade code`:** Nâng cấp code.
           *  **Ví dụ:** `# "C:\old_code.py" upgrade code`

*   **Tải bộ nhớ (`!`):** Để tải thông tin từ một tệp tin memory đã lưu trước đó, hãy bắt đầu câu hỏi bằng ký tự `!`, theo sau là tên tệp tin memory (không cần đường dẫn đầy đủ, chỉ cần tên tệp tin).

    *   **Ví dụ:** `! previous_session.json`

* **Thoát chương trình:** Gõ `0` và nhấn Enter.

* **Ngắt tiến trình đang chạy:** Gõ `2` và nhấn Enter.

## Cấu trúc thư mục

```
System_Assistant_GUI/
├── .git/               (Thư mục Git - Không liệt kê)
├── .gitignore          (File cấu hình Git)
├── bieutuong/          (Thư mục chứa các file biểu tượng - Không liệt kê)
├── cac_plugin/         (Thư mục chứa các plugin)
│   ├── thuc_thi_lenh_he_thong.py  (Plugin thực thi lệnh hệ thống)
│   ├── thuc_thi_python.py      (Plugin thực thi mã Python)
│   ├── xu_ly_file_plugin.py   (Plugin xử lý file)
│   ├── __init__.py
│   ├── __pycache__/    (Thư mục cache - Không liệt kê)
├── core/               (Thư mục chứa các module lõi)
│   ├── chat.py         (Module xử lý giao tiếp với Gemini)
│   ├── __init__.py
│   ├── __pycache__/    (Không liệt kê)
├── memory/             (Thư mục chứa các file memory - Không liệt kê)
├── rin.py              (File Python chính của chương trình)
├── run.bat             (File batch để chạy chương trình trên Windows)
├── static/             (Chứa file css cho web)
│   ├── style.css
├── templates/          (Chứa file html giao diện)
│   ├── index.html
├── utils/              (Thư mục chứa các module tiện ích)
│   ├── animation/      (Module tạo hiệu ứng animation)
│   │   ├── hieu_ung.py
│   │   ├── __init__.py
│   │   ├── __pycache__/ (Không liệt kê)
│   ├── cau_hinh.py     (Module cấu hình)
│   ├── nhat_ky.py      (Module ghi log)
│   ├── __init__.py
│   ├── __pycache__/    (Không liệt kê)
├── web_rin.py          (Chương trình chạy web)
├── __init__.py
├── __pycache__/        (Không liệt kê)
```

## Góp ý và Báo lỗi

Nếu bạn có bất kỳ góp ý, đề xuất tính năng mới, hoặc phát hiện lỗi, vui lòng tạo một "Issue" mới trên trang GitHub của dự án.



</details>

<!-- English -->
<details>
  <summary>🇬🇧 English</summary>

## Introduction

**Assistant - Rin** is a powerful, versatile virtual assistant built using Python and powered by Google AI's Gemini large language model (LLM).  Rin is designed to perform a wide array of tasks, including executing Python code, running on Windows, Linux handling various file types, and interacting naturally with users through a command-line interface.  A key feature of Rin is its ability to **self-assess and improve** execution results by utilizing a second Gemini model for cross-checking and validation.

## Key Features

*   **Flexible Python Code Execution:** Rin allows users to request the execution of Python code snippets directly.  The assistant automatically generates code, executes it, and returns detailed results, including output (stdout), errors (stderr), execution time, and the executed Python code.
*   **EX : Windows System Command Execution (PowerShell):** Rin can execute PowerShell commands on the Windows operating system.  The assistant uses Gemini to generate PowerShell commands based on user requests, execute the commands, and return comprehensive results, including output, errors, return code, and most importantly, **assessment and validation from a second Gemini model**.
*   **Versatile File Handling:** Rin offers a robust set of file handling capabilities, including:
    *   Reading content from various file formats (text, JSON, CSV, DOCX, XLSX).
    *   Writing content to files.
    *   Editing file content: replacing, deleting, and adding text.
    *   Creating new Python code and saving it to a file.
    *   Fixing syntax and logic errors in existing Python code.
    *   Upgrading and improving Python code.
*   **Direct Interaction with Gemini:** Users can ask questions directly to the Gemini model to receive answers to general inquiries, unrelated to specific plugins.
*   **Memory:** Rin can store the history of interactions, executed commands, and results in "memory" files. This allows users to reload and reuse information from previous sessions, saving time and increasing continuity.
*   **File Monitoring (Experimental Feature):**  Rin has the ability to monitor specified files for changes and notify the user when changes occur.
*   **User-Friendly Command-Line Interface:** Interaction with Rin is done through an intuitive command-line interface (CLI), with colors and dynamic animations to enhance the user experience.

## Installation

1.  **System Requirements:**
    *   Python 3.7 or higher.
    *   Python libraries (detailed in the `requirements.txt` file):
        *   `google-generativeai`
        *   `python-magic`
        *   `psutil`
        *   `watchdog`
        *   `pygments`
        *   `docx` (python-docx)
        *   `openpyxl`
        *   `wmi`
        *   `ctypes`
        *   `rich`
        *   `Flask`

2.  **Installation Steps:**

    Open a terminal (or Command Prompt on Windows) and execute the following commands:

    ```bash
    git clone https://github.comRin1809/System_Assistant_GUI.git 
    cd "Name folder"
    python -m venv virtual_environment_name
    virtual_environment_name\Scripts\activate  # On Windows.  Or: source virtual_environment_name/bin/activate (on Linux/macOS)
    pip install -r requirements.txt
    ```


3.  **Running the Application:**
    *   Method 1: Run the `run.bat` file (this includes the steps to create and activate the virtual environment, install libraries).
      ```bash
      run.bat
      ```
    *  Method 2: Run the `web_rin.py` file
    ```bash
    python web_rin.py
    ```

4.  **Configuration:**

    *   Open the `utils/cau_hinh.py` file and configure the following parameters:
        *   **`API_KEY`:** Replace with your Gemini API key (required). You can obtain an API key from Google AI Studio.
        *   **`MODEL_NAME`:** The name of the Gemini model you want to use (default: `gemini-2.0-flash-exp`).  You can change this if necessary.
        *   Other parameters can be left as they are or adjusted according to your needs.

## Detailed Usage Instructions

*   **General Interaction:** Type your question or request directly into the command-line interface and press Enter. Rin will attempt to understand and respond.

*   **Executing Python Code (`$`):** To request Rin to execute Python code, start your question with the `$` character, followed by the Python code or a request to write Python code.

    *   **Examples:**
        *   `$ print("Hello, world!")` (Execute Python code directly)
        *   `$ write python code to calculate the sum of two numbers a and b` (Request to write Python code)

*   **Executing Windows System Commands - PowerShell (`@`):** To request Rin to execute a PowerShell command, start your question with the `@` character, followed by the PowerShell command or a request to write a PowerShell command.

    *   **Examples:**
        *   `@ Get-Process` (Execute a PowerShell command directly)
        *   `@ powershell command to list files in the current directory` (Request to write a PowerShell command)

*   **File Handling (`#`):** To interact with files, start your question with the `#` character, followed by the full path to the file (enclose in double quotes if the path contains spaces) and the specific request.

    *   **Syntax:** `# "<file_path>" <action> [parameters]`

    *   **Supported Actions:**
        *   **`read file`:** Read the content of the file.
            *   **Example:** `# "C:\Users\MyUser\Documents\test.txt" read file`
        *   **`edit file`:** Edit the file content, supporting the following operations:
            *   `replace "<old_string>" with "<new_string>"`
            *   `delete "<string_to_delete>"`
            *   `add "<string_to_add>" to end`
            *   **Example:** `# "C:\data.txt" edit file, replace "apple" with "orange", delete "banana", add "grape" to end`
        *   **`write file`:** Write (or overwrite) content to the file.
            *   **Example:** `# "C:\output.txt" write file with content "This is the new content."`
        *   **`create code`:** Create Python code as requested and save it to the file.
            *    **Example:** `# "C:\my_script.py" create code: Write a Python function to calculate the factorial of a number.`
        *   **`fix_code`:** Fix errors in the Python code (if any) of the file.
             * **Example:** `# "C:\broken_code.py" fix_code`
        *   **`upgrade code`:** Upgrade the code.
           *   **Example:**  `# "C:\old_code.py" upgrade code`

*   **Loading Memory (`!`):** To load information from a previously saved memory file, start your question with the `!` character, followed by the memory file name (no need for the full path, just the file name).

    *   **Example:** `! previous_session.json`

*   **Exit the program:** Type `0` and press Enter.

*   **Interrupt a running process:** Type `2` and press Enter.

## Folder Structure

```
System_Assistant_GUI/
├── .git/               (Git directory - Not listed)
├── .gitignore          (Git configuration file)
├── bieutuong/          (Directory containing icon files - Not listed)
├── cac_plugin/         (Directory containing plugins)
│   ├── thuc_thi_lenh_he_thong.py  (Plugin for executing system commands)
│   ├── thuc_thi_python.py      (Plugin for executing Python code)
│   ├── xu_ly_file_plugin.py   (Plugin for file handling)
│   ├── __init__.py
│   ├── __pycache__/    (Cache directory - Not listed)
├── core/               (Directory containing core modules)
│   ├── chat.py         (Module for handling communication with Gemini)
│   ├── __init__.py
│   ├── __pycache__/    (Not listed)
├── memory/             (Directory containing memory files - Not listed)
├── rin.py              (Main Python file of the program)
├── run.bat             (Batch file to run the program on Windows)
├── static/             (Contains css file for the web)
│   ├── style.css
├── templates/          (Contains html interface file)
│   ├── index.html
├── utils/              (Directory containing utility modules)
│   ├── animation/      (Module for creating animation effects)
│   │   ├── hieu_ung.py
│   │   ├── __init__.py
│   │   ├── __pycache__/ (Not listed)
│   ├── cau_hinh.py     (Configuration module)
│   ├── nhat_ky.py      (Logging module)
│   ├── __init__.py
│   ├── __pycache__/    (Not listed)
├── web_rin.py          (Program to run the web)
├── __init__.py
├── __pycache__/        (Not listed)
```

## Feedback and Bug Reports

If you have any feedback, suggestions for new features, or find any bugs, please create a new "Issue" on the project's GitHub page.


</details>

<!-- Japanese -->
<details>
  <summary>🇯🇵 日本語</summary>

## 概要

**Assistant - Rin** は、Python で構築され、Google AI の Gemini 大規模言語モデル (LLM) を活用した、強力で多用途な仮想アシスタントです。Rin は、Python コードの実行、Windows, Linux システム、さまざまなファイル タイプの処理、コマンドライン インターフェイスを介したユーザーとの自然な対話など、幅広いタスクを実行できるように設計されています。Rin の主な特徴は、第 2 の Gemini モデルを利用してクロスチェックと検証を行うことで、実行結果を**自己評価および改善**できることです。

## 主要機能

*   **柔軟な Python コード実行:** Rin を使用すると、ユーザーは Python コード スニペットの実行を直接要求できます。アシスタントは自動的にコードを生成、実行し、出力 (stdout)、エラー (stderr)、実行時間、実行された Python コードなどの詳細な結果を返します。
*   **EX : Windows システム コマンド実行 (PowerShell):** Rin は、Windows オペレーティング システムで PowerShell コマンドを実行できます。アシスタントは Gemini を使用して、ユーザーの要求に基づいて PowerShell コマンドを生成、実行し、出力、エラー、戻りコード、そして最も重要なことに、**第 2 の Gemini モデルからの評価と検証**を含む包括的な結果を返します。
*   **多用途なファイル処理:** Rin は、次のような堅牢なファイル処理機能を提供します。
    *   さまざまなファイル形式 (テキスト、JSON、CSV、DOCX、XLSX) からのコンテンツの読み取り。
    *   ファイルへのコンテンツの書き込み。
    *   ファイル コンテンツの編集: テキストの置換、削除、追加。
    *   新しい Python コードを作成し、ファイルに保存します。
    *   既存の Python コードの構文エラーとロジック エラーの修正。
    *   Python コードのアップグレードと改善。
*   **Gemini との直接対話:** ユーザーは Gemini モデルに直接質問して、特定のプラグインに関連しない一般的な問い合わせに対する回答を得ることができます。
*   **メモリ:** Rin は、対話、実行されたコマンド、および結果の履歴を「メモリ」ファイルに保存できます。これにより、ユーザーは以前のセッションから情報をリロードして再利用できるため、時間を節約し、継続性を高めることができます。
*   **ファイル監視 (実験的機能):** Rin は、指定されたファイルの変更を監視し、変更が発生したときにユーザーに通知する機能を備えています。
*   **ユーザーフレンドリーなコマンドライン インターフェイス:** Rin との対話は、直感的なコマンドライン インターフェイス (CLI) を介して行われ、色と動的なアニメーションによってユーザー エクスペリエンスが向上します。

## インストール

1.  **システム要件:**
    *   Python 3.7 以上。
    *   Python ライブラリ (詳細は `requirements.txt` ファイルを参照):
        *   `google-generativeai`
        *   `python-magic`
        *   `psutil`
        *   `watchdog`
        *   `pygments`
        *   `docx` (python-docx)
        *   `openpyxl`
        *   `wmi`
        *   `ctypes`
        *   `rich`
        *   `Flask`

2.  **インストール手順:**

    ターミナル (または Windows のコマンド プロンプト) を開き、次のコマンドを実行します。

    ```bash
    git clone https://github.comRin1809/System_Assistant_GUI.git 
    cd "Name folder"
    python -m venv virtual_environment_name
    virtual_environment_name\Scripts\activate  # Windows の場合。 または: source virtual_environment_name/bin/activate (Linux/macOS の場合)
    pip install -r requirements.txt
    ```


3.  **アプリケーションの実行:**
      * 方法1: `run.bat`ファイルを実行します（仮想環境の作成、アクティブ化、必要なライブラリのインストールを含みます）。
        ```
        run.bat
        ```
     * 方法2: `web_rin.py`ファイルを実行します。
    ```bash
    python web_rin.py
    ```

4.  **設定:**

    *   `utils/cau_hinh.py` ファイルを開き、次のパラメータを設定します。
        *   **`API_KEY`:** あなたの Gemini API キーに置き換えます (必須)。API キーは Google AI Studio から取得できます。
        *   **`MODEL_NAME`:** 使用する Gemini モデルの名前 (デフォルト: `gemini-2.0-flash-exp`)。必要に応じて変更できます。
        *   その他のパラメータは、そのままにしておくか、必要に応じて調整できます。

## 詳細な使用方法

*   **一般的な対話:** コマンドライン インターフェイスに質問またはリクエストを直接入力し、Enter キーを押します。Rin は理解して応答しようとします。

*   **Python コードの実行 (`$`):** Rin に Python コードの実行を要求するには、質問を `$` 文字で始め、その後に Python コードまたは Python コードの作成リクエストを続けます。

    *   **例:**
        *   `$ print("Hello, world!")` (Python コードを直接実行)
        *   `$ 2 つの数値 a と b の合計を計算する Python コードを作成する` (Python コードの作成をリクエスト)

*   **Windows システム コマンドの実行 - PowerShell (`@`):** Rin に PowerShell コマンドの実行を要求するには、質問を `@` 文字で始め、その後に PowerShell コマンドまたは PowerShell コマンドの作成リクエストを続けます。

    *   **例:**
        *   `@ Get-Process` (PowerShell コマンドを直接実行)
        *   `@ 現在のディレクトリ内のファイルを一覧表示する PowerShell コマンド` (PowerShell コマンドの作成をリクエスト)

*   **ファイル処理 (`#`):** ファイルを操作するには、質問を `#` 文字で始め、その後にファイルへのフルパス (パスにスペースが含まれる場合は二重引用符で囲む) と特定のリクエストを続けます。

    *   **構文:** `# "<ファイルパス>" <アクション> [パラメータ]`

    *   **サポートされているアクション:**
        *   **`read file`:** ファイルの内容を読み込みます。
            *   **例:** `# "C:\Users\MyUser\Documents\test.txt" read file`
        *   **`edit file`:** ファイルの内容を編集します。次の操作をサポートしています。
            *   `replace "<古い文字列>" with "<新しい文字列>"`
            *   `delete "<削除する文字列>"`
            *   `add "<追加する文字列>" to end`
            *   **例:** `# "C:\data.txt" edit file, replace "apple" with "orange", delete "banana", add "grape" to end`
        *   **`write file`:** ファイルにコンテンツを書き込みます (または上書きします)。
            *   **例:** `# "C:\output.txt" write file with content "This is the new content."`
        *   **`create code`:** 要求に応じて Python コードを作成し、ファイルに保存します。
            *   **例:** `# "C:\my_script.py" create code: 数値の階乗を計算する Python 関数を記述してください。`
        *   **`fix_code`:** ファイル内のPythonコードのエラーを修正します。
           *   **例:** `# "C:\broken_code.py" fix_code`
        *   **`upgrade code`:**  コードをアップグレードします。
           *   **例:** `# "C:\old_code.py" upgrade code`

*   **メモリのロード (`!`):** 以前に保存されたメモリ ファイルから情報をロードするには、質問を `!` 文字で始め、その後にメモリ ファイル名 (フルパスは不要、ファイル名のみ) を続けます。

    *   **例:** `! previous_session.json`

*   **プログラムを終了する:** `0` と入力して Enter キーを押します。

*   **実行中のプロセスを中断する:** `2` と入力して Enter キーを押します。

## フォルダ構造

```
System_Assistant_GUI/
├── .git/               (Git ディレクトリ - リストされていません)
├── .gitignore          (Git 構成ファイル)
├── bieutuong/          (アイコン ファイルを含むディレクトリ - リストされていません)
├── cac_plugin/         (プラグインを含むディレクトリ)
│   ├── thuc_thi_lenh_he_thong.py  (システム コマンドを実行するためのプラグイン)
│   ├── thuc_thi_python.py      (Python コードを実行するためのプラグイン)
│   ├── xu_ly_file_plugin.py   (ファイル処理用のプラグイン)
│   ├── __init__.py
│   ├── __pycache__/    (キャッシュ ディレクトリ - リストされていません)
├── core/               (コア モジュールを含むディレクトリ)
│   ├── chat.py         (Gemini との通信を処理するモジュール)
│   ├── __init__.py
│   ├── __pycache__/    (リストされていません)
├── memory/             (メモリ ファイルを含むディレクトリ - リストされていません)
├── rin.py              (プログラムのメイン Python ファイル)
├── run.bat             (Windows でプログラムを実行するためのバッチ ファイル)
├── static/             (Web 用の CSS ファイルが含まれています)
│   ├── style.css
├── templates/          (HTML インターフェイス ファイルが含まれています)
│   ├── index.html
├── utils/              (ユーティリティ モジュールを含むディレクトリ)
│   ├── animation/      (アニメーション効果を作成するためのモジュール)
│   │   ├── hieu_ung.py
│   │   ├── __init__.py
│   │   ├── __pycache__/ (リストされていません)
│   ├── cau_hinh.py     (構成モジュール)
│   ├── nhat_ky.py      (ロギング モジュール)
│   ├── __init__.py
│   ├── __pycache__/    (リストされていません)
├── web_rin.py          (Web を実行するプログラム)
├── __init__.py
├── __pycache__/        (リストされていません)
```

## フィードバックとバグレポート

フィードバック、新機能の提案、またはバグの発見がある場合は、プロジェクトの GitHub ページで新しい「Issue」を作成してください。



</details>
