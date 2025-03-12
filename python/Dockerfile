FROM python:3.10-alpine

RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR /app

# requirements.txt をコピーして依存ライブラリをインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# python ディレクトリ内の全ファイル・フォルダを /app にコピー
COPY . /app

RUN addgroup -S mercari && adduser -S trainee -G mercari
RUN chown -R trainee:mercari /app

ENV PATH="/usr/local/bin:$PATH"

USER trainee

# アプリが使うポート番号を宣言
EXPOSE 9000

# コンテナ起動時に uvicorn で FastAPI アプリを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
