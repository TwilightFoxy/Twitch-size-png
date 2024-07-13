import os
import sys
from PIL import Image


def create_resized_images(input_path):
    try:
        if not os.path.exists(input_path):
            print(f"Файл {input_path} не найден.")
            return

        img = Image.open(input_path)
        sizes = [(112, 112), (56, 56), (28, 28)]
        file_name, ext = os.path.splitext(os.path.basename(input_path))

        output_folder = os.path.join(os.path.dirname(input_path), file_name)
        os.makedirs(output_folder, exist_ok=True)

        for size in sizes:
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            output_path = os.path.join(output_folder, f"{file_name}_{size[0]}x{size[1]}{ext}")
            resized_img.save(output_path)
            print(f"Сохранено: {output_path}")

        print("Все изображения созданы успешно.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        create_resized_images(input_path)
    else:
        print("Пожалуйста, укажите путь к изображению.")
