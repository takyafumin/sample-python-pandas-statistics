#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import os
import unicodedata

def get_east_asian_width_count(text):
    """
    文字列の表示幅をカウントする（全角文字は2、半角文字は1としてカウント）
    
    Args:
        text: カウント対象の文字列
        
    Returns:
        int: 表示幅の合計
    """
    count = 0
    for c in text:
        # East Asian Ambiguous は全角として扱う
        if unicodedata.east_asian_width(c) in ['F', 'W', 'A']:
            count += 2
        else:
            count += 1
    return count

def aggregate_by_country(df):
    """
    国別に集計する
    
    Args:
        df: 集計対象のDataFrame
        
    Returns:
        pd.Series: 国別の集計結果
    """
    return df['国'].value_counts()

def get_ordered_countries(country_counts):
    """
    国名を所定の順序に並び替える（日本を先頭に、それ以外は五十音順）
    
    Args:
        country_counts: 国別集計結果
        
    Returns:
        list: 並び替えた国名リスト
    """
    # 国名のリストを取得（日本を除く）
    other_countries = sorted([country for country in country_counts.index if country != '日本'])
    
    # 並び順を指定（日本を先頭に、あとは五十音順）
    return ['日本'] + other_countries if '日本' in country_counts.index else other_countries

def create_ordered_counts(country_counts, ordered_countries):
    """
    指定した順序で国別カウントを並べ替える
    
    Args:
        country_counts: 国別集計結果
        ordered_countries: 並び替えた国名リスト
        
    Returns:
        pd.Series: 並び替えた国別集計結果
    """
    return pd.Series([country_counts.get(country, 0) for country in ordered_countries], 
                   index=ordered_countries)

def calculate_format_parameters(ordered_counts, country_counts):
    """
    表示のためのフォーマットパラメータを計算する
    
    Args:
        ordered_counts: 並び替えた国別集計結果
        country_counts: 国別集計結果
        
    Returns:
        tuple: (最大表示幅, 数値の最大桁数)
    """
    # 最長の国名の表示幅を取得
    max_display_width = max([get_east_asian_width_count(country) for country in ordered_counts.index])
    max_display_width = max(max_display_width, get_east_asian_width_count("合計"))
    
    # 数値の最大桁数を取得（カンマ表示も考慮）
    max_count = max(max(ordered_counts), country_counts.sum())
    max_count_len = len(f"{max_count:,}")
    
    return max_display_width, max_count_len

def format_and_print_item(label, count, max_display_width, max_count_len):
    """
    項目を整形して出力する
    
    Args:
        label: 表示ラベル（国名または合計）
        count: カウント数
        max_display_width: 最大表示幅
        max_count_len: 数値の最大桁数
        
    Returns:
        None
    """
    padding = max_display_width - get_east_asian_width_count(label)
    padding_spaces = " " * padding
    formatted_count = f"{count:,}".rjust(max_count_len)
    print(f'{label}{padding_spaces}：{formatted_count}件')

def display_results(ordered_counts, country_counts):
    """
    結果を表示する
    
    Args:
        ordered_counts: 並び替えた国別集計結果
        country_counts: 国別集計結果
        
    Returns:
        None
    """
    print('【国別集計結果】')
    
    # フォーマットパラメータを計算
    max_display_width, max_count_len = calculate_format_parameters(ordered_counts, country_counts)
    
    # 国別のカウントを表示
    for country, count in ordered_counts.items():
        format_and_print_item(country, count, max_display_width, max_count_len)
    
    # 合計件数を表示
    format_and_print_item("合計", country_counts.sum(), max_display_width, max_count_len)

def count_by_country(file_path):
    """
    CSVファイルを読み込み、国別の件数を集計する
    
    Args:
        file_path: CSVファイルのパス
        
    Returns:
        None
    
    Raises:
        FileNotFoundError: ファイルが存在しない場合
        KeyError: CSVファイルに「国」カラムが存在しない場合
        pd.errors.EmptyDataError: CSVファイルが空の場合
        pd.errors.ParserError: CSVファイルの形式が不正な場合
    """
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(file_path)
        
        # 「国」カラムの存在確認
        if '国' not in df.columns:
            raise KeyError("CSVファイルに「国」カラムが存在しません")
        
        # 国別にカウント
        country_counts = aggregate_by_country(df)
        
        # 国名を所定の順序に並び替え
        ordered_countries = get_ordered_countries(country_counts)
        
        # 指定した順序で国別カウントを並べ替え
        ordered_counts = create_ordered_counts(country_counts, ordered_countries)
        
        # 結果を表示
        display_results(ordered_counts, country_counts)
        
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません")
    except KeyError as e:
        print(f"エラー: {str(e)}")
    except pd.errors.EmptyDataError:
        print(f"エラー: ファイル '{file_path}' は空です")
    except pd.errors.ParserError:
        print(f"エラー: ファイル '{file_path}' はCSV形式として解析できません")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {str(e)}")


if __name__ == "__main__":
    try:
        # プロジェクトのルートディレクトリからの相対パス
        file_path = os.path.join("resources", "csv", "sample_data.csv")
        
        # ファイルの存在確認
        if not os.path.exists(file_path):
            print(f"エラー: ファイル '{file_path}' が見つかりません")
        else:
            count_by_country(file_path)
    except Exception as e:
        print(f"プログラムの実行中にエラーが発生しました: {str(e)}")
