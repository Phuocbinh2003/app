import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from PIL import Image

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
  
  # Hiển thị một lưới 10x9 ảnh từ bộ dữ liệu, xếp theo hàng từ 0 đến 9
  st.subheader("Một số hình ảnh từ MNIST Dataset")
  fig, axes = plt.subplots(10, 9, figsize=(10, 11))
  
  for row in range(10):
      count = 0
      for i in range(len(train_images)):
          if train_labels[i] == row:
              ax = axes[row, count]
              ax.imshow(train_images[i], cmap='gray')
              ax.axis('off')
              ax.set_title(str(train_labels[i]), fontsize=8)
              count += 1
              if count == 9:
                  break
  
  plt.tight_layout()
  st.pyplot(fig)
  st.header("Phần 2: Phương pháp")
   
  st.write("""
  Mô hình CNN (Convolutional Neural Network) được sử dụng để trích xuất đặc trưng và phân loại chữ số.
  """
  result_image = Image.open('Handwriting_Letter_Recognition/2dd5b8be-d455-4d5c-b2b0-9e706d9d893b.png')
  st.image(result_image, caption="Detection Result", use_column_width=True)      
  st.write("""         
  Kiến trúc mạng bao gồm:
  - **Convolution Layer**: Trích xuất đặc trưng từ ảnh đầu vào.
  - **MaxPooling Layer**: Giảm kích thước dữ liệu, giữ lại các đặc trưng quan trọng.
  - **Flatten Layer**: Chuyển đổi tensor nhiều chiều thành vector.
  - **Dense Layer**: Học và phân loại đặc trưng.
  """)
  st.write("""
  ### Kiến trúc chi tiết của mạng CNN:
  - **Input**: 28x28x1 (ảnh đầu vào dạng grayscale).
  - **Conv1**: 16 kernel kích thước 3x3, stride = 1.
    - **Chức năng**: Phát hiện các đặc trưng cơ bản như đường viền, cạnh.
    - **Lý do chọn**: Sử dụng kernel nhỏ (3x3) giúp giữ được chi tiết của ảnh.
  - **MaxPool1**: Kernel kích thước 2x2, stride = 2.
    - **Chức năng**: Giảm kích thước dữ liệu, tăng tốc độ tính toán.
    - **Lý do chọn**: Tăng tính bất biến đối với phép dịch chuyển và nhiễu.
  - **Conv2**: 32 kernel kích thước 3x3, stride = 1.
    - **Chức năng**: Trích xuất các đặc trưng phức tạp hơn từ các tầng trước.
    - **Lý do chọn**: Tăng số lượng kernel để học thêm nhiều đặc trưng chi tiết.
  - **MaxPool2**: Kernel kích thước 2x2, stride = 2.
    - **Chức năng**: Tiếp tục giảm kích thước dữ liệu, giữ lại các đặc trưng quan trọng.
    - **Lý do chọn**: Giảm độ phức tạp và tránh overfitting.
  - **Flatten**: Biến đổi tensor thành vector 1 chiều.
    - **Chức năng**: Chuẩn bị dữ liệu đầu vào cho tầng Fully Connected.
    - **Lý do chọn**: Đơn giản hóa việc xử lý dữ liệu.
  - **Dense**: 64 neuron với hàm kích hoạt ReLU.
    - **Chức năng**: Học các đặc trưng phi tuyến từ vector đầu vào.
    - **Lý do chọn**: Hàm ReLU giúp mạng hội tụ nhanh hơn và tránh vanishing gradient.
  - **Output**: 10 lớp tương ứng với các chữ số từ 0 đến 9.
    - **Chức năng**: Phân loại chữ số đầu ra.
    - **Lý do chọn**: Sử dụng softmax để đảm bảo tổng xác suất bằng 1, phù hợp với bài toán phân loại.
  """)
  st.header("Phần 3: Kết quả")
  # Dữ liệu mô phỏng accuracy và loss
  epochs = list(range(1, 21))
  accuracy = [0.8581, 0.9815, 0.9870, 0.9900, 0.9917, 0.9933, 0.9943, 0.9945, 0.9962, 0.9969, 0.9972, 0.9976, 0.9982, 0.9989, 0.9982, 0.9967, 0.9986, 0.9989, 0.9987, 0.9985]
  val_accuracy = [0.9815, 0.9858, 0.9866, 0.9901, 0.9913, 0.9896, 0.9892, 0.9910, 0.9896, 0.9886, 0.9891, 0.9897, 0.9903, 0.9876, 0.9890, 0.9909, 0.9903, 0.9911, 0.9899, 0.9913]
  loss = [0.4890, 0.0627, 0.0419, 0.0333, 0.0261, 0.0210, 0.0187, 0.0156, 0.0113, 0.0096, 0.0079, 0.0072, 0.0049, 0.0041, 0.0052, 0.0094, 0.0041, 0.0032, 0.0041, 0.0041]
  val_loss = [0.0596, 0.0448, 0.0409, 0.0316, 0.0256, 0.0323, 0.0330, 0.0281, 0.0368, 0.0347, 0.0388, 0.0406, 0.0352, 0.0495, 0.0451, 0.0378, 0.0401, 0.0428, 0.0442, 0.0420]
  
  # Tạo biểu đ
  fig, ax = plt.subplots(figsize=(10, 6))
  ax.plot(epochs, accuracy, label="Accuracy", marker='o')
  ax.plot(epochs, val_accuracy, label="Validation Accuracy", marker='o')
  ax.plot(epochs, loss, label="Loss", marker='o')
  ax.plot(epochs, val_loss, label="Validation Loss", marker='o')
  
  ax.set_title("Biểu đồ Accuracy và Loss", fontsize=16)
  ax.set_xlabel("Epochs", fontsize=14)
  ax.set_ylabel("Giá trị", fontsize=14)
  ax.legend()
  ax.grid(True)
  
  st.pyplot(fig)
  st.write("Test 1000 ảnh với mỗi ký tự với accuracy=0.9815 ")
  st.write("Ma trận nhầm lẫn là: ")
  result_image = Image.open('Handwriting_Letter_Recognition/download.png')
  st.image(result_image, caption="Detection Result", use_column_width=True)

if __name__ == "__main__":
    run_app11()
