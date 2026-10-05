import os
import pandas as pd
import ezdxf
from pathlib import Path

def load_translation_map(excel_path):
    df = pd.read_excel(excel_path)
    return dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

def translate_text_entity(msp, entity, translation_map, text_height=1, text_color=1, x_offset=0, y_offset=-0.75, use_original_size=False):
    # 在这里添加打印语句来检查 x_offset 和 y_offset
    print(f"x_offset type: {type(x_offset)}, value: {x_offset}")
    print(f"y_offset type: {type(y_offset)}, value: {y_offset}")

    original_text = entity.dxf.text
    translated_text = translation_map.get(original_text, original_text)

    if translated_text != original_text:
        # 使用原文的颜色和大小（如果选项被选中）
        if text_color == 0:  # 假设 "使用原文颜色" 选项的索引为 0
            text_color = entity.dxf.color
        if use_original_size:
            text_height = entity.dxf.height

        # 在这里添加打印语句来检查 text_height 和 text_color
        print(f"text_height type: {type(text_height)}, value: {text_height}")
        print(f"text_color type: {type(text_color)}, value: {text_color}")

        # 在这里添加打印语句来检查 entity.dxf.insert
        print(f"entity.dxf.insert: {entity.dxf.insert}")

        msp.add_text(translated_text, dxfattribs={
            'insert': (entity.dxf.insert[0] + x_offset, entity.dxf.insert[1] + y_offset),
            'height': text_height,
            'color': text_color
        })

def translate_dwg(dwg_path, translation_map, text_height, text_color, x_offset, y_offset):
    # 确保 x_offset 和 y_offset 是浮点数
    x_offset = float(x_offset)
    y_offset = float(y_offset)

    doc = ezdxf.readfile(dwg_path)
    msp = doc.modelspace()

    for entity in msp.query('TEXT MTEXT'):
        translate_text_entity(msp, entity, translation_map, text_height, text_color, x_offset, y_offset)
    for block in doc.blocks:
        for entity in block.query('TEXT MTEXT'):
            translate_text_entity(msp, entity, translation_map, text_height, text_color, x_offset, y_offset)

    return doc

def process_directory(directory, translation_map, output_folder, update_status_function, text_color, x_offset, y_offset, text_height):
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d != output_folder.name]
        for name in files:
            if name.endswith('.dxf'):
                file_path = Path(root) / name
                relative_path = file_path.relative_to(directory)
                output_path = output_folder / relative_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                doc = translate_dwg(file_path, translation_map, text_height, text_color, x_offset, y_offset)
                doc.saveas(str(output_path))

def main(source_folder, translation_excel_path, output_folder, text_height=1, text_color=1, x_offset=0, y_offset=-0.75):
    translation_map = load_translation_map(translation_excel_path)
    source_folder = Path(source_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True)
    process_directory(source_folder, translation_map, output_folder, text_height, text_color, x_offset, y_offset)

if __name__ == "__main__":
    main('.', '3.xlsx', 'translated_drawings')
