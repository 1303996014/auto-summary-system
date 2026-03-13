# 自动化汇总系统 - 使用示例

## 快速开始

### 1. 安装系统

```bash
# 方式1: GitHub克隆到 OpenClaw skills 目录（推荐）
git clone https://github.com/1303996014/auto-summary-system.git ~/.openclaw/skills/auto-summary-system
cd ~/.openclaw/skills/auto-summary-system

# 方式2: 本地目录安装
# 进入项目目录
cd auto-summary-system

# 安装依赖
pip install -r requirements.txt

# 初始化系统
python3 main.py init
```

### 2. 配置系统

编辑 `config.yaml` 文件：

```yaml
storage:
  path: ./data

report:
  output_path: ./reports

schedule:
  daily:
    enabled: true
    time: "18:00"  # 每天18:00生成日报
  weekly:
    enabled: true
    day: "friday"  # 每周五生成周报
    time: "17:00"

client:
  email: "client@example.com"  # 客户邮箱

notification:
  email:
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    username: "your-email@gmail.com"
    password: "your-app-password"  # 建议使用应用专用密码
```

### 3. 日常使用

#### 添加工作记录

```bash
# 添加一条工作记录
python3 main.py add "完成了用户登录模块的开发"

# 添加带类别的记录
python3 main.py add "修复了支付功能的bug" --category "Bug修复"

# 使用OpenClaw方式
openclaw run auto-summary-system add "完成了用户登录模块的开发"
```

#### 查看记录

```bash
# 查看今日记录
python3 main.py list --today

# 查看最近10条记录
python3 main.py list --limit 10

# 使用OpenClaw方式
openclaw run auto-summary-system list --today
```

输出示例：
```
📅 今日记录 (3 条):

1. [工作记录] 完成了用户登录模块的开发
2. [Bug修复] 修复了支付功能的bug
3. [工作记录] 编写了单元测试代码
```

#### 手动生成报表

**生成日报：**

```bash
# 生成昨天的日报
python3 main.py report daily

# 生成指定日期的日报
python3 main.py report daily --date 2026-03-13

# 生成日报并自动发送给客户
python3 main.py report daily --notify

# 使用OpenClaw方式
openclaw run auto-summary-system report daily --notify
```

日报包含以下内容：
- 记录详情（时间、类别、内容）
- 统计摘要（总记录数、类别数量）
- 类别分布统计

**生成周报：**

```bash
# 生成本周周报
python3 main.py report weekly

# 生成指定日期所在周的周报
python3 main.py report weekly --date 2026-03-13

# 生成周报并自动发送给客户
python3 main.py report weekly --notify

# 使用OpenClaw方式
openclaw run auto-summary-system report weekly --notify
```

周报包含以下内容：
- 周报摘要（本周天数、总记录数、平均记录数）
- 每日统计
- 类别统计（记录数和占比）
- 详细记录
- 空白记录日期

### 4. 自动调度

#### 启动定时调度器

```bash
# 启动调度器（前台运行）
python3 main.py scheduler start

# 使用OpenClaw方式
openclaw run auto-summary-system scheduler start
```

调度器启动后：
- 每天18:00自动生成昨天的日报并发送给客户
- 每周五17:00自动生成上周的周报并发送给客户
- 每30分钟打印一次心跳日志

#### 查看调度器信息

```bash
python3 main.py scheduler info
```

输出示例：
```
📅 定时任务信息:
日报任务:
  状态: 启用
  触发时间: 每天 18:00

周报任务:
  状态: 启用
  触发时间: 每周 friday 17:00

🕐 下次运行时间:
  日报: 2026-03-14 18:00:00
  周报: 2026-03-18 17:00:00
```

#### 手动触发任务

```bash
# 手动触发日报任务
python3 main.py scheduler run daily

# 手动触发周报任务
python3 main.py scheduler run weekly
```

### 5. 查看系统状态

```bash
python3 main.py status
```

输出示例：
```
============================================================
📊 自动化汇总系统状态
============================================================

📅 今日记录: 3 条
📈 本周记录: 15 条

⚙️  配置信息:
  数据存储路径: ./data
  报表输出路径: ./reports

📅 定时任务信息:
日报任务:
  状态: 启用
  触发时间: 每天 18:00

周报任务:
  状态: 启用
  触发时间: 每周 friday 17:00

🕐 下次运行时间:
  日报: 2026-03-14 18:00:00
  周报: 2026-03-18 17:00:00
============================================================
```

## 高级用法

### 1. 批量添加记录

```bash
# 创建一个记录文件 records.txt
cat > records.txt << EOF
完成了需求分析
设计了数据库结构
编写了API接口
修复了前端bug
编写了测试用例
EOF

# 批量导入
while IFS= read -r line; do
    python3 main.py add "$line"
done < records.txt
```

### 2. 数据导出

```bash
# 使用storage-manager导出所有数据
python3 skills/storage_manager.py export ./data/all_records.json
```

### 3. 测试邮件通知

```bash
# 测试邮件配置是否正确
python3 skills/client_notifier.py test
```

### 4. 自定义报表格式

可以修改 `skills/report_generator.py` 来自定义Excel报表的：
- 表格样式（字体、颜色、边框）
- 列宽和行高
- 添加公司Logo
- 添加图表（使用openpyxl的图表功能）

## 常见问题

### Q1: 邮件发送失败？

A: 检查以下几点：
1. SMTP服务器地址和端口是否正确
2. 邮箱账号和密码是否正确（建议使用应用专用密码）
3. 是否开启了SMTP服务
4. 网络连接是否正常

### Q2: 定时任务没有触发？

A: 检查以下几点：
1. 调度器是否正在运行
2. 系统时间是否正确
3. 配置文件中的时间设置是否正确
4. 查看日志文件了解详细错误信息

### Q3: 如何修改报表生成时间？

A: 编辑 `config.yaml` 文件：
```yaml
schedule:
  daily:
    time: "09:00"  # 改为早上9点
  weekly:
    day: "monday"  # 改为周一
    time: "09:00"
```

然后重启调度器。

### Q4: 如何备份数据？

A: 备份 `data` 目录下的所有文件即可：
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz data/
```

## 最佳实践

1. **每天定时记录**：养成每天记录工作的习惯，可以设置定时提醒
2. **使用类别标签**：合理使用类别（工作记录、Bug修复、会议、学习等）便于统计分析
3. **定期备份数据**：每周备份一次数据文件
4. **测试邮件配置**：首次使用前测试邮件发送功能
5. **监控调度器**：定期检查调度器运行状态和日志
6. **及时更新配置**：根据实际需求调整报表生成时间和频率

## 故障排查

### 查看日志

```bash
# 查看系统日志
tail -f logs/system.log
```

### 检查数据文件

```bash
# 查看数据文件内容
cat data/daily_records.json | python3 -m json.tool
```

### 测试各个模块

```bash
# 测试存储管理
python3 skills/storage_manager.py list --today

# 测试报表生成
python3 skills/report_generator.py

# 测试邮件通知
python3 skills/client_notifier.py test
```