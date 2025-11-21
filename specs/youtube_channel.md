# 项目说明：youtube-api - 频道功能

## 目标
- 提供轻量的 YouTube Data API v3 客户端：支持键轮换、重试/退避，方便获取频道信息。
- 提供命令行工具 `yt-channel`，便捷输出和格式化查看频道信息。

## 底层技术栈
- 官方 API：YouTube Data API v3（REST HTTP）。
- HTTP 客户端：`requests` 直接请求官方 REST 端点，不依赖 Google 官方 Python SDK。
- 配置与认证：`python-dotenv` 加载 `.env`，API Key 通过环境变量传入（不写入代码）。

## 依赖与环境
- Python >= 3.9
- 运行时：`requests`, `python-dotenv`
- 开发/测试：`pytest`, `pytest-cov`（示例使用 `uv` 运行）
- API Key：环境变量 `YOUTUBE_API_KEYS`（逗号分隔）或 `YOUTUBE_API_KEY`。项目根目录 `.env` 与 `youtube_api/.env` 会自动加载。

## 核心功能（`youtube_api.client.YouTubeClient` - 频道相关）

### 基础请求方法
- `request(url, params, max_retries=5)`: GET 请求，默认 20s 超时；指数退避；遇 403 配额/429/限流时尝试轮换 Key；重试耗尽抛 `RuntimeError`，网络异常同样包装后抛。
- Key 轮换：多 Key 时按顺序切换；`key` 属性暴露当前 Key。
- `_to_int`: 字符串数字转 int，不可转时返回 None。

### 频道解析方法
- `resolve_channel_id(input_str)`: 支持 Channel ID、频道 URL、handle（含 @ 或 URL），找不到抛错。

### 频道信息方法
- `get_channel_profile(channel_input, include_recent_videos=False, max_videos=5)`: 返回频道元数据、缩略图、统计（int）、关键词/横幅/话题/隐私，可选最近视频。
- `_get_recent_videos(channel_id, max_videos=5)`: 搜索 + videos 取最新视频及基础统计。

## CLI 规范 - yt-channel（频道）

### 入口
- 入口（pyproject 脚本）：`yt-channel` → `youtube_api.cli_channel:main`
- Key 加载优先级：命令行 `--keys` > `.env`（自动加载） > 环境变量。

### 命令行参数
- 输入：`--id`|`--handle`|`--url`（必选其一）。
- 选项：`--include-videos`（带最近视频）、`--max-videos`(默认5)、`--keys`。
- 输出：`--format`=`json`|`human`（默认 json），`--pretty` 仅作用于 json。
- 行为：解析频道，取档案，可选最近视频；按格式输出；出错非零退出。

## 格式化（`youtube_api.formatter` - 频道相关）
- 人类可读输出，处理缺失值（N/A）、文本截断、日期格式化。
- 支持频道信息和最近视频的格式化展示。

## 错误与限额
- 网络/非 200 响应：重试后抛 `RuntimeError`。
- 配额/限流：多 Key 时轮换，否则继续退避重试直至耗尽。
- 频道缺失：抛 `RuntimeError`，带描述信息。

## 测试
- 单元：`tests/test_client.py`，Mock requests/time，覆盖重试/轮换及频道相关方法。
- 集成（真实 API，缺 Key 自动跳过）：`tests/integration/test_integration_client.py`。
- 端到端 E2E（真实 API，缺 Key 自动跳过）：`tests/e2e/test_cli_e2e.py` 覆盖 CLI 路径（频道 JSON+最近视频）。
- 常用命令：
  - 仅单元+覆盖率：`uv run -m pytest -m "not integration and not e2e" --cov=youtube_api --cov-report=term-missing`
  - 全量（含真实 API，注意配额）：`uv run -m pytest --cov=youtube_api --cov-report=term-missing --cov-report=html`
