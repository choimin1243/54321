import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox
from PyPDF2 import PdfMerger

class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_files = []

    def initUI(self):
        self.setWindowTitle('PDF 병합 프로그램 (Vibe Coding)')
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('PDF 파일들을 선택해주세요.', self)
        layout.addWidget(self.label)

        btn_select = QPushButton('PDF 파일 선택', self)
        btn_select.clicked.connect(self.showFileDialog)
        layout.addWidget(btn_select)

        btn_merge = QPushButton('하나로 합치기', self)
        btn_merge.clicked.connect(self.mergePDFs)
        layout.addWidget(btn_merge)

        self.setLayout(layout)

    def showFileDialog(self):
        # 여러 파일 선택 가능하도록 설정
        files, _ = QFileDialog.getOpenFileNames(self, "PDF 파일 선택", "", "PDF Files (*.pdf)")
        if files:
            self.selected_files = files
            self.label.setText(f'{len(files)}개의 파일이 선택됨')

    def mergePDFs(self):
        if not self.selected_files:
            QMessageBox.warning(self, "경고", "먼저 PDF 파일을 선택하세요!")
            return

        # 저장할 파일 경로 선택
        save_path, _ = QFileDialog.getSaveFileName(self, "결과 저장", "merged_result.pdf", "PDF Files (*.pdf)")
        
        if save_path:
            try:
                merger = PdfMerger()
                for pdf in self.selected_files:
                    merger.append(pdf)
                merger.write(save_path)
                merger.close()
                QMessageBox.information(self, "성공", "PDF 병합이 완료되었습니다!")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"에러 발생: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFMergerApp()
    ex.show()
    sys.exit(app.exec_())