import io
import os
import sys
from PIL import Image, ImageOps

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
            resized_img = img.resize((int(size[0]*0.8), int(size[1]*0.8)), Image.Resampling.LANCZOS)
            new_img = Image.new("RGBA", size, (255, 255, 255, 0))  # Создаем новое изображение с пустым фоном
            offset = ((size[0] - resized_img.size[0]) // 2, (size[1] - resized_img.size[1]) // 2)
            new_img.paste(resized_img, offset)

            png_output_path = os.path.join(output_folder, f"{file_name}_{size[0]}x{size[1]}.png")

            # Попробуем сохранить как PNG с минимальными размерами
            buffer = io.BytesIO()
            new_img.save(buffer, format='PNG', optimize=True)
            file_size = buffer.tell()

            with open(png_output_path, 'wb') as f:
                f.write(buffer.getvalue())

            print(f"Сохранено: {png_output_path} (размер: {file_size} байт)")

            # Если PNG размер все еще больше 25 КБ, сохраняем как JPEG
            if file_size > 25 * 1024:
                jpeg_output_path = os.path.join(output_folder, f"{file_name}_{size[0]}x{size[1]}.jpg")
                quality = 85
                buffer.seek(0)
                new_img.convert('RGB').save(buffer, format='JPEG', quality=quality)
                file_size = buffer.tell()
                while file_size > 25 * 1024 and quality > 10:
                    buffer.seek(0)
                    quality -= 5
                    new_img.convert('RGB').save(buffer, format='JPEG', quality=quality)
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
