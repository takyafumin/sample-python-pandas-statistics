import csv
import random
import argparse
import os

def generate_sample_data(file_name, num_rows):
    """
    指定された行数のサンプルデータを生成してCSVファイルに保存する
    
    Args:
        file_name: 生成するCSVファイルのパス
        num_rows: 生成するデータの行数
    """
    # サンプルデータのヘッダー
    headers = ["ID", "名前", "年齢", "国", "スコア"]
    names = ["太郎", "花子", "次郎", "美咲", "健一"]
    countries = ["日本", "アメリカ", "ドイツ", "インド", "カナダ"]
    
    print(f"{num_rows}件のサンプルデータを生成しています...")
    
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
                row = [
                    i,  # ID
                    random.choice(names),  # ランダムな名前
                    random.randint(18, 60),  # 年齢 (18〜60)
                    random.choice(countries),  # ランダムな国
                    round(random.uniform(0, 100), 2),  # スコア (0〜100, 小数点2桁)
                ]
                batch_rows.append(row)
                
                # 進捗状況を表示（10万件ごと）
                if i % 100000 == 0:
                    print(f"{i}件生成済み...")
            
            # バッチ単位でまとめて書き込み
            writer.writerows(batch_rows)
    
    print(f"完了: {num_rows}件のデータを{file_name}に生成しました。")

if __name__ == "__main__":
    # コマンドラインからパラメータを受け取る
    parser = argparse.ArgumentParser(description='サンプルデータのCSVを生成します。')
    parser.add_argument('--rows', type=int, default=5000, 
                        help='生成する行数 (デフォルト: 5,000)')
    parser.add_argument('--output', type=str, default="resources/csv/sample_data.csv", 
                        help='出力ファイル名 (デフォルト: resources/csv/sample_data.csv)')
    args = parser.parse_args()
    
    # サンプルデータを生成
    generate_sample_data(args.output, args.rows)
