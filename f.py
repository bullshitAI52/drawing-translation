import os
import pandas as pd
import ezdxf
from pathlib import Path
from tkinter import messagebox

def extract_text_from_dxf(file_path):
    try:
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        texts = set()  # 使用集合来自动去除重复项

        # 提取模型空间中的文本
        for entity in msp.query('TEXT MTEXT'):
            texts.add(entity.dxf.text)

        # 提取块中的文本
        for block in doc.blocks:
            for entity in block.query('TEXT MTEXT'):
                texts.add(entity.dxf.text)

        return list(texts)  # 将集合转换回列表
    except IOError:
        print(f"Could not read file: {file_path}")
        return []
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file: {file_path}")
        return []

def process_directory(directory, progress_callback=None):
    all_texts = []
    total_files = sum([len(files) for r, d, files in os.walk(directory) if any(file.endswith('.dxf') for file in files)])
    processed_files = 0

    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith('.dxf'):
                file_path = Path(root) / name
                texts = extract_text_from_dxf(file_path)
                for text in texts:
                    all_texts.append([file_path, text])

                processed_files += 1
                if progress_callback:
                    progress_callback(processed_files, total_files)

    return all_texts

def main(directory_path, output_excel_path='extracted_texts.xlsx', progress_callback=None):
    directory = Path(directory_path)
    texts = process_directory(directory, progress_callback)

    # 将提取的文本保存到Excel文件中
    df = pd.DataFrame(texts, columns=['File Path', 'Text'])
    df.to_excel(output_excel_path, index=False)
    print(f"Texts have been extracted and saved to '{output_excel_path}'.")

if __name__ == "__main__":
    main('.')