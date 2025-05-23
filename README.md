# Python Pandas 統計処理プロジェクト

このプロジェクトはPandasを使用してCSVデータの統計処理を行うサンプルプロジェクトです。

## 概要

このプロジェクトでは、サンプルデータを生成し、Pandasを使用してデータ分析や統計処理を行います。

## ファイル構成

```
requirements.txt      # 必要なライブラリの一覧
resources/
    csv/
        sample_data.csv  # サンプルデータファイル
    master/
        country_region_map.csv  # 国と地域のマッピングデータ
src/
    generate_sample_data.py  # サンプルデータ生成スクリプト
    count_by_country.py      # 国別・地域別データ集計スクリプト
```

## セットアップ方法

### 必要なライブラリ

このプロジェクトでは以下のライブラリを使用します：
- pandas
- numpy
- unicodedata
- matplotlib (データ可視化用)

### 環境構築

1. 仮想環境を作成し、アクティベートします：

```bash
source venv/bin/activate  # macOSの場合
# または
venv\Scripts\activate  # Windowsの場合
```

2. 必要なライブラリをインストールします：

```bash
pip install -r requirements.txt
```

## 使用方法

### サンプルデータの生成

以下のコマンドを実行してサンプルデータを生成します：

```bash
python src/generate_sample_data.py
```

このスクリプトは以下の項目を含む100件のランダムなデータを生成します：
- ID: 連番
- 名前: 5種類の名前からランダム選択
- 年齢: 18〜60歳のランダムな値
- 国: 5カ国からランダム選択
- スコア: 0〜100の範囲のランダムな数値（小数点2桁）

生成されたデータは `sample_data.csv` として保存されます。

### 国別・地域別データの集計

以下のコマンドを実行して、CSVファイルから国別・地域別のデータ件数を集計します：

```bash
python src/count_by_country.py
```

このスクリプトは `sample_data.csv` ファイルを読み込み、次の処理を行います：
- 国ごとのデータ件数を集計（日本を先頭に、他の国は五十音順で表示）
- `country_region_map.csv` のマッピングデータを使用して地域ごとのデータ件数を集計
- 国別・地域別の集計結果を整形して表示（全角・半角文字の表示幅を考慮）

### テストの実行

以下のコマンドでテストを実行できます：

```bash
# すべてのテストを実行
pytest

# 詳細な出力でテストを実行
pytest -v

# テストカバレッジレポートを生成
pytest --cov=src tests/
```

テストはプロジェクトの機能が正しく動作することを確認するために作成されています。テストファイルは `tests/` ディレクトリに配置されています。

## 今後の開発予定

- 基本統計量の計算
- データのグループ化と分析
- グラフによるデータ可視化
- より複雑な統計モデルの実装
