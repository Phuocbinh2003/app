import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist


def run_app11():
  # Tiêu đề phần 1
  st.header("Phần 1: MNIST Dataset")

  # Mô tả về bộ dữ liệu
  st.write(
      """
      **MNIST** là một trong những bộ dữ liệu nổi tiếng và phổ biến nhất trong cộng đồng học máy, 
      đặc biệt là trong các nghiên cứu về nhận diện mẫu và phân loại hình ảnh.
  
      - Bộ dữ liệu bao gồm tổng cộng **70.000 ảnh chữ số viết tay** từ **0** đến **9**, 
        mỗi ảnh có kích thước **28 x 28 pixel**.
      - Chia thành:
        - **Training set**: 60.000 ảnh để huấn luyện.
        - **Test set**: 10.000 ảnh để kiểm tra.
      - Mỗi hình ảnh là một chữ số viết tay, được chuẩn hóa và chuyển thành dạng grayscale (đen trắng).
  
      Dữ liệu này được sử dụng rộng rãi để xây dựng các mô hình nhận diện chữ số.
      """
  )
  
  # Tải dữ liệu MNIST
  (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
  
  # Hiển thị một lưới 9x9 ảnh từ bộ dữ liệu
  st.subheader("Lưới 9x9 hình ảnh từ MNIST Dataset")
  fig, axes = plt.subplots(9, 9, figsize=(10, 10))
  indices = np.random.choice(len(train_images), size=81, replace=False)
  
  for i, ax in enumerate(axes.flatten()):
      ax.imshow(train_images[indices[i]], cmap='gray')
      ax.axis('off')
      ax.set_title(str(train_labels[indices[i]]), fontsize=8)
  
  plt.tight_layout()
  st.pyplot(fig)

if __name__ == "__main__":
    run_app11()