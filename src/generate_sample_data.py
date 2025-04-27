import csv
import random

def generate_sample_data(file_name, num_rows):
    # サンプルデータのヘッダー
    headers = ["ID", "名前", "年齢", "国", "スコア"]
    names = ["太郎", "花子", "次郎", "美咲", "健一"]
    countries = ["日本", "アメリカ", "ドイツ", "インド", "カナダ"]

    # CSVファイルにデータを書き込む
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # ヘッダーを書き込む

        for i in range(1, num_rows + 1):
            row = [
                i,  # ID
                random.choice(names),  # ランダムな名前
                random.randint(18, 60),  # 年齢 (18〜60)
                random.choice(countries),  # ランダムな国
                round(random.uniform(0, 100), 2),  # スコア (0〜100, 小数点2桁)
            ]
            writer.writerow(row)

if __name__ == "__main__":
    generate_sample_data("resources/csv/sample_data.csv", 100)  # 100行のサンプルデータを生成
