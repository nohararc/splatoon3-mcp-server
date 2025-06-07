# Splatoon3 MCP Server

Splatoon3のスケジュール情報を取得するMCP (Model Context Protocol) サーバーです。
[spla3.yuu26.com](https://spla3.yuu26.com/) APIを使用してバトルやサーモンランの情報を提供します。

## 機能

- 現在のバトル情報取得（レギュラー、バンカラオープン/チャレンジ、Xマッチ）
- 次回のバトル情報取得
- サーモンランスケジュール取得（現在と次回のシフト）

## 必要環境

- Python 3.10以上
- uv（推奨）またはpip

## インストール

1. リポジトリをクローンまたはダウンロード
```bash
git clone <repository-url>
cd splatoon3-mcp-server
```

2. 仮想環境の作成と有効化（uvを使用）
```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# または .venv\Scripts\activate  # Windows
```

3. 依存関係をインストール
```bash
uv pip install -r requirements.txt
```

## Claude Codeでの設定

### 方法1: claude mcp add-jsonコマンド（推奨）

```bash
claude mcp add-json splatoon3 '{
  "command": "/path/to/splatoon3-mcp-server/.venv/bin/python",
  "args": ["/path/to/splatoon3-mcp-server/run.py"],
  "env": {
    "PYTHONPATH": "/path/to/splatoon3-mcp-server/src"
  }
}'
```

**注意**: パスは実際のプロジェクトの場所に置き換えてください。

### 方法2: CLAUDE.mdファイル

プロジェクトルートの`CLAUDE.md`ファイルに以下の設定を記載：

```json
{
  "splatoon3": {
    "command": "/path/to/splatoon3-mcp-server/.venv/bin/python",
    "args": ["/path/to/splatoon3-mcp-server/run.py"],
    "env": {
      "PYTHONPATH": "/path/to/splatoon3-mcp-server/src"
    }
  }
}
```

## 使用例

Claude Codeで以下のように使用できます：

- 「現在のレギュラーマッチの情報を教えて」
- 「バンカラマッチ（チャレンジ）の次のスケジュールは？」
- 「サーモンランの今のシフトと次のシフトを見せて」
- 「現在のXマッチのステージとルールは？」

## 利用可能なツール

### get_current_battles_tool
現在開催中のバトル情報を取得します。
- **パラメータ**: `mode` (string)
  - `"regular"`: レギュラーマッチのみ
  - `"bankara-open"`: バンカラマッチ（オープン）のみ
  - `"bankara-challenge"`: バンカラマッチ（チャレンジ）のみ
  - `"x"`: Xマッチのみ
  - `"all"`: 全てのバトルタイプ（デフォルト）

### get_next_battles_tool
次回のバトル情報を取得します。
- **パラメータ**: `mode` (string) - 上記と同様

### get_salmon_run_tool
サーモンランのスケジュール情報を取得します。
- **パラメータ**: なし
- **取得情報**: 現在のシフトと次回のシフト

## 動作確認

サーバーが正常に動作するかテストできます：

```bash
# 仮想環境を有効化
source .venv/bin/activate

# サーバー起動テスト（数秒で停止）
timeout 3 python run.py

# APIテスト
python -c "
import asyncio
import sys
sys.path.insert(0, 'src')
from tools import get_current_battles
print(asyncio.run(get_current_battles('regular')))
"
```

## トラブルシューティング

### MCPサーバーが認識されない場合
1. パスが正しいか確認
2. 仮想環境のPythonパスが正しいか確認
3. `claude mcp list`でサーバー登録を確認

### API接続エラーの場合
1. インターネット接続を確認
2. spla3.yuu26.com が利用可能か確認

## 開発

### コードフォーマット
```bash
source .venv/bin/activate
black src/ run.py
ruff check src/ run.py --fix
```

### テスト実行
```bash
source .venv/bin/activate
python -c "
import asyncio
import sys
sys.path.insert(0, 'src')
from tools import get_current_battles, get_next_battles, get_salmon_run

async def test_all():
    print('現在のバトル:', await get_current_battles('all'))
    print('次のバトル:', await get_next_battles('regular'))
    print('サーモンラン:', await get_salmon_run())

asyncio.run(test_all())
"
```

## ライセンス

MIT License

## 謝辞

- [spla3.yuu26.com](https://spla3.yuu26.com/) - Splatoon3 API提供
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP仕様