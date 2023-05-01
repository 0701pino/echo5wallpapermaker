from PIL import Image
import os
import sys

# 引数からファイルパスを取得
if len(sys.argv) != 2:
    print("Usage: python make_wall_paper.py target")
    sys.exit(1)
else:
    target_path  = sys.argv[1]

# 出力ディレクトリ
OUTPUT_DIR = "output"
# リサイズするサイズ
WIDTH, HEIGHT = 960, 480

# 出力先ディレクトリが存在しなければ作成
if os.path.isabs(OUTPUT_DIR):
    print("This is an absolute path.")
else:
    # 相対パスの場合は、入力ファイル/ディレクトリと同じ階層に出力ディレクトリを作成する
    output_path = os.path.join(os.path.dirname(target_path), OUTPUT_DIR)

if not os.path.exists(output_path):
    os.makedirs(output_path)

print("output path:" + output_path )

def resize_image(filepath):
    # ファイル名と拡張子を取得
    filename, ext = os.path.splitext(os.path.basename(filepath))

    # 出力先ファイルパスを作成
    output_filepath = os.path.join(output_path, f"{filename}_convert{ext}")

    # 出力先ファイルが存在する場合は処理をスキップ
    if os.path.exists(output_filepath):
        print(f"{output_filepath} already exists, skipping")
        return

    # 画像を開く
    try:
        img = Image.open(filepath)
    except:
        print(f"{filepath} isn't image, skipping")
        return

    # 現在のサイズを取得
    img_width, img_height = img.size

    # 縦横比を維持したまま指定サイズに収まるようにリサイズ
    if img_width > WIDTH or img_height > HEIGHT:
        width_ratio = img_width / WIDTH
        height_ratio = img_height / HEIGHT
    else:
        width_ratio = 1
        height_ratio = 1

    # 縦横比を維持したまま指定サイズに収まるようにリサイズ
    if width_ratio > height_ratio:
        resize_width = WIDTH
        resize_height = int(img_height * (WIDTH / img_width))
    else:
        resize_width = int(img_width * (HEIGHT / img_height))
        resize_height = HEIGHT

    # リサイズ処理
    resized_img = img.resize((resize_width, resize_height), Image.LANCZOS)


    # 背景画像を作成
    background_img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))

    # リサイズした画像を中央に配置
    x = int((WIDTH - resize_width) / 2)
    y = int((HEIGHT - resize_height) / 2)
    background_img.paste(resized_img, (x, y))

    # 画像を保存
    background_img.save(output_filepath)
    print(f"{filepath} -> {output_filepath}")

if os.path.isdir(target_path):
    # ディレクトリが指定された場合は、ディレクトリ内のすべてのファイルを処理
    for root, dirs, files in os.walk(target_path):
        for file in files:
            resize_image(os.path.join(root, file))
else:
    # ファイルが指定された場合
    resize_image(target_path)