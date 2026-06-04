import os
import json

# ==========================================
# 設定：請確保你的 PDF / ZIP 檔案擺在 assets 文件夾內
# ==========================================
TARGET_FOLDER = "assets"

# 品牌與專有名詞自動糾正字典 (自動將細階修正為官方大細階)
BRAND_DICTIONARY = {
    "koasis": "KOASIS",
    "kodak": "Kodak",
    "huago": "HuaGo",
    "unis": "Unis",
    "rpa": "RPA",
    "ai": "AI",
    "ocr": "OCR",
    "bi": "BI",
    "twain": "TWAIN",
    "wia": "WIA",
    "pdf": "PDF",
    "zip": "ZIP",
    "rpa": "RPA"
}

def format_title(filename):
    """將檔名（如 kodak_i3000_user_guide.pdf）美化為標準英文與中文字眼"""
    name_without_ext, _ = os.path.splitext(filename)
    
    # 拆開底線或連字號
    words = name_without_ext.replace('_', ' ').replace('-', ' ').split()
    
    formatted_words = []
    for word in words:
        lower_word = word.lower()
        # 檢查字典，如果匹配就用官方寫法，否則首字母大階
        if lower_word in BRAND_DICTIONARY:
            formatted_words.append(BRAND_DICTIONARY[lower_word])
        else:
            formatted_words.append(word.capitalize())
            
    return " ".join(formatted_words)

def get_file_size(filepath):
    """自動計算實際檔案大小，並轉換為 MB 或 KB"""
    try:
        bytes_size = os.path.getsize(filepath)
        if bytes_size >= 1024 * 1024:
            return f"{bytes_size / (1024 * 1024):.1f} MB"
        else:
            return f"{bytes_size / 1024:.1f} KB"
    except Exception:
        return "2.5 MB" # 讀取失敗時的默認大小

def main():
    if not os.path.exists(TARGET_FOLDER):
        print(f"❌ 錯誤：找不到 '{TARGET_FOLDER}' 文件夾！")
        print(f"請在你的專案目錄下建立一個名為 '{TARGET_FOLDER}' 的文件夾，並放入你的文檔。")
        return

    supported_extensions = ['.pdf', '.zip', '.rar', '.docx', '.xlsx']
    documents_list = []
    doc_id = 1

    # 掃描目標資料夾
    files = sorted(os.listdir(TARGET_FOLDER))
    for file in files:
        _, ext = os.path.splitext(file)
        if ext.lower() in supported_extensions:
            filepath = os.path.join(TARGET_FOLDER, file)
            size_str = get_file_size(filepath)
            format_str = ext.replace('.', '').upper()
            beautiful_title = format_title(file)
            
            # 建立符合 React Code 規格的 Document 對象
            doc_entry = {
                "id": doc_id,
                "size": size_str,
                "format": format_str,
                "path": f"../{TARGET_FOLDER}/{file}",
                "title": {
                    "en": beautiful_title,
                    "zh": beautiful_title, # 中文預設和英文一樣，方便你稍後微調
                    "sc": beautiful_title  # 簡體預設和英文一樣
                }
            }
            documents_list.append(doc_entry)
            doc_id += 1

    # 輸出完美的 JS 陣列
    print("\n" + "="*50)
    print("🎉 掃描完成！請複製以下陣列，取代 download/index.html 內的 documents = [...]")
    print("="*50 + "\n")
    
    # 使用 json.dumps 輸出，並保持美觀縮排
    formatted_json = json.dumps(documents_list, indent=4, ensure_ascii=False)
    # 將 JSON 的 Key 去除引號，更符合原生 JS Array 的寫法 (可選)
    print(f"const documents = {formatted_json};")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()