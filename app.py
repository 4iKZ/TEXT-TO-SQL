"""
主应用程序 - Streamlit界面和应用逻辑
"""

import streamlit as st
import pandas as pd
from config import *
from query_engine import query_engine


def setup_page_config():
    """设置页面配置"""
    st.set_page_config(
        page_title="SQL智能助手",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def setup_sidebar():
    """设置侧边栏"""
    with st.sidebar:
        st.title("🔍 SQL智能助手")
        st.markdown("---")
        
        # 模型选择
        st.subheader("🤖 模型配置")
        
        # 模型分类选择
        model_category = st.selectbox(
            "选择模型类别",
            options=["推荐SQL模型", "SQL专用模型", "大型通用模型", "中型通用模型", "小型通用模型", "全部模型"],
            index=0,
            help="选择模型类别以筛选适合的模型"
        )
        
        # 根据分类筛选模型
        if model_category == "推荐SQL模型":
            available_models = RECOMMENDED_SQL_MODELS
            st.info("💡 推荐使用SQL专用模型以获得最佳查询效果")
        elif model_category == "SQL专用模型":
            available_models = MODEL_CATEGORIES["sql_specialized"]
        elif model_category == "大型通用模型":
            available_models = MODEL_CATEGORIES["general_large"]
            st.warning("⚠️ 大型模型需要更多内存和计算资源")
        elif model_category == "中型通用模型":
            available_models = MODEL_CATEGORIES["general_medium"]
        elif model_category == "小型通用模型":
            available_models = MODEL_CATEGORIES["general_small"]
        else:  # 全部模型
            available_models = AVAILABLE_MODELS
        
        # 模型选择
        model_name = st.selectbox(
            "选择具体模型",
            options=available_models,
            index=0,
            help="选择用于生成SQL查询的语言模型"
        )
        
        # 显示模型信息
        if model_name in MODEL_CATEGORIES["sql_specialized"]:
            st.success("✅ SQL专用模型 - 推荐用于SQL查询")
        elif "72b" in model_name or "32b" in model_name:
            st.warning("⚠️ 大型模型 - 需要充足的系统资源")
        elif "14b" in model_name or "7b" in model_name:
            st.info("ℹ️ 中型模型 - 平衡性能与资源消耗")
        else:
            st.info("ℹ️ 小型模型 - 快速响应，资源消耗低")
        
        # 连接状态检查
        st.subheader("🔗 连接状态")
        if st.button("检查连接状态", use_container_width=True):
            with st.spinner("检查连接中..."):
                db_status, llm_status, error_msg = query_engine.test_connections()
                
                if db_status:
                    st.success("✅ 数据库连接正常")
                else:
                    st.error("❌ 数据库连接失败")
                
                if llm_status:
                    st.success("✅ LLM模型连接正常")
                else:
                    st.error("❌ LLM模型连接失败")
                
                if error_msg:
                    st.error(f"错误详情: {error_msg}")
        
        # 数据库Schema信息
        st.subheader("📊 数据库Schema")
        show_database_schema()
        
        return model_name


def show_database_schema():
    """显示数据库Schema信息表格"""
    # 显示视图选择器
    view_mode = st.selectbox(
        "选择显示模式",
        options=["分表显示", "选择单表"],
        index=0,
        help="选择如何显示数据库表结构信息"
    )
    
    if view_mode == "分表显示":
        show_all_tables_separately()
    else:  # 选择单表
        show_single_table_selector()


def show_all_tables_separately():
    """分别显示每个表的结构"""
    st.write("**📋 数据库表结构详情**")
    
    # 为每个表创建独立的表格
    for table_name, columns in TABLE_COLUMNS.items():
        with st.expander(f"📊 {table_name} 表", expanded=False):
            # 创建该表的数据
            table_data = []
            for i, column in enumerate(columns, 1):
                data_type = infer_column_type(column)
                table_data.append({
                    "序号": i,
                    "列名": column,
                    "数据类型": data_type,
                    "说明": get_column_description(column)
                })
            
            # 创建DataFrame并显示
            df = pd.DataFrame(table_data)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=min(250, len(table_data) * 35 + 50)
            )
            
            # 显示表统计信息 - 使用小字体
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div style="text-align: center;"><p style="font-size: 12px; color: #666; margin: 0;">列数</p><p style="font-size: 18px; font-weight: bold; margin: 0;">{len(columns)}</p></div>', unsafe_allow_html=True)
            with col2:
                # 统计不同数据类型的数量
                type_counts = {}
                for column in columns:
                    dtype = infer_column_type(column)
                    type_counts[dtype] = type_counts.get(dtype, 0) + 1
                most_common_type = max(type_counts, key=type_counts.get) if type_counts else "N/A"
                st.markdown(f'<div style="text-align: center;"><p style="font-size: 12px; color: #666; margin: 0;">主要类型</p><p style="font-size: 18px; font-weight: bold; margin: 0;">{most_common_type}</p></div>', unsafe_allow_html=True)
            with col3:
                # 统计ID字段数量
                id_count = sum(1 for col in columns if col.lower().endswith('id'))
                st.markdown(f'<div style="text-align: center;"><p style="font-size: 12px; color: #666; margin: 0;">ID字段</p><p style="font-size: 18px; font-weight: bold; margin: 0;">{id_count}</p></div>', unsafe_allow_html=True)
            
            # 添加快速查询示例
            if st.button(f"查看 {table_name} 查询示例", key=f"examples_{table_name}", use_container_width=True):
                show_table_query_examples_inline(table_name)


