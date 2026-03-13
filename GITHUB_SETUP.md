# GitHub 仓库设置指南

## 快速创建和发布

### 方法1: 使用GitHub CLI (推荐)

```bash
# 安装GitHub CLI (如果尚未安装)
# macOS: brew install gh
# Ubuntu: sudo apt install gh

# 登录GitHub
gh auth login

# 创建新仓库
cd /Users/a1111/user/skill/auto-summary-system
gh repo create auto-summary-system --public --source=. --remote=origin --push

# 创建发布标签
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions会自动触发并创建发布
```

### 方法2: 手动创建

#### 步骤1: 在GitHub上创建仓库

1. 访问 https://github.com/new
2. 输入仓库名称: `auto-summary-system`
3. 选择 "Public" (开源)
4. 勾选 "Add a README file" (可选)
5. 点击 "Create repository"

#### 步骤2: 推送本地代码

```bash
cd /Users/a1111/user/skill/auto-summary-system

# 初始化Git仓库（如果尚未初始化）
git init

# 添加远程仓库
# 将 YOUR_USERNAME 替换为你的GitHub用户名
git remote add origin https://github.com/YOUR_USERNAME/auto-summary-system.git

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial release: Automated summary system with multi-skill architecture"

# 推送到GitHub
git push -u origin main
```

#### 步骤3: 创建发布

```bash
# 创建标签
git tag v1.0.0

# 推送标签到GitHub
git push origin v1.0.0
```

GitHub Actions会自动检测到标签并创建发布。

### 方法3: 使用GitHub网页界面

1. 推送代码到GitHub后，访问仓库页面
2. 点击 "Releases" -> "Create a new release"
3. 输入版本号: `v1.0.0`
4. 填写发布说明（可以参考下面的模板）
5. 上传 `auto-summary-system.zip` 文件
6. 点击 "Publish release"

## 发布说明模板

```markdown
## 自动化汇总系统 v1.0.0

### 🎉 新功能

- **多Skill协同架构**: 采用模块化设计，各Skill职责清晰
- **日常记录管理**: 记录用户每天的工作内容和数据
- **日报自动生成**: 按设定时间自动汇总当天内容生成表格
- **周报自动生成**: 按设定时间（周几）自动汇总本周内容生成报告
- **自动推送**: 自动将汇总结果推送给客户
- **定时任务调度**: 支持灵活配置触发时间

### 📦 安装方式

**通过OpenClaw安装（推荐）:**
```bash
openclaw install auto-summary-system
```

**手动安装:**
```bash
git clone https://github.com/YOUR_USERNAME/auto-summary-system.git
cd auto-summary-system
pip install -r requirements.txt
python3 main.py init
```

### 🚀 快速开始

1. **编辑配置文件:**
   ```bash
   cp config.yaml config.yaml.bak
   nano config.yaml
   # 配置客户邮箱、SMTP等信息
   ```

2. **添加工作记录:**
   ```bash
   openclaw run auto-summary-system add "今日完成项目A的需求分析"
   ```

3. **生成日报并发送:**
   ```bash
   openclaw run auto-summary-system report daily --notify
   ```

4. **启动定时调度器:**
   ```bash
   openclaw run auto-summary-system scheduler start
   ```

### 📖 文档

- [详细使用文档](./USAGE_EXAMPLES.md)
- [配置说明](./README.md)

### 🛠️ 技术栈

- Python 3.8+
- pandas - 数据处理
- openpyxl - Excel表格生成
- schedule - 定时任务调度
- PyYAML - 配置文件解析

### 🤝 贡献

欢迎提交Issue和Pull Request！

### 📄 许可证

MIT License
```

## 配置GitHub Secrets (可选)

如果你需要自动发布到PyPI或其他平台，可以配置Secrets：

1. 进入仓库 Settings -> Secrets and variables -> Actions
2. 点击 "New repository secret"
3. 添加以下Secrets（根据需要）：
   - `PYPI_API_TOKEN`: PyPI发布令牌
   - `DOCKER_USERNAME`: Docker Hub用户名
   - `DOCKER_PASSWORD`: Docker Hub密码

## 启用GitHub Pages (可选)

如果你想为项目创建文档网站：

1. 进入仓库 Settings -> Pages
2. Source选择 "Deploy from a branch"
3. Branch选择 "main" 和 "/docs" 或 "/ (root)"
4. 点击 "Save"

## 项目徽章

在README.md中添加徽章：

```markdown
[![Release](https://img.shields.io/github/v/release/YOUR_USERNAME/auto-summary-system)](https://github.com/YOUR_USERNAME/auto-summary-system/releases)
[![License](https://img.shields.io/github/license/YOUR_USERNAME/auto-summary-system)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-brightgreen)](https://openclaw.org/)
```

## 推广你的项目

1. **在OpenClaw社区分享**
   - 在OpenClaw论坛发布介绍帖子
   - 分享到OpenClaw的社交媒体

2. **添加标签**
   - automation
   - reporting
   - productivity
   - openclaw-skill
   - python

3. **创建演示视频**
   - 录制使用演示
   - 上传到YouTube或B站
   - 在README中添加链接

## 版本管理

### 版本号规范

采用语义化版本控制：
- `v1.0.0` - 初始发布
- `v1.0.1` - Bug修复
- `v1.1.0` - 新功能
- `v2.0.0` - 不兼容的更改

### 发布流程

```bash
# 开发新功能
git checkout -b feature/new-feature
# ... 开发 ...
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# 创建Pull Request并合并到main

# 准备发布
git checkout main
git pull origin main

# 更新版本号
# 编辑 skill.yaml, skill.json, 和其他相关文件

# 创建标签
git tag v1.1.0
git push origin v1.1.0

# GitHub Actions会自动创建发布
```

## 社区参与

- 关注用户反馈
- 及时响应Issue
- 定期更新文档
- 维护更新日志
- 考虑添加贡献指南 (CONTRIBUTING.md)

## 联系方式

- GitHub Issues: 报告Bug和提出功能建议
- Discussions: 讨论使用问题和最佳实践
- Email: 你的邮箱@example.com (可选)

---

**祝你的项目取得成功！ 🎉**