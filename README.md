基于Flask的光谱数据管理与分类系统，支持多种光谱数据格式的存储、检索和相似度分析。

## 主要特性

- 🧬 支持CSV/TSV/JSON多格式光谱数据解析
- 🧩 模块化模板继承体系，统一UI风格
- 🔍 基于余弦相似度的光谱匹配算法
- 📊 结构化JSON数据存储，保留元数据
- ⚙️ 自动化Bootstrap前端集成
- 📈 数据版本追踪（创建/更新时间戳）

## 技术栈

- **Web框架**: Flask 3.0
- **数据库**: SQLAlchemy 3.0 + SQLite
- **数据处理**: NumPy + Scikit-learn
- **前端**: Bootstrap 5.3 + Jinja2

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourrepo/nRamanSpectra.git

# 安装依赖
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 启动服务
flask run
```

## API接口

### 创建光谱数据
`POST /spectras`
```http
Content-Type: multipart/form-data

{
  "name": "样本名称",
  "file": "光谱数据文件"
}
```

### 光谱分类
`POST /spectras/classify`
```http
Content-Type: multipart/form-data

{
  "file": "待分类光谱文件"
}
```

响应示例：
```json
{
  "match": "最匹配样本",
  "similarity": 0.956,
  "evaluated_samples": 5
}
```

## 数据格式要求
1. 二维数组格式：[[x1,y1], [x2,y2], ...]
2. CSV/TSV文件需包含两列数据
3. 支持单文件或多文件同时上传

⚠️ **注意**：首次使用前需配置`.flaskenv`环境文件