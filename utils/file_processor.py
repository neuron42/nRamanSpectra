import ast
from flask import abort
from typing import List, Any

class FileProcessor:
    @staticmethod
    def parse_spectral_file(file) -> List[List[float]]:
        """处理光谱文件并返回标准化数据格式"""
        try:
            content = file.read().decode("utf-8")
            return FileProcessor._normalize_data(content)
        except (UnicodeDecodeError, SyntaxError, ValueError) as e:
            abort(400, f"文件解析失败: {str(e)}")

    @staticmethod
    def _normalize_data(content: str) -> List[List[float]]:
        """统一不同格式的数据为二维数组"""
        lines = content.splitlines()
        
        # 尝试解析为二维数组
        try:
            return ast.literal_eval(content)
        except SyntaxError:
            pass
            
        # 处理CSV格式
        if any(',' in line for line in lines):
            return [
                [float(x) for x in line.split(',')]
                for line in lines if line.strip()
            ]
            
        # 处理空格分隔
        return [
            [float(x) for x in line.split()]
            for line in lines if line.strip()
        ]