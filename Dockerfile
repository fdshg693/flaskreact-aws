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


# Expose the port App Runner expects (8080)
EXPOSE 8080

# Healthcheck should target the runtime PORT if provided, otherwise default to 8080
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fsS http://127.0.0.1:${PORT:-8080}/healthz || exit 1

USER appuser

# Flask(Gunicorn)起動
# ${PORT} が与えられればそれを使い、なければ 8501 にフォールバック
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:${PORT:-8080} --workers=2 --threads=4 --timeout=60"
CMD sh -c 'exec gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --workers ${WEB_CONCURRENCY:-2} --threads ${WEB_THREADS:-4} --timeout ${WEB_TIMEOUT:-60}'
