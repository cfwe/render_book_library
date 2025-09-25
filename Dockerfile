# ベースイメージとして公式のPythonイメージを使用
FROM python:3.11-slim

# 環境変数: Pythonが.pycファイルを生成しないようにし、バッファリングを無効化
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを/appに設定
WORKDIR /app

# non-rootユーザーを作成
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# 依存関係をインストールするために requirements.txt をコピー
COPY ./requirements.txt /app/requirements.txt

# pipで依存関係をインストール
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# プロジェクト全体をコンテナにコピーし、所有者を変更
COPY . /app/
RUN chown -R appuser:appgroup /app

# non-rootユーザーに切り替え
USER appuser