def show_single_table_selector():
    """单表选择器模式"""
    selected_table = st.selectbox(
        "选择表查看详细信息",
        options=list(TABLE_COLUMNS.keys()),
        index=0,
        help="选择特定表查看其列信息"
    )
    
    if selected_table:
        st.write(f"**📊 {selected_table} 表结构详情**")
        
        # 创建该表的数据
        columns = TABLE_COLUMNS[selected_table]
        table_data = []
        for i, column in enumerate(columns, 1):
            data_type = infer_column_type(column)
            table_data.append({
                "序号": i,
                "列名": column,
                "数据类型": data_type,
                "说明": get_column_description(column)
            })
        
        # 显示表格
        df = pd.DataFrame(table_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=min(400, len(table_data) * 35 + 50)
        )
        
        # 显示统计信息 - 使用小字体
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div style="text-align: center;"><p style="font-size: 12px; color: #666; margin: 0;">总列数</p><p style="font-size: 18px; font-weight: bold; margin: 0;">{len(columns)}</p></div>', unsafe_allow_html=True)
        with col2:
            id_count = sum(1 for col in columns if col.lower().endswith('id'))
            st.markdown(f'<div style="text-align: center;"><p style="font-size: 12px; color: #666; margin: 0;">ID字段</p><p style="font-size: 18px; font-weight: bold; margin: 0;">{id_count}</p></div>', unsafe_allow_html=True)
        with col3:
            date_count = sum(1 for col in columns if any(keyword in col.lower() for keyword in ['date', 'time']))
            st.markdown(f'<div style="text-align: center;"><p style="font-size: 12px; color: #666; margin: 0;">日期字段</p><p style="font-size: 18px; font-weight: bold; margin: 0;">{date_count}</p></div>', unsafe_allow_html=True)
        with col4:
            text_count = sum(1 for col in columns if infer_column_type(col) in ['TEXT', 'VARCHAR(255)', 'VARCHAR(100)'])
            st.markdown(f'<div style="text-align: center;"><p style="font-size: 12px; color: #666; margin: 0;">文本字段</p><p style="font-size: 18px; font-weight: bold; margin: 0;">{text_count}</p></div>', unsafe_allow_html=True)
        
        # 显示查询示例
        with st.expander(f"💡 {selected_table} 查询示例", expanded=True):
            show_table_query_examples(selected_table)



