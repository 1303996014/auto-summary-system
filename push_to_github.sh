#!/bin/bash
# 自动化汇总系统 - GitHub发布脚本

set -e

echo "🚀 准备发布到GitHub..."

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Git是否已初始化
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Git仓库尚未初始化，正在初始化...${NC}"
    git init
fi

# 检查远程仓库
if ! git remote get-url origin >/dev/null 2>&1; then
    echo -e "${YELLOW}未配置远程仓库，请先设置远程仓库地址${NC}"
    echo "例如: git remote add origin https://github.com/YOUR_USERNAME/auto-summary-system.git"
    echo "或者运行: gh repo create auto-summary-system --public --source=. --remote=origin --push"
    exit 1
fi

# 检查是否有更改
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}没有需要提交的更改${NC}"
else
    echo -e "${GREEN}发现更改，正在添加到Git...${NC}"
    git add .
    
    # 获取用户输入提交信息
    read -p "请输入提交信息 (或直接回车使用默认): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Update: $(date +'%Y-%m-%d %H:%M:%S')"
    fi
    
    git commit -m "$commit_msg"
    echo -e "${GREEN}✅ 提交完成${NC}"
fi

# 推送到GitHub
echo -e "${GREEN}正在推送到GitHub...${NC}"
if git push -u origin main 2>/dev/null; then
    echo -e "${GREEN}✅ 代码推送成功！${NC}"
else
    echo -e "${YELLOW}首次推送需要设置上游分支${NC}"
    git push -u origin main
    echo -e "${GREEN}✅ 代码推送成功！${NC}"
fi

# 检查是否创建标签
echo ""
read -p "是否创建发布标签 (v1.0.0)? [y/N]: " create_tag
if [[ "$create_tag" =~ ^[Yy]$ ]]; then
    read -p "请输入版本号 (例如: v1.0.0): " version
    if [ -z "$version" ]; then
        version="v1.0.0"
    fi
    
    # 创建并推送标签
    git tag "$version"
    git push origin "$version"
    
    echo -e "${GREEN}✅ 标签 $version 创建并推送成功！${NC}"
    echo -e "${GREEN}GitHub Actions将自动创建发布${NC}"
fi

echo ""
echo -e "${GREEN}="$(printf '%*s' 60 | tr ' ' '=')"${NC}"
echo -e "${GREEN}🎉 GitHub发布完成！${NC}"
echo -e "${GREEN}="$(printf '%*s' 60 | tr ' ' '=')"${NC}"
echo ""
echo "📊 仓库信息:"
echo "   远程仓库: $(git remote get-url origin)"
echo "   分支: main"
echo "   最后提交: $(git log -1 --pretty=format:'%h - %s')"
echo ""
echo "🔗 访问你的仓库:"
echo "   仓库地址: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')"
echo ""
echo "📦 如果创建了标签，请访问 Releases 页面查看发布:"
echo "   Releases: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/releases"
echo ""
echo "📝 下一步:"
echo "   1. 访问GitHub仓库查看代码"
echo "   2. 在 Releases 页面查看自动发布的版本"
echo "   3. 分享你的项目给其他人: openclaw install auto-summary-system"
echo "   4. 在OpenClaw社区分享你的Skill"
echo ""