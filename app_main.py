import streamlit as st
from Grabcut.Grabcut_app import run_app1
from Watershed_Segmentation import run_app2  # Đã sửa tên module không có khoảng trắn
from app_face_detection import run_app3
from app_update_firebase import run_app4
from App_Face_Verification import run_app5
from folder_Keypoint_Detection.Semantic_Keypoint_Detection import run_app6
from folder_SuperPoint_Rotation.app_superpoint_rotation import run_app7
from truy_van.Instance_Search import run_app8
from foder_Object_racking.Object_Tracking_app import run_app9
from mot_sort.mot_sort import run_app10
from Handwriting_Letter_Recognition.app_handwriting import run_app11
from Image_Processing.Image_Processing import run_app12
# Tạo thanh điều hướn
option = st.sidebar.selectbox(
    'Chọn ứng dụng:',
    ('GrabCut', 'Watershed_Segmentation','Face_detection','Face_Verification','Semantic_Keypoint_Detection','Instance_Search','Thuật toán SORT'
    ,'OpenCV_Object_Tracking','Handwriting_Letter_Recognition','Image_Processing')  # Đã loại bỏ Ứng dụng 2 nếu không sử dụng
)

# Hiển thị ứng dụng tương ứng
if option == 'GrabCut':
    run_app1()  # Gọi hàm chạy ứng dụng 1
elif option == 'Watershed_Segmentation':
    run_app2()  # Gọi hàm chạy ứng dụng 2
elif option == 'Face_detection':
    run_app3()  # Gọi hàm chạy ứng dụng 3
# elif option == 'Update_firebase':
#     st.write("Ứng dụng đang fix. Tạm tắt để tránh lỗi toàn cục")

elif option == 'Face_Verification':
    run_app5()  # Gọi hàm chạy ứng dụng 5
elif option == 'Semantic_Keypoint_Detection':
    run_app6()  # Gọi hàm chạy ứng dụng 6
# elif option == 'SuperPoint_Rotation':
#     run_app7()  # Gọi hàm chạy ứng dụng 
elif option == 'Instance_Search':
    run_app8()  # Gọi hàm chạy ứng dụng 
elif option == 'OpenCV_Object_Tracking':
    run_app9()  # Gọi hàm chạy ứng dụng 
elif option == 'Thuật toán SORT':
    run_app10()  # Gọi hàm chạy ứng dụng    
elif option == 'Handwriting_Letter_Recognition':
    run_app11()  # Gọi hàm chạy ứng dụng   
elif option == 'Image_Processing':
    run_app12()  # Gọi hàm chạy ứng dụng   
else:
    st.write("Vui lòng chọn một ứng dụng từ thanh điều hướng.")