def get_column_description(column_name):
    """根据列名生成描述"""
    column_lower = column_name.lower()
    
    # 常见字段描述
    descriptions = {
        'id': '主键标识符',
        'customerid': '客户ID',
        'employeeid': '员工ID', 
        'productid': '产品ID',
        'salesorderid': '销售订单ID',
        'supplierid': '供应商ID',
        'firstname': '名字',
        'lastname': '姓氏',
        'email': '电子邮箱',
        'phone': '电话号码',
        'address': '地址信息',
        'city': '城市',
        'state': '州/省',
        'zipcode': '邮政编码',
        'country': '国家',
        'birthdate': '出生日期',
        'hiredate': '入职日期',
        'salary': '薪资',
        'position': '职位',
        'department': '部门',
        'isactive': '是否激活',
        'customersince': '成为客户时间',
        'productname': '产品名称',
        'description': '描述信息',
        'unitprice': '单价',
        'stockquantity': '库存数量',
        'reorderlevel': '补货水平',
        'discontinued': '是否停产',
        'categoryid': '分类ID',
        'orderdate': '订单日期',
        'requireddate': '要求日期',
        'shippeddate': '发货日期',
        'freight': '运费',
        'shipname': '收货人',
        'shipaddress': '收货地址',
        'status': '状态',
        'ispaid': '是否已付款',
        'quantity': '数量',
        'discount': '折扣',
        'totalprice': '总价',
        'changedate': '变更日期',
        'quantitychange': '数量变更',
        'reason': '原因',
        'companyname': '公司名称',
        'contactname': '联系人姓名',
        'contacttitle': '联系人职位',
        'fax': '传真',
        'homepage': '主页',
        'comments': '备注',
        'paymentmethod': '支付方式'
    }
    
    # 直接匹配
    if column_lower in descriptions:
        return descriptions[column_lower]
    
    # 模糊匹配
    for key, desc in descriptions.items():
        if key in column_lower:
            return desc
    
    # 根据类型推断
    if column_lower.endswith('id'):
        return '标识符'
    elif 'date' in column_lower or 'time' in column_lower:
        return '日期时间'
    elif 'name' in column_lower:
        return '名称'
    elif 'price' in column_lower or 'amount' in column_lower:
        return '金额'
    elif 'quantity' in column_lower:
        return '数量'
    elif column_lower.startswith('is'):
        return '布尔标志'
    
    return '数据字段'


def get_dominant_type(columns):
    """获取表中的主要数据类型"""
    type_counts = {}
    for column in columns:
        dtype = infer_column_type(column)
        type_counts[dtype] = type_counts.get(dtype, 0) + 1
    
    if not type_counts:
        return "N/A"
    
    return max(type_counts, key=type_counts.get)


def show_table_query_examples_inline(table_name):
    """在当前位置显示查询示例"""
    examples = {
        "Customer": [
            "SELECT * FROM Customer WHERE IsActive = 1;",
            "SELECT FirstName, LastName, Email FROM Customer;",
            "SELECT COUNT(*) FROM Customer WHERE CustomerSince >= '2024-01-01';"
        ],
        "Employee": [
            "SELECT * FROM Employee ORDER BY Salary DESC LIMIT 10;",
            "SELECT Position, AVG(Salary) FROM Employee GROUP BY Position;",
            "SELECT * FROM Employee WHERE HireDate >= '2024-01-01';"
        ],
        "Product": [
            "SELECT * FROM Product WHERE StockQuantity < ReorderLevel;",
            "SELECT ProductName, UnitPrice FROM Product WHERE UnitPrice > 100;",
            "SELECT * FROM Product WHERE Discontinued = 0;"
        ],
        "SalesOrder": [
            "SELECT * FROM SalesOrder WHERE Status = 'Completed';",
            "SELECT COUNT(*) FROM SalesOrder WHERE IsPaid = 1;",
            "SELECT * FROM SalesOrder WHERE OrderDate >= CURDATE() - INTERVAL 30 DAY;"
        ],
        "LineItem": [
            "SELECT SalesOrderID, SUM(TotalPrice) FROM LineItem GROUP BY SalesOrderID;",
            "SELECT ProductID, SUM(Quantity) FROM LineItem GROUP BY ProductID;",
            "SELECT * FROM LineItem WHERE Discount > 0;"
        ],
        "InventoryLog": [
            "SELECT * FROM InventoryLog WHERE ChangeDate >= CURDATE() - INTERVAL 7 DAY;",
            "SELECT ProductID, SUM(QuantityChange) FROM InventoryLog GROUP BY ProductID;",
            "SELECT * FROM InventoryLog WHERE QuantityChange < 0;"
        ],
        "Supplier": [
            "SELECT CompanyName, ContactName, Email FROM Supplier;",
            "SELECT * FROM Supplier WHERE Email IS NOT NULL;",
            "SELECT COUNT(*) FROM Supplier;"
        ]
    }
    
    table_examples = examples.get(table_name, [])
    
    if table_examples:
        st.write(f"**💡 {table_name} 表查询示例：**")
        for i, example in enumerate(table_examples, 1):
            st.code(example, language="sql")
            if st.button(f"使用示例 {i}", key=f"inline_example_{table_name}_{i}", use_container_width=True):
                st.session_state.sql_input = example
                st.success(f"已将示例SQL复制到查询框！")
    else:
        st.info("暂无查询示例")


