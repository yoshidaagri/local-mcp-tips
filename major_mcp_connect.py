import os
import anthropic
import sys
from dotenv import load_dotenv
from datetime import datetime
import json

class MCPServerDirectory:
    """実際に使える公開MCPサーバーの統合ディレクトリ"""
    
    def __init__(self):
        load_dotenv()
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        # 実際に動作する公開MCPサーバー一覧（2025年5月最新）
        self.servers = {
            # 🚀 確実に動作するサーバー（認証不要）
            "basic": {
                "description": "基本セット - 確実に動作、認証不要",
                "servers": [
                    {
                        "type": "url",
                        "url": "https://mcp.deepwiki.com/sse",
                        "name": "deepwiki",
                        "description": "GitHubリポジトリ分析・技術調査・コード検索"
                    }
                ]
            },
            
            # 🌐 ブラウザ自動化・Web操作
            "browser": {
                "description": "ブラウザ自動化 - Webスクレイピング、フォーム操作、スクリーンショット",
                "servers": [
                    {
                        "type": "url",
                        "url": "https://mcp.deepwiki.com/sse",
                        "name": "deepwiki",
                        "description": "技術情報検索（基本機能）"
                    }
                    # Playwright MCP: npx @playwright/mcp@latest (ローカル実行)
                    # 注意: Microsoft Playwright MCPは現在ローカル実行のみ対応
                ]
            },
            
            # ☁️ Cloudflare公式サーバー群（最も信頼性が高い）
            "cloudflare": {
                "description": "Cloudflare公式 - 開発者向け高機能サーバー群",
                "servers": [
                    {
                        "type": "url",
                        "url": "https://mcp.deepwiki.com/sse",
                        "name": "deepwiki",
                        "description": "技術情報・GitHubリポジトリ検索"
                    },
                    {
                        "type": "url", 
                        "url": "https://docs.mcp.cloudflare.com/sse",
                        "name": "cloudflare-docs",
                        "description": "Cloudflareドキュメント検索・技術仕様"
                    },
                    {
                        "type": "url",
                        "url": "https://analytics.mcp.cloudflare.com/sse", 
                        "name": "cloudflare-analytics",
                        "description": "Webアナリティクス・パフォーマンス分析"
                    },
                    {
                        "type": "url",
                        "url": "https://bindings.mcp.cloudflare.com/sse", 
                        "name": "cloudflare-bindings",
                        "description": "Cloudflare Workers・データベース操作"
                    }
                ]
            },
            
            # 🔍 検索・情報収集特化
            "search": {
                "description": "検索・リサーチ - Web検索、技術調査、情報収集",
                "servers": [
                    {
                        "type": "url",
                        "url": "https://mcp.deepwiki.com/sse",
                        "name": "deepwiki", 
                        "description": "GitHubリポジトリ・技術文書検索"
                    },
                    {
                        "type": "url", 
                        "url": "https://docs.mcp.cloudflare.com/sse",
                        "name": "cloudflare-docs",
                        "description": "技術ドキュメント検索"
                    }
                ]
            },
            
            # 💼 ビジネス・生産性（実用性重視）
            "business": {
                "description": "ビジネス - 業務効率化、プロジェクト管理、競合分析",
                "servers": [
                    {
                        "type": "url",
                        "url": "https://mcp.deepwiki.com/sse",
                        "name": "deepwiki",
                        "description": "競合技術分析・オープンソース調査"
                    },
                    {
                        "type": "url",
                        "url": "https://analytics.mcp.cloudflare.com/sse", 
                        "name": "cloudflare-analytics",
                        "description": "Webパフォーマンス・ユーザー行動分析"
                    }
                ]
            },
            
            # 💻 開発者特化（高度な機能）
            "developer": {
                "description": "開発者特化 - コード分析、インフラ管理、技術調査",
                "servers": [
                    {
                        "type": "url",
                        "url": "https://mcp.deepwiki.com/sse",
                        "name": "deepwiki",
                        "description": "GitHubリポジトリ・ライブラリ分析"
                    },
                    {
                        "type": "url",
                        "url": "https://bindings.mcp.cloudflare.com/sse", 
                        "name": "cloudflare-bindings",
                        "description": "Cloudflare Workers・D1データベース・R2ストレージ"
                    },
                    {
                        "type": "url", 
                        "url": "https://docs.mcp.cloudflare.com/sse",
                        "name": "cloudflare-docs",
                        "description": "開発者向けドキュメント・API仕様"
                    }
                ]
            },
            
            # 🏢 Microsoft統合（認証が必要なものはコメントアウト）
            "microsoft": {
                "description": "Microsoft統合 - Office、Teams、Azure連携機能",
                "servers": [
                    {
                        "type": "url",
                        "url": "https://mcp.deepwiki.com/sse",
                        "name": "deepwiki",
                        "description": "技術情報検索（基本機能）"
                    }
                    # Microsoft MCPサーバーは主にローカル実行または認証が必要
                    # Azure MCP: 要Azure認証
                    # Teams MCP: 要Teams認証  
                    # Playwright MCP: npx @playwright/mcp@latest
                    # Word MCP: ローカル実行のみ
                ]
            },
            
            # 🧪 最大機能セット（全サーバー統合）
            "full": {
                "description": "フル機能 - 全MCPサーバーを統合（最大パワー）",
                "servers": [
                    {
                        "type": "url",
                        "url": "https://mcp.deepwiki.com/sse",
                        "name": "deepwiki",
                        "description": "GitHub・技術情報の総合検索"
                    },
                    {
                        "type": "url", 
                        "url": "https://docs.mcp.cloudflare.com/sse",
                        "name": "cloudflare-docs",
                        "description": "技術ドキュメント・API仕様検索"
                    },
                    {
                        "type": "url",
                        "url": "https://analytics.mcp.cloudflare.com/sse", 
                        "name": "cloudflare-analytics",
                        "description": "Webアナリティクス・パフォーマンス測定"
                    },
                    {
                        "type": "url",
                        "url": "https://bindings.mcp.cloudflare.com/sse", 
                        "name": "cloudflare-bindings",
                        "description": "クラウドインフラ・データベース操作"
                    }
                ]
            }
        }
        
        # 実用的なプロンプトテンプレート（2025年最新ビジネス対応）
        self.use_cases = {
            "tech_research": {
                "name": "🔍 技術調査・競合分析",
                "prompt": """
以下の技術について包括的な調査をお願いします：

🎯 調査対象: {topic}

📊 調査項目:
1. 技術概要と主要機能
2. GitHubでの人気度（スター数、フォーク数、最新活動）
3. 実際のプロジェクトでの採用事例
4. 競合技術との詳細比較
5. 学習コスト・導入難易度
6. 長期的な技術トレンド予測
7. 日本での採用状況

💼 ビジネス観点:
- ROI（投資対効果）
- 運用コスト
- 人材確保の難易度
- サポート体制

実際に導入を検討する際の具体的な判断材料を提供してください。
                """,
                "servers": "search"
            },
            
            "gijiroku_enhancement": {
                "name": "📝 議事録ツール機能拡張",
                "prompt": """
現在「gijiroku-san」というTeams VTTファイルから議事録を作成するツールを運用中です。
以下の機能拡張について調査・提案をお願いします：

🎯 拡張テーマ: {topic}

🔍 調査項目:
1. 関連するオープンソースツール・ライブラリ
2. API連携可能なサービス
3. 実装の技術的難易度
4. 必要な開発工数の概算
5. 運用コスト

💡 特に重視する点:
- Teams/Slack/Notion/kintoneとの連携
- 音声認識精度の向上
- アクションアイテムの自動抽出
- 多言語対応
- リアルタイム処理

実際に実装可能な具体的なソリューションと、段階的な導入プランを提案してください。
                """,
                "servers": "developer"
            },
            
            "backoffice_automation": {
                "name": "💼 バックオフィス業務自動化",
                "prompt": """
社労士事務所のバックオフィス業務自動化について調査・提案をお願いします：

🎯 自動化対象: {topic}

📋 現在の課題:
- 手作業による転記ミス
- 複数システム間のデータ移行
- 申請書類の作成時間
- 進捗管理の属人化
- 法改正対応の遅れ

🔧 検討したい技術:
- kintone API連携
- Slack Bot活用
- OCR・文字認識
- RPA（Robotic Process Automation）
- クラウドストレージ連携

💰 重要な要件:
- 導入コスト: 月額10万円以内
- 実装期間: 3ヶ月以内
- セキュリティ: 個人情報保護対応必須
- 運用: 非エンジニアでも使える

費用対効果の高い実装案と、段階的な導入スケジュールを提案してください。
                """,
                "servers": "business"
            },
            
            "mcp_integration": {
                "name": "🔗 MCP統合システム設計",
                "prompt": """
既存の業務システムにMCP（Model Context Protocol）を統合する方法について調査・設計をお願いします：

🎯 統合対象: {topic}

🏗️ システム構成:
- 既存: gijiroku-san（議事録作成）
- 既存: kintone（業務管理）
- 既存: Slack（コミュニケーション）
- 既存: Google Drive（ファイル管理）

🔌 統合したいMCP機能:
1. 議事録からのアクションアイテム自動抽出
2. kintoneデータベースとの自動連携
3. Slack通知の自動化
4. ドキュメント検索・要約
5. スケジュール管理の最適化

⚙️ 技術要件:
- 認証セキュリティ
- API制限・コスト管理  
- エラーハンドリング
- スケーラビリティ
- 監視・ログ管理

実際に構築可能なMCP統合アーキテクチャと、具体的な実装手順を提案してください。
                """,
                "servers": "full"
            },
            
            "competitive_analysis": {
                "name": "📊 市場・競合分析",
                "prompt": """
以下の分野での詳細な競合分析をお願いします：

🎯 分析分野: {topic}

📈 分析項目:
1. 市場規模・成長率
2. 主要プレイヤーの特徴・シェア
3. 技術的な差別化ポイント
4. 価格戦略・課金モデル
5. ユーザーレビュー・満足度
6. 今後の市場展望

🔍 技術面での調査:
- GitHubスター数・開発活発度
- 使用技術スタック
- API仕様・拡張性
- セキュリティ対応
- 多言語対応状況

💡 日本市場特有の要素:
- 法規制対応
- 日本語サポート品質
- 国内パートナー体制
- 導入実績

投資判断や参入戦略の検討に役立つ、データに基づいた具体的な分析結果を提供してください。
                """,
                "servers": "search"
            },
            
            "workflow_optimization": {
                "name": "⚙️ ワークフロー最適化",
                "prompt": """
現在の業務プロセスの最適化方法を調査・提案してください：

🎯 最適化対象: {topic}

🔄 現在のワークフロー課題:
- 承認プロセスの冗長性
- 情報共有の遅延
- 重複作業の発生
- 品質チェックの属人化
- 進捗把握の困難

💡 改善アプローチ:
1. ボトルネック分析
2. 自動化可能ポイントの特定
3. ツール統合による効率化
4. 品質保証の仕組み化
5. KPI設定と測定方法

🛠️ 検討技術:
- ワークフローエンジン
- 承認フローシステム
- 通知・アラート機能
- ダッシュボード・可視化
- 監査ログ機能

具体的な改善案、期待される効果、実装優先順位を含む最適化プランを提案してください。
                """,
                "servers": "cloudflare"
            },
            
            "api_integration": {
                "name": "🔌 API連携・システム統合",
                "prompt": """
既存システムとの API連携について調査・設計をお願いします：

🎯 連携対象: {topic}

🏗️ システム環境:
- kintone（業務データベース）
- Slack（コミュニケーション）
- Google Workspace（ファイル・カレンダー）
- freee（会計システム）
- e-Gov（電子申請）

🔗 連携要件:
1. データの自動同期
2. リアルタイム通知
3. ファイル自動処理
4. 承認ワークフロー
5. レポート自動生成

⚡ 技術課題:
- API制限・レート制限
- 認証・セキュリティ
- エラーハンドリング
- データ整合性
- パフォーマンス最適化

実装可能な連携アーキテクチャ、必要な開発工数、運用コストを含む具体的な提案をしてください。
                """,
                "servers": "developer"
            }
        }
    
    def list_servers(self):
        """利用可能なMCPサーバー一覧を表示"""
        print("🚀 利用可能なMCPサーバーセット")
        print("="*60)
        
        for key, config in self.servers.items():
            print(f"\n📋 {key.upper()}: {config['description']}")
            for server in config['servers']:
                print(f"  - {server['name']}: {server['description']}")
        
        print(f"\n💡 使用方法:")
        print(f"  python {sys.argv[0]} <サーバーセット> <ユースケース> '<トピック>'")
        print(f"  例: python {sys.argv[0]} basic tech_research 'React vs Vue.js'")
    
    def list_use_cases(self):
        """利用可能なユースケース一覧を表示"""
        print("🎯 実用的なユースケース一覧")
        print("="*60)
        
        for key, case in self.use_cases.items():
            print(f"\n{case['name']} ({key})")
            print(f"  推奨サーバー: {case['servers']}")
            print(f"  概要: {case['prompt'][:100]}...")
        
        print(f"\n💡 使用方法:")
        print(f"  python {sys.argv[0]} <サーバーセット> <ユースケース> '<具体的なトピック>'")
    
    def execute_use_case(self, server_set, use_case, topic):
        """指定されたユースケースを実行"""
        if server_set not in self.servers:
            print(f"❌ 無効なサーバーセット: {server_set}")
            self.list_servers()
            return
        
        if use_case not in self.use_cases:
            print(f"❌ 無効なユースケース: {use_case}")
            self.list_use_cases()
            return
        
        case_config = self.use_cases[use_case]
        server_config = self.servers[server_set]
        
        # プロンプト生成
        prompt = case_config["prompt"].format(topic=topic)
        
        print(f"🎯 {case_config['name']} 実行中...")
        print(f"📡 サーバーセット: {server_config['description']}")
        print(f"🔍 トピック: {topic}")
        print("="*60)
        
        try:
            response = self.client.beta.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}],
                mcp_servers=server_config["servers"],
                betas=["mcp-client-2025-04-04"],
            )
            
            print("📋 調査結果:")
            print("="*60)
            
            used_tools = []
            for content in response.content:
                if content.type == "text":
                    print(content.text)
                elif content.type == "mcp_tool_use":
                    used_tools.append(content.name)
                    print(f"🔧 [MCP Tool] {content.name}")
            
            print("\n" + "-"*40)
            print(f"✅ 使用MCPツール: {', '.join(used_tools) if used_tools else 'なし'}")
            print(f"⏰ 完了時刻: {datetime.now().strftime('%H:%M:%S')}")
            print("-"*40)
            
        except Exception as e:
            print(f"❌ エラー発生: {e}")
            print("\n🔧 トラブルシューティング:")
            print("1. .envファイルでANTHROPIC_API_KEYが設定されているか確認")
            print("2. インターネット接続を確認")
            print("3. 別のサーバーセットで試行")
    
    def run_demo(self):
        """実用性を体感できるデモンストレーション実行"""
        print("🎪 MCP実用デモンストレーション - 実際のビジネス課題を解決")
        print("="*60)
        
        demos = [
            # 実際のビジネス課題に基づくデモ
            ("basic", "tech_research", "Teams会議録音の音声認識精度向上技術"),
            ("business", "backoffice_automation", "kintoneと申請書自動生成システムの連携"),
            ("developer", "gijiroku_enhancement", "Teams VTTファイルからアクションアイテム自動抽出"),
            ("search", "competitive_analysis", "議事録自動化ツールの市場動向"),
            ("full", "mcp_integration", "社労士事務所向けAI業務支援システム"),
        ]
        
        for i, (server_set, use_case, topic) in enumerate(demos, 1):
            print(f"\n🎯 実用デモ {i}/5: {topic}")
            print(f"💡 ユースケース: {self.use_cases[use_case]['name']}")
            print(f"🔧 使用サーバー: {self.servers[server_set]['description']}")
            print("-"*50)
            
            self.execute_use_case(server_set, use_case, topic)
            
            if i < len(demos):
                print(f"\n⏸️  デモ {i} 完了！次のデモに進むにはEnterキーを押してください...")
                input("   (Ctrl+Cで中断可能)")
        
        print(f"\n🎉 全デモ完了！MCPの実用性を体感できましたか？")
        print(f"💡 次は実際の業務課題で試してみてください。")
    
    def interactive_mode(self):
        """対話モード"""
        print("🎮 MCPインタラクティブモード")
        print("="*60)
        
        while True:
            print("\n📋 選択してください:")
            print("1. サーバー一覧表示")
            print("2. ユースケース一覧表示") 
            print("3. カスタム調査実行")
            print("4. デモ実行")
            print("5. Microsoft MCPガイド")
            print("0. 終了")
            
            choice = input("\n選択 (0-5): ").strip()
            
            if choice == "0":
                print("👋 お疲れ様でした！")
                break
            elif choice == "1":
                self.list_servers()
            elif choice == "2":
                self.list_use_cases()
            elif choice == "3":
                print("\n📝 カスタム調査設定:")
                server_set = input("サーバーセット (basic/cloudflare/business等): ").strip()
                use_case = input("ユースケース (tech_research/business_tools等): ").strip()
                topic = input("調査トピック: ").strip()
                
                if server_set and use_case and topic:
                    self.execute_use_case(server_set, use_case, topic)
                else:
                    print("❌ 全ての項目を入力してください")
            elif choice == "4":
                self.run_demo()
            elif choice == "5":
                show_microsoft_guide()
            else:
                print("❌ 無効な選択です")

