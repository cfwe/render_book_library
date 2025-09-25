# ベースイメージとして公式のPythonイメージを使用
FROM python:3.11-slim

# 作業ディレクトリを/appに設定
WORKDIR /app

# 依存関係をインストールするために requirements.txt をコピー
COPY ./requirements.txt /app/requirements.txt

# pipで依存関係をインストール
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# プロジェクト全体をコンテナにコピー
COPY . /app/