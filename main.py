#!/usr/bin/env python3
"""
办公自动化工具箱 - 安卓 App 主程序
KivyMD Material Design 界面
"""
import os
import sys
from pathlib import Path

from kivy.core.window import Window
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar

# 设置窗口大小（桌面调试用）
if platform != 'android':
    Window.size = (400, 700)


class MainScreen(MDBoxLayout):
    """主界面"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.md_bg_color = (0.12, 0.14, 0.17, 1)
        self.spacing = 15
        self.padding = [20, 10, 20, 10]
        
        # 顶部标题栏
        toolbar = MDTopAppBar(
            title="办公自动化工具箱",
            md_bg_color=(0.2, 0.6, 1.0, 1),
            specific_text_color=(1, 1, 1, 1)
        )
        self.add_widget(toolbar)
        
        # 功能按钮
        tools = [
            ("📊  Excel 合并", "excel_merge"),
            ("📊  Excel 拆分", "excel_split"),
            ("🧹  数据清洗", "excel_clean"),
            ("📄  PDF 提取文字", "pdf_extract"),
            ("📄  PDF 转 Word", "pdf_to_word"),
            ("🖼️  图片压缩", "image_compress"),
            ("🖼️  图片缩放", "image_resize"),
            ("📁  文件分类整理", "file_organize"),
        ]
        
        for text, tool_id in tools:
            btn = MDFlatButton(
                text=text,
                md_bg_color=(0.95, 0.95, 0.95, 1),
                size_hint_y=None,
                height=55,
                on_release=lambda x, t=tool_id: self.on_tool_click(t)
            )
            self.add_widget(btn)
        
        # 底部留白和版本号
        self.add_widget(MDBoxLayout())  # spacer
        
        version_label = MDLabel(
            text="你的品牌名称 v1.0",
            halign="center",
            theme_text_color="Hint"
        )
        self.add_widget(version_label)
    
    def on_tool_click(self, tool_id):
        """点击功能按钮"""
        if tool_id in ['excel_merge', 'excel_split', 'file_organize']:
            self.show_result(f"请选择文件后操作")
        else:
            # 弹出文件选择器
            self.open_file_picker(tool_id)
    
    def open_file_picker(self, tool_id):
        """打开文件选择器"""
        # Android 上使用 SAF 文件选择
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        
        from plyer import filechooser
        filechooser.open_file(on_selection=lambda x: self.on_file_selected(x, tool_id))
    
    def on_file_selected(self, selection, tool_id):
        """文件选择完成"""
        if not selection:
            return
        file_path = selection[0]
        result = self.execute_tool(tool_id, file_path)
        self.show_result(result)
    
    def execute_tool(self, tool_id, file_path):
        """执行工具"""
        try:
            if tool_id == 'excel_merge':
                return "请选择多个 Excel 文件合并"
            
            elif tool_id == 'excel_split':
                import pandas as pd
                df = pd.read_excel(file_path)
                col = df.columns[0]
                groups = df.groupby(col)
                out_dir = os.path.join(os.path.dirname(file_path), '拆分结果')
                os.makedirs(out_dir, exist_ok=True)
                for name, group in groups:
                    safe = str(name).replace('/', '_')[:30]
                    group.to_excel(os.path.join(out_dir, f"{safe}.xlsx"), index=False)
                return f"✅ 拆分完成！共 {len(groups)} 个文件\n保存至: {out_dir}"
            
            elif tool_id == 'excel_clean':
                import pandas as pd
                df = pd.read_excel(file_path)
                before = len(df)
                df = df.drop_duplicates().dropna(how='all')
                for col in df.select_dtypes(include=['object']).columns:
                    df[col] = df[col].str.strip()
                out = file_path.rsplit('.', 1)[0] + '_清洗后.xlsx'
                df.to_excel(out, index=False)
                return f"✅ 清洗完成!\n{before}行 → {len(df)}行\n保存至: {out}"
            
            elif tool_id == 'pdf_extract':
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = []
                    for page in reader.pages:
                        text.append(page.extract_text() or "")
                    out = file_path.rsplit('.', 1)[0] + '.txt'
                    with open(out, 'w', encoding='utf-8') as fw:
                        fw.write('\n'.join(text))
                return f"✅ 提取完成！共 {len(reader.pages)} 页\n保存至: {out}"
            
            elif tool_id == 'pdf_to_word':
                import PyPDF2
                from docx import Document
                doc = Document()
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        doc.add_paragraph(page.extract_text() or "")
                out = file_path.rsplit('.', 1)[0] + '.docx'
                doc.save(out)
                return f"✅ 转换完成！共 {len(reader.pages)} 页\n保存至: {out}"
            
            elif tool_id == 'image_compress':
                from PIL import Image
                img = Image.open(file_path)
                orig = os.path.getsize(file_path)
                out = file_path.rsplit('.', 1)[0] + '_压缩.jpg'
                img.save(out, 'JPEG', quality=60, optimize=True)
                new = os.path.getsize(out)
                return f"✅ 压缩完成!\n{orig//1024}KB → {new//1024}KB (省{(1-new/orig)*100:.0f}%)"
            
            elif tool_id == 'image_resize':
                from PIL import Image
                img = Image.open(file_path)
                w = img.size[0] // 2
                h = img.size[1] // 2
                img.resize((w, h), Image.LANCZOS).save(file_path.rsplit('.', 1)[0] + '_缩放.png')
                return f"✅ 缩放完成!\n{img.size[0]}x{img.size[1]} → {w}x{h}"
            
            elif tool_id == 'file_organize':
                folder = os.path.dirname(file_path)
                FILE_CATEGORIES = {
                    '文档': ['.doc', '.docx', '.xlsx', '.pdf', '.txt'],
                    '图片': ['.jpg', '.jpeg', '.png', '.gif'],
                    '代码': ['.py', '.js', '.html', '.css'],
                }
                import shutil
                stats = {}
                for f in os.listdir(folder):
                    fpath = os.path.join(folder, f)
                    if os.path.isdir(fpath): continue
                    ext = os.path.splitext(f)[1].lower()
                    for cat, exts in FILE_CATEGORIES.items():
                        if ext in exts:
                            os.makedirs(os.path.join(folder, cat), exist_ok=True)
                            shutil.move(fpath, os.path.join(folder, cat, f))
                            stats[cat] = stats.get(cat, 0) + 1
                            break
                return f"✅ 整理完成!\n" + '\n'.join([f"  {k}: {v}个" for k, v in stats.items()])
            
            return "功能开发中..."
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    def show_result(self, text):
        """显示结果弹窗"""
        dialog = MDDialog(
            title="执行结果",
            text=text,
            buttons=[MDFlatButton(text="确定", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


class OfficeApp(MDApp):
    """主 App 类"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "办公自动化工具箱"
        self.icon = "icon.png"
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        main_screen = MainScreen()
        return main_screen


if __name__ == '__main__':
    OfficeApp().run()
