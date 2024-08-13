import filetype
import aiofiles
import asyncio
from database.connect import execute_query
from rag.utils import logger


async def process_single_file(file, username):
    async with aiofiles.open(file, 'rb') as f:
        kind = filetype.guess(await f.read()).mime
    logger.info(f"receive {file.filename}, and file type is {kind}")
    
    await execute_query(
            "INSERT INTO uploads (username, type, file_name, status) VALUES (?, ?, ?, 'pending')",
            (username, file.type, file.filename)
        )
    
    if kind == 'application/pdf':
        # 处理 PDF 文件的逻辑
        logger.info(f"Processing PDF: {file.filename}")
        # await process_pdf(file)
        
    elif kind == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        # 处理 Word 文件的逻辑
        logger.info(f"Processing Word document: {file.filename}")
        # await process_word(file)
        
    elif kind == 'image/jpeg':
        # 处理 JPEG 图片的逻辑
        logger.info(f"Processing JPEG image: {file.filename}")
        # await process_image(file)
    
    else:
        logger.warning(f"Unsupported file type: {kind}")


async def processFile(file, username):
    task = process_single_file(file, username)
    await asyncio.gather(task)


