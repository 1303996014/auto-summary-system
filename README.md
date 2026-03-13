# 🚀 自动化汇总系统

<div align="center">

[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-brightgreen)](https://openclaw.org/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)]()

**基于OpenClaw的自动化汇总系统 - 支持日报、周报自动生成与推送**

</div>

---

## 📖 简介

自动化汇总系统是一个基于OpenClaw平台的多Skill协同系统，帮助用户自动记录日常工作、生成专业报表并定时推送给客户。采用模块化架构，功能强大且易于扩展。

## ✨ 核心特性

### 🎯 智能记录管理
- ✅ 一键记录工作内容，支持分类标签
- ✅ 自动时间戳，精确到秒
- ✅ 按日期自动归档，便于查询

### 📊 自动报表生成
- ✅ **日报**: 每天自动生成Excel报表
- ✅ **周报**: 每周自动生成汇总报告
- ✅ **多维度统计**: 类别分布、趋势分析
- ✅ **专业格式**: 多Sheet Excel，支持图表

### ⏰ 定时任务调度
- ✅ 灵活的触发时间配置
- ✅ 支持Cron表达式
- ✅ 自动邮件推送
- ✅ Webhook通知支持

### 🔧 多Skill协同架构
- **存储管理**: 数据持久化和查询
- **日报汇总**: 每日数据分析
- **周报汇总**: 每周综合分析
- **定时调度**: 任务自动化触发
- **报表生成**: 专业Excel生成
- **客户推送**: 多渠道通知

## 🚀 快速安装

### 方式1: OpenClaw一键安装（推荐）

```bash
# 一键安装（自动处理所有依赖和配置）
openclaw install auto-summary-system

# 进入项目目录
cd auto-summary-system

# 编辑配置文件（关键步骤）
nano config.yaml
```

### 方式2: GitHub源码安装

```bash
# 克隆仓库
git clone https://github.com/1303996014/auto-summary-system.git
cd auto-summary-system

# 安装依赖
pip install -r requirements.txt

# 初始化系统
python3 main.py init

# 编辑配置
nano config.yaml
```

### 方式3: 手动下载安装

```bash
# 下载最新发布版本
wget https://github.com/1303996014/auto-summary-system/releases/latest/download/auto-summary-system.zip

# 解压
unzip auto-summary-system.zip
cd auto-summary-system

# 安装和初始化
pip install -r requirements.txt
python3 main.py init
```

## ⚙️ 配置说明

### 关键配置（必须修改）

编辑 `config.yaml` 文件：

```yaml
# 客户邮箱（必须）
client:
  email: "your-client@example.com"  # ← 改为客户的邮箱地址

# SMTP配置（必须）- 用于发送邮件
notification:
  email:
    smtp_server: "smtp.gmail.com"     # 根据你的邮箱服务商修改
    smtp_port: 587
    username: "your-email@gmail.com"  # ← 你的邮箱地址
    password: "your-app-password"     # ← 应用专用密码（不是普通密码）
    use_tls: true
```

**获取应用专用密码：**
- **Gmail**: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- **QQ邮箱**: 设置 → 账户 → 开启SMTP服务
- **Outlook**: [https://account.microsoft.com/security](https://account.microsoft.com/security)

### 可选配置

```yaml
# 定时任务（可选）
schedule:
  daily:
    enabled: true
    time: "18:00"   # 日报生成时间（24小时制）
  weekly:
    enabled: true
    day: "friday"   # 周报星期几（monday-sunday）
    time: "17:00"   # 周报生成时间

# 报表配置（可选）
report:
  output_path: ./reports
  format: excel
  include_charts: true

# 存储配置（可选）
storage:
  path: ./data
```

## 🎮 使用指南

### 基础命令（5个核心命令）

#### 1. 添加工作记录
```bash
openclaw run auto-summary-system add "完成用户登录模块的开发"

# 添加带分类的记录
openclaw run auto-summary-system add "修复支付功能的bug" --category "Bug修复"
```

#### 2. 查看记录
```bash
# 查看今日记录
openclaw run auto-summary-system list --today

# 查看最近20条记录
openclaw run auto-summary-system list --limit 20
```

#### 3. 生成日报并发送
```bash
# 生成昨天的日报并发送给客户
openclaw run auto-summary-system report daily --notify

# 生成指定日期的日报
openclaw run auto-summary-system report daily --date 2026-03-13
```

#### 4. 生成周报并发送
```bash
# 生成本周周报并发送
openclaw run auto-summary-system report weekly --notify

# 生成指定日期所在周的周报
openclaw run auto-summary-system report weekly --date 2026-03-13
```

#### 5. 启动自动调度
```bash
# 启动定时任务（只需运行一次，保持运行即可）
openclaw run auto-summary-system scheduler start

# 查看调度器状态
openclaw run auto-summary-system scheduler info
```

### 完整工作流程示例

```bash
# 步骤1: 初始化系统
openclaw run auto-summary-system init

# 步骤2: 配置客户邮箱和SMTP（编辑config.yaml）
nano config.yaml

# 步骤3: 测试邮件发送
python3 skills/client_notifier.py test

# 步骤4: 白天记录工作（随时添加）
openclaw run auto-summary-system add "完成项目A的需求分析"
openclaw run auto-summary-system add "编写用户登录API" --category "开发"

# 步骤5: 查看今日记录
openclaw run auto-summary-system list --today

# 步骤6: 启动自动调度（让系统自动处理报表）
openclaw run auto-summary-system scheduler start

# 系统现在会自动：
# - 每天18:00生成昨天的日报并发送
# - 每周五17:00生成本周的周报并发送
```

## 📊 报表示例

### 日报内容
- **记录详情**: 时间、类别、工作内容
- **统计摘要**: 总记录数、类别数量、平均数
- **类别分布**: 各类别占比分析

### 周报内容
- **周报摘要**: 本周天数、总记录数、平均每天记录
- **每日统计**: 每天的记录数量
- **类别统计**: 各类别的记录数和百分比
- **详细记录**: 本周所有工作记录
- **空白记录**: 无记录的工作日提醒

## 🔧 高级功能

### 测试邮件配置
```bash
# 测试邮件是否能正常发送
python3 skills/client_notifier.py test --email your-test@example.com
```

### 手动触发任务
```bash
# 手动触发日报任务（测试用）
openclaw run auto-summary-system scheduler run daily

# 手动触发周报任务（测试用）
openclaw run auto-summary-system scheduler run weekly
```

### 查看系统状态
```bash
openclaw run auto-summary-system status
```

### 导出数据
```bash
# 导出所有数据到JSON文件
python3 skills/storage_manager.py export backup_$(date +%Y%m%d).json
```

## 🧪 测试系统

运行系统测试验证安装是否正确：

```bash
python3 test_system.py
```

如果所有测试通过，说明系统配置正确，可以正常使用。

## 📚 文档

- **[快速上手指南](QUICKSTART.md)** - 5分钟快速入门
- **[详细使用示例](USAGE_EXAMPLES.md)** - 完整的使用教程和最佳实践
- **[项目总结](PROJECT_SUMMARY.md)** - 架构设计和开发文档
- **[GitHub发布指南](GITHUB_SETUP.md)** - 如何发布到GitHub

## 🤝 贡献

欢迎贡献代码、提出建议或报告问题！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (2026-03-13)
- ✅ 初始版本发布
- ✅ 多Skill协同架构
- ✅ 日报、周报自动生成
- ✅ 定时任务调度
- ✅ 邮件自动推送
- ✅ OpenClaw一键安装支持

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⭐ 支持项目

如果这个项目对你有帮助，请给颗星星 ⭐️

## 📧 联系方式

- 项目地址: [https://github.com/1303996014/auto-summary-system](https://github.com/1303996014/auto-summary-system)
- 问题反馈: [GitHub Issues](https://github.com/1303996014/auto-summary-system/issues)
- OpenClaw社区: [https://openclaw.org/community](https://openclaw.org/community)

---

<div align="center">

**Made with ❤️ by OpenClaw Community**

[🏠 首页](https://github.com/1303996014/auto-summary-system) • 
[📖 文档](https://github.com/1303996014/auto-summary-system/blob/main/USAGE_EXAMPLES.md) • 
[🚀 快速开始](https://github.com/1303996014/auto-summary-system/blob/main/QUICKSTART.md) • 
[🤝 贡献](https://github.com/1303996014/auto-summary-system/blob/main/README.md#贡献)

</div>