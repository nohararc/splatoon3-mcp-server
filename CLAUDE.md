# Splatoon3 MCP Server

このプロジェクトはSplatoon3のバトル情報とサーモンラン情報を取得するMCPサーバーです。

## MCP Server Configuration

```json
{
  "splatoon3": {
    "command": "/home/fukafuka/src/splatoon3-mcp-server/.venv/bin/python",
    "args": ["/home/fukafuka/src/splatoon3-mcp-server/run.py"],
    "env": {
      "PYTHONPATH": "/home/fukafuka/src/splatoon3-mcp-server/src"
    }
  }
}
```

## 利用可能なツール

1. **get_current_battles_tool** - 現在のバトル情報を取得
   - パラメータ: mode ("regular", "bankara-open", "bankara-challenge", "x", "all")

2. **get_next_battles_tool** - 次のバトル情報を取得  
   - パラメータ: mode ("regular", "bankara-open", "bankara-challenge", "x", "all")

3. **get_salmon_run_tool** - サーモンラン情報を取得（現在と次回のシフト）
   - パラメータ: なし

## 使用例

- 「現在のバンカラマッチ（オープン）の情報を教えて」
- 「次のXマッチのステージとルールは？」
- 「今のサーモンランの武器とステージを確認して」