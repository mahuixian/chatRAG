import logging
import logging.handlers

class Logger:
    def __init__(self, log_file='application.log', console_output=True, max_file_size=5*1024*1024, backup_count=3, log_format=None):
        """
        初始化日志记录器
        :param log_file: 日志文件路径
        :param console_output: 是否输出到控制台 (默认: True)
        :param max_file_size: 日志文件的最大大小 (默认: 5MB)
        :param backup_count: 备份的日志文件数量 (默认: 3)
        :param log_format: 自定义日志格式 (默认: None)
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        if not log_format:
            log_format = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)

        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_file_size, backupCount=backup_count, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)


