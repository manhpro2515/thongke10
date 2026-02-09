import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai

# --- Cấu hình trang ---
st.set_page_config(page_title="Thống kê Lớp 10", layout="wide", page_icon="📊")

# --- Ẩn Menu mặc định ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("📊 Phân Tích Số Liệu & Trợ Lý AI - Toán 10")
st.markdown("---")

# --- KẾT NỐI AI (Lấy key từ Secrets) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Bạn có thể đổi tên model ở đây nếu muốn (ví dụ gemini-1.5-pro)
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("⚠️ Lỗi hệ thống: Chưa cấu hình API Key trong Secrets.")
    st.stop()

# --- GIAO DIỆN CHÍNH ---
col1, col2 = st.columns([1, 1])

# === CỘT TRÁI: NHẬP LIỆU & TÍNH TOÁN ===
with col1:
    st.header("1. Nhập Dữ Liệu")
    
    # --- TÍNH NĂNG MỚI: Đặt tên cho dữ liệu ---
    data_name = st.text_input("Tên bảng dữ liệu (Ví dụ: Điểm Toán 10A, Chiều cao tổ 1...):", "Số liệu mẫu")
    
    st.info("Nhập các con số cách nhau bởi dấu phẩy (ví dụ: 6.5, 8, 9, 10).")
    data_input = st.text_area(f"Dãy số của '{data_name}':", "6, 8, 9, 10, 5, 7, 8, 9, 10, 6", height=100)
    
    current_stats = "" 
    
    if data_input:
        try:
            # Xử lý dữ liệu
            raw_data = [float(x.strip()) for x in data_input.split(',')]
            df = pd.DataFrame(raw_data, columns=['GiaTri'])
            
            # Tính toán
            stats = {
                "Trung bình (Mean)": np.mean(raw_data),
                "Phương sai (S²)": np.var(raw_data, ddof=1),
                "Độ lệch chuẩn (S)": np.std(raw_data, ddof=1),
                "Khoảng biến thiên (R)": np.max(raw_data) - np.min(raw_data)
            }
            
            current_stats = str(stats)

            # Hiển thị bảng
            st.success(f"✅ Kết quả tính toán cho: {data_name}")
            st.table(pd.DataFrame(stats.items(), columns=["Chỉ số", "Giá trị"]))
            
            # Vẽ biểu đồ (Cập nhật tiêu đề theo tên dữ liệu)
            st.write("---")
            fig = px.box(df, y="GiaTri", points="all", title=f"Biểu đồ hộp: {data_name}")
            st.plotly_chart(fig, use_container_width=True)
            
        except ValueError:
            st.error("❌ Lỗi nhập liệu: Chỉ nhập số và dấu phẩy thôi nhé!")

# === CỘT PHẢI: CHATBOT ===
with col2:
    st.header("2. Trợ lý AI giải đáp 🤖")
    st.write(f"Hỏi thầy AI về '{data_name}'...")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "Chào em! Em cần thầy giải thích gì về bảng số liệu bên cạnh không?"})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ví dụ: Tại sao phương sai lại lớn thế?"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Cập nhật ngữ cảnh với Tên dữ liệu mới
        context = f"""
        Bạn là giáo viên Toán lớp 10 thân thiện.
        
        Thông tin bài toán:
        - Tên dữ liệu: {data_name}
        - Các con số cụ thể: {data_input}
        - Kết quả tính toán: {current_stats}
        
        Học sinh hỏi: "{prompt}"
        
        Yêu cầu:
        1. Trả lời ngắn gọn, dễ hiểu.
        2. Luôn gắn câu trả lời với ngữ cảnh là "{data_name}" (Ví dụ: "Sở dĩ điểm Toán thấp là do...").
        3. Giải thích ý nghĩa thực tế của các chỉ số thống kê.
        """

        try:
            response = model.generate_content(context)
            ai_reply = response.text
            
            with st.chat_message("assistant"):
                st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        except Exception as e:
            st.error("Mạng đang bận, em thử lại chút nữa nhé.")
