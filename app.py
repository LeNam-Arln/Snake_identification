import sys
import torch
import timm
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
import os

# ===== Cấu hình =====
IMG_SIZE = 224
NUM_CLASSES = 5
CLASS_NAMES = ['ran_cap_nong','ran_ho_mang', 'ran_luc_duoi_do', 'ran_nuoc','ran_rao_trau' ]
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = "D:\Projects\Snake_identification\snake_classifier_efficientnetb0.pth"

# ===== Load model =====
def load_model():
    model = timm.create_model('efficientnet_b0', pretrained=False, num_classes=NUM_CLASSES)
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f" File '{MODEL_PATH}' không tồn tại.")
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model

model = load_model()

# ===== Transform ảnh =====
transform = A.Compose([
    A.Resize(IMG_SIZE, IMG_SIZE),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2()
])

# ===== Dự đoán =====
def predict(image: Image.Image):
    image = np.array(image.convert("RGB"))
    augmented = transform(image=image)
    image_tensor = augmented['image'].unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)[0]

    top_probs = probs.cpu().numpy()
    return top_probs

# ===== Giao diện =====
class SnakeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng Nhận diện Rắn")
        self.setGeometry(100, 100, 800, 500)

        # --- Widgets chính ---
        self.img_label = QLabel("📷 Ảnh đã chọn", self)
        self.img_label.setFixedSize(350, 350)
        self.img_label.setStyleSheet("border: 1px dashed gray")
        self.img_label.setScaledContents(True)

        self.result_label = QLabel("📊 Kết quả nhận diện", self)
        self.result_label.setStyleSheet("font-size: 14px;")
        self.result_label.setWordWrap(True)

        self.select_button = QPushButton("🖼 Chọn ảnh", self)
        self.select_button.clicked.connect(self.select_image)

        # --- Layout chia 2 cột ---
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        top_layout.addWidget(self.img_label)
        top_layout.addWidget(self.result_label)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.select_button)
        bottom_layout.addStretch()

        layout.addStretch()
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        layout.addStretch()

        self.setLayout(layout)
        self.current_image = None

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh rắn", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.current_image = Image.open(file_path)
            self.img_label.setPixmap(QPixmap(file_path).scaled(350, 350))

            probs = predict(self.current_image)
            result_text = "<b>Kết quả nhận diện:</b><br><ul>"
            for i, p in enumerate(probs):
                result_text += f"<li>{CLASS_NAMES[i]}: {p*100:.2f}%</li>"
            result_text += "</ul>"

            self.result_label.setText(result_text)

# ===== Khởi chạy =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SnakeApp()
    win.show()
    sys.exit(app.exec_())
