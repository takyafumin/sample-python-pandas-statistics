import csv
import random
import argparse
import os
import pandas as pd

def load_country_region_map(file_path=None):
    """
    国と地域のマッピングをマスタデータからロードする
    
    Args:
        file_path: マスタデータのCSVファイルのパス（省略時はデフォルトのパスを使用）
        
    Returns:
        dict: 国名をキー、地域名を値とする辞書
    """
    if file_path is None:
        # デフォルトのファイルパス
        file_path = os.path.join("resources", "master", "country_region_map.csv")
    
    try:
        # CSVファイルからマスタデータを読み込む
        master_df = pd.read_csv(file_path)
        
        # 必要なカラムが存在するか確認
        required_columns = ["国名", "地域名"]
        if not all(col in master_df.columns for col in required_columns):
            print(f"警告: マスタファイル '{file_path}' には必要なカラムが不足しています")
            return get_default_country_region_map()
        
        # 国名と地域名のマッピング辞書を作成
        country_region_map = dict(zip(master_df["国名"], master_df["地域名"]))
        return country_region_map
    
    except Exception as e:
        print(f"警告: マスタファイル '{file_path}' の読み込みに失敗しました: {str(e)}")
        # マスタファイルの読み込みに失敗した場合はデフォルトのマッピングを返す
        return get_default_country_region_map()

def get_default_country_region_map():
    """
    デフォルトの国と地域のマッピングを定義する（マスタデータの読み込みに失敗した場合のフォールバック）
    
    Returns:
        dict: 国名をキー、地域名を値とする辞書
    """
    return {
        # アジア州
        '日本': 'アジア',
        '中国': 'アジア',
        '韓国': 'アジア',
        'インド': 'アジア',
        'タイ': 'アジア',
        'ベトナム': 'アジア',
        'インドネシア': 'アジア',
        'マレーシア': 'アジア',
        'シンガポール': 'アジア',
        'フィリピン': 'アジア',
        
        # ヨーロッパ州
        'ドイツ': 'ヨーロッパ',
        'フランス': 'ヨーロッパ',
        'イギリス': 'ヨーロッパ',
        'イタリア': 'ヨーロッパ',
        'スペイン': 'ヨーロッパ',
        'オランダ': 'ヨーロッパ',
        'スイス': 'ヨーロッパ',
        'スウェーデン': 'ヨーロッパ',
        'ノルウェー': 'ヨーロッパ',
        'ロシア': 'ヨーロッパ',
        
        # アフリカ州
        'エジプト': 'アフリカ',
        'ケニア': 'アフリカ',
        '南アフリカ': 'アフリカ',
        'モロッコ': 'アフリカ',
        'ナイジェリア': 'アフリカ',
        'エチオピア': 'アフリカ',
        'ガーナ': 'アフリカ',
        'タンザニア': 'アフリカ',
        'アルジェリア': 'アフリカ',
        'チュニジア': 'アフリカ',
        
        # 北アメリカ州
        'アメリカ': '北アメリカ',
        'カナダ': '北アメリカ',
        'メキシコ': '北アメリカ',
        'キューバ': '北アメリカ',
        'パナマ': '北アメリカ',
        'ジャマイカ': '北アメリカ',
        'コスタリカ': '北アメリカ',
        'グアテマラ': '北アメリカ',
        
        # 南アメリカ州
        'ブラジル': '南アメリカ',
        'アルゼンチン': '南アメリカ',
        'コロンビア': '南アメリカ',
        'チリ': '南アメリカ',
        'ペルー': '南アメリカ',
        'ベネズエラ': '南アメリカ',
        'エクアドル': '南アメリカ',
        'ボリビア': '南アメリカ',
        
        # オセアニア州
        'オーストラリア': 'オセアニア',
        'ニュージーランド': 'オセアニア',
        'フィジー': 'オセアニア',
        'パプアニューギニア': 'オセアニア',
        'ソロモン諸島': 'オセアニア',
        'バヌアツ': 'オセアニア',
        'サモア': 'オセアニア'
    }

def generate_sample_data(file_name, num_rows):
    """
    指定された行数のサンプルデータを生成してCSVファイルに保存する
    
    Args:
        file_name: 生成するCSVファイルのパス
        num_rows: 生成するデータの行数
        
    Raises:
        ValueError: 無効な行数が指定された場合
        PermissionError: ファイル書き込み権限がない場合
        IOError: ファイル操作に関連する問題が発生した場合
    """
    # 入力値の検証
    if num_rows <= 0:
        raise ValueError("行数は1以上の整数を指定してください")
    
    # サンプルデータのヘッダー
    headers = ["ID", "名前", "年齢", "国", "スコア"]
    names = ["太郎", "花子", "次郎", "美咲", "健一"]
    
    # テストで期待される国のリスト
    countries = ["日本", "アメリカ", "ドイツ", "インド", "カナダ"]
    
    # 国名と地域のマッピングをロード
    country_region_map = load_country_region_map()
    
    print(f"{num_rows}件のサンプルデータを生成しています...")
    
    try:
        # 親ディレクトリが存在しない場合は作成する
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        # CSVファイルにデータを書き込む
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # ヘッダーを書き込む
            
            # バッチサイズを設定して大量データの生成を効率化
            batch_size = 10000
            for start_idx in range(1, num_rows + 1, batch_size):
                batch_rows = []
                end_idx = min(start_idx + batch_size - 1, num_rows)
                
                for i in range(start_idx, end_idx + 1):
                    # ランダムな国を選択
                    country = random.choice(countries)
                    
                    # 国に対応する地域を取得（マッピングにない場合は「その他」）
                    region = country_region_map.get(country, 'その他')
                    
                    row = [
                        i,  # ID
                        random.choice(names),  # ランダムな名前
                        random.randint(18, 60),  # 年齢 (18〜60)
                        country,  # ランダムな国
                        round(random.uniform(0, 100), 2),  # スコア (0〜100, 小数点2桁)
                    ]
                    batch_rows.append(row)
                    
                    # 進捗状況を表示（10万件ごと）
                    if i % 100000 == 0:
                        print(f"{i}件生成済み...")
                
                # バッチ単位でまとめて書き込み
                writer.writerows(batch_rows)
        
        print(f"完了: {num_rows}件のデータを{file_name}に生成しました。")
        
    except PermissionError:
        print(f"エラー: ファイル '{file_name}' への書き込み権限がありません")
    except OSError as e:
        if e.errno == 28:  # No space left on device
            print("エラー: ディスク容量が不足しています")
        else:
            print(f"ファイル操作エラー: {str(e)}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {str(e)}")

if __name__ == "__main__":
    try:
        # コマンドラインからパラメータを受け取る
        parser = argparse.ArgumentParser(description='サンプルデータのCSVを生成します。')
        parser.add_argument('--rows', type=int, default=5000, 
                            help='生成する行数 (デフォルト: 5,000)')
        parser.add_argument('--output', type=str, default="resources/csv/sample_data.csv", 
                            help='出力ファイル名 (デフォルト: resources/csv/sample_data.csv)')
        args = parser.parse_args()
        
        # 引数の検証
        if args.rows <= 0:
            print("エラー: 行数は1以上の整数を指定してください")
        else:
            # サンプルデータを生成
            generate_sample_data(args.output, args.rows)
            
    except ValueError as e:
        print(f"エラー: {str(e)}")
    except Exception as e:
        print(f"プログラムの実行中にエラーが発生しました: {str(e)}")
