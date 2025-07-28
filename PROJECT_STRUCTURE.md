# SQL Assistant 项目结构

## 目录结构

```
sql-assistant/
├── README.md                    # 项目主要说明文档
├── README_SQLCoder.md          # SQLCoder集成说明文档
├── __init__.py                 # 包初始化文件
├── app.py                      # Streamlit应用主入口
├── config.py                   # 配置管理
├── database.py                 # 数据库连接管理
├── llm_model.py               # LLM模型管理
├── query_engine.py            # 查询引擎核心逻辑
├── requirements.txt           # Python依赖包
├── start_app.py              # 应用启动脚本
│
├── prompts/                   # Prompt相关模块
│   ├── __init__.py
│   ├── base_prompts.py       # 基础prompt模板（原prompts.py）
│   ├── sqlcoder_prompt.py    # SQLCoder专用prompt模板
│   └── sqlcoder_examples.json # SQLCoder示例集合
│
├── adapters/                  # 适配器模块
│   ├── __init__.py
│   └── sqlcoder_adapter.py   # SQLCoder Ollama适配器
│
├── utils/                     # 工具模块
│   ├── __init__.py
│   ├── data_formatter.py     # 数据格式化工具
│   ├── schema_converter.py   # Schema转换工具
│   └── sql_processor.py      # SQL处理工具
│
└── tests/                     # 测试模块
    ├── __init__.py
    └── test_sqlcoder.py      # SQLCoder测试套件
```

## 模块说明

### 核心模块
- **app.py**: Streamlit Web应用界面
- **query_engine.py**: 查询引擎，整合LLM和数据库功能
- **database.py**: 数据库连接和管理
- **llm_model.py**: LLM模型管理和调用
- **config.py**: 配置文件管理

### Prompts模块 (`prompts/`)
- **base_prompts.py**: 基础prompt模板和管理器
- **sqlcoder_prompt.py**: SQLCoder专用prompt生成器
- **sqlcoder_examples.json**: SQLCoder使用示例集合

### 适配器模块 (`adapters/`)
- **sqlcoder_adapter.py**: SQLCoder模型的Ollama API适配器

### 工具模块 (`utils/`)
- **data_formatter.py**: 查询结果格式化工具
- **schema_converter.py**: 数据库schema转换工具
- **sql_processor.py**: SQL语句处理和清理工具

### 测试模块 (`tests/`)
- **test_sqlcoder.py**: SQLCoder功能完整测试套件

## 重构说明

本次重构将原本混乱的文件结构重新组织为清晰的模块化结构：

1. **按功能分类**: 将相关功能的文件归类到对应的子目录
2. **提高可读性**: 重命名部分文件以更好地反映其功能
3. **模块化设计**: 每个子目录都有独立的`__init__.py`文件
4. **向后兼容**: 更新所有导入路径以适配新结构

## 使用方式

### 启动应用
```bash
python app.py
# 或
python start_app.py
```

### 导入模块示例
```python
# 导入prompt相关功能
from prompts.base_prompts import prompt_manager
from prompts.sqlcoder_prompt import SQLCoderPrompt

# 导入适配器
from adapters.sqlcoder_adapter import SQLCoderAdapter

# 导入工具
from utils.schema_converter import SchemaConverter
from utils.data_formatter import data_formatter
from utils.sql_processor import sql_processor
```

### 运行测试
```bash
cd tests
python test_sqlcoder.py
```