#!/bin/bash
# 自动化汇总系统 - GitHub仓库配置和提交脚本

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  自动化汇总系统 - GitHub提交工具${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# GitHub仓库地址
GITHUB_REPO="https://github.com/1303996014/auto-summary-system.git"

echo -e "${GREEN}📍 GitHub仓库地址:${NC}"
echo "   $GITHUB_REPO"
echo ""

# 步骤1: 检查Git是否已初始化
echo -e "${YELLOW}步骤 1: 检查Git仓库状态...${NC}"
if [ ! -d ".git" ]; then
    echo "   Git仓库未初始化，正在初始化..."
    git init
    echo -e "   ${GREEN}✅ Git初始化完成${NC}"
else
    echo -e "   ${GREEN}✅ Git仓库已存在${NC}"
fi
echo ""

# 步骤2: 配置远程仓库
echo -e "${YELLOW}步骤 2: 配置远程仓库...${NC}"
if git remote get-url origin >/dev/null 2>&1; then
    CURRENT_REMOTE=$(git remote get-url origin)
    echo "   当前远程仓库: $CURRENT_REMOTE"
    
    if [ "$CURRENT_REMOTE" != "$GITHUB_REPO" ]; then
        echo "   远程仓库地址不匹配，正在更新..."
        git remote set-url origin "$GITHUB_REPO"
        echo -e "   ${GREEN}✅ 远程仓库已更新${NC}"
    else
        echo -e "   ${GREEN}✅ 远程仓库已正确配置${NC}"
    fi
else
    echo "   未配置远程仓库，正在添加..."
    git remote add origin "$GITHUB_REPO"
    echo -e "   ${GREEN}✅ 远程仓库已添加${NC}"
fi
echo ""

# 步骤3: 检查是否有未提交的更改
echo -e "${YELLOW}步骤 3: 检查文件状态...${NC}"
if [ -z "$(git status --porcelain)" ]; then
    echo -e "   ${GREEN}✅ 工作目录干净，没有需要提交的更改${NC}"
else
    echo "   发现未提交的更改:"
    git status --short
    echo ""
    
    # 步骤4: 添加所有文件到暂存区
    echo -e "${YELLOW}步骤 4: 添加文件到Git...${NC}"
    git add .
    echo -e "   ${GREEN}✅ 所有文件已添加到暂存区${NC}"
    echo ""
    
    # 步骤5: 创建提交
    echo -e "${YELLOW}步骤 5: 创建提交...${NC}"
    
    # 生成默认提交信息
    DEFAULT_MSG="🎉 Initial release: Auto Summary System v1.0.0

✨ 功能特性:
- 多Skill协同架构 (6个独立Skill)
- 日常记录管理
- 日报自动生成与推送
- 周报自动生成与推送
- 定时任务调度
- Excel报表生成
- 邮件通知支持

📦 技术栈:
- Python 3.8+
- pandas, openpyxl
- schedule, PyYAML

🚀 使用方法:
- openclaw run auto-summary-system add '工作内容'
- openclaw run auto-summary-system report daily --notify
- openclaw run auto-summary-system scheduler start

📚 文档:
- README.md - 项目说明
- QUICKSTART.md - 快速上手
- USAGE_EXAMPLES.md - 详细示例
- PROJECT_SUMMARY.md - 项目总结

🔗 GitHub: https://github.com/1303996014/auto-summary-system"
    
    # 询问用户是否使用默认提交信息
    echo "   是否使用默认提交信息？ [Y/n]"
    read -r use_default
    
    if [[ "$use_default" =~ ^[Nn]$ ]]; then
        echo "   请输入提交信息:"
        read -r custom_msg
        COMMIT_MSG="$custom_msg"
    else
        COMMIT_MSG="$DEFAULT_MSG"
    fi
    
    git commit -m "$COMMIT_MSG"
    echo -e "   ${GREEN}✅ 提交创建成功${NC}"
    echo ""
fi

# 步骤6: 推送到GitHub
echo -e "${YELLOW}步骤 6: 推送到GitHub...${NC}"
echo "   正在推送到远程仓库..."

if git push -u origin main 2>/dev/null; then
    echo -e "   ${GREEN}✅ 代码推送成功！${NC}"
else
    echo -e "   ${YELLOW}⚠️  首次推送需要认证${NC}"
    echo ""
    echo "   请按以下步骤操作："
    echo "   1. 使用Personal Access Token作为密码"
    echo "   2. 访问: https://github.com/settings/tokens"
    echo "   3. 生成Token: ghp_xxxxxxxxxxxxxxxx"
    echo ""
    
    git push -u origin main
fi
echo ""

# 步骤7: 创建发布标签
echo -e "${YELLOW}步骤 7: 创建发布标签...${NC}"
echo "   是否创建v1.0.0发布标签？ [Y/n]"
read -r create_tag

if [[ ! "$create_tag" =~ ^[Nn]$ ]]; then
    echo "   请输入版本号 (默认: v1.0.0):"
    read -r version
    
    if [ -z "$version" ]; then
        version="v1.0.0"
    fi
    
    # 创建并推送标签
    git tag "$version"
    git push origin "$version"
    
    echo -e "   ${GREEN}✅ 标签 $version 创建并推送成功！${NC}"
    echo -e "   ${BLUE}ℹ️  GitHub Actions将自动创建发布${NC}"
fi
echo ""

# 完成信息
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}🎉 GitHub配置和提交完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${BLUE}📊 仓库信息:${NC}"
echo "   远程仓库: $(git remote get-url origin)"
echo "   分支: main"
if git rev-parse HEAD >/dev/null 2>&1; then
    echo "   提交: $(git log -1 --pretty=format:'%h - %s')"
fi
echo ""
echo -e "${BLUE}🔗 访问你的仓库:${NC}"
echo "   https://github.com/1303996014/auto-summary-system"
echo ""
echo -e "${BLUE}📝 下一步操作:${NC}"
echo "   1. 访问GitHub查看代码"
echo "   2. 查看Actions页面确认工作流运行"
echo "   3. 访问Releases查看自动发布"
echo "   4. 分享项目: openclaw install auto-summary-system"
echo "   5. 在OpenClaw社区分享你的Skill"
echo ""
echo -e "${BLUE}📚 文档链接:${NC}"
echo "   README: https://github.com/1303996014/auto-summary-system/blob/main/README.md"
echo "   快速开始: https://github.com/1303996014/auto-summary-system/blob/main/QUICKSTART.md"
echo ""
echo -e "${GREEN}✨ 项目已成功发布到GitHub！${NC}"
echo ""
