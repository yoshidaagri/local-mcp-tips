import os
import anthropic
import sys
from dotenv import load_dotenv

def main():
    # .envファイルから環境変数を読み込み
    load_dotenv()
    
    # 環境変数からAPIキーを取得
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY環境変数を設定してください。")
    
    # Client を初期化
    client = anthropic.Anthropic(
        api_key=api_key,
    )
    
    # コマンドライン引数から content を取得
    if len(sys.argv) < 2:
        print("使用方法: python main.py 'ユーザメッセージ'")
        sys.exit(1)
    
    user_content = sys.argv[1]
    
    # 環境変数からMCPサーバーURLを取得（デフォルト値も設定）
    deepwiki_url = os.getenv("DEEPWIKI_API_URL", "https://mcp.deepwiki.com/sse")
    custom_mcp_url = os.getenv("CUSTOM_MCP_URL", "https://your-custom-mcp.workers.dev/mcp")
    
    # デバッグ情報表示
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    if debug_mode:
        print(f"DeepWiki URL: {deepwiki_url}")
        print(f"Custom MCP URL: {custom_mcp_url}")
        print(f"User message: {user_content}")
    
    try:
        response = client.beta.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": user_content,
                }
            ],
            mcp_servers=[
                {
                    "type": "url",
                    "url": deepwiki_url,
                    "name": "deepwiki",
                },
                # カスタムMCPは一旦コメントアウト（実際のURLが必要）
                # {
                #     "type": "url", 
                #     "url": custom_mcp_url,
                #     "name": "my-mcp-worker",
                # },
            ],
            betas=["mcp-client-2025-04-04"],
        )
        
        # レスポンス表示
        print("=== Claude の応答 ===")
        for content in response.content:
            if content.type == "text":
                print(content.text)
            elif content.type == "mcp_tool_use":
                print(f"tool use: {content.name}")
                
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()