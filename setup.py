import json
import requests
import os
from urllib.parse import urlparse, parse_qs
import areaImage


class MapImageDownloader:
    def __init__(self, config_path="settings.json"):
        """
        マップ画像ダウンローダーの初期化
        
        Args:
            config_path (str): 設定ファイルのパス
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.base_url_template = self.config["url"]["mapImage"]["sampleURL"]
        self.base_map_dir = self.config["map"]["baseMapAssetsDir"]
        
        # サンプルURLから動的にパターンを抽出
        self._extract_url_pattern()
    
    def _extract_url_pattern(self):
        """
        サンプルURLからパターンを抽出
        """
        from urllib.parse import urlparse
        
        parsed_url = urlparse(self.base_url_template)
        path_parts = parsed_url.path.split('/')
        
        # パスから Day1-e456/2-1.png のような部分を特定
        for i, part in enumerate(path_parts):
            if part.startswith('Day') and '-' in part:
                self.original_day_area = part
                self.original_filename = path_parts[i + 1]
                break
        else:
            # フォールバック: デフォルト値を使用
            self.original_day_area = "Day1-e456"
            self.original_filename = "2-1.png"
        
        # ファイル名から座標を抽出 (例: "2-1.png" -> x=2, y=1)
        filename_base = self.original_filename.replace('.png', '')
        if '-' in filename_base:
            self.original_x, self.original_y = map(int, filename_base.split('-'))
        else:
            self.original_x, self.original_y = 0, 0
        
    def generate_image_url(self, day_area, x, y, sub_type="main"):
        """
        指定された位置の画像URLを生成
        
        Args:
            day_area (str): 日とエリア（例: "Day1-e7", "Day2-w12"）
            x (int): X座標
            y (int): Y座標
            sub_type (str): メインまたはサブ（"main" or "sub"）
            
        Returns:
            str: 生成された画像URL
        """
        # 元のパスパターンを新しい値に置換
        original_path = f"{self.original_day_area}/{self.original_filename}"
        
        if sub_type == "sub":
            # subの場合は overlay-Day1-e456 形式
            new_path = f"overlay-{day_area}/{x}-{y}.png"
        else:
            # mainの場合は Day1-e456 形式
            new_path = f"{day_area}/{x}-{y}.png"
        
        return self.base_url_template.replace(original_path, new_path)
    
    def get_folder_path(self, day_area, sub_type="main"):
        """
        保存先フォルダパスを取得
        
        Args:
            day_area (str): 日とエリア（例: "Day1-e7"）
            sub_type (str): メインまたはサブ（"main" or "sub"）
            
        Returns:
            str: フォルダパス
        """
        # Day1-e7 -> e7-day1 の形式に変換
        day, area = day_area.split("-")
        day_num = day.replace("Day", "day").lower()
        folder_name = f"{area}-{day_num}"
        
        return os.path.join(self.base_map_dir, folder_name, sub_type)
    
    def download_image(self, day_area, x, y, sub_type="main"):
        """
        指定された位置の画像をダウンロード
        
        Args:
            day_area (str): 日とエリア（例: "Day1-e7"）
            x (int): X座標
            y (int): Y座標
            sub_type (str): メインまたはサブ（"main" or "sub"）
            
        Returns:
            bool: ダウンロード成功の可否
        """
        try:
            # URLを生成
            url = self.generate_image_url(day_area, x, y, sub_type)
            
            # フォルダパスを取得
            folder_path = self.get_folder_path(day_area, sub_type)
            
            # フォルダが存在しない場合は作成
            os.makedirs(folder_path, exist_ok=True)
            
            # ファイル名を生成
            filename = f"{x}-{y}.png"
            file_path = os.path.join(folder_path, filename)
            
            # 画像をダウンロード
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # ファイルに保存
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ ダウンロード完了: {file_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ ダウンロードエラー ({day_area} {x}-{y}): {e}")
            return False
        except Exception as e:
            print(f"✗ 予期しないエラー ({day_area} {x}-{y}): {e}")
            return False
    
    def download_area_images_auto(self, day_area, sub_type="main", max_attempts=20):
        """
        指定されたエリアの画像を自動的にダウンロード（200番以外のエラーが出るまで）
        
        Args:
            day_area (str): 日とエリア（例: "Day1-e7"）
            sub_type (str): メインまたはサブ（"main" or "sub"）
            max_attempts (int): 最大試行回数（無限ループ防止）
        """
        print(f"=== {day_area} {sub_type} エリアの画像自動ダウンロード開始 ===")
        
        success_count = 0
        x = 0
        
        while x < max_attempts:
            y = 0
            row_has_success = False
            
            while y < max_attempts:
                try:
                    url = self.generate_image_url(day_area, x, y, sub_type)
                    response = requests.get(url, stream=True)
                    
                    if response.status_code == 200:
                        # 成功した場合のみファイルを保存
                        folder_path = self.get_folder_path(day_area, sub_type)
                        os.makedirs(folder_path, exist_ok=True)
                        
                        filename = f"{x}-{y}.png"
                        file_path = os.path.join(folder_path, filename)
                        
                        with open(file_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        print(f"✓ ダウンロード完了: {file_path}")
                        success_count += 1
                        row_has_success = True
                        y += 1
                    else:
                        # 200以外のステータスコードの場合、この行は終了
                        print(f"✗ HTTP {response.status_code}: {day_area} {x}-{y} (行終了)")
                        break
                        
                except requests.exceptions.RequestException as e:
                    print(f"✗ ダウンロードエラー ({day_area} {x}-{y}): {e} (行終了)")
                    break
                except Exception as e:
                    print(f"✗ 予期しないエラー ({day_area} {x}-{y}): {e} (行終了)")
                    break
            
            # この行で一つも成功しなかった場合、ダウンロード終了
            if not row_has_success:
                print(f"✗ 行 {x} で画像が見つからないため終了")
                break
                
            x += 1
        
        print(f"=== ダウンロード完了: {success_count}枚 ===\n")
        return success_count
    
    def download_all_areas(self):
        """
        settings.jsonの設定に基づいて全エリア・全日の画像をダウンロード
        """
        blocks = self.config.get("block", {})
        dates = self.config.get("date", {})
        
        print("=== 全エリア・全日の画像ダウンロード開始 ===")
        print(f"対象ブロック: {list(blocks.values())}")
        print(f"対象日程: {list(dates.values())}")
        print()
        
        total_downloaded = 0
        
        for date_key, date_name in dates.items():
            for block_key, block_name in blocks.items():
                day_area = f"Day{date_key}-{block_name}"
                
                print(f"--- {date_name}曜日 {block_name}エリア ---")
                
                # mainとsubの両方をダウンロード
                for sub_type in ["main", "sub"]:
                    count = self.download_area_images_auto(day_area, sub_type)
                    total_downloaded += count
        
        print(f"=== 全体ダウンロード完了: 総計{total_downloaded}枚 ===")
        return total_downloaded



    