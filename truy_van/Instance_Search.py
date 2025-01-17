import os
import streamlit as st
import numpy as np
import cv2
import joblib
from scipy.cluster.vq import vq
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image

# Đường dẫn đến thư mục chứa tệp mô hình và dữ liệu
model_directory = "truy_van"  # Đường dẫn đến thư mục chứa mô hình và dữ liệu
test_directory = os.path.join(model_directory, "test")  # Đường dẫn đến thư mục chứa ảnh thử nghiệm

# Tải các mô hình và dữ liệu đã lưu
codebook_path = os.path.join(model_directory, "bovw_codebook.joblib")
frequency_vectors_path = os.path.join(model_directory, "frequency_vectors.joblib")
image_paths_path = os.path.join(model_directory, "image_paths.joblib")

codebook = joblib.load(codebook_path)
frequency_vectors = joblib.load(frequency_vectors_path)
image_paths = joblib.load(image_paths_path)

# Thiết lập SIFT cho việc trích xuất đặc trưng
sift = cv2.SIFT_create()
k = codebook.shape[0]  # Số lượng visual words

def extract_bovw_vector(image, codebook, k):
    # Tiền xử lý và trích xuất đặc trưng SIFT từ ảnh đầu vào
    img = np.array(image)

    if len(img.shape) == 3 and img.shape[2] == 3:
        img_resized = cv2.resize(img, (200, int(200 * img.shape[0] / img.shape[1])))
        img_smoothed = cv2.GaussianBlur(img_resized, (5, 5), 0)
        img_gray = cv2.cvtColor(img_smoothed, cv2.COLOR_BGR2GRAY)
    elif len(img.shape) == 2:  # Ảnh đã ở dạng grayscale
        img_gray = img
    else:
        st.error("Định dạng ảnh không hợp lệ.")
        return None
    
    # Trích xuất đặc trưng SIFT
    _, descriptors = sift.detectAndCompute(img_gray, None)
    if descriptors is None:
        return None

    # Mã hóa các đặc trưng thành vector BoVW
    visual_words, _ = vq(descriptors, codebook)
    bovw_vector = np.zeros(k)
    for word in visual_words:
        bovw_vector[word] += 1

    return bovw_vector

def find_similar_images(query_vector, frequency_vectors, image_paths, top_n=5):
    # Tính độ tương đồng cosine giữa vector truy vấn và tất cả vector BoVW
    similarities = cosine_similarity([query_vector], frequency_vectors)[0]
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    top_images = [(image_paths[i], similarities[i]) for i in top_indices]
    return top_images

def run_app8():
    # Thiết lập giao diện Streamlit
    st.title("1.Dữ liệu truy vấn")
    img = Image.open('truy_van/data.png')
    st.image(img, caption=f"Dữ liệu trái cây", use_column_width=True)
    st.write("""
    Tập dữ liệu "Fruit 360" trên Kaggle là một bộ sưu tập hình ảnh chứa 36 loại trái cây khác nhau.

    Với sự đa dạng về hình ảnh, tập dữ liệu "Fruit 360" giúp cải thiện độ chính xác của các mô hình nhận diện hình ảnh trong môi trường thực tế.
    """)

    st.title("1.Phương pháp")
    img = Image.open('truy_van/anh_buoc.png')
    st.image(img, caption=f"", use_column_width=True)
    st.write("""
    Các bước chính trong quy trình nhận diện hình ảnh bao gồm:
    
    **Bước 1:** Chuyển đổi ảnh màu sang ảnh xám để giảm độ phức tạp và tập trung vào các đặc trưng quan trọng.
    
    **Bước 2:** Sử dụng hai phương pháp phát hiện đặc trưng mạnh mẽ là SIFT và ORB để tìm ra các điểm đặc trưng quan trọng trong ảnh.
    
    **Bước 3:** Lọc ra các đặc trưng mà cả hai mô hình SIFT và ORB đều nhận diện được, đảm bảo tính chính xác cao trong việc nhận diện.
    
    **Bước 4:** So sánh các đặc trưng đã chọn với ảnh trong thư mục để tìm ra sự trùng khớp, từ đó xác định đối tượng cần truy vấn.
    """)


    st.title("Tìm Kiếm Ảnh Tương Tự(Trái cây)")
    
    uploaded_file = st.file_uploader("Tải lên một ảnh", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        query_image = Image.open(uploaded_file)
        st.image(query_image, caption="Ảnh đã tải lên", use_column_width=True)
    
        # Trích xuất vector BoVW cho ảnh truy vấn
        query_vector = extract_bovw_vector(query_image, codebook, k)
        if query_vector is not None:
            # Tìm ảnh tương tự
            similar_images = find_similar_images(query_vector, frequency_vectors, image_paths, top_n=5)
    
            st.write("5 Ảnh Tương Tự Nhất:")
            for img_path, similarity in similar_images:
                # Kết hợp đường dẫn của ảnh thử nghiệm với đường dẫn đã lưu
                full_image_path = os.path.join(test_directory, img_path)
                st.write(f"Độ tương đồng: {similarity:.2f}")
                similar_image = Image.open(full_image_path)
                st.image(similar_image, caption=full_image_path, use_column_width=True)
        else:
            st.error("Không tìm thấy đặc trưng trong ảnh tải lên.")

if __name__ == "__main__":
    run_app8()
