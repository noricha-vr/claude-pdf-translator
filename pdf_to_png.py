import os
from pdf2image import convert_from_path
from pathlib import Path

def convert_pdf_to_png(pdf_path, output_dir='output'):
    """
    PDFファイルを連番のPNGファイルに変換する
    
    Args:
        pdf_path (str): 入力PDFファイルのパス
        output_dir (str): 出力ディレクトリ（デフォルト: 'output'）
    """
    # 出力ディレクトリの作成
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # PDFをPNGに変換
        images = convert_from_path(pdf_path)
        
        # 各ページを連番で保存
        for i, image in enumerate(images):
            # 3桁の連番でファイル名を生成（001.png, 002.png, ...）
            output_file = os.path.join(output_dir, f'{i+1:03d}.png')
            image.save(output_file, 'PNG')
            print(f'Saved: {output_file}')
            
    except Exception as e:
        print(f'エラーが発生しました: {str(e)}')

def main():
    # 入力PDFファイルのパス
    pdf_path = 'sample.pdf'  # ここに実際のPDFファイルパスを指定してください
    
    # PDFが存在するか確認
    if not os.path.exists(pdf_path):
        print('PDFファイルが見つかりません。')
        return
    
    # 変換を実行
    convert_pdf_to_png(pdf_path)

if __name__ == '__main__':
    main()