def infer_column_type(column_name):
    """根据列名推断数据类型"""
    column_lower = column_name.lower()
    
    # ID类型
    if column_lower.endswith('id'):
        return "INT"
    
    # 日期类型
    if any(keyword in column_lower for keyword in ['date', 'time']):
        return "DATE/DATETIME"
    
    # 布尔类型
    if column_lower.startswith('is') or column_lower in ['active', 'paid', 'discontinued']:
        return "TINYINT(BOOL)"
    
    # 数值类型
    if any(keyword in column_lower for keyword in ['price', 'salary', 'quantity', 'amount', 'discount']):
        return "DECIMAL"
    
    # 文本类型
    if any(keyword in column_lower for keyword in ['description', 'address', 'comments', 'notes']):
        return "TEXT"
    
    # 邮箱
    if 'email' in column_lower:
        return "VARCHAR(255)"
    
    # 电话
    if 'phone' in column_lower:
        return "VARCHAR(20)"
    
    # 名称类型
    if any(keyword in column_lower for keyword in ['name', 'title', 'position', 'status', 'method']):
        return "VARCHAR(100)"
    
    # 默认
    return "VARCHAR(255)"


def show_table_query_examples(table_name):
    """显示特定表的查询示例"""
    examples = {
        "Customer": [
            "SELECT * FROM Customer WHERE IsActive = 1;",
            "SELECT FirstName, LastName, Email FROM Customer;",
            "SELECT COUNT(*) FROM Customer WHERE CustomerSince >= '2024-01-01';"
        ],
        "Employee": [
            "SELECT * FROM Employee ORDER BY Salary DESC LIMIT 10;",
            "SELECT Position, AVG(Salary) FROM Employee GROUP BY Position;",
            "SELECT * FROM Employee WHERE HireDate >= '2024-01-01';"
        ],
        "Product": [
            "SELECT * FROM Product WHERE StockQuantity < ReorderLevel;",
            "SELECT ProductName, UnitPrice FROM Product WHERE UnitPrice > 100;",
            "SELECT * FROM Product WHERE Discontinued = 0;"
        ],
        "SalesOrder": [
            "SELECT * FROM SalesOrder WHERE Status = 'Completed';",
            "SELECT COUNT(*) FROM SalesOrder WHERE IsPaid = 1;",
            "SELECT * FROM SalesOrder WHERE OrderDate >= CURDATE() - INTERVAL 30 DAY;"
        ],
        "LineItem": [
            "SELECT SalesOrderID, SUM(TotalPrice) FROM LineItem GROUP BY SalesOrderID;",
            "SELECT ProductID, SUM(Quantity) FROM LineItem GROUP BY ProductID;",
            "SELECT * FROM LineItem WHERE Discount > 0;"
        ],
        "InventoryLog": [
            "SELECT * FROM InventoryLog WHERE ChangeDate >= CURDATE() - INTERVAL 7 DAY;",
            "SELECT ProductID, SUM(QuantityChange) FROM InventoryLog GROUP BY ProductID;",
            "SELECT * FROM InventoryLog WHERE QuantityChange < 0;"
        ],
        "Supplier": [
            "SELECT CompanyName, ContactName, Email FROM Supplier;",
            "SELECT * FROM Supplier WHERE Email IS NOT NULL;",
            "SELECT COUNT(*) FROM Supplier;"
        ]
    }
    
    table_examples = examples.get(table_name, [])
    
    if table_examples:
        for i, example in enumerate(table_examples, 1):
            st.code(example, language="sql")
            if st.button(f"使用示例 {i}", key=f"example_{table_name}_{i}", use_container_width=True):
                st.session_state.sql_input = example
                st.success(f"已将示例SQL复制到查询框！")
    else:
        st.info("暂无查询示例")


def show_query_examples():
    """显示查询示例"""
    st.subheader("📝 查询示例")
    
    examples = [
        "查询所有用户的信息",
        "统计每个部门的员工数量",
        "查找工资最高的前10名员工",
        "查询最近一个月的订单数据",
        "统计各产品类别的销售额"
    ]
    
    cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with cols[i]:
            if st.button(example, key=f"example_{i}", use_container_width=True):
                st.session_state.user_input = example


