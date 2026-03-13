#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报表生成Skill
负责生成Excel和PDF格式的报表
"""

import os
import json
from datetime import datetime, date, timedelta
from pathlib import Path


class ReportGenerator:
    def __init__(self, config_path="config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._check_dependencies()
    
    def _load_config(self):
        """加载配置文件"""
        try:
            import yaml
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def _check_dependencies(self):
        """检查依赖库"""
        try:
            import pandas as pd
            import openpyxl
            print("✅ 依赖库检查通过")
        except ImportError as e:
            print(f"❌ 缺少依赖库: {e}")
            print("请安装: pip install pandas openpyxl")
            raise
    
    def generate_daily_report(self, target_date, records, stats, output_path):
        """
        生成日报表
        
        Args:
            target_date: 目标日期
            records: 记录列表
            stats: 统计信息
            output_path: 输出文件路径
        
        Returns:
            生成的文件路径
        """
        try:
            import pandas as pd
            
            print(f"📝 正在生成日报表格...")
            
            # 创建工作簿
            writer = pd.ExcelWriter(output_path, engine='openpyxl')
            
            # Sheet 1: 记录详情
            if records:
                records_df = pd.DataFrame(records)
                records_df['timestamp'] = pd.to_datetime(records_df['timestamp'])
                records_df['time'] = records_df['timestamp'].dt.strftime('%H:%M')
                
                # 选择显示的列
                display_df = records_df[['time', 'category', 'content']].copy()
                display_df.columns = ['时间', '类别', '内容']
                
                display_df.to_excel(writer, sheet_name='记录详情', index=False)
            else:
                # 创建空记录表
                empty_df = pd.DataFrame(columns=['时间', '类别', '内容'])
                empty_df.to_excel(writer, sheet_name='记录详情', index=False)
            
            # Sheet 2: 统计摘要
            summary_data = {
                '统计项': [
                    '记录总数',
                    '类别数量',
                    '平均每类记录数'
                ],
                '数值': [
                    stats['total_records'],
                    len(stats['categories']),
                    round(stats['avg_per_category'], 2)
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='统计摘要', index=False)
            
            # Sheet 3: 类别分布
            if stats['categories']:
                category_data = {
                    '类别': list(stats['categories'].keys()),
                    '记录数': list(stats['categories'].values())
                }
                category_df = pd.DataFrame(category_data)
                category_df.to_excel(writer, sheet_name='类别分布', index=False)
            
            # 保存文件
            writer.close()
            
            print(f"✅ 日报表格已生成: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 生成日报表格失败: {e}")
            return None
    
    def generate_weekly_report(self, week_start, week_end, records, daily_stats, weekly_stats, output_path):
        """
        生成周报表
        
        Args:
            week_start: 周开始日期
            week_end: 周结束日期
            records: 记录列表
            daily_stats: 每日统计数据
            weekly_stats: 周统计信息
            output_path: 输出文件路径
        
        Returns:
            生成的文件路径
        """
        try:
            import pandas as pd
            
            print(f"📝 正在生成周报表格...")
            
            # 创建工作簿
            writer = pd.ExcelWriter(output_path, engine='openpyxl')
            
            # Sheet 1: 周报摘要
            summary_data = {
                '统计项': [
                    '本周天数',
                    '有记录的天数',
                    '总记录数',
                    '平均每天记录数',
                    '记录类别数'
                ],
                '数值': [
                    7,
                    weekly_stats['total_days'],
                    weekly_stats['total_records'],
                    round(weekly_stats['avg_per_day'], 2),
                    len(weekly_stats['category_stats'])
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='周报摘要', index=False)
            
            # Sheet 2: 每日统计
            if daily_stats:
                daily_data = {
                    '日期': list(daily_stats.keys()),
                    '记录数': [len(records) for records in daily_stats.values()]
                }
                daily_df = pd.DataFrame(daily_data)
                daily_df.to_excel(writer, sheet_name='每日统计', index=False)
            
            # Sheet 3: 类别统计
            if weekly_stats['category_stats']:
                category_data = {
                    '类别': list(weekly_stats['category_stats'].keys()),
                    '记录数': [info['count'] for info in weekly_stats['category_stats'].values()],
                    '占比': [f"{info['percentage']:.1f}%" for info in weekly_stats['category_stats'].values()]
                }
                category_df = pd.DataFrame(category_data)
                category_df.to_excel(writer, sheet_name='类别统计', index=False)
            
            # Sheet 4: 详细记录
            if records:
                records_df = pd.DataFrame(records)
                records_df['timestamp'] = pd.to_datetime(records_df['timestamp'])
                records_df['date'] = records_df['timestamp'].dt.strftime('%Y-%m-%d')
                records_df['time'] = records_df['timestamp'].dt.strftime('%H:%M')
                
                # 选择显示的列
                display_df = records_df[['date', 'time', 'category', 'content']].copy()
                display_df.columns = ['日期', '时间', '类别', '内容']
                
                display_df.to_excel(writer, sheet_name='详细记录', index=False)
            
            # Sheet 5: 空白记录日期
            all_dates = []
            current_date = week_start
            while current_date <= week_end:
                date_str = str(current_date)
                if date_str not in daily_stats:
                    all_dates.append({
                        '日期': date_str,
                        '星期': self._get_weekday_name(current_date),
                        '状态': '无记录',
                        '备注': ''
                    })
                current_date += timedelta(days=1)
            
            if all_dates:
                missing_df = pd.DataFrame(all_dates)
                missing_df.to_excel(writer, sheet_name='空白记录', index=False)
            
            # 保存文件
            writer.close()
            
            print(f"✅ 周报表格已生成: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 生成周报表格失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _get_weekday_name(self, date_obj):
        """获取星期几的名称"""
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return weekdays[date_obj.weekday()]
    
    def generate_simple_report(self, records, output_path):
        """
        生成简单报表（用于测试）
        
        Args:
            records: 记录列表
            output_path: 输出文件路径
        
        Returns:
            生成的文件路径
        """
        try:
            import pandas as pd
            
            if not records:
                print("⚠️  没有记录可生成报表")
                return None
            
            df = pd.DataFrame(records)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            df['time'] = df['timestamp'].dt.time
            
            # 导出到Excel
            df.to_excel(output_path, index=False)
            
            print(f"✅ 简单报表已生成: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 生成简单报表失败: {e}")
            return None
    
    def export_to_csv(self, records, output_path):
        """
        导出为CSV格式
        
        Args:
            records: 记录列表
            output_path: 输出文件路径
        
        Returns:
            生成的文件路径
        """
        try:
            import pandas as pd
            
            if not records:
                print("⚠️  没有记录可导出")
                return None
            
            df = pd.DataFrame(records)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            print(f"✅ CSV文件已导出: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 导出CSV失败: {e}")
            return None


def main():
    """测试函数"""
    # 这里可以添加测试代码
    print("报表生成Skill已加载")


if __name__ == '__main__':
    main()
