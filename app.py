import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai

# --- Cấu hình trang ---
st.set_page_config(page_title="Thống kê Lớp 10", layout="wide")

st.title("📊 Phân Tích Số Liệu & Trợ Lý AI - Toán 10")
st.markdown("---")

# --- Sidebar: Cài đặt API Key ---
with st.sidebar:
    st.header("Cài đặt")
    api_key = st.text_input("Nhập Google API Key của bạn", type="password")
    st.info("Nhập API Key để Chatbot hoạt động. Lấy key tại aistudio.google.com")
    st.markdown("---")
    st.write("Hướng dẫn: Nhập các số liệu cách nhau bởi dấu phẩy. Ví dụ: 5, 8, 9, 10, 12")

# --- Chia cột giao diện ---
col1, col2 = st.columns([1, 1])

# === PHẦN 1: TÍNH TOÁN & BIỂU ĐỒ (CỘT TRÁI) ===
with col1:
    st.header("🧮 Nhập Số Liệu")
    data_input = st.text_area("Nhập dãy số (cách nhau dấu phẩy):", "6, 8, 9, 10, 5, 7, 8, 9, 10, 6")
    
    if data_input:
        try:
            # Xử lý dữ liệu đầu vào
            raw_data = [float(x.strip()) for x in data_input.split(',')]
            df = pd.DataFrame(raw_data, columns=['GiaTri'])
            
            # Tính toán các chỉ số
            mean_val = np.mean(raw_data)
            min_val = np.min(raw_data)
            max_val = np.max(raw_data)
            range_val = max_val - min_val
            
            # Tứ phân vị
            q1 = np.percentile(raw_data, 25)
            q2 = np.percentile(raw_data, 50) # Trung vị
            q3 = np.percentile(raw_data, 75)
            iqr = q3 - q1
            
            # Phương sai & Độ lệch chuẩn (Mẫu hiệu chỉnh - ddof=1 cho giống SGK)
            var_val = np.var(raw_data, ddof=1)
            std_val = np.std(raw_data, ddof=1)
            
            # Hiển thị bảng kết quả
            st.subheader("Kết quả tính toán")
            metrics = {
                "Số trung bình (Mean)": f"{mean_val:.2f}",
                "Khoảng biến thiên (R)": f"{range_val:.2f}",
                "Tứ phân vị Q1": f"{q1:.2f}",
                "Trung vị (Q2/Median)": f"{q2:.2f}",
                "Tứ phân vị Q3": f"{q3:.2f}",
                "Khoảng tứ phân vị (IQR)": f"{iqr:.2f}",
                "Phương sai (S²)": f"{var_val:.2f}",
                "Độ lệch chuẩn (S)": f"{std_val:.2f}"
            }
            st.table(pd.DataFrame(metrics.items(), columns=["Chỉ số", "Giá trị"]))
            
            # Vẽ biểu đồ Boxplot
            st.subheader("Biểu đồ hộp (Boxplot)")
            fig = px.box(df, y="GiaTri", points="all", title="Biểu đồ phân tán dữ liệu")
            st.plotly_chart(fig, use_container_width=True)
            
        except ValueError:
            st.error("Dữ liệu nhập vào chưa đúng định dạng số. Vui lòng kiểm tra lại!")

# === PHẦN 2: AI CHATBOT (CỘT PHẢI) ===
with col2:
    st.header("🤖 Trợ lý Toán học AI")
    
    # Kiểm tra API Key
    if not api_key:
        st.warning("Vui lòng nhập API Key ở cột bên trái để bắt đầu chat.")
    else:
        # Cấu hình Gemini
        genai.configure(api_key=api_key)
        
        # Khởi tạo lịch sử chat
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Hiển thị lịch sử chat cũ
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Nhận câu hỏi từ người dùng
        if prompt := st.chat_input("Hỏi thầy AI về bài học..."):
            # Lưu câu hỏi người dùng
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Tạo context cho AI
            context_prompt = f"""
            Bạn là một trợ lý ảo dạy Toán lớp 10, chuyên về phần Thống kê (Độ phân tán).
            
            Nếu có dữ liệu người dùng đang nhập là: {data_input if 'data_input' in locals() else 'Chưa có dữ liệu'}, 
            hãy dùng nó để minh họa nếu phù hợp.
            
            Nhiệm vụ của bạn:
            1. Giải thích ý nghĩa các chỉ số (Phương sai, độ lệch chuẩn, khoảng biến thiên...).
            2. Không giải bài tập về nhà hộ, chỉ hướng dẫn cách làm.
            3. Dùng ngôn ngữ thân thiện, dễ hiểu với học sinh lớp 10.
            
            Câu hỏi của học sinh: {prompt}
            """

            # Gọi Gemini trả lời
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(context_prompt)
                ai_reply = response.text
                
                # Hiển thị câu trả lời
                with st.chat_message("assistant"):
                    st.markdown(ai_reply)
                
                # Lưu câu trả lời
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")
          
