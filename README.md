# 蔵書管理アプリ

個人が所有する蔵書を効率的にデジタル化し、一元管理することを目的としたWebアプリケーションです。

## ✨ 主な機能

-   **蔵書管理**: 書籍の登録、一覧表示、変更、削除 (CRUD)
-   **ISBN自動入力**: ISBNコードを入力するだけで、書籍名、著者、出版社などの情報を自動で取得します。
-   **価格自動取得**: Book-Off Onlineから中古価格と定価を自動で取得し、資産価値の参考にできます。
-   **絞り込み・検索**: キーワードや出版社名で蔵書を簡単に検索できます。

## 🛠️ 使用技術

-   **バックエンド**: FastAPI, Python 3.11
-   **データベース**: PostgreSQL
-   **フロントエンド**: HTML, CSS, Vanilla JavaScript
-   **コンテナ技術**: Docker, Docker Compose
-   **データベースマイグレーション**: Alembic
-   **テスト**: Pytest

## 🚀 実行方法

### 1. 前提条件

- Docker
- Docker Compose
- (Windowsの場合) WSL2

### 2. セットアップ

1.  **リポジトリをクローンします。**
    ```bash
    git clone <repository_url>
    cd library-manager
    ```

2.  **環境変数ファイルを作成します。**
    `.env.example` をコピーして `.env` ファイルを作成します。楽天APIは現在使用していませんが、設定項目は残っています。
    ```bash
    cp .env.example .env
    ```

3.  **Dockerコンテナをビルドして起動します。**
    ```bash
    docker compose up --build -d
    ```
![実行画面](./image/docker-compose-up.png)

4.  **データベースのマイグレーションを実行します。**
    初回起動時、またはデータベースのテーブル構造に変更があった場合に実行してください。
    ```bash
    docker compose run --rm backend alembic upgrade head
    ```

5.  **アプリケーションにアクセスします。**
    ブラウザで `http://localhost:8000` を開きます。


## 📝 使い方

-   **書籍の登録**:
    -   トップページの「ISBNコードで登録」欄にISBNコードを入力し、「書籍情報を取得して登録」ボタンを押すか、Enterキーを押します。
    -   書籍情報が見つからない場合は、手動登録用のモーダルが開きます。
-   **価格の更新**:
    -   各書籍の「価格を更新」ボタンを押すと、最新の中古価格と定価がBook-Off Onlineから取得されます。
-   **書籍情報の変更・削除**:
    -   各書籍の「変更」「削除」ボタンで操作します。

## 📚 APIエンドポイント

主要なAPIエンドポイントは以下の通りです。詳細は `http://localhost:8000/docs` で確認できます。

-   `GET /`: 蔵書一覧のHTMLページを返します。
-   `GET /api/books/`: 登録されている蔵書の一覧をJSONで返します。
-   `POST /api/books/`: 新しい書籍を登録します。
-   `GET /api/lookup_book/{isbn}`: ISBNコードを元に外部サービスから書籍情報を検索します。
-   `GET /api/prices/{isbn}`: ISBNコードを元にBook-Off Onlineから価格情報を取得します。
-   `GET /api/books/{isbn}/update_prices`: 登録済みの書籍の価格情報を更新します。
-   `PUT /api/books/{book_id}`: 登録済みの書籍情報を更新します。
-   `DELETE /api/books/{book_id}`: 登録済みの書籍を削除します。

## テストの実行方法

以下のコマンドで、バックエンドのテストを実行できます。

```bash
docker compose run --rm test
```

## ライセンス (Licenses) 
 
このプロジェクトは、下記のオープンソースソフトウェアを利用しています。各ソフトウェアのライセンス条項に従ってください。

| 技術 | ライセンス |
| :------------- | :--------------------------------------- |
| Python | Python Software Foundation License |
| FastAPI | MIT License |
| SQLAlchemy | MIT License |
| Alembic | MIT License |
| Pydantic | MIT License |
| Jinja2 | BSD-3-Clause License |
| Uvicorn | BSD-3-Clause License |
| PostgreSQL | PostgreSQL Licence |
| Docker | Apache License 2.0 |

※ 上記は主要なライブラリです。依存関係にある他のライブラリについては、それぞれのライセンスをご確認ください。

