# import fitz
# import layoutparser as lp

# def pdf_to_high_res_images(pdf_path, output, zoom_x, zoom_y):
#     """
#     将 PDF 的每一页转换为高分辨率图像。
    
#     :param pdf_path: PDF 文件路径
#     :param output_folder: 图像输出文件夹
#     :param zoom_x: X 方向的缩放比例
#     :param zoom_y: Y 方向的缩放比例
#     """
    
#     doc = fitz.open(pdf_path)

#     for page_num in range(doc.page_count):
#         page = doc.load_page(page_num)

#         #设置生成图片的DPI
#         matrix = fitz.Matrix(zoom_x, zoom_y)
#         pix = page.get_pixmap(matrix=matrix) #pil Image
        
        
        
# import fitz
# import base64
# import io

# def handle_pdf_stream(data):
#     pdf_data = base64.b64decode(data)
#     pdf_stream = 
        
        