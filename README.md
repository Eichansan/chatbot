# テスト

## 事前準備
以下のコマンドをインストールしてください。(必要なコマンドがあればリンクを追記してください)
- [Taskfile](https://taskfile.dev/ja-JP/installation/)

## インストール

```bash
task install
```

## 起動

```bash
task up
```

## 実行

- wiki下にexample.txtを配置

- ベクトルDB（Qdrant）に保存（仮）

```bash
python app/vector_store.py
```

- 実行（仮）

```bash
python app/main.py
```

## 停止
```bash
task stop
```

## 削除
```bash
task down
```
