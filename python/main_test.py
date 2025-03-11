from fastapi.testclient import TestClient
from main import app, get_db
import pytest
import sqlite3
import os
import pathlib

# STEP 6-4: uncomment this test setup
test_db = pathlib.Path(__file__).parent.resolve() / "db" / "test_mercari.sqlite3"

def override_get_db():
    conn = sqlite3.connect(test_db)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture(autouse=True)
def db_connection():
    # テスト用のDB接続を作成
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    # categories テーブルの作成
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )"""
    )
    # items テーブルの作成（本番のスキーマに合わせる場合）
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category_id INTEGER,
            image_name TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )"""
    )
    conn.commit()
    conn.row_factory = sqlite3.Row  # 辞書型の結果を返す
    yield conn
    conn.close()
    # テスト終了後、テスト用DBファイルを削除
    if test_db.exists():
        test_db.unlink()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.mark.parametrize(
    "want_status_code, want_body",
    [
        (200, {"message": "Hello, world!"}),
    ],
)
def test_hello(want_status_code, want_body):
    response = client.get("/")
    # STEP 6-2: confirm the status code
    assert response.status_code == want_status_code,  f"unexpected result of status_code: want={want_status_code}, got={response.status_code}"
 
    # STEP 6-2: confirm response body
    response_body = response.json()   
    assert response_body == want_body, f"unexpected result of hello: want={want_body}, got={response_body}"



# STEP 6-4: uncomment this test
@pytest.mark.parametrize(
    "args, want_status_code",
    [
        # 2パターンのテストケース[入力, 期待する出力]を用意
        ({"name":"used iPhone 16e", "category":"phone"}, 200),
        ({"name":"", "category":"phone"}, 400),
    ],
)
def test_add_item_e2e(args,want_status_code,db_connection):
    response = client.post("/items/", data=args)
    assert response.status_code == want_status_code
    
    if want_status_code >= 400:
        return
    
    
    # Check if the response body is correct
    response_data = response.json()
    assert "message" in response_data

    # Check if the data was saved to the database correctly
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM items WHERE name = ?", (args["name"],))
    db_item = cursor.fetchone()
    assert db_item is not None
    assert dict(db_item)["name"] == args["name"]