def show_sql_cleaner():
    """显示SQL清理测试工具"""
    with st.expander("🧹 SQL清理测试工具", expanded=False):
        st.write("测试SQL查询清理功能")
        
        test_sql = st.text_area(
            "输入需要清理的SQL",
            placeholder="粘贴包含格式问题的SQL查询...",
            height=100
        )
        
        if st.button("清理SQL", key="clean_sql"):
            if test_sql:
                cleaned = query_engine.sql_processor.clean_sql_query(test_sql)
                st.subheader("清理结果:")
                st.code(cleaned, language="sql")
            else:
                st.warning("请输入SQL查询")


def main_query_interface(model_name):
    """主查询界面"""
    st.title("🔍 SQL智能助手")
    st.markdown("输入自然语言问题或直接输入SQL查询，我将帮您查询数据库。")
    
    # 查询方式选择
    query_mode = st.radio(
        "选择查询方式:",
        ["自然语言查询", "直接SQL查询"],
        horizontal=True
    )
    
    # 用户输入
    if query_mode == "自然语言查询":
        user_input = st.text_area(
            "请输入您的问题:",
            value=st.session_state.get('user_input', ''),
            placeholder="例如：查询所有用户的姓名和邮箱",
            height=100,
            key="natural_language_input"
        )
    else:
        user_input = st.text_area(
            "请输入SQL查询:",
            placeholder="例如：SELECT name, email FROM users;",
            height=100,
            key="sql_input"
        )
    
    # 结果显示格式选择
    display_format = st.radio(
        "结果显示格式:",
        ["表格", "原始"],
        horizontal=True,
        help="表格格式：结构化显示；原始格式：显示原始查询结果"
    )
    
    # 查询按钮
    col1, col2 = st.columns([1, 4])
    with col1:
        query_button = st.button("🔍 执行查询", type="primary", use_container_width=True)
    
    # 执行查询
    if query_button and user_input.strip():
        if query_mode == "自然语言查询":
            success, result, sql_query, error_msg = query_engine.execute_natural_language_query(
                user_input, model_name
            )
        else:
            success, result, sql_query, error_msg = query_engine.execute_direct_sql_query(
                user_input
            )
        
        # 显示结果
        if success:
            # 显示生成的SQL（仅自然语言查询）
            if query_mode == "自然语言查询":
                st.subheader("🔧 生成的SQL查询")
                st.code(sql_query, language="sql")
            
            # 显示查询结果
            query_engine.format_and_display_result(result, sql_query, display_format)
            
        else:
            st.error(f"查询失败: {error_msg}")
            if sql_query:
                st.subheader("生成的SQL查询")
                st.code(sql_query, language="sql")
    
    elif query_button:
        st.warning("请输入查询内容")


def show_usage_instructions():
    """显示使用说明"""
    with st.expander("📖 使用说明", expanded=False):
        st.markdown("""
        ### 🔍 SQL智能助手使用指南
        
        #### 🤖 自然语言查询
        - 直接用中文描述您想要查询的内容
        - 例如："查询所有用户的姓名和邮箱"
        - 系统会自动生成对应的SQL查询并执行
        
        #### 💻 直接SQL查询
        - 直接输入标准的SQL查询语句
        - 支持SELECT、INSERT、UPDATE、DELETE等操作
        - 系统会自动清理和优化您的SQL语句
        
        #### 📊 结果显示
        - **表格格式**: 以结构化表格形式显示结果，支持下载CSV
        - **原始格式**: 显示数据库返回的原始结果
        
        #### 🔧 功能特性
        - ✅ 智能SQL生成和清理
        - ✅ 多种显示格式支持
        - ✅ 连接状态实时检查
        - ✅ 查询结果导出功能
        - ✅ 表结构信息查看
        
        #### ⚠️ 注意事项
        - 请确保数据库和LLM模型连接正常
        - 复杂查询可能需要更长的处理时间
        - 建议先在测试环境中验证查询结果
        """)


def show_footer():
    """显示页脚"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>🔍 SQL智能助手 | 基于Ollama和LangChain构建</p>
            <p>💡 支持自然语言转SQL查询 | 🚀 提升数据查询效率</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """主函数"""
    # 初始化session state
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''
    
    # 设置页面配置
    setup_page_config()
    
    # 设置侧边栏并获取模型选择
    model_name = setup_sidebar()
    
    # 主界面
    show_query_examples()
    show_sql_cleaner()
    main_query_interface(model_name)
    show_usage_instructions()
    show_footer()


if __name__ == "__main__":
    main()