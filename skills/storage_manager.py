#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据存储管理Skill
负责记录、查询和管理用户的日常输入数据
"""

import os
import json
import uuid
import argparse
from datetime import datetime, date
from pathlib import Path

class StorageManager:
    def __init__(self, storage_path="./data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.data_file = self.storage_path / "daily_records.json"
        
        # 初始化数据文件
        if not self.data_file.exists():
            self._save_data({})
    
    def _load_data(self):
        """加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载数据失败: {e}")
            return {}
    
    def _save_data(self, data):
        """保存数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def add_record(self, content, category="工作记录"):
        """添加记录"""
        data = self._load_data()
        today = str(date.today())
        
        if today not in data:
            data[today] = []
        
        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "category": category
        }
        
        data[today].append(record)
        
        if self._save_data(data):
            print(f"✅ 记录已添加 (ID: {record['id']})")
            return record
        else:
            print("❌ 添加记录失败")
            return None
    
    def get_today_records(self):
        """获取今日记录"""
        data = self._load_data()
        today = str(date.today())
        return data.get(today, [])
    
    def get_records_by_date(self, target_date):
        """获取指定日期的记录"""
        data = self._load_data()
        date_str = str(target_date)
        return data.get(date_str, [])
    
    def get_records_by_range(self, start_date, end_date):
        """获取日期范围内的记录"""
        data = self._load_data()
        records = []
        
        start = datetime.strptime(str(start_date), '%Y-%m-%d').date()
        end = datetime.strptime(str(end_date), '%Y-%m-%d').date()
        
        for date_str, day_records in data.items():
            try:
                current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if start <= current_date <= end:
                    records.extend(day_records)
            except ValueError:
                continue
        
        return records
    
    def delete_record(self, record_id):
        """删除记录"""
        data = self._load_data()
        deleted = False
        
        for date_str, records in data.items():
            data[date_str] = [r for r in records if r['id'] != record_id]
            if len(data[date_str]) != len(records):
                deleted = True
        
        if deleted:
            self._save_data(data)
            print(f"✅ 记录已删除 (ID: {record_id})")
            return True
        else:
            print(f"❌ 未找到记录 (ID: {record_id})")
            return False
    
    def list_records(self, limit=10):
        """列出最近的记录"""
        data = self._load_data()
        all_records = []
        
        for date_str, records in sorted(data.items(), reverse=True):
            for record in records:
                record_with_date = record.copy()
                record_with_date['date'] = date_str
                all_records.append(record_with_date)
        
        all_records.sort(key=lambda x: x['timestamp'], reverse=True)
        return all_records[:limit]
    
    def export_data(self, output_file):
        """导出所有数据"""
        data = self._load_data()
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 数据已导出到: {output_file}")
            return True
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='数据存储管理工具')
    parser.add_argument('--storage-path', default='./data', help='存储路径')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 添加记录
    add_parser = subparsers.add_parser('add', help='添加记录')
    add_parser.add_argument('content', help='记录内容')
    add_parser.add_argument('--category', default='工作记录', help='记录类别')
    
    # 列出记录
    list_parser = subparsers.add_parser('list', help='列出记录')
    list_parser.add_argument('--limit', type=int, default=10, help='限制数量')
    list_parser.add_argument('--today', action='store_true', help='仅显示今日记录')
    
    # 删除记录
    delete_parser = subparsers.add_parser('delete', help='删除记录')
    delete_parser.add_argument('id', help='记录ID')
    
    # 导出数据
    export_parser = subparsers.add_parser('export', help='导出数据')
    export_parser.add_argument('output', help='输出文件路径')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = StorageManager(args.storage_path)
    
    if args.command == 'add':
        manager.add_record(args.content, args.category)
    
    elif args.command == 'list':
        if args.today:
            records = manager.get_today_records()
            print(f"\n📅 今日记录 ({len(records)} 条):")
        else:
            records = manager.list_records(args.limit)
            print(f"\n📋 最近记录 ({len(records)} 条):")
        
        if not records:
            print("暂无记录")
        else:
            for record in records:
                date = record.get('date', '未知')
                content = record['content']
                category = record['category']
                print(f"\n[{date}] {category}")
                print(f"  ID: {record['id']}")
                print(f"  内容: {content[:100]}{'...' if len(content) > 100 else ''}")
    
    elif args.command == 'delete':
        manager.delete_record(args.id)
    
    elif args.command == 'export':
        manager.export_data(args.output)


if __name__ == '__main__':
    main()
