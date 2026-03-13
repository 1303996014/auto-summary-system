#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化汇总系统 - 主协调器
整合所有Skill，提供统一的命令行接口
"""

import os
import sys
import argparse
from pathlib import Path

# 添加skills目录到路径
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'skills'))

from skills.storage_manager import StorageManager
from skills.daily_summary import DailySummary
from skills.weekly_summary import WeeklySummary
from skills.schedule_trigger import ScheduleTrigger
from skills.report_generator import ReportGenerator
from skills.client_notifier import ClientNotifier


class AutoSummarySystem:
    """自动化汇总系统主类"""
    
    def __init__(self, config_path="config.yaml"):
        self.config_path = Path(config_path)
        self.storage = StorageManager()
        self.daily_summary = DailySummary(config_path)
        self.weekly_summary = WeeklySummary(config_path)
        self.scheduler = ScheduleTrigger(config_path)
        self.report_generator = ReportGenerator(config_path)
        self.notifier = ClientNotifier(config_path)
    
    def add_record(self, content, category="工作记录"):
        """添加工作记录"""
        return self.storage.add_record(content, category)
    
    def list_records(self, limit=10, today_only=False):
        """列出记录"""
        if today_only:
            return self.storage.get_today_records()
        return self.storage.list_records(limit)
    
    def generate_daily_report(self, target_date=None, auto_notify=False):
        """生成日报"""
        return self.daily_summary.generate_daily_summary(
            target_date=target_date,
            auto_notify=auto_notify
        )
    
    def generate_weekly_report(self, target_date=None, auto_notify=False):
        """生成周报"""
        return self.weekly_summary.generate_weekly_summary(
            target_date=target_date,
            auto_notify=auto_notify
        )
    
    def start_scheduler(self):
        """启动定时调度器"""
        return self.scheduler.start_scheduler()
    
    def stop_scheduler(self):
        """停止定时调度器"""
        return self.scheduler.stop_scheduler()
    
    def show_status(self):
        """显示系统状态"""
        print("\n" + "="*60)
        print("📊 自动化汇总系统状态")
        print("="*60)
        
        # 今日记录统计
        today_records = self.storage.get_today_records()
        print(f"\n📅 今日记录: {len(today_records)} 条")
        
        # 本周记录统计
        week_start, week_end = self.weekly_summary.get_week_range()
        week_records = self.storage.get_records_by_range(week_start, week_end)
        print(f"📈 本周记录: {len(week_records)} 条")
        
        # 配置信息
        print(f"\n⚙️  配置信息:")
        print(f"  数据存储路径: {self.config_path.parent / 'data'}")
        print(f"  报表输出路径: {self.config_path.parent / 'reports'}")
        
        # 定时任务状态
        self.scheduler.show_schedule_info()
        
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='自动化汇总系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 添加记录
  python main.py add "今日完成项目A的需求分析"
  
  # 查看今日记录
  python main.py list --today
  
  # 生成日报并发送
  python main.py report daily --notify
  
  # 生成周报
  python main.py report weekly
  
  # 启动定时调度器
  python main.py scheduler start
  
  # 显示系统状态
  python main.py status
        """
    )
    
    parser.add_argument('--config', default='config.yaml', help='配置文件路径')
    subparsers = parser.add_subparsers(dest='command', help='主命令')
    
    # 记录管理
    record_parser = subparsers.add_parser('add', help='添加记录')
    record_parser.add_argument('content', help='记录内容')
    record_parser.add_argument('--category', default='工作记录', help='记录类别')
    
    list_parser = subparsers.add_parser('list', help='列出记录')
    list_parser.add_argument('--limit', type=int, default=10, help='限制数量')
    list_parser.add_argument('--today', action='store_true', help='仅显示今日记录')
    
    # 报表生成
    report_parser = subparsers.add_parser('report', help='生成报表')
    report_subparsers = report_parser.add_subparsers(dest='report_type', help='报表类型')
    
    daily_report_parser = report_subparsers.add_parser('daily', help='生成日报')
    daily_report_parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)')
    daily_report_parser.add_argument('--notify', action='store_true', help='自动发送给客户')
    
    weekly_report_parser = report_subparsers.add_parser('weekly', help='生成周报')
    weekly_report_parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)')
    weekly_report_parser.add_argument('--notify', action='store_true', help='自动发送给客户')
    
    # 调度器管理
    scheduler_parser = subparsers.add_parser('scheduler', help='调度器管理')
    scheduler_subparsers = scheduler_parser.add_subparsers(dest='scheduler_action', help='调度器操作')
    
    scheduler_start_parser = scheduler_subparsers.add_parser('start', help='启动调度器')
    scheduler_stop_parser = scheduler_subparsers.add_parser('stop', help='停止调度器')
    scheduler_info_parser = scheduler_subparsers.add_parser('info', help='显示调度器信息')
    
    # 系统状态
    status_parser = subparsers.add_parser('status', help='显示系统状态')
    
    # 初始化系统
    init_parser = subparsers.add_parser('init', help='初始化系统（创建必要目录）')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    system = AutoSummarySystem(args.config)
    
    # 记录管理
    if args.command == 'add':
        system.add_record(args.content, args.category)
    
    elif args.command == 'list':
        records = system.list_records(args.limit, args.today)
        
        if args.today:
            print(f"\n📅 今日记录 ({len(records)} 条):")
        else:
            print(f"\n📋 最近记录 ({len(records)} 条):")
        
        if not records:
            print("暂无记录")
        else:
            for i, record in enumerate(records, 1):
                date = record.get('date', '未知')
                if not args.today:
                    print(f"\n日期: {date}")
                
                content = record['content']
                category = record.get('category', '未分类')
                print(f"{i}. [{category}] {content[:100]}{'...' if len(content) > 100 else ''}")
    
    # 报表生成
    elif args.command == 'report':
        if args.report_type == 'daily':
            target_date = None
            if args.date:
                from datetime import datetime
                target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
            
            system.generate_daily_report(target_date, args.notify)
        
        elif args.report_type == 'weekly':
            target_date = None
            if args.date:
                from datetime import datetime
                target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
            
            system.generate_weekly_report(target_date, args.notify)
        
        else:
            report_parser.print_help()
    
    # 调度器管理
    elif args.command == 'scheduler':
        if args.scheduler_action == 'start':
            system.start_scheduler()
        elif args.scheduler_action == 'stop':
            system.stop_scheduler()
        elif args.scheduler_action == 'info':
            system.scheduler.show_schedule_info()
        else:
            scheduler_parser.print_help()
    
    # 系统状态
    elif args.command == 'status':
        system.show_status()
    
    # 初始化系统
    elif args.command == 'init':
        print("\n🏗️  初始化系统...")
        
        # 创建必要目录
        dirs_to_create = [
            Path(args.config).parent / 'data',
            Path(args.config).parent / 'reports',
            Path(args.config).parent / 'logs'
        ]
        
        for dir_path in dirs_to_create:
            if not dir_path.exists():
                dir_path.mkdir(parents=True)
                print(f"✅ 创建目录: {dir_path}")
            else:
                print(f"⏭️  目录已存在: {dir_path}")
        
        print("\n✅ 系统初始化完成")
    
    print()


if __name__ == '__main__':
    main()
