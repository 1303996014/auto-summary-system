#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化汇总系统 - 测试脚本
用于验证系统安装和基本功能是否正常
"""

import sys
import os
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'skills'))

def test_imports():
    """测试模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        from skills.storage_manager import StorageManager
        from skills.daily_summary import DailySummary
        from skills.weekly_summary import WeeklySummary
        from skills.schedule_trigger import ScheduleTrigger
        from skills.report_generator import ReportGenerator
        from skills.client_notifier import ClientNotifier
        from main import AutoSummarySystem
        
        print("✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """测试配置文件"""
    print("\n🧪 测试配置文件...")
    
    try:
        import yaml
        config_path = Path('config.yaml')
        
        if not config_path.exists():
            print("❌ 配置文件不存在")
            return False
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        required_keys = ['storage', 'report', 'schedule', 'client']
        for key in required_keys:
            if key not in config:
                print(f"❌ 配置文件缺少必要字段: {key}")
                return False
        
        print("✅ 配置文件验证通过")
        return True
    except Exception as e:
        print(f"❌ 配置文件测试失败: {e}")
        return False

def test_data_storage():
    """测试数据存储"""
    print("\n🧪 测试数据存储...")
    
    try:
        from skills.storage_manager import StorageManager
        
        # 使用测试目录
        test_dir = Path('test_data')
        manager = StorageManager(str(test_dir))
        
        # 添加测试记录
        record = manager.add_record('测试记录 - 系统功能测试', '测试')
        
        if not record:
            print("❌ 添加记录失败")
            return False
        
        # 查询记录
        records = manager.get_today_records()
        
        if len(records) == 0:
            print("❌ 查询记录失败")
            return False
        
        print(f"✅ 数据存储测试通过 (记录ID: {record['id']})")
        return True
    except Exception as e:
        print(f"❌ 数据存储测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_report_generation():
    """测试报表生成"""
    print("\n🧪 测试报表生成...")
    
    try:
        from skills.report_generator import ReportGenerator
        import pandas as pd
        
        # 创建测试数据
        test_records = [
            {
                'id': 'test-001',
                'timestamp': '2026-03-13T09:00:00',
                'content': '测试记录1',
                'category': '测试'
            },
            {
                'id': 'test-002',
                'timestamp': '2026-03-13T14:00:00',
                'content': '测试记录2',
                'category': '测试'
            }
        ]
        
        # 创建测试目录
        test_report_dir = Path('test_reports')
        test_report_dir.mkdir(exist_ok=True)
        
        # 生成CSV报表
        generator = ReportGenerator()
        output_file = test_report_dir / 'test_report.csv'
        result = generator.export_to_csv(test_records, str(output_file))
        
        if not result or not output_file.exists():
            print("❌ CSV报表生成失败")
            return False
        
        print("✅ 报表生成测试通过")
        return True
    except Exception as e:
        print(f"❌ 报表生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_directory_structure():
    """测试目录结构"""
    print("\n🧪 测试目录结构...")
    
    required_files = [
        'main.py',
        'config.yaml',
        'skill.yaml',
        'skill.json',
        'requirements.txt',
        'README.md',
        'USAGE_EXAMPLES.md'
    ]
    
    required_dirs = [
        'skills',
        'data',
        'reports',
        'logs'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    for dir in required_dirs:
        if not Path(dir).exists():
            missing_dirs.append(dir)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    if missing_dirs:
        print(f"⚠️  缺少目录（将自动创建）: {', '.join(missing_dirs)}")
    
    print("✅ 目录结构测试通过")
    return True

def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("🚀 自动化汇总系统 - 测试程序")
    print("="*60)
    
    tests = [
        test_imports,
        test_configuration,
        test_directory_structure,
        test_data_storage,
        test_report_generation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    print(f"总测试数: {len(tests)}")
    print(f"通过: {passed} ✅")
    print(f"失败: {failed} ❌")
    
    if failed == 0:
        print("\n🎉 所有测试通过！系统运行正常")
        return True
    else:
        print(f"\n⚠️  {failed} 个测试失败，请检查系统配置")
        return False

def cleanup():
    """清理测试文件"""
    print("\n🧹 清理测试文件...")
    
    import shutil
    
    test_dirs = ['test_data', 'test_reports']
    
    for dir_path in test_dirs:
        if Path(dir_path).exists():
            shutil.rmtree(dir_path)
            print(f"  已删除: {dir_path}")
    
    print("✅ 清理完成")

if __name__ == '__main__':
    try:
        success = run_all_tests()
        cleanup()
        
        if success:
            print("\n✅ 系统测试完成，可以开始使用！")
            print("\n快速开始:")
            print("  python3 main.py add '今日工作记录'")
            print("  python3 main.py list --today")
            print("  python3 main.py status")
        else:
            print("\n❌ 系统测试失败，请检查错误信息")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
        cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试程序异常: {e}")
        import traceback
        traceback.print_exc()
        cleanup()
        sys.exit(1)
