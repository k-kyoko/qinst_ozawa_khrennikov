# qinst-ozawa

Python 3.12、JupyterLab、Docker Composeを使用する開発環境です。

## JupyterLab

イメージをビルドしてJupyterLabを起動します。

```bash
docker compose up --build
```

起動ログに表示される `http://127.0.0.1:8888/lab?token=...` をブラウザで開いてください。
ホスト側のディレクトリ全体がコンテナ内の `/work` にマウントされます。

停止する場合は `Ctrl-C` を押した後、次を実行します。

```bash
docker compose down
```

## 環境の確認

```bash
make smoke
```

このコマンドは、コンテナ内のカレントディレクトリ、Pythonパッケージのimport、
JupyterLabのバージョンを確認します。

## テストと静的チェック

```bash
docker compose run --rm jupyter pytest
docker compose run --rm jupyter ruff check .
```

または次のコマンドを使用できます。

```bash
make test
make lint
```

## 依存関係

依存関係は `pyproject.toml` で管理します。変更した場合はイメージを再ビルドします。

```bash
docker compose build
```

`src/` 以下はeditable installされるため、Pythonコードだけの変更では再ビルドは不要です。

## Git

初回だけ、このディレクトリで次を実行します。

```bash
git init -b main
git status
```
