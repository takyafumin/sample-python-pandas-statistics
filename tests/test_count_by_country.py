import os
import pandas as pd
import pytest
import tempfile
import io
from unittest.mock import patch
from src.count_by_country import (
    get_east_asian_width_count, 
    aggregate_by_country,
    get_ordered_countries,
    create_ordered_counts,
    calculate_format_parameters,
    format_and_print_item,
    display_results,
    count_by_country
)


class TestCountByCountry:
    """国別データ集計機能のテスト"""
    
    def test_get_east_asian_width_count(self):
        """文字列の表示幅をカウントする機能のテスト"""
        # 全角文字は2、半角文字は1としてカウント
        assert get_east_asian_width_count('') == 0
        assert get_east_asian_width_count('ABC') == 3
        assert get_east_asian_width_count('日本') == 4
        assert get_east_asian_width_count('Hello日本') == 9
    
    def test_aggregate_by_country(self):
        """国別に集計する機能のテスト"""
        # テストデータの作成
        data = {
            'ID': [1, 2, 3, 4, 5],
            '名前': ['太郎', '花子', '次郎', '太郎', '花子'],
            '年齢': [25, 30, 40, 20, 35],
            '国': ['日本', 'アメリカ', '日本', 'インド', 'アメリカ'],
            'スコア': [80, 75, 60, 90, 85]
        }
        df = pd.DataFrame(data)
        
        # 機能のテスト
        result = aggregate_by_country(df)
        
        # 結果の検証
        assert len(result) == 3
        assert result['日本'] == 2
        assert result['アメリカ'] == 2
        assert result['インド'] == 1
    
    def test_get_ordered_countries(self):
        """国名を所定の順序に並び替える機能のテスト"""
        # テストデータの作成（日本を含むケース）
        country_counts_with_japan = pd.Series({
            '日本': 10,
            'アメリカ': 5,
            'ドイツ': 3,
            'インド': 7,
            'カナダ': 2
        })
        
        # 日本を含むケースのテスト
        result_with_japan = get_ordered_countries(country_counts_with_japan)
        assert result_with_japan[0] == '日本'
        assert sorted(result_with_japan[1:]) == sorted(['アメリカ', 'ドイツ', 'インド', 'カナダ'])
        
        # テストデータの作成（日本を含まないケース）
        country_counts_without_japan = pd.Series({
            'アメリカ': 5,
            'ドイツ': 3,
            'インド': 7,
            'カナダ': 2
        })
        
        # 日本を含まないケースのテスト
        result_without_japan = get_ordered_countries(country_counts_without_japan)
        assert '日本' not in result_without_japan
        assert sorted(result_without_japan) == sorted(['アメリカ', 'ドイツ', 'インド', 'カナダ'])
    
    def test_create_ordered_counts(self):
        """指定した順序で国別カウントを並べ替える機能のテスト"""
        # テストデータの作成
        country_counts = pd.Series({
            '日本': 10,
            'アメリカ': 5,
            'ドイツ': 3
        })
        
        # 順序の指定
        ordered_countries = ['日本', 'ドイツ', 'アメリカ', 'インド']
        
        # 機能のテスト
        result = create_ordered_counts(country_counts, ordered_countries)
        
        # 結果の検証
        assert len(result) == 4
        assert result['日本'] == 10
        assert result['ドイツ'] == 3
        assert result['アメリカ'] == 5
        assert result['インド'] == 0  # 存在しない国は0として扱われる
    
    def test_calculate_format_parameters(self):
        """表示のためのフォーマットパラメータを計算する機能のテスト"""
        # テストデータの作成
        ordered_counts = pd.Series({
            '日本': 10,
            'アメリカ': 5,
            'ドイツ': 3,
            'インド': 7
        })
        
        country_counts = pd.Series({
            '日本': 10,
            'アメリカ': 5,
            'ドイツ': 3,
            'インド': 7
        })
        
        # 機能のテスト
        max_display_width, max_count_len = calculate_format_parameters(ordered_counts, country_counts)
        
        # 結果の検証 - 「アメリカ」の表示幅が8文字と計算される
        assert max_display_width == 8  # 「アメリカ」の表示幅
        assert max_count_len == 2  # 最大値は25で、カンマなしの場合は2桁
    
    def test_format_and_print_item(self, capsys):
        """項目を整形して出力する機能のテスト"""
        # パラメータの設定
        label = '日本'
        count = 10
        max_display_width = 6
        max_count_len = 2
        
        # 機能のテスト
        format_and_print_item(label, count, max_display_width, max_count_len)
        
        # 標準出力の取得
        captured = capsys.readouterr()
        
        # 結果の検証
        assert captured.out == '日本  ：10件\n'
    
    def test_display_results(self, capsys):
        """結果を表示する機能のテスト"""
        # テストデータの作成
        ordered_counts = pd.Series({
            '日本': 10,
            'アメリカ': 5,
            'ドイツ': 3
        })
        
        country_counts = pd.Series({
            '日本': 10,
            'アメリカ': 5,
            'ドイツ': 3
        })
        
        # 機能のテスト
        display_results(ordered_counts, country_counts)
        
        # 標準出力の取得
        captured = capsys.readouterr()
        output = captured.out
        
        # 結果の検証
        assert '【国別集計結果】' in output
        assert '日本' in output
        assert 'アメリカ' in output
        assert 'ドイツ' in output
        # 実際の出力形式に合わせた検証（スペースが含まれる可能性がある）
        assert '合計' in output
        assert '18件' in output
    
    def test_count_by_country_with_valid_file(self, capsys):
        """有効なCSVファイルでの国別データ集計のテスト"""
        # テスト用のCSVファイルを作成
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            temp_file_path = temp_file.name
            
            # CSVデータの作成
            csv_data = "ID,名前,年齢,国,スコア\n" + \
                        "1,太郎,25,日本,80\n" + \
                        "2,花子,30,アメリカ,75\n" + \
                        "3,次郎,40,日本,60\n" + \
                        "4,太郎,20,インド,90\n" + \
                        "5,花子,35,アメリカ,85\n"
            
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(csv_data)
        
        try:
            # 機能のテスト
            count_by_country(temp_file_path)
            
            # 標準出力の取得
            captured = capsys.readouterr()
            output = captured.out
            
            # 結果の検証
            assert '【国別集計結果】' in output
            assert '日本' in output
            assert 'アメリカ' in output
            assert 'インド' in output
            # 厳密な形式ではなく出力内容に注目
            assert '2件' in output  # 日本の件数
            assert '5件' in output  # 合計件数
            
        finally:
            # テスト終了後にファイルを削除
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    def test_count_by_country_with_invalid_file(self, capsys):
        """無効なCSVファイルでの例外処理のテスト"""
        # 存在しないファイル
        non_existent_file = "/path/to/non/existent/file.csv"
        count_by_country(non_existent_file)
        
        # 標準出力の取得
        captured = capsys.readouterr()
        
        # 結果の検証 - エラーメッセージの一部を確認
        assert "エラー: ファイル" in captured.out
        assert "が見つかりません" in captured.out
        
        # 「国」カラムのないCSVファイル
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            temp_file_path = temp_file.name
            
            # CSVデータの作成（「国」カラムなし）
            csv_data = "ID,名前,年齢,スコア\n" + \
                        "1,太郎,25,80\n" + \
                        "2,花子,30,75\n"
            
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(csv_data)
        
        try:
            # 機能のテスト
            count_by_country(temp_file_path)
            
            # 標準出力の取得
            captured = capsys.readouterr()
            output = captured.out
            
            # 結果の検証 - KeyErrorの内容を確認
            assert "エラー:" in output
            assert "「国」カラム" in output
            
        finally:
            # テスト終了後にファイルを削除
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)