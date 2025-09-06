FROM python:3.12-slim

# 依存に必要なツール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# 非rootユーザ
RUN useradd -m -u 10001 appuser
WORKDIR /home/appuser

# 依存を先に入れてビルドキャッシュを効かせる
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体
COPY . .

# 8501を外に出す
EXPOSE 8501

# ヘルスチェック（素朴にトップを叩く）
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fsS http://127.0.0.1:8501/ || exit 1

USER appuser

# Streamlit起動
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
