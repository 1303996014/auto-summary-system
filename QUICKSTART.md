# 自动化汇总系统 - 5分钟快速上手指南

## 安装启动

### 方式1: OpenClaw安装（推荐）

```bash
# 安装Skill
openclaw install auto-summary-system

# 进入项目目录
cd /Users/a1111/user/skill/auto-summary-system

# 编辑配置（填写客户邮箱和SMTP信息）
nano config.yaml

# 测试系统
python3 test_system.py
```

### 方式2: 手动安装

```bash
# 进入项目目录
cd /Users/a1111/user/skill/auto-summary-system

# 安装依赖
pip install -r requirements.txt

# 初始化系统
python3 main.py init

# 编辑配置
nano config.yaml

# 测试系统
python3 test_system.py
```

## 基础使用（5个核心命令）

### 1. 添加工作记录
```bash
openclaw run auto-summary-system add "今日完成项目A的需求分析"
```

### 2. 查看今日记录
```bash
openclaw run auto-summary-system list --today
```

### 3. 生成日报并发送
```bash
openclaw run auto-summary-system report daily --notify
```

### 4. 生成周报
```bash
openclaw run auto-summary-system report weekly --notify
```

### 5. 启动自动调度
```bash
openclaw run auto-summary-system scheduler start
```

## 配置要点

编辑 `config.yaml`，配置以下关键项：

```yaml
# 客户邮箱（必须）
client:
  email: "your-client@example.com"

# SMTP配置（必须）
notification:
  email:
    smtp_server: "smtp.gmail.com"    # 根据你的邮箱修改
    smtp_port: 587
    username: "your-email@gmail.com"  # 你的邮箱
    password: "your-app-password"     # 应用专用密码

# 定时任务（可选）
schedule:
  daily:
    time: "18:00"   # 日报时间
  weekly:
    day: "friday"   # 周报星期几
    time: "17:00"   # 周报时间
```

**获取应用专用密码：**
- Gmail: https://myaccount.google.com/apppasswords
- QQ邮箱: 设置 → 账户 → 开启SMTP服务

## 常见场景

### 场景1: 日常记录 + 自动日报
```bash
# 1. 白天随时记录
openclaw run auto-summary-system add "完成登录功能开发"
openclaw run auto-summary-system add "修复支付bug" --category "Bug修复"

# 2. 启动自动调度（只需一次）
openclaw run auto-summary-system scheduler start

# 系统每天18:00自动生成昨天的日报并发送
```

### 场景2: 手动生成周报
```bash
# 1. 确认本周记录
openclaw run auto-summary-system list --limit 50

# 2. 生成并发送周报
openclaw run auto-summary-system report weekly --notify
```

### 场景3: 查看系统状态
```bash
openclaw run auto-summary-system status
```

## 故障排查

### 问题1: 邮件发送失败
```bash
# 测试邮件配置
python3 skills/client_notifier.py test

# 检查配置文件
nano config.yaml
```

### 问题2: 调度器未运行
```bash
# 查看调度器信息
openclaw run auto-summary-system scheduler info

# 重新启动调度器
openclaw run auto-summary-system scheduler start
```

### 问题3: 报表生成失败
```bash
# 测试报表生成
python3 test_system.py

# 检查数据文件
ls -la data/
```

## 快速测试

运行完整测试：
```bash
python3 test_system.py
```

如果所有测试通过，说明系统配置正确。

## 获取更多帮助

- **详细文档**: `USAGE_EXAMPLES.md`
- **项目总结**: `PROJECT_SUMMARY.md`
- **GitHub发布**: `GITHUB_SETUP.md`
- **配置文件**: `config.yaml`

## 核心文件说明

```
main.py              # 主程序入口
config.yaml          # 配置文件（必须修改）
skills/              # Skill模块目录
  ├── storage_manager.py    # 数据存储
  ├── daily_summary.py      # 日报生成
  ├── weekly_summary.py     # 周报生成
  └── client_notifier.py    # 邮件推送
```

---

**现在就开始使用吧！ 🚀**

1. 配置邮箱 → 2. 添加记录 → 3. 生成报表 → 4. 启动自动调度