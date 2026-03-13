#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周报汇总Skill
负责生成每周工作汇总报告
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


class WeeklySummary:
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
    
    def get_week_range(self, target_date=None):
        """
        获取指定日期所在周的日期范围
        
        Args:
            target_date: 目标日期，默认为今天
        
        Returns:
            (week_start, week_end) 周一到周日的日期
        """
        if target_date is None:
            target_date = date.today()
        
        # 计算周一（0=周一，6=周日）
        weekday = target_date.weekday()  # 0=周一, 6=周日
        week_start = target_date - timedelta(days=weekday)
        week_end = week_start + timedelta(days=6)
        
        return week_start, week_end
    
    def generate_weekly_summary(self, target_date=None, output_path=None, auto_notify=False):
        """
        生成周报汇总
        
        Args:
            target_date: 目标日期（用于确定是哪一周），默认为今天
            output_path: 输出路径
            auto_notify: 是否自动发送给客户
        """
        week_start, week_end = self.get_week_range(target_date)
        
        print(f"\n📊 正在生成周报汇总 ({week_start} 至 {week_end})...")
        
        # 获取本周记录
        records = self.storage.get_records_by_range(week_start, week_end)
        
        if not records:
            print(f"⚠️  本周暂无记录")
        
        # 按日期分组统计
        daily_stats = self._group_by_date(records)
        
        # 按类别统计
        category_stats = self._analyze_by_category(records)
        
        # 生成周统计数据
        weekly_stats = {
            'total_records': len(records),
            'total_days': len(daily_stats),
            'avg_per_day': len(records) / len(daily_stats) if daily_stats else 0,
            'category_stats': category_stats
        }
        
        # 生成报告内容
        report_content = self._create_weekly_report_content(
            week_start, week_end, records, daily_stats, weekly_stats
        )
        
        # 生成表格文件
        if output_path is None:
            report_dir = Path(self.config.get('report', {}).get('output_path', './reports'))
            report_dir.mkdir(exist_ok=True)
            week_num = week_start.isocalendar()[1]
            output_path = report_dir / f"weekly_summary_{week_start}_W{week_num}.xlsx"
        
        report_file = self.report_generator.generate_weekly_report(
            week_start, week_end, records, daily_stats, weekly_stats, str(output_path)
        )
        
        if report_file:
            print(f"✅ 周报已生成: {report_file}")
            
            # 自动发送给客户
            if auto_notify:
                self._send_to_client(report_file, week_start, week_end, "weekly")
            
            return report_file
        else:
            print("❌ 生成周报失败")
            return None
    
    def _group_by_date(self, records):
        """按日期分组统计"""
        daily_stats = {}
        
        for record in records:
            record_date = record['timestamp'][:10]  # 提取日期部分
            if record_date not in daily_stats:
                daily_stats[record_date] = []
            daily_stats[record_date].append(record)
        
        return daily_stats
    
    def _analyze_by_category(self, records):
        """按类别分析"""
        category_stats = {}
        
        for record in records:
            category = record.get('category', '未分类')
            if category not in category_stats:
                category_stats[category] = []
            category_stats[category].append(record)
        
        # 转换为统计信息
        result = {}
        for category, cat_records in category_stats.items():
            result[category] = {
                'count': len(cat_records),
                'percentage': len(cat_records) / len(records) * 100 if records else 0
            }
        
        return result
    
    def _create_weekly_report_content(self, week_start, week_end, records, daily_stats, weekly_stats):
        """创建周报内容"""
        content = {
            'week_start': str(week_start),
            'week_end': str(week_end),
            'title': f'工作周报 ({week_start} 至 {week_end})',
            'summary': {
                'total_records': weekly_stats['total_records'],
                'total_days': weekly_stats['total_days'],
                'avg_per_day': round(weekly_stats['avg_per_day'], 1)
            },
            'daily_breakdown': {
                date: {
                    'count': len(day_records),
                    'records': day_records
                }
                for date, day_records in daily_stats.items()
            },
            'category_breakdown': weekly_stats['category_stats'],
            'all_records': records
        }
        return content
    
    def _send_to_client(self, report_file, week_start, week_end, report_type):
        """发送报告给客户"""
        try:
            # 动态导入避免循环依赖
            from skills.client_notifier import ClientNotifier
            
            notifier = ClientNotifier(str(self.config_path))
            week_num = week_start.isocalendar()[1]
            subject = f"工作周报 - 第{week_num}周 ({week_start} 至 {week_end})"
            message = f"您好，附件是本周（{week_start} 至 {week_end}）的工作周报，请查收。"
            
            success = notifier.send_report(report_file, subject, message)
            
            if success:
                print(f"✅ 已发送给客户")
            else:
                print(f"❌ 发送失败")
            
            return success
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def get_last_week_summary(self):
        """获取上周的周报"""
        today = date.today()
        last_week = today - timedelta(days=7)
        return self.generate_weekly_summary(last_week)
    
    def show_week_preview(self):
        """显示本周记录预览"""
        week_start, week_end = self.get_week_range()
        records = self.storage.get_records_by_range(week_start, week_end)
        daily_stats = self._group_by_date(records)
        
        print(f"\n📅 本周记录预览 ({week_start} 至 {week_end})")
        print(f"共 {len(records)} 条记录，{len(daily_stats)} 天有记录\n")
        
        if daily_stats:
            for record_date in sorted(daily_stats.keys()):
                day_records = daily_stats[record_date]
                print(f"\n{record_date} ({len(day_records)} 条记录):")
                
                for i, record in enumerate(day_records[:3], 1):  # 只显示前3条
                    content = record['content']
                    category = record.get('category', '未分类')
                    print(f"  {i}. [{category}] {content[:50]}{'...' if len(content) > 50 else ''}")
                
                if len(day_records) > 3:
                    print(f"  ... 还有 {len(day_records) - 3} 条记录")
        else:
            print("暂无记录")


def main():
    parser = argparse.ArgumentParser(description='周报汇总工具')
    parser.add_argument('--config', default='config.yaml', help='配置文件路径')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 生成周报
    generate_parser = subparsers.add_parser('generate', help='生成周报')
    generate_parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)')
    generate_parser.add_argument('--output', help='输出文件路径')
    generate_parser.add_argument('--notify', action='store_true', help='自动发送给客户')
    generate_parser.add_argument('--last-week', action='store_true', help='生成上周周报')
    
    # 预览本周记录
    preview_parser = subparsers.add_parser('preview', help='预览本周记录')
    
    # 查看日期范围
    range_parser = subparsers.add_parser('range', help='查看本周日期范围')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    weekly_summary = WeeklySummary(args.config)
    
    if args.command == 'generate':
        if args.last_week:
            weekly_summary.get_last_week_summary()
        else:
            target_date = None
            if args.date:
                from datetime import datetime
                target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
            
            weekly_summary.generate_weekly_summary(
                target_date=target_date,
                output_path=args.output,
                auto_notify=args.notify
            )
    
    elif args.command == 'preview':
        weekly_summary.show_week_preview()
    
    elif args.command == 'range':
        week_start, week_end = weekly_summary.get_week_range()
        week_num = week_start.isocalendar()[1]
        print(f"\n📅 本周日期范围:")
        print(f"周数: 第 {week_num} 周")
        print(f"开始: {week_start}")
        print(f"结束: {week_end}")


if __name__ == '__main__':
    main()
