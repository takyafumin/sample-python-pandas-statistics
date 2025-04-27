import os
import csv
import pytest
import tempfile
from src.generate_sample_data import generate_sample_data


class TestGenerateSampleData:
    """サンプルデータ生成機能のテスト"""
    
    def test_generate_sample_data_creates_file(self):
        """ファイルが正常に作成されることをテスト"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            temp_file_path = temp_file.name
        
        try:
            # テスト実行
            generate_sample_data(temp_file_path, 10)
            
            # ファイルが存在するか確認
            assert os.path.exists(temp_file_path), f"ファイル {temp_file_path} が作成されていません"
            
            # 正確に11行（ヘッダー + 10行のデータ）あるか確認
            with open(temp_file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                assert len(rows) == 11, f"生成されたデータ行数が不正です（期待値: 11, 実際: {len(rows)}）"
                
                # ヘッダーが正しいか確認
                assert rows[0] == ["ID", "名前", "年齢", "国", "スコア"], "ヘッダーが正しくありません"
                
                # データが正しい形式か確認
                for i, row in enumerate(rows[1:], 1):
                    assert len(row) == 5, f"行 {i} のカラム数が不正です"
                    assert int(row[0]) == i, f"行 {i} のIDが不正です"
                    assert row[1] in ["太郎", "花子", "次郎", "美咲", "健一"], f"行 {i} の名前が不正です"
                    assert 18 <= int(row[2]) <= 60, f"行 {i} の年齢が範囲外です"
                    assert row[3] in ["日本", "アメリカ", "ドイツ", "インド", "カナダ"], f"行 {i} の国名が不正です"
                    score = float(row[4])
                    assert 0 <= score <= 100, f"行 {i} のスコアが範囲外です"
        
        finally:
            # テスト終了後にファイルを削除
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    def test_generate_sample_data_with_invalid_rows(self):
        """無効な行数で例外が発生することをテスト"""
        with tempfile.NamedTemporaryFile(suffix='.csv') as temp_file:
            # 無効な行数（0以下）でエラーが発生するか確認
            with pytest.raises(ValueError) as excinfo:
                generate_sample_data(temp_file.name, 0)
            assert "行数は1以上の整数を指定してください" in str(excinfo.value)
            
            with pytest.raises(ValueError) as excinfo:
                generate_sample_data(temp_file.name, -5)
            assert "行数は1以上の整数を指定してください" in str(excinfo.value)
    
    def test_generate_sample_data_with_invalid_path(self, monkeypatch, capsys):
        """無効なファイルパスに対するエラー出力をテスト"""
        # os.makedirsをモックして常に例外を発生させる
        def mock_makedirs(*args, **kwargs):
            raise PermissionError("テスト用の権限エラー")
        
        # os.makedirsをモック関数に置き換え
        monkeypatch.setattr(os, "makedirs", mock_makedirs)
        
        # どのようなパスでもPermissionErrorが発生するはず
        generate_sample_data("test.csv", 10)
        
        # 標準出力の取得
        captured = capsys.readouterr()
        
        # エラーメッセージの検証
        assert "エラー: ファイル" in captured.out
        assert "への書き込み権限がありません" in captured.out
