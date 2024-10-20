# 博麗神社Bot

## 概要
東方Project同好会サークルのディスコード鯖でおみくじを引くためのBot。

## 実行方法
1. python環境構築を行う。
2. discordパッケージをインストール。
3. pipの場合
```bash
pip install discord
```
anacondaの場合
```bash
conda install discord
```
3. このリポジトリをクローンする。
4. HakureiShrineBotディレクトリに移動。
```bash
cd HakureiShrineBot/
```
5. .envファイルを作成し、tokenを入力(以下、.envファイル内の例)
```
TOKEN="abcdefghij"
```
6. pythonコマンドを実行
```bash
python3 src/main.py
```

## 免責
深夜テンションのノリで10分程度で書いたコードですので、バグが発生する場合がございます。もしバグがありましたらissueへお願いします。
