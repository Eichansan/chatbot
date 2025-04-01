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

- app/wiki下にexample.txtを配置

- 実行（仮）

```bash
curl -X POST "http://localhost:8000/chat"     -H "Content-Type: application/json"     -d '{"question": "VPN接続の方法は？"}'
```

## 停止
```bash
task stop
```

## 削除
```bash
task down
```
