#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import webbrowser
import os
import sys
from urllib.parse import quote

def start_server(port=8000, directory=None, open_browser=True):
    """
    启动一个简单的 HTTP 服务器
    
    参数:
        port (int): 服务器端口号，默认为 8000
        directory (str): 服务器根目录，默认为当前目录
        open_browser (bool): 是否自动打开浏览器，默认为 True
    """
    # 设置处理程序
    handler = http.server.SimpleHTTPRequestHandler
    
    # 如果指定了目录，更改当前工作目录
    if directory:
        os.chdir(directory)
        
    # 创建服务器
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            file_to_open = "a-practical-guide-to-building-agents.html"
            
            print(f"服务器启动在 http://localhost:{port}")
            print(f"您可以在浏览器中访问: http://localhost:{port}/{quote(file_to_open)}")
            print("按 Ctrl+C 停止服务器")
            
            # 自动在浏览器中打开文件
            if open_browser and os.path.exists(file_to_open):
                webbrowser.open(f'http://localhost:{port}/{quote(file_to_open)}')
            
            # 启动服务器
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"错误: 端口 {port} 已被占用，请尝试其他端口")
            # 尝试其他端口
            start_server(port + 1, directory, open_browser)
        else:
            print(f"启动服务器时出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    import argparse
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='启动简单的 HTTP 服务器来查看网页')
    parser.add_argument('-p', '--port', type=int, default=8000, help='服务器端口号 (默认: 8000)')
    parser.add_argument('-d', '--directory', help='服务器根目录 (默认: 当前目录)')
    parser.add_argument('--no-browser', action='store_true', help='不自动打开浏览器')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 启动服务器
    start_server(args.port, args.directory, not args.no_browser) 