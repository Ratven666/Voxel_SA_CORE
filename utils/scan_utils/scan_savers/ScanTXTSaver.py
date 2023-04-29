from utils.scan_utils.scan_savers.ScanSaverABC import ScanSaverABC


class ScanTXTSaver(ScanSaverABC):

    def save_scan(self, scan, file_name):
        if file_name is None:
            file_name = f"src/{scan.scan_name}.txt"
        with open(file_name, "w", encoding="UTF-8") as file:
            for point in scan:
                point_line = f"{point.X} {point.Y} {point.Z} {point.R} {point.G} {point.B}\n"
                file.write(point_line)
        self.logger.info(f"Сохранение скана {scan} в файл {file_name} завершено")
