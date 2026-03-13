#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日报汇总Skill
负责生成每日工作汇总报告
"""

import os
import sys
import json
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))
from skills.storage_manager import StorageManager
from skills.report_generator import ReportGenerator


class DailySummary:
    def __init__(self, config_path="config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.storage = StorageManager(self.config.get('storage', {}).get('path', './data'))
        self.report_generator = ReportGenerator(config_path)
    
    def _load_config(self):
        """加载配置文件"""
        try:
            import yaml
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def generate_daily_summary(self, target_date=None, output_path=None, auto_notify=False):
        """
        生成日报汇总
        
        Args:
            target_date: 目标日期，默认为今天
            output_path: 输出路径
            auto_notify: 是否自动发送给客户
        """
        if target_date is None:
            target_date = date.today()
        
        print(f"\n📊 正在生成日报汇总 ({target_date})...")
        
        # 获取当日记录
        records = self.storage.get_records_by_date(target_date)
        
        if not records:
            print(f"⚠️  {target_date} 暂无记录")
            # 仍然生成空报告
        
        # 统计数据
        stats = self._analyze_records(records)
        
        # 生成报告内容
        report_content = self._create_report_content(target_date, records, stats)
        
        # 生成表格文件
        if output_path is None:
            report_dir = Path(self.config.get('report', {}).get('output_path', './reports'))
            report_dir.mkdir(exist_ok=True)
            output_path = report_dir / f"daily_summary_{target_date}.xlsx"
        
        report_file = self.report_generator.generate_daily_report(
            target_date, records, stats, str(output_path)
        )
        
        if report_file:
            print(f"✅ 日报已生成: {report_file}")
            
            # 自动发送给客户
            if auto_notify:
                self._send_to_client(report_file, target_date, "daily")
            
            return report_file
        else:
            print("❌ 生成日报失败")
            return None
    
    def _analyze_records(self, records):
        """分析记录数据"""
        categories = {}
        total_records = len(records)
        
        for record in records:
            category = record.get('category', '未分类')
            categories[category] = categories.get(category, 0) + 1
        
        return {
            'total_records': total_records,
            'categories': categories,
            'avg_per_category': total_records / len(categories) if categories else 0
        }
    
    def _create_report_content(self, target_date, records, stats):
        """创建报告内容"""
        content = {
            'date': str(target_date),
            'title': f'工作日报 - {target_date}',
            'summary': {
                'total_records': stats['total_records'],
                'categories_count': len(stats['categories'])
            },
            'categories': stats['categories'],
            'records': records
        }
        return content
    
    def _send_to_client(self, report_file, target_date, report_type):
        """发送报告给客户"""
        try:
            # 动态导入避免循环依赖
            from skills.client_notifier import ClientNotifier
            
            notifier = ClientNotifier(str(self.config_path))
            subject = f"工作日报 - {target_date}"
            message = f"您好，附件是{target_date}的工作日报，请查收。"
            
            success = notifier.send_report(report_file, subject, message)
            
            if success:
                print(f"✅ 已发送给客户")
            else:
                print(f"❌ 发送失败")
            
            return success
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def get_yesterday_summary(self):
        """获取昨天的日报"""
        yesterday = date.today() - timedelta(days=1)
        return self.generate_daily_summary(yesterday)
    
    def show_today_preview(self):
        """显示今日记录预览"""
        records = self.storage.get_today_records()
        
        print(f"\n📅 今日记录预览 ({date.today()})")
        print(f"共 {len(records)} 条记录\n")
        
        if records:
            for i, record in enumerate(records, 1):
                content = record['content']
                category = record.get('category', '未分类')
                print(f"{i}. [{category}] {content[:60]}{'...' if len(content) > 60 else ''}")
        else:
            print("暂无记录")


def main():
    parser = argparse.ArgumentParser(description='日报汇总工具')
    parser.add_argument('--config', default='config.yaml', help='配置文件路径')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 生成日报
    generate_parser = subparsers.add_parser('generate', help='生成日报')
    generate_parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)')
    generate_parser.add_argument('--output', help='输出文件路径')
    generate_parser.add_argument('--notify', action='store_true', help='自动发送给客户')
    generate_parser.add_argument('--yesterday', action='store_true', help='生成昨天的日报')
    
    # 预览今日记录
    preview_parser = subparsers.add_parser('preview', help='预览今日记录')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    daily_summary = DailySummary(args.config)
    
    if args.command == 'generate':
        if args.yesterday:
            daily_summary.get_yesterday_summary()
        else:
            target_date = None
            if args.date:
                from datetime import datetime
                target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
            
            daily_summary.generate_daily_summary(
                target_date=target_date,
                output_path=args.output,
                auto_notify=args.notify
            )
    
    elif args.command == 'preview':
        daily_summary.show_today_preview()


if __name__ == '__main__':
    main()
