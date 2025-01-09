import streamlit as st
from sklearn.datasets import make_classification
import numpy as np
import matplotlib.pyplot as plt


def app_ket_thuc():
  # Hàm tạo dữ liệu
  def generate_data(n_samples, n_features, n_classes, random_state):
      X, y = make_classification(
          n_samples=n_samples, 
          n_features=n_features, 
          n_informative=n_features, 
          n_redundant=0, 
          n_classes=n_classes, 
          random_state=random_state
      )
      return X, y
  
  # Tạo giao diện Streamlit
  st.title("Tạo dữ liệu 2D cho Logistic Regression")
  
  # Các tham số điều chỉnh
  n_samples = st.slider("Số lượng mẫu (n_samples)", min_value=50, max_value=1000, value=200, step=50)
  n_features = st.slider("Số lượng đặc trưng (n_features)", min_value=2, max_value=10, value=2)
  n_classes = st.slider("Số lớp (n_classes)", min_value=2, max_value=4, value=2)
  random_state = st.slider("Seed ngẫu nhiên (random_state)", min_value=0, max_value=100, value=42)
  
  # Sinh dữ liệu
  X, y = generate_data(n_samples, n_features, n_classes, random_state)
  
  # Hiển thị dữ liệu đã tạo
  st.subheader("Dữ liệu được tạo")
  fig, ax = plt.subplots()
  scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', edgecolor='k')
  ax.set_xlabel("Feature 1")
  ax.set_ylabel("Feature 2")
  ax.set_title("Tập dữ liệu")
  st.pyplot(fig)
  st.title("Giới thiệu Logistic Regression")




    
  # Tiêu đề chính
  st.title("Giới thiệu Logistic Regression")
  
  # Mở bài
  st.header("Bài toán phân loại")
  st.write("""
  Phân loại là một bài toán cơ bản trong học máy, nơi chúng ta dự đoán nhãn của một dữ liệu dựa trên các đặc trưng của nó. 
  Ví dụ, dự đoán liệu một email là spam hay không, hoặc dự đoán một bệnh nhân có mắc bệnh không dựa trên các chỉ số y tế.
  """)
  
  # Giới thiệu Linear Regression
  st.header("Linear Regression cho bài toán phân loại?")
  st.write("""
  Linear Regression là một trong những mô hình cơ bản nhất trong học máy. Nó dựa trên công thức:
  """)
  st.latex(r"y = w^T x + b")
  st.write("""
  Linear Regression phù hợp cho các bài toán hồi quy (dự đoán giá trị liên tục). Tuy nhiên, khi áp dụng vào bài toán phân loại, nó gặp nhiều hạn chế, như:
  """)
  st.markdown("- Giá trị đầu ra không bị giới hạn trong khoảng [0, 1].")
  st.markdown("- Khó xác định ranh giới quyết định rõ ràng giữa các lớp.")
  
  # Tạo dữ liệu minh họa
  st.subheader("Trực quan hóa Linear Regression")
  st.write("""
  Hãy xem ví dụ dưới đây: Chúng ta có một tập dữ liệu với hai lớp (0 và 1). Linear Regression cố gắng dự đoán giá trị liên tục \(y\), và sử dụng ngưỡng (ví dụ \(y=0.5\)) để phân loại.
  """)
  
  # Dữ liệu mô phỏng
  np.random.seed(42)
  class_0 = np.random.normal(2, 1, size=(30, 2))  # Dữ liệu lớp 0
  class_1 = np.random.normal(6, 1, size=(30, 2))  # Dữ liệu lớp 1
  X = np.vstack([class_0, class_1])
  y = np.array([0]*30 + [1]*30)
  
  # Huấn luyện Linear Regression
  from sklearn.linear_model import LinearRegression
  
  lr_model = LinearRegression()
  lr_model.fit(X, y)
  w, b = lr_model.coef_, lr_model.intercept_
  
  # Ranh giới quyết định
  x1_range = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 100)
  x2_range = -(w[0] * x1_range + b) / w[1]
  
  # Trực quan hóa
  fig, ax = plt.subplots(figsize=(8, 6))
  ax.scatter(class_0[:, 0], class_0[:, 1], color='blue', label="Lớp 0")
  ax.scatter(class_1[:, 0], class_1[:, 1], color='red', label="Lớp 1")
  ax.plot(x1_range, x2_range, color='green', label="Ranh giới quyết định (Linear Regression)")
  ax.axhline(0.5, color='orange', linestyle="--", label="Ngưỡng phân loại")
  ax.set_title("Linear Regression trên bài toán phân loại")
  ax.set_xlabel("Đặc trưng 1")
  ax.set_ylabel("Đặc trưng 2")
  ax.legend()
  st.pyplot(fig)
  
  # Dẫn dắt sang Logistic Regression
  st.header("Giới thiệu Logistic Regression")
  st.write("""
  Linear Regression không phù hợp cho bài toán phân loại vì:
  - Giá trị dự đoán không bị giới hạn trong khoảng [0, 1].
  - Không đảm bảo ý nghĩa xác suất.
  
  Do đó, Logistic Regression sử dụng hàm sigmoid để đưa giá trị đầu ra vào khoảng [0, 1]:
  """)
  st.latex(r"P(y=1|x) = \sigma(w^T x + b) = \frac{1}{1 + e^{-(w^T x + b)}}")
  st.write("""
  Ranh giới quyết định được xác định khi xác suất \(P(y=1|x) = 0.5\).
  """)
  


if __name__ == "__main__":
    app_ket_thuc()
