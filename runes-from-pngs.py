import os
from PIL import Image

base = "/storage/emulated/0/Pictures"
out_dir = os.path.join(base, "SVG_RESULTS2")
os.makedirs(out_dir, exist_ok=True)

# Загружаем слои в порядке снизу вверх
layers = []
for i in range(6):
    path = os.path.join(base, f"{i}x5.png")
    img = Image.open(path).convert("RGBA")
    layers.append(img)

# Все изображения должны быть одного размера
W, H = layers[0].size

# Перебираем все 2^6 = 64 комбинации (маска от 0 до 63)
for mask in range(64):
    # Собираем SVG
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">')
    
    # Проходим слои от нижнего (0) к верхнему (5)
    for layer_idx in range(6):
        if (mask >> layer_idx) & 1:          # слой присутствует в комбинации
            img = layers[layer_idx]
            pixels = img.load()              # быстрый доступ к пикселям
            for y in range(H):
                for x in range(W):
                    r, g, b, a = pixels[x, y]
                    if a == 0:
                        continue
                    opacity = f' fill-opacity="{a/255:.2f}"' if a < 255 else ""
                    svg.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="rgb({r},{g},{b})"{opacity}/>')
    
    svg.append('</svg>')
    
    # Имя файла: combination_00.svg … combination_63.svg
    filename = f"{mask}.svg"
    filepath = os.path.join(out_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

print("Готово. 64 SVG‑файла созданы в", out_dir)