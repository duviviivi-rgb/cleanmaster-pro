from flask import Blueprint, request, jsonify
import os
import datetime

bp = Blueprint('generate', __name__, url_prefix='/api')

def generate_html_report(data):
    """生成HTML格式报告"""
    project_name = data.get('project_name', '未知项目')
    floors = data.get('floors', [])
    
    generated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total_materials = 0
    floor_count = len(floors)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>检验批容量与隐蔽工程报告</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 40px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
            }
            .info {
                margin-bottom: 30px;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 5px;
            }
            .info p {
                margin: 5px 0;
            }
            h2 {
                color: #333;
                margin-top: 40px;
                margin-bottom: 20px;
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
            }
            h3 {
                color: #555;
                margin-top: 30px;
                margin-bottom: 15px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .section {
                margin-bottom: 40px;
            }
            .footer {
                margin-top: 50px;
                text-align: center;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>检验批容量与隐蔽工程报告</h1>
            <div class="info">
                <p><strong>项目名称：</strong>{project_name}</p>
                <p><strong>生成时间：</strong>{generated_at}</p>
                <p><strong>楼层数量：</strong>{floor_count}</p>
                <p><strong>材料总数：</strong>{total_materials}</p>
            </div>
    """
    
    html = html.format(
        project_name=project_name,
        generated_at=generated_at,
        floor_count=floor_count,
        total_materials=total_materials
    )
    
    for floor in floors:
        floor_name = floor.get('floor', '未知楼层')
        drawings = floor.get('drawings', [])
        
        html += f"""
            <div class="section">
                <h2>楼层：{floor_name}</h2>
        """
        
        for drawing in drawings:
            drawing_number = drawing.get('drawing_number', '未知图号')
            drawing_name = drawing.get('drawing_name', '未知图纸名称')
            materials = drawing.get('materials', [])
            total_materials += len(materials)
            
            html += f"""
                <h3>图纸：{drawing_number} - {drawing_name}</h3>
                <table>
                    <thead>
                        <tr>
                            <th>材料名称</th>
                            <th>型号</th>
                            <th>数量</th>
                            <th>单位</th>
                            <th>位置</th>
                            <th>分类</th>
                            <th>检验批</th>
                            <th>标准</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for material in materials:
                html += f"""
                        <tr>
                            <td>{material.get('name', '')}</td>
                            <td>{material.get('model', '')}</td>
                            <td>{material.get('quantity', 0)}</td>
                            <td>{material.get('unit', '')}</td>
                            <td>{material.get('position', '')}</td>
                            <td>{material.get('category', '')}</td>
                            <td>{material.get('inspection_batch', '')}</td>
                            <td>{material.get('standard', '')}</td>
                        </tr>
                """
            
            html += """
                    </tbody>
                </table>
            """
        
        html += """
            </div>
        """
    
    html += f"""
            <div class="section">
                <h2>隐蔽工程检查内容</h2>
                <p>根据提取的材料信息，以下是隐蔽工程检查内容：</p>
                <ul>
                    <li>管道安装：检查管道材质、规格、连接方式是否符合设计要求</li>
                    <li>电气线路：检查线路敷设、接地装置是否符合规范</li>
                    <li>通风空调：检查风管安装、保温措施是否到位</li>
                    <li>医疗气体：检查气体管道安装、压力测试是否合格</li>
                </ul>
            </div>
            <div class="footer">
                <p>报告生成时间：{generated_at}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def generate_markdown_report(data):
    """生成Markdown格式报告"""
    project_name = data.get('project_name', '未知项目')
    floors = data.get('floors', [])
    generated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total_materials = 0
    
    markdown = f"""
# 检验批容量与隐蔽工程报告

## 项目信息
- **项目名称：** {project_name}
- **生成时间：** {generated_at}
- **楼层数量：** {len(floors)}
- **材料总数：** {total_materials}

    """
    
    for floor in floors:
        floor_name = floor.get('floor', '未知楼层')
        drawings = floor.get('drawings', [])
        
        markdown += f"""
## 楼层：{floor_name}

        """
        
        for drawing in drawings:
            drawing_number = drawing.get('drawing_number', '未知图号')
            drawing_name = drawing.get('drawing_name', '未知图纸名称')
            materials = drawing.get('materials', [])
            total_materials += len(materials)
            
            markdown += f"""
### 图纸：{drawing_number} - {drawing_name}

| 材料名称 | 型号 | 数量 | 单位 | 位置 | 分类 | 检验批 | 标准 |
|----------|------|------|------|------|------|--------|------|
            """
            
            for material in materials:
                markdown += f"""
| {material.get('name', '')} | {material.get('model', '')} | {material.get('quantity', 0)} | {material.get('unit', '')} | {material.get('position', '')} | {material.get('category', '')} | {material.get('inspection_batch', '')} | {material.get('standard', '')} |
                """
    
    markdown += f"""

## 隐蔽工程检查内容

根据提取的材料信息，以下是隐蔽工程检查内容：

- 管道安装：检查管道材质、规格、连接方式是否符合设计要求
- 电气线路：检查线路敷设、接地装置是否符合规范
- 通风空调：检查风管安装、保温措施是否到位
- 医疗气体：检查气体管道安装、压力测试是否合格
    """
    
    return markdown

@bp.route('/generate', methods=['POST'])
def generate_report():
    """生成检验批容量和隐蔽工程报告"""
    try:
        data = request.json
        report_data = data.get('data', {})
        format = data.get('format', 'html')
        
        if not report_data:
            return jsonify({
                "success": False,
                "error": "请提供报告数据"
            })
        
        # 生成报告
        if format == 'html':
            content = generate_html_report(report_data)
            file_ext = 'html'
        elif format == 'markdown':
            content = generate_markdown_report(report_data)
            file_ext = 'md'
        else:
            return jsonify({
                "success": False,
                "error": "不支持的格式"
            })
        
        # 保存报告文件
        output_dir = os.path.join(os.getcwd(), 'reports')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        file_name = f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
        file_path = os.path.join(output_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            "success": True,
            "data": {
                "content": content,
                "file_path": file_path
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
