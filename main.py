import os
import sys
from PIL import Image, ImageOps
import io


def create_resized_images(input_path):
    try:
        # Проверка существования файла
        if not os.path.exists(input_path):
            print(f"Файл {input_path} не найден.")
            return

        img = Image.open(input_path)
        sizes = [(112, 112), (56, 56), (28, 28)]
        file_name, _ = os.path.splitext(os.path.basename(input_path))

        output_folder = os.path.join(os.path.dirname(input_path), file_name)
        os.makedirs(output_folder, exist_ok=True)

        for size in sizes:
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            png_output_path = os.path.join(output_folder, f"{file_name}_{size[0]}x{size[1]}.png")

            # Установка DPI для уменьшения размера файла
            resized_img = ImageOps.exif_transpose(resized_img)
            resized_img.info['dpi'] = (72, 72)

            # Проверка размера файла и сжатие, если размер больше 25 КБ
            buffer = io.BytesIO()
            compress_level = 9  # Начальное значение уровня сжатия
            resized_img.save(buffer, format='PNG', dpi=(72, 72), compress_level=compress_level, optimize=True)
            file_size = buffer.tell()
            while file_size > 25 * 1024 and compress_level > 1:
                buffer.seek(0)
                compress_level -= 1
                resized_img.save(buffer, format='PNG', dpi=(72, 72), compress_level=compress_level, optimize=True)
                file_size = buffer.tell()

            with open(png_output_path, 'wb') as f:
                f.write(buffer.getvalue())

            print(f"Сохранено: {png_output_path} (размер: {file_size} байт)")

            # Если PNG размер все еще больше 25 КБ, сохраняем как JPEG
            if file_size > 25 * 1024:
                jpeg_output_path = os.path.join(output_folder, f"{file_name}_{size[0]}x{size[1]}.jpg")
                buffer.seek(0)
                quality = 85
                resized_img.convert('RGB').save(buffer, format='JPEG', dpi=(72, 72), quality=quality)
                file_size = buffer.tell()
                while file_size > 25 * 1024 and quality > 10:
                    buffer.seek(0)
                    quality -= 5
                    resized_img.convert('RGB').save(buffer, format='JPEG', dpi=(72, 72), quality=quality)
                    file_size = buffer.tell()

                with open(jpeg_output_path, 'wb') as f:
                    f.write(buffer.getvalue())

                print(f"Сохранено: {jpeg_output_path} (размер: {file_size} байт)")

        print("Все изображения созданы успешно.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        create_resized_images(input_path)
    else:
        print("Пожалуйста, укажите путь к изображению.")