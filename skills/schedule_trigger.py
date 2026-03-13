#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时调度触发器Skill
负责定时触发日报和周报的生成任务
"""

import os
import sys
import time
import argparse
import schedule
from datetime import datetime, date
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))
from skills.daily_summary import DailySummary
from skills.weekly_summary import WeeklySummary


class ScheduleTrigger:
    def __init__(self, config_path="config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.daily_summary = DailySummary(config_path)
        self.weekly_summary = WeeklySummary(config_path)
        self.is_running = False
        
        # 定时任务配置
        schedule_config = self.config.get('schedule', {})
        
        # 日报配置
        daily_config = schedule_config.get('daily', {})
        self.daily_enabled = daily_config.get('enabled', True)
        self.daily_time = daily_config.get('time', '18:00')
        
        # 周报配置
        weekly_config = schedule_config.get('weekly', {})
        self.weekly_enabled = weekly_config.get('enabled', True)
        self.weekly_day = weekly_config.get('day', 'friday')
        self.weekly_time = weekly_config.get('time', '17:00')
    
    def _load_config(self):
        """加载配置文件"""
        try:
            import yaml
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def setup_schedule(self):
        """设置定时任务"""
        print("\n⏰ 设置定时任务...")
        
        # 设置日报任务
        if self.daily_enabled:
            schedule.every().day.at(self.daily_time).do(self._run_daily_summary)
            print(f"✅ 日报任务: 每天 {self.daily_time} 触发")
        else:
            print("⏸️  日报任务: 已禁用")
        
        # 设置周报任务
        if self.weekly_enabled:
            day_map = {
                'monday': schedule.every().monday,
                'tuesday': schedule.every().tuesday,
                'wednesday': schedule.every().wednesday,
                'thursday': schedule.every().thursday,
                'friday': schedule.every().friday,
                'saturday': schedule.every().saturday,
                'sunday': schedule.every().sunday
            }
            
            if self.weekly_day in day_map:
                day_map[self.weekly_day].at(self.weekly_time).do(self._run_weekly_summary)
                print(f"✅ 周报任务: 每周 {self.weekly_day} {self.weekly_time} 触发")
            else:
                print(f"❌ 周报任务: 无效的星期设置 '{self.weekly_day}'")
        else:
            print("⏸️  周报任务: 已禁用")
        
        # 设置状态检查任务（每30分钟）
        schedule.every(30).minutes.do(self._print_status)
        
        print("\n📋 定时任务设置完成")
        self._print_next_run_time()
    
    def _run_daily_summary(self):
        """运行日报生成任务"""
        print(f"\n{'='*60}")
        print(f"📝 开始执行日报生成任务 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        print(f"{'='*60}")
        
        try:
            # 生成昨天（工作日）的日报
            yesterday = date.today() - timedelta(days=1)
            
            # 如果是周一，则生成上周五的日报（跳过周末）
            if yesterday.weekday() == 6:  # 周日
                yesterday = date.today() - timedelta(days=2)  # 上周五
            elif yesterday.weekday() == 5:  # 周六
                yesterday = date.today() - timedelta(days=1)  # 上周五
            
            self.daily_summary.generate_daily_summary(
                target_date=yesterday,
                auto_notify=True
            )
            
            print(f"✅ 日报任务执行完成")
            
        except Exception as e:
            print(f"❌ 日报任务执行失败: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"{'='*60}\n")
    
    def _run_weekly_summary(self):
        """运行周报生成任务"""
        print(f"\n{'='*60}")
        print(f"📊 开始执行周报生成任务 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        print(f"{'='*60}")
        
        try:
            # 生成上周的周报
            last_week = date.today() - timedelta(days=7)
            
            self.weekly_summary.generate_weekly_summary(
                target_date=last_week,
                auto_notify=True
            )
            
            print(f"✅ 周报任务执行完成")
            
        except Exception as e:
            print(f"❌ 周报任务执行失败: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"{'='*60}\n")
    
    def _print_status(self):
        """打印状态信息"""
        print(f"💓 系统运行正常 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    
    def _print_next_run_time(self):
        """打印下次运行时间"""
        print(f"\n🕐 下次运行时间:")
        
        if self.daily_enabled:
            next_daily = schedule.next_run()
            if next_daily:
                print(f"  日报: {next_daily.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.weekly_enabled:
            # 获取下一个指定星期几的时间
            from datetime import datetime, timedelta
            now = datetime.now()
            days_ahead = self._get_day_index(self.weekly_day) - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_weekly = now + timedelta(days=days_ahead)
            hour, minute = map(int, self.weekly_time.split(':'))
            next_weekly = next_weekly.replace(hour=hour, minute=minute, second=0, microsecond=0)
            print(f"  周报: {next_weekly.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _get_day_index(self, day_name):
        """获取星期几的索引（0=周一）"""
        day_map = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }
        return day_map.get(day_name.lower(), 4)  # 默认为周五
    
    def run_pending(self):
        """运行待执行的任务"""
        schedule.run_pending()
    
    def start_scheduler(self):
        """启动调度器"""
        print(f"\n{'='*60}")
        print("🚀 启动定时调度器")
        print(f"{'='*60}")
        
        self.setup_schedule()
        self.is_running = True
        
        try:
            while self.is_running:
                self.run_pending()
                time.sleep(60)  # 每分钟检查一次
                
        except KeyboardInterrupt:
            print("\n\n⏹️  收到停止信号，正在关闭调度器...")
            self.stop_scheduler()
        
        except Exception as e:
            print(f"❌ 调度器运行出错: {e}")
            import traceback
            traceback.print_exc()
            self.stop_scheduler()
    
    def stop_scheduler(self):
        """停止调度器"""
        self.is_running = False
        print("✅ 调度器已停止")
    
    def show_schedule_info(self):
        """显示定时任务信息"""
        print("\n📅 定时任务信息:")
        print(f"日报任务:")
        print(f"  状态: {'启用' if self.daily_enabled else '禁用'}")
        print(f"  触发时间: 每天 {self.daily_time}")
        
        print(f"\n周报任务:")
        print(f"  状态: {'启用' if self.weekly_enabled else '禁用'}")
        print(f"  触发时间: 每周 {self.weekly_day} {self.weekly_time}")
        
        self._print_next_run_time()
    
    def run_once(self, task_type):
        """
        立即运行一次任务（用于测试）
        
        Args:
            task_type: 任务类型 ('daily' 或 'weekly')
        """
        print(f"\n🔄 手动触发 {task_type} 任务...")
        
        if task_type == 'daily':
            self._run_daily_summary()
        elif task_type == 'weekly':
            self._run_weekly_summary()
        else:
            print(f"❌ 无效的任务类型: {task_type}")


def main():
    parser = argparse.ArgumentParser(description='定时调度触发器')
    parser.add_argument('--config', default='config.yaml', help='配置文件路径')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 启动调度器
    start_parser = subparsers.add_parser('start', help='启动调度器')
    
    # 停止调度器（通过PID文件或其他方式）
    stop_parser = subparsers.add_parser('stop', help='停止调度器')
    
    # 显示任务信息
    info_parser = subparsers.add_parser('info', help='显示任务信息')
    
    # 手动运行任务
    run_parser = subparsers.add_parser('run', help='手动运行任务')
    run_parser.add_argument('task', choices=['daily', 'weekly'], help='任务类型')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    scheduler = ScheduleTrigger(args.config)
    
    if args.command == 'start':
        scheduler.start_scheduler()
    
    elif args.command == 'stop':
        scheduler.stop_scheduler()
    
    elif args.command == 'info':
        scheduler.show_schedule_info()
    
    elif args.command == 'run':
        scheduler.run_once(args.task)


if __name__ == '__main__':
    main()
