#!/usr/bin/env python3
import logging
from mcp.server.fastmcp import FastMCP

try:
    from .tools import get_current_battles, get_next_battles, get_salmon_run
except ImportError:
    from tools import get_current_battles, get_next_battles, get_salmon_run

# ロギング設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastMCPサーバーを作成
mcp = FastMCP("splatoon3-mcp-server")


@mcp.tool()
async def get_current_battles_tool(mode: str = "all") -> dict:
    """
    現在のバトル情報を取得します。

    Args:
        mode: 取得するモード ("regular", "bankara-open", "bankara-challenge", "x", "all")

    Returns:
        現在のバトル情報
    """
    return await get_current_battles(mode)


@mcp.tool()
async def get_next_battles_tool(mode: str = "all") -> dict:
    """
    次のバトル情報を取得します。

    Args:
        mode: 取得するモード ("regular", "bankara-open", "bankara-challenge", "x", "all")

    Returns:
        次のバトル情報
    """
    return await get_next_battles(mode)


@mcp.tool()
async def get_salmon_run_tool() -> dict:
    """
    サーモンラン情報を取得します（現在と次回のシフト）。

    Returns:
        現在と次回のサーモンラン情報
    """
    return await get_salmon_run()


def main():
    """メインエントリーポイント"""
    logger.info("Starting Splatoon3 MCP Server...")

    try:
        # FastMCPサーバーを実行
        mcp.run()
    except Exception as e:
        logger.error(f"Server error: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
