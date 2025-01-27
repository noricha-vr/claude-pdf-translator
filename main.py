import os
import base64
from anthropic import Anthropic
from PIL import Image
import io
import time

def encode_image(image_path):
    """画像をbase64エンコードする"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def translate_image(img_dir, output_file='translated.md', start_page=1):
    """指定ディレクトリの画像を順番に翻訳してMDファイルに保存する"""
    # APIキーの取得
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    
    # Anthropicクライアントの初期化
    client = Anthropic()
    
    try:
        # 出力ファイルの準備
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# PDF翻訳結果\n\n")
            
            # 画像ファイルを取得してソート
            image_files = sorted(
                [f for f in os.listdir(img_dir) if f.endswith('.png')],
                key=lambda x: int(x.split('.')[0])
            )
            
            # 開始ページから処理を開始
            image_files = image_files[start_page-1:]
            total_images = len(image_files)
            
            # 各画像を翻訳
            for i, image_file in enumerate(image_files, start_page):
                image_path = os.path.join(img_dir, image_file)
                print(f"翻訳中 ({i}/{total_images + start_page - 1}): {image_file}")
                
                try:
                    with Image.open(image_path) as img:
                        base64_image = encode_image(image_path)
                        
                        # APIリクエストの作成と送信
                        message = client.messages.create(
                            model="claude-3-5-sonnet-latest",
                            max_tokens=4096,
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
                                            "text": "日本語に翻訳してください。"
                                        }
                                    ]
                                }
                            ]
                        )
                        
                        # Markdownに書き込み
                        f.write(f"## ページ {i}\n\n")
                        f.write(f"{message.content[0].text}\n\n")
                        
                        # APIレート制限を考慮して少し待機
                        time.sleep(1)
                except Exception as e:
                    f.write(f"## ページ {i}\n\n")
                    f.write(f"エラーが発生しました: {str(e)}\n\n")
                    
            print(f"\n翻訳が完了しました。結果は {output_file} に保存されました。")
            
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def main():
    """メイン関数"""
    # 画像ディレクトリのパスを指定
    image_dir = "./output"
    os.makedirs(image_dir, exist_ok=True)
    
    # 翻訳を実行（4ページ目から開始）
    result = translate_image(image_dir, start_page=1)
    if result:  # エラーメッセージがある場合
        print("\nエラー:")
        print(result)

if __name__ == "__main__":
    main()
