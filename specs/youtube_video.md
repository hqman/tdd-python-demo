# 项目说明：youtube-api - 视频功能

## 目标
- 提供轻量的 YouTube Data API v3 客户端：支持键轮换、重试/退避，方便获取视频信息及评论。
- 提供命令行工具 `yt-fetch`，便捷输出和格式化查看视频信息。

## 底层技术栈
- 官方 API：YouTube Data API v3（REST HTTP）。
- HTTP 客户端：`requests` 直接请求官方 REST 端点，不依赖 Google 官方 Python SDK。
- 配置与认证：`python-dotenv` 加载 `.env`，API Key 通过环境变量传入（不写入代码）。

## 依赖与环境
- Python >= 3.9
- 运行时：`requests`, `python-dotenv`
- 开发/测试：`pytest`, `pytest-cov`（示例使用 `uv` 运行）
- API Key：环境变量 `YOUTUBE_API_KEYS`（逗号分隔）或 `YOUTUBE_API_KEY`。项目根目录 `.env` 与 `youtube_api/.env` 会自动加载。

## 核心功能（`youtube_api.client.YouTubeClient` - 视频相关）

### 基础请求方法
- `request(url, params, max_retries=5)`: GET 请求，默认 20s 超时；指数退避；遇 403 配额/429/限流时尝试轮换 Key；重试耗尽抛 `RuntimeError`，网络异常同样包装后抛。
- Key 轮换：多 Key 时按顺序切换；`key` 属性暴露当前 Key。
- `_to_int`: 字符串数字转 int，不可转时返回 None。

### 视频信息方法
- `get_video_statistics(video_id)`: 返回 view/like/comment 计数（int 或 None），视频缺失抛错。
- `get_video_details(video_id)`: 返回包含 snippet/contentDetails/status/topicDetails/statistics 的完整字典，数字转 int。

### 评论方法
- `list_comments(video_id, page_size=100, max_comments=200, page_token=None)`: 分页取顶层评论，返回 (comments, next_page_token)，达到 `max_comments` 即停。
- `get_all_comments(video_id, page_size=100)`: 拉取全部评论。

## CLI 规范 - yt-fetch（视频）

### 入口
- 入口（pyproject 脚本）：`yt-fetch` → `youtube_api.cli:main`
- Key 加载优先级：命令行 `--keys` > `.env`（自动加载） > 环境变量。

### 命令行参数
- 输入：`--url` 或 `--id`（必选其一）。
- 评论：`--max-comments`(默认200)、`--page-size`(默认100)、`--all-comments`(全量)、`--stats-only`(仅统计)。
- 输出：`--format`=`json`|`human`|`table`|`summary`（默认 json）；`--pretty` 美化 JSON。
- 行为：解析视频 ID，取完整详情；根据选项取评论；按格式输出；出错非零退出。

## 格式化（`youtube_api.formatter` - 视频相关）
- 人类可读/表格/摘要输出，简单 ASCII 表格；处理缺失值（N/A）、文本截断、日期格式化。
- 支持视频信息和评论的格式化展示。

## 错误与限额
- 网络/非 200 响应：重试后抛 `RuntimeError`。
- 配额/限流：多 Key 时轮换，否则继续退避重试直至耗尽。
- 视频缺失：抛 `RuntimeError`，带描述信息。

## 测试
- 单元：`tests/test_client.py`，Mock requests/time，覆盖重试/轮换及视频相关方法。
- 集成（真实 API，缺 Key 自动跳过）：`tests/integration/test_integration_client.py`。
- 端到端 E2E（真实 API，缺 Key 自动跳过）：`tests/e2e/test_cli_e2e.py` 覆盖 CLI 路径（stats-only JSON、表格+评论）。
- 常用命令：
  - 仅单元+覆盖率：`uv run -m pytest -m "not integration and not e2e" --cov=youtube_api --cov-report=term-missing`
  - 全量（含真实 API，注意配额）：`uv run -m pytest --cov=youtube_api --cov-report=term-missing --cov-report=html`
