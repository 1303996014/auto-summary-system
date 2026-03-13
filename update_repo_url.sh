#!/bin/bash
# 更新GitHub仓库地址脚本

set -e

echo "🔄 正在更新GitHub仓库地址..."
echo "旧地址: yourusername/auto-summary-system"
echo "新地址: 1303996014/auto-summary-system"
echo ""

# 更新所有文件中的GitHub链接
files_to_update=(
  "README.md"
  "QUICKSTART.md"
  "USAGE_EXAMPLES.md"
  "PROJECT_SUMMARY.md"
  "GITHUB_SETUP.md"
  "GITHUB_SUBMIT.md"
  "SUBMIT_CHECKLIST.md"
  "INSTALL_AND_SUBMIT.md"
  "openclaw.yaml"
  "skill.yaml"
  "skill.json"
  "push_to_github.sh"
)

for file in "${files_to_update[@]}"; do
  if [ -f "$file" ]; then
    # 备份原始文件
    cp "$file" "$file.bak"
    
    # 替换GitHub链接
    sed -i '' 's/github\.com\/yourusername\/auto-summary-system/github.com\/1303996014\/auto-summary-system/g' "$file"
    sed -i '' 's/yourusername\/auto-summary-system/1303996014\/auto-summary-system/g' "$file"
    
    # 检查是否替换成功
    if grep -q "1303996014/auto-summary-system" "$file"; then
      echo "✅ 已更新: $file"
    else
      echo "⚠️  未找到需要替换的链接: $file"
      # 恢复备份
      mv "$file.bak" "$file"
    fi
    
    # 删除备份文件
    rm -f "$file.bak"
  else
    echo "⚠️  文件不存在: $file"
  fi
done

echo ""
echo "🎉 GitHub仓库地址更新完成！"
echo ""
echo "📊 更新统计："
echo "   已处理的文件数: ${#files_to_update[@]}"
echo ""
echo "🚀 下一步："
echo "   1. 运行: bash push_to_github.sh"
echo "   2. 或手动提交到GitHub"
echo ""
echo "📋 验证命令："
echo "   grep -r '1303996014/auto-summary-system' *.md *.yaml *.json 2>/dev/null | wc -l"
echo "   # 应该显示多个匹配结果"