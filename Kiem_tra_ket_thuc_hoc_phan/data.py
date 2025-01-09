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
  
  # Trả về dữ liệu để sử dụng trong các phần sau
  st.write("Dữ liệu X:")
  st.write(X)
  st.write("Nhãn y:")
  st.write(y)
  
  # Lưu lại dữ liệu để dùng tiếp
  st.session_state['X'] = X
  st.session_state['y'] = y