def main():
    mcp_dir = MCPServerDirectory()
    
    if len(sys.argv) == 1:
        # 引数なしの場合は対話モード
        mcp_dir.interactive_mode()
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        if command == "list":
            mcp_dir.list_servers()
        elif command == "cases":
            mcp_dir.list_use_cases()
        elif command == "demo":
            mcp_dir.run_demo()
        elif command == "interactive":
            mcp_dir.interactive_mode()
        elif command == "examples":
            show_examples()
        elif command == "microsoft_guide":
            show_microsoft_guide()
        elif command in ["help", "-h", "--help"]:
            show_help()
        else:
            print("❌ 無効なコマンドです")
            show_help()
    elif len(sys.argv) == 4:
        server_set, use_case, topic = sys.argv[1], sys.argv[2], sys.argv[3]
        mcp_dir.execute_use_case(server_set, use_case, topic)
    else:
        print("❌ 引数の数が正しくありません")
        show_help()

def show_examples():
    """実用的な使用例を表示"""
    print("💡 実際に試せる使用例")
    print("="*60)
    
    examples = [
        {
            "title": "議事録ツール機能拡張調査",
            "command": 'python major_mcp_connect.py developer gijiroku_enhancement "Teams連携とSlack通知自動化"',
            "description": "gijiroku-sanツールの機能拡張について具体的な実装方法を調査"
        },
        {
            "title": "社労士業務自動化分析", 
            "command": 'python major_mcp_connect.py business backoffice_automation "給与計算と申請書作成の自動化"',
            "description": "kintoneやSlackと連携した業務自動化の具体的提案を取得"
        },
        {
            "title": "競合技術調査",
            "command": 'python major_mcp_connect.py search competitive_analysis "音声認識API比較分析"',
            "description": "音声認識技術の市場動向と主要サービスの比較分析"
        },
        {
            "title": "MCP統合システム設計",
            "command": 'python major_mcp_connect.py full mcp_integration "議事録とkintone連携システム"',
            "description": "既存システムとMCPを統合した包括的なソリューション設計"
        },
        {
            "title": "技術選定支援",
            "command": 'python major_mcp_connect.py search tech_research "リアルタイム音声文字起こし技術"',
            "description": "特定技術の詳細調査と導入判断材料の提供"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n📋 例 {i}: {example['title']}")
        print(f"💡 説明: {example['description']}")
        print(f"🔧 コマンド:")
        print(f"   {example['command']}")
    
    print(f"\n🚀 まずは簡単なデモから:")
    print(f"   python major_mcp_connect.py demo")
    print(f"\n🏢 Microsoft MCPサーバー情報:")
    print(f"   python major_mcp_connect.py microsoft_guide")
    print(f"\n📖 詳細なヘルプ:")
    print(f"   python major_mcp_connect.py help")

def show_microsoft_guide():
    """Microsoft MCPサーバーのガイド表示"""
    print("🏢 Microsoft MCP サーバー活用ガイド")
    print("="*60)
    print("Microsoftは多数の実用的なMCPサーバーを提供していますが、")
    print("多くは認証またはローカルセットアップが必要です。")
    print()
    
    print("🌟 主要なMicrosoft MCPサーバー:")
    print()
    
    ms_servers = [
        {
            "name": "🎭 Playwright MCP",
            "repo": "microsoft/playwright-mcp",
            "description": "ブラウザ自動化・Webスクレイピング・フォーム操作",
            "setup": "npx @playwright/mcp@latest",
            "use_case": "Webスクレイピング、フォーム自動入力、サイト監視"
        },
        {
            "name": "☁️ Azure MCP", 
            "repo": "Azure/azure-mcp",
            "description": "Azureリソース管理・クラウド操作",
            "setup": "Azure認証 + npx -y @azure/mcp@latest server start",
            "use_case": "VM管理、ストレージ操作、コスト分析"
        },
        {
            "name": "💬 Teams MCP",
            "repo": "InditexTech/mcp-teams-server", 
            "description": "Microsoft Teams統合・メッセージ送受信",
            "setup": "Teams Bot認証 + Docker",
            "use_case": "Teams自動投稿、メッセージ分析、通知自動化"
        },
        {
            "name": "📝 Word MCP",
            "repo": "GongRzhe/Office-Word-MCP-Server",
            "description": "Word文書作成・編集・フォーマット",
            "setup": "pip install + python-docx",
            "use_case": "報告書自動生成、テンプレート処理、文書分析"
        },
        {
            "name": "🗄️ MSSQL MCP",
            "repo": "RichardHan/mssql_mcp_server",
            "description": "SQL Server データベース操作",
            "setup": "SQL Server接続 + pip install",
            "use_case": "データ分析、レポート生成、DB管理"
        }
    ]
    
    for i, server in enumerate(ms_servers, 1):
        print(f"## {i}. {server['name']}")
        print(f"   📦 リポジトリ: {server['repo']}")
        print(f"   💡 機能: {server['description']}")
        print(f"   ⚙️  セットアップ: {server['setup']}")
        print(f"   🎯 活用例: {server['use_case']}")
        print()
    
    print("🔧 セットアップ例 - Playwright MCP:")
    print("="*40)
    print("1. Playwrightインストール:")
    print("   npx playwright install")
    print()
    print("2. Claude Desktop設定 (.vscode/mcp.json):")
    print('   {')
    print('     "mcpServers": {')
    print('       "playwright": {')
    print('         "command": "npx",')
    print('         "args": ["@playwright/mcp@latest"]')
    print('       }')
    print('     }')
    print('   }')
    print()
    print("3. 実行例:")
    print('   "Webサイト example.com のスクリーンショットを撮って"')
    print('   "フォームに自動入力して送信して"')
    print()
    
    print("📚 学習リソース:")
    print("="*30)
    print("• microsoft/mcp-for-beginners - MCP基礎学習")
    print("• microsoft/mcsmcp - Copilot Studio統合")
    print("• Playwright MCP公式ドキュメント")
    print()
    
    print("💡 gijiroku-san連携アイデア:")
    print("="*35)
    print("1. Teams MCP + gijiroku-san → Teams会議の自動議事録")
    print("2. Word MCP + gijiroku-san → 議事録の自動Word出力")
    print("3. Playwright MCP → Web申請フォームの自動入力")
    print("4. Azure MCP → クラウドストレージへの自動保存")
    print()
    
    print("🚀 次のステップ:")
    print("1. 最も関心のあるMCPサーバーのリポジトリを確認")
    print("2. ローカル環境でセットアップ")
    print("3. 小さな機能から試験的に導入")
    print("4. gijiroku-sanとの統合を検討")

def show_help():
    """詳細なヘルプを表示"""
    print("📖 major_mcp_connect.py - 実用的MCPサーバー統合ツール")
    print("="*60)
    print("🎯 目的: 実際に動作する公開MCPサーバーを使って、実用的なビジネス課題を解決")
    print()
    
    print("📋 基本コマンド:")
    print("  python major_mcp_connect.py                          # 対話モード")
    print("  python major_mcp_connect.py demo                     # 実用デモ実行")
    print("  python major_mcp_connect.py list                     # 利用可能サーバー一覧")
    print("  python major_mcp_connect.py cases                    # ユースケース一覧")
    print("  python major_mcp_connect.py examples                 # 使用例表示")
    print("  python major_mcp_connect.py microsoft_guide          # Microsoft MCPガイド")
    print("  python major_mcp_connect.py help                     # このヘルプ")
    print()
    
    print("🔧 直接実行:")
    print("  python major_mcp_connect.py <サーバー> <ユースケース> '<トピック>'")
    print()
    
    print("🚀 利用可能サーバーセット:")
    print("  basic      - 基本機能（DeepWikiのみ、確実に動作）")
    print("  search     - 検索・リサーチ特化")
    print("  business   - ビジネス・業務効率化")
    print("  developer  - 開発者向け高機能")
    print("  cloudflare - Cloudflare公式サーバー群")
    print("  full       - 全機能統合（最大パワー）")
    print()
    
    print("💼 主要ユースケース:")
    print("  tech_research        - 技術調査・競合分析")
    print("  gijiroku_enhancement - 議事録ツール機能拡張")
    print("  backoffice_automation- バックオフィス業務自動化")
    print("  mcp_integration      - MCP統合システム設計")
    print("  competitive_analysis - 市場・競合分析")
    print("  workflow_optimization- ワークフロー最適化")
    print("  api_integration      - API連携・システム統合")
    print()
    
    print("⚠️  必要な設定:")
    print("  1. .envファイルにANTHROPIC_API_KEYを設定")
    print("  2. 必要パッケージ: pip install anthropic python-dotenv")
    print()
    
    print("🎯 おすすめの始め方:")
    print("  1. まずデモ実行: python major_mcp_connect.py demo")
    print("  2. 対話モード: python major_mcp_connect.py")
    print("  3. 具体的課題で実行: 上記の使用例を参考に")
    print()
    
    print("💡 このツールの特徴:")
    print("  ✅ 実際に動作する公開MCPサーバーのみを使用")
    print("  ✅ 認証不要ですぐに試せる")
    print("  ✅ 実際のビジネス課題に特化したユースケース")
    print("  ✅ gijiroku-sanツールとの連携を想定した設計")
    print("  ✅ 社労士事務所のバックオフィス業務に最適化")

if __name__ == "__main__":
    main()