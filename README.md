# Smart Home
スイッチボットを使用してスマートホーム化を目指す

## 環境構築
1. dockerコンテナ立ち上げ
`docker compose up -d`

## 設定ファイル
スイッチボットアプリからトークン、シークレットを取得する。取得方法は以下参照。  
[スイッチボットGitHub](https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file)  
取得した値を`src/config/config.json`に入れる。  
config.jsonの構造はsample.jsonを参照。  
