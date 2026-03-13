#!/bin/bash
# 自动化汇总系统安装脚本

set -e

echo "🚀 开始安装自动化汇总系统..."

# 检查Python版本
echo "📋 检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $python_version"

# 创建虚拟环境（可选）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建完成"
else
    echo "⏭️  虚拟环境已存在"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "⬆️  升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

echo "✅ 依赖包安装完成"

# 初始化系统目录
echo "🏗️  初始化系统目录..."
python3 main.py init

# 设置执行权限
echo "🔑 设置执行权限..."
chmod +x main.py
chmod +x skills/*.py

echo ""
echo "="*60
echo "🎉 安装完成！"
echo "="*60
echo ""
echo "使用说明:"
echo "1. 编辑 config.yaml 配置客户邮箱等信息"
echo "2. 添加记录: python3 main.py add '工作内容'"
echo "3. 查看记录: python3 main.py list --today"
echo "4. 生成日报: python3 main.py report daily --notify"
echo "5. 启动调度器: python3 main.py scheduler start"
echo ""
echo "或者直接使用OpenClaw命令:"
echo "openclaw run auto-summary-system add '工作内容'"
echo ""
echo "="*60
