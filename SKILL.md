---
name: auto-summary-system
description: "自动化汇总系统 - 支持日报、周报自动生成与推送"
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "python": ">=3.8", "bins": [], "pip": ["pandas", "openpyxl", "schedule", "PyYAML", "requests", "python-dateutil"] },
        "install": ["pip install -r requirements.txt"],
      },
  }
---

# 自动化汇总系统

基于OpenClaw的自动化汇总系统，支持日报、周报自动生成与推送。

## Commands

```bash
# 添加工作记录
auto-summary-system add '工作内容'

# 查看工作记录
auto-summary-system list --today

# 生成日报
auto-summary-system report daily

# 生成周报
auto-summary-system report weekly

# 启动定时调度器
auto-summary-system scheduler start
```

## 安装

```bash
pip install -r requirements.txt
python3 main.py init
```

## 配置

编辑 `config.yaml` 配置邮箱、SMTP 等信息。
