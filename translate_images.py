import os
from pathlib import Path
from anthropic import Anthropic
import base64
from PIL import Image
import time

def encode_image(image_path):
    """画像をbase64エンコードする"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def translate_image(client, image_path):
    """画像を翻訳する"""
    try:
        with Image.open(image_path) as img:
            base64_image = encode_image(image_path)
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": f"image/{img.format.lower()}",
                                    "data": base64_image
                                }
                            },
                            {
                                "type": "text",
                                "text": "この画像の内容を日本語で詳しく説明してください。"
                            }
                        ]
                    }
                ]
            )
            
            return message.content[0].text
            
    except Exception as e:
        return f"エラーが発生しました（{image_path}）: {str(e)}"

def translate_all_images(input_dir='output', output_file='translated.md'):
    """ディレクトリ内の全画像を翻訳してMarkdownファイルに保存"""
    # APIクライアントの初期化
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    client = Anthropic()
    
    # 出力ファイルの準備
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# PDF翻訳結果\n\n")
        
        # 画像ファイルを取得してソート
        image_files = sorted(
            [f for f in os.listdir(input_dir) if f.endswith('.png')],
            key=lambda x: int(x.split('.')[0])
        )
        
        total_images = len(image_files)
        
        # 各画像を翻訳
        for i, image_file in enumerate(image_files, 1):
            image_path = os.path.join(input_dir, image_file)
            print(f"翻訳中 ({i}/{total_images}): {image_file}")
            
            # 翻訳を実行
            translation = translate_image(client, image_path)
            
            # Markdownに書き込み
            f.write(f"## ページ {i}\n\n")
            f.write(f"{translation}\n\n")
            
            # APIレート制限を考慮して少し待機
            time.sleep(1)
            
        print(f"\n翻訳が完了しました。結果は {output_file} に保存されました。")

def main():
    try:
        translate_all_images()
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main() 
