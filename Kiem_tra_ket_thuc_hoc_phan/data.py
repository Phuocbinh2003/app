import streamlit as st
from sklearn.datasets import make_classification
import numpy as np
import matplotlib.pyplot as plt


def app_ket_thuc():
  # Hàm tạo dữ liệu
  def generate_data(n_samples, n_classes, random_state):
      X, y = make_classification(
          n_samples=n_samples, 
          n_features=2,
          n_informative=2,
          n_redundant=0, 
          n_classes=n_classes, 
          random_state=random_state
      )
      return X, y
  
  # Tạo giao diện Streamlit
  st.title("Tạo dữ liệu 2D cho Logistic Regression")
  
  # Các tham số điều chỉnh
  n_samples = st.slider("Số lượng mẫu (n_samples)", min_value=50, max_value=1000, value=200, step=50)
  
  n_classes = st.slider("Số lớp (n_classes)", min_value=2, max_value=4, value=2)
  random_state = st.slider("Seed ngẫu nhiên (random_state)", min_value=0, max_value=100, value=42)
  
  # Sinh dữ liệu
  X, y = generate_data(n_samples, n_classes, random_state)
  
  # Hiển thị dữ liệu đã tạo
  st.subheader("Dữ liệu được tạo")
  fig, ax = plt.subplots()
  scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', edgecolor='k')
  ax.set_xlabel("Feature 1")
  ax.set_ylabel("Feature 2")
  ax.set_title("Tập dữ liệu")
  st.pyplot(fig)
  st.title("Giới thiệu Logistic Regression")




    
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
  Trong đó:
  - \(x\) là vector đặc trưng.
  - \(w\) là vector trọng số.
  - \(b\) là hệ số tự do.
  
  Linear Regression phù hợp cho các bài toán hồi quy (dự đoán giá trị liên tục), nhưng khi áp dụng vào bài toán phân loại, nó có nhiều hạn chế:
  """)
  st.markdown("- Giá trị dự đoán \(y\) không bị giới hạn trong khoảng [0, 1], điều này không phù hợp để biểu diễn xác suất.")
  st.markdown("- Không thể trực tiếp thiết lập một ranh giới quyết định rõ ràng giữa các lớp.")
  
  # Chuyển sang Logistic Regression
  st.header("Giới thiệu Logistic Regression")
  st.write("""
  Để khắc phục nhược điểm của Linear Regression trong bài toán phân loại, Logistic Regression sử dụng một hàm kích hoạt, cụ thể là hàm sigmoid, để giới hạn giá trị đầu ra trong khoảng [0, 1].
  Công thức Logistic Regression:
  """)
  st.latex(r"P(y=1|x) = \sigma(w^T x + b) = \frac{1}{1 + e^{-(w^T x + b)}}")
  st.write("""
  Trong đó:
  - \( \sigma(z) \): Hàm sigmoid, đảm bảo đầu ra nằm trong khoảng [0, 1].
  - \(w, b\): Tham số của mô hình.
  
  Ranh giới quyết định (Decision Boundary) được xác định khi xác suất \( P(y=1|x) = 0.5 \), tức là:
  """)
  st.latex(r"w^T x + b = 0")
  
  # Trực quan hóa hàm sigmoid
  st.subheader("Trực quan hóa hàm sigmoid")
  z = np.linspace(-10, 10, 100)
  sigmoid = 1 / (1 + np.exp(-z))
  
  fig, ax = plt.subplots()
  ax.plot(z, sigmoid, label=r"$\sigma(z) = \frac{1}{1 + e^{-z}}$", color="blue")
  ax.axhline(0.5, color="red", linestyle="--", label="Decision Boundary (y=0.5)")
  ax.set_title("Hàm sigmoid")
  ax.set_xlabel("z")
  ax.set_ylabel(r"$\sigma(z)$")
  ax.legend()
  st.pyplot(fig)
  
  # Công thức hàm mất mát
  st.header("Hàm mất mát (Log-Loss)")
  st.write("""
  Trong Logistic Regression, hàm mất mát (Log-Loss) đo lường sự khác biệt giữa giá trị dự đoán và giá trị thực tế:
  """)
  st.latex(r"""
  \text{Loss} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i) \right]
  """)
  st.write("""
  Trong đó:
  - \(N\): Số lượng mẫu.
  - \(y_i\): Nhãn thực tế (0 hoặc 1).
  - \(\hat{y}_i\): Xác suất dự đoán.
  
  Hàm mất mát này được sử dụng để tối ưu hóa mô hình qua Gradient Descent.
  """)





  st.header("Gradient Descent: Phương pháp tối ưu hóa trong Logistic Regression")
  
  # Giới thiệu cơ bản
  st.write("""
  Gradient Descent là một trong những thuật toán phổ biến nhất để tối ưu hóa mô hình học máy. 
  Nó giúp tìm giá trị tối ưu của tham số \(w\) và \(b\) bằng cách giảm thiểu hàm mất mát (loss function) qua nhiều vòng lặp.
  """)
  
  # Công thức Gradient Descent
  st.write("""
  Hàm mất mát Logistic Regression thường được biểu diễn dưới dạng Cross-Entropy Loss:
  """)
  st.latex(r"L(w, b) = -\frac{1}{m} \sum_{i=1}^m \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]")
  st.write("""
  Gradient Descent cập nhật tham số theo công thức:
  """)
  st.latex(r"w := w - \alpha \frac{\partial L}{\partial w}, \quad b := b - \alpha \frac{\partial L}{\partial b}")
  st.write("""
  - \(w\), \(b\): Các tham số cần tối ưu.
  - \(\alpha\): Learning rate (tốc độ học).
  - \(\frac{\partial L}{\partial w}\), \(\frac{\partial L}{\partial b}\): Gradient (đạo hàm) của hàm mất mát theo tham số.
  
  Hãy trực quan hóa quá trình Gradient Descent để hiểu rõ hơn.
  """)
  
  # Trực quan hóa Gradient Descent
  st.subheader("Trực quan hóa Gradient Descent")
  
  # Hàm mất mát và Gradient
  def loss_function(w):
      """Giả lập hàm mất mát dựa trên tham số w"""
      return (w - 3)**2 + 5
  
  def gradient(w):
      """Đạo hàm (gradient) của hàm mất mát"""
      return 2 * (w - 3)
  
  # Vẽ đồ thị minh họa Gradient Descent
  w_values = np.linspace(-1, 7, 100)
  loss_values = loss_function(w_values)
  
  # Khởi tạo tham số w
  w_start = 6
  learning_rate = st.slider("Điều chỉnh Learning Rate (α)", 0.01, 0.5, 0.1, step=0.01)
  
  # Quá trình cập nhật Gradient Descent
  w_current = w_start
  steps = []
  losses = []
  
  for _ in range(20):  # 20 vòng lặp
      loss = loss_function(w_current)
      steps.append(w_current)
      losses.append(loss)
      grad = gradient(w_current)
      w_current = w_current - learning_rate * grad
  
  # Vẽ đồ thị
  fig, ax = plt.subplots(1, 2, figsize=(12, 5))
  
  # Đồ thị hàm mất mát
  ax[0].plot(w_values, loss_values, label="Hàm mất mát")
  ax[0].scatter(steps, losses, color="red", label="Quá trình tối ưu", zorder=5)
  ax[0].set_title("Hàm mất mát và Gradient Descent")
  ax[0].set_xlabel("Tham số w")
  ax[0].set_ylabel("Loss")
  ax[0].legend()
  
  # Đồ thị Gradient Descent
  iterations = list(range(len(steps)))
  ax[1].plot(iterations, losses, label="Loss qua các vòng lặp", marker='o', color='green')
  ax[1].set_title("Loss giảm dần qua các vòng lặp")
  ax[1].set_xlabel("Số vòng lặp")
  ax[1].set_ylabel("Loss")
  ax[1].legend()
  
  st.pyplot(fig)
  
  # Kết luận
  st.write("""
  Qua trực quan hóa, bạn có thể thấy Gradient Descent giảm giá trị của hàm mất mát qua từng vòng lặp, giúp tối ưu hóa tham số \(w\).
  """)



  # Tạo dữ liệu từ phần 1
  def generate_data(n_samples, centers, cluster_std, random_state):
      from sklearn.datasets import make_blobs
      X, y = make_blobs(
          n_samples=n_samples, centers=centers, cluster_std=cluster_std, random_state=random_state
      )
      y = y.reshape(-1, 1)  # Chuyển thành dạng cột
      return X, y
  
  # Hàm sigmoid
  def sigmoid(z):
      return 1 / (1 + np.exp(-z))
  
  # Hàm mất mát (Binary Cross Entropy)
  def loss_function(y_true, y_pred):
      return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
  
  # Gradient Descent cập nhật tham số
  def gradient_descent(X, y, w, b, learning_rate):
      m = X.shape[0]
      z = np.dot(X, w) + b
      y_pred = sigmoid(z)
      dw = np.dot(X.T, (y_pred - y)) / m
      db = np.sum(y_pred - y) / m
      w -= learning_rate * dw
      b -= learning_rate * db
      loss = loss_function(y, y_pred)
      return w, b, loss
  
  # Khởi tạo giao diện Streamlit
  st.title("Trực quan hóa Gradient Descent trong Logistic Regression")
  st.write("Nhấn nút **Tiến hành một vòng lặp** để quan sát thay đổi ranh giới quyết định qua mỗi lần cập nhật.")
  
  # Điều chỉnh tham số dữ liệu
  
  
  cluster_std = st.sidebar.slider("Độ lệch cụm", 0.5, 2.0, 1.0, step=0.1)
  learning_rate = st.sidebar.slider("Learning Rate (α)", 0.01, 1.0, 0.1, step=0.01)
  random_state = st.sidebar.number_input("Random Seed", 0, 100, 42)
  
  # Tạo dữ liệu
  X, y = generate_data(n_samples, n_classes, random_state)
  
  # Thêm cột bias
  X_bias = np.c_[np.ones((X.shape[0], 1)), X]
  
  # Khởi tạo tham số nếu chưa có
  if "w" not in st.session_state:
      st.session_state.w = np.zeros((X_bias.shape[1], 1))
  if "b" not in st.session_state:
      st.session_state.b = 0
  if "losses" not in st.session_state:
      st.session_state.losses = []
  if "iterations" not in st.session_state:
      st.session_state.iterations = 0
  
  # Hiển thị dữ liệu ban đầu và ranh giới quyết định
  fig, ax = plt.subplots()
  ax.scatter(X[:, 0], X[:, 1], c=y.flatten(), cmap="coolwarm", edgecolor="k")
  
  # Vẽ ranh giới quyết định
  if st.session_state.iterations > 0:
      w, b = st.session_state.w, st.session_state.b
      x_vals = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)
      slope = -w[1][0] / w[2][0]
      intercept = -w[0][0] / w[2][0]
      y_vals = slope * x_vals + intercept
      ax.plot(x_vals, y_vals, color="red", label=f"Decision Boundary (Iter {st.session_state.iterations})")
  else:
      st.write("Ranh giới ban đầu là ngẫu nhiên vì các tham số chưa được cập nhật.")
  
  ax.legend()
  st.pyplot(fig)
  
  # Nút tiến hành một vòng lặp Gradient Descent
  if st.button("Tiến hành một vòng lặp"):
      st.session_state.w, st.session_state.b, loss = gradient_descent(
          X_bias, y, st.session_state.w, st.session_state.b, learning_rate
      )
      st.session_state.losses.append(loss)
      st.session_state.iterations += 1
  
  # Hiển thị số lần lặp và đồ thị hàm mất mát
  st.write(f"Số lần lặp: {st.session_state.iterations}")
  st.line_chart(st.session_state.losses)
  st.write("Đồ thị hàm mất mát giảm qua từng vòng lặp.")



if __name__ == "__main__":
    app_ket_thuc()
