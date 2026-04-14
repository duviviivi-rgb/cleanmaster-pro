from flask import Blueprint, request, jsonify
import os
import ezdxf
import PyPDF2

bp = Blueprint('parse', __name__, url_prefix='/api')

@bp.route('/parse', methods=['POST'])
def parse_files():
    """解析图纸文件，提取文字和图形信息"""
    try:
        data = request.json
        file_paths = data.get('file_paths', [])
        
        if not file_paths:
            return jsonify({
                "success": False,
                "error": "请提供文件路径"
            })
        
        results = []
        for file_path in file_paths:
            if not os.path.exists(file_path):
                results.append({
                    "file_path": file_path,
                    "error": "文件不存在"
                })
                continue
            
            file_ext = os.path.splitext(file_path)[1].lower()
            texts = []
            notes = []
            drawing_info = {
                "name": os.path.basename(file_path),
                "number": "",
                "format": file_ext[1:].upper(),
                "software": ""
            }
            
            if file_ext in ['.dwg', '.dxf']:
                try:
                    doc = ezdxf.readfile(file_path)
                    modelspace = doc.modelspace()
                    
                    # 提取文字
                    for entity in modelspace:
                        if entity.dxftype() == 'TEXT' or entity.dxftype() == 'MTEXT':
                            texts.append(entity.dxf.text)
                    
                    drawing_info["software"] = "AutoCAD"
                except Exception as e:
                    notes.append(f"解析错误: {str(e)}")
            
            elif file_ext == '.pdf':
                try:
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        for page_num in range(len(reader.pages)):
                            page = reader.pages[page_num]
                            text = page.extract_text()
                            if text:
                                texts.extend(text.split('\n'))
                    
                    drawing_info["software"] = "PDF Reader"
                except Exception as e:
                    notes.append(f"解析错误: {str(e)}")
            
            else:
                notes.append("不支持的文件格式")
            
            results.append({
                "file_path": file_path,
                "texts": texts,
                "notes": notes,
                "drawing_info": drawing_info
            })
        
        return jsonify({
            "success": True,
            "data": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
