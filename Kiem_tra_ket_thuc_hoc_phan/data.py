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

    # Gradient Descent: Phương pháp tối ưu hóa trong Logistic Regression
    st.header("Gradient Descent: Phương pháp tối ưu hóa trong Logistic Regression")
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
    ax[1].plot(range(20), losses, label="Loss")
    ax[1].set_title("Mất mát theo số vòng lặp")
    ax[1].set_xlabel("Số vòng lặp")
    ax[1].set_ylabel("Loss")
    ax[1].legend()
    
    st.pyplot(fig)
    
    # Cập nhật kết quả cho người dùng
    st.write(f"Tham số cuối cùng: w = {w_current:.2f}")
    st.write(f"Loss cuối cùng: {losses[-1]:.2f}")
