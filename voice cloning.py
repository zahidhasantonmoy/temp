# app.py
# Requirements: PyQt6, torch, ffmpeg in PATH, your chosen VC engine (RVC/so-vits-svc) wrapped as `engine`
# This is a skeleton; fill engine functions per your chosen repo's API/CLI.

import sys, os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox
)

class VCApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Voice Conversion")
        self.target_path = ""
        self.source_path = ""
        self.output_dir = ""
        self.model_path = ""
        self.init_ui()

    def init_ui(self):
        self.lbl_target = QLabel("Target voice (folder/file):")
        self.txt_target = QLineEdit()
        self.btn_target = QPushButton("Browse")
        self.btn_target.clicked.connect(self.pick_target)

        self.lbl_source = QLabel("Source voice (file):")
        self.txt_source = QLineEdit()
        self.btn_source = QPushButton("Browse")
        self.btn_source.clicked.connect(self.pick_source)

        self.lbl_out = QLabel("Output folder:")
        self.txt_out = QLineEdit()
        self.btn_out = QPushButton("Browse")
        self.btn_out.clicked.connect(self.pick_out)

        self.lbl_model = QLabel("Model (.pth/.json):")
        self.txt_model = QLineEdit()
        self.btn_model = QPushButton("Browse")
        self.btn_model.clicked.connect(self.pick_model)

        self.btn_train = QPushButton("Train model from target")
        self.btn_train.clicked.connect(self.train_model)

        self.btn_convert = QPushButton("Convert source → target voice")
        self.btn_convert.clicked.connect(self.convert_audio)

        grid1 = QHBoxLayout(); grid1.addWidget(self.txt_target); grid1.addWidget(self.btn_target)
        grid2 = QHBoxLayout(); grid2.addWidget(self.txt_source); grid2.addWidget(self.btn_source)
        grid3 = QHBoxLayout(); grid3.addWidget(self.txt_out); grid3.addWidget(self.btn_out)
        grid4 = QHBoxLayout(); grid4.addWidget(self.txt_model); grid4.addWidget(self.btn_model)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_target); layout.addLayout(grid1)
        layout.addWidget(self.lbl_source); layout.addLayout(grid2)
        layout.addWidget(self.lbl_out); layout.addLayout(grid3)
        layout.addWidget(self.lbl_model); layout.addLayout(grid4)
        layout.addWidget(self.btn_train); layout.addWidget(self.btn_convert)
        self.setLayout(layout)

    def pick_target(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dlg.setOption(QFileDialog.Option.DontUseNativeDialog, False)
        if dlg.exec():
            files = dlg.selectedFiles()
            self.target_path = files[0]
            self.txt_target.setText(self.target_path)

    def pick_source(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select source audio", "", "Audio Files (*.wav *.flac *.mp3)")
        if path:
            self.source_path = path
            self.txt_source.setText(path)

    def pick_out(self):
        path = QFileDialog.getExistingDirectory(self, "Select output directory")
        if path:
            self.output_dir = path
            self.txt_out.setText(path)

    def pick_model(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select model file (.pth/.json)", "", "Model Files (*.pth *.json)")
        if path:
            self.model_path = path
            self.txt_model.setText(path)

    def train_model(self):
        if not self.target_path:
            QMessageBox.warning(self, "Missing", "Pick target voice dataset/audio.")
            return
        # TODO: call your engine training here
        # Example placeholder:
        # engine.train(dataset=self.target_path, out_dir="models/my_voice", sr=44100, epochs=50)
        QMessageBox.information(self, "Training", "Training started (placeholder). See console for logs.")

    def convert_audio(self):
        if not (self.source_path and self.output_dir):
            QMessageBox.warning(self, "Missing", "Pick source audio and output folder.")
            return
        # TODO: call your engine inference here
        # Example placeholder:
        # out_path = engine.convert(model_dir="models/my_voice", src=self.source_path, out_dir=self.output_dir, transpose=0)
        # QMessageBox.information(self, "Done", f"Saved: {out_path}")
        QMessageBox.information(self, "Conversion", "Conversion started (placeholder). See console for logs.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = VCApp()
    w.resize(700, 320)
    w.show()
    sys.exit(app.exec())
