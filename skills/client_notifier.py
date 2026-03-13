#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客户推送通知Skill
负责将报表通过邮件或Webhook推送给客户
"""

import os
import smtplib
import requests
import argparse
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class ClientNotifier:
    def __init__(self, config_path="config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.client_email = self.config.get('client', {}).get('email', '')
        self.smtp_config = self.config.get('notification', {}).get('email', {})
        self.webhook_config = self.config.get('notification', {}).get('webhook', {})
    
    def _load_config(self):
        """加载配置文件"""
        try:
            import yaml
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def send_report(self, report_file, subject, message, client_email=None):
        """
        发送报告给客户
        
        Args:
            report_file: 报表文件路径
            subject: 邮件主题
            message: 邮件正文
            client_email: 客户邮箱（可选，如不提供则使用配置文件中的邮箱）
        
        Returns:
            是否发送成功
        """
        if not client_email:
            client_email = self.client_email
        
        if not client_email:
            print("❌ 未配置客户邮箱地址")
            return False
        
        # 优先使用邮件发送
        if self.smtp_config and self.smtp_config.get('smtp_server'):
            return self.send_via_email(report_file, subject, message, client_email)
        
        # 备选使用Webhook
        elif self.webhook_config and self.webhook_config.get('enabled'):
            return self.send_via_webhook(report_file, subject, message)
        
        else:
            print("❌ 未配置有效的通知方式（邮件或Webhook）")
            return False
    
    def send_via_email(self, report_file, subject, message, client_email):
        """
        通过邮件发送报告
        
        Args:
            report_file: 报表文件路径
            subject: 邮件主题
            message: 邮件正文
            client_email: 客户邮箱
        
        Returns:
            是否发送成功
        """
        try:
            # 检查配置
            smtp_server = self.smtp_config.get('smtp_server')
            smtp_port = self.smtp_config.get('smtp_port', 587)
            username = self.smtp_config.get('username')
            password = self.smtp_config.get('password')
            
            if not all([smtp_server, username, password]):
                print("❌ 邮件配置不完整")
                return False
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = client_email
            msg['Subject'] = subject
            
            # 添加正文
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            # 添加附件
            with open(report_file, 'rb') as f:
                attachment = MIMEApplication(f.read())
                attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(report_file)
                )
                msg.attach(attachment)
            
            # 发送邮件
            print(f"📧 正在发送邮件到 {client_email}...")
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            
            if self.smtp_config.get('use_tls', True):
                server.starttls()
            
            server.login(username, password)
            text = msg.as_string()
            server.sendmail(username, client_email, text)
            server.quit()
            
            print(f"✅ 邮件发送成功")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def send_via_webhook(self, report_file, subject, message):
        """
        通过Webhook发送报告
        
        Args:
            report_file: 报表文件路径
            subject: 标题
            message: 消息内容
        
        Returns:
            是否发送成功
        """
        try:
            webhook_url = self.webhook_config.get('url')
            
            if not webhook_url:
                print("❌ Webhook URL未配置")
                return False
            
            # 准备数据
            with open(report_file, 'rb') as f:
                file_content = f.read()
            
            # 这里假设Webhook支持文件上传
            # 具体实现可能需要根据实际的Webhook API进行调整
            payload = {
                'subject': subject,
                'message': message,
                'filename': os.path.basename(report_file)
            }
            
            files = {
                'file': (os.path.basename(report_file), file_content)
            }
            
            print(f"🌐 正在通过Webhook发送...")
            
            response = requests.post(
                webhook_url,
                data=payload,
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Webhook发送成功")
                return True
            else:
                print(f"❌ Webhook发送失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Webhook发送失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_notification(self, client_email=None):
        """
        测试通知功能
        
        Args:
            client_email: 测试邮箱（可选）
        
        Returns:
            是否测试成功
        """
        if not client_email:
            client_email = self.client_email
        
        if not client_email:
            print("❌ 未配置客户邮箱地址")
            return False
        
        subject = "测试邮件 - 自动化汇总系统"
        message = "这是一封测试邮件，用于验证自动化汇总系统的邮件发送功能是否正常。"
        
        print(f"🧪 正在测试邮件通知功能...")
        
        return self.send_via_email(
            __file__,  # 使用当前文件作为测试附件
            subject,
            message,
            client_email
        )
    
    def show_notification_config(self):
        """显示通知配置信息"""
        print("\n📬 通知配置信息:")
        
        # 客户信息
        print(f"客户邮箱: {self.client_email or '未配置'}")
        
        # SMTP配置
        if self.smtp_config and self.smtp_config.get('smtp_server'):
            print(f"SMTP服务器: {self.smtp_config.get('smtp_server')}")
            print(f"SMTP端口: {self.smtp_config.get('smtp_port', 587)}")
            print(f"发件人: {self.smtp_config.get('username', '未配置')}")
            print("SMTP状态: 已配置 ✓")
        else:
            print("SMTP状态: 未配置 ✗")
        
        # Webhook配置
        if self.webhook_config and self.webhook_config.get('enabled'):
            print(f"Webhook URL: {self.webhook_config.get('url', '未配置')}")
            print("Webhook状态: 已启用 ✓")
        else:
            print("Webhook状态: 未启用")


def main():
    parser = argparse.ArgumentParser(description='客户推送通知工具')
    parser.add_argument('--config', default='config.yaml', help='配置文件路径')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 发送报告
    send_parser = subparsers.add_parser('send', help='发送报告')
    send_parser.add_argument('report_file', help='报告文件路径')
    send_parser.add_argument('--subject', required=True, help='邮件主题')
    send_parser.add_argument('--message', required=True, help='邮件正文')
    send_parser.add_argument('--email', help='客户邮箱（可选）')
    
    # 测试通知
    test_parser = subparsers.add_parser('test', help='测试通知功能')
    test_parser.add_argument('--email', help='测试邮箱（可选）')
    
    # 显示配置
    config_parser = subparsers.add_parser('config', help='显示配置信息')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    notifier = ClientNotifier(args.config)
    
    if args.command == 'send':
        notifier.send_report(
            args.report_file,
            args.subject,
            args.message,
            args.email
        )
    
    elif args.command == 'test':
        notifier.test_notification(args.email)
    
    elif args.command == 'config':
        notifier.show_notification_config()


if __name__ == '__main__':
    main()
