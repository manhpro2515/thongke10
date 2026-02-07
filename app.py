import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import google.generativeai as genai

# --- Cấu hình trang ---
st.set_page_config(page_title="Thống kê Lớp 10", layout="wide", page_icon="📊")

# --- Ẩn Menu mặc định của Streamlit để học sinh không bấm linh tinh ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("📊 Phân Tích Số Liệu & Trợ Lý AI - Toán 10")
st.markdown("---")

# --- KẾT NỐI AI TỰ ĐỘNG (Lấy key từ Secrets) ---
try:
    # Lấy API Key từ "két sắt" (Secrets)
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Cấu hình Model mặc định (Dùng bản Flash cho nhanh và ổn định)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("⚠️ Lỗi hệ thống: Giáo viên chưa cấu hình API Key trong phần Secrets.")
    st.stop()

# --- GIAO DIỆN CHÍNH ---
col1, col2 = st.columns([1, 1])

# === CỘT TRÁI: TÍNH TOÁN ===
with col1:
    st.subheader("1. Nhập Dữ Liệu")
    st.info("Nhập các con số cách nhau bởi dấu phẩy. Ví dụ: 6, 8, 9, 10, 5")
    
    data_input = st.text_area("Dãy số của em:", "6, 8, 9, 10, 5, 7, 8, 9, 10, 6", height=100)
    
    current_stats = "" # Biến để lưu kết quả gửi cho AI
    
    if data_input:
        try:
            # Xử lý dữ liệu
            raw_data = [float(x.strip()) for x in data_input.split(',')]
            df = pd.DataFrame(raw_data, columns=['GiaTri'])
            
            # Tính toán
            mean_val = np.mean(raw_data)
            var_val = np.var(raw_data, ddof=1)
            std_val = np.std(raw_data, ddof=1)
            range_val = np.max(raw_data) - np.min(raw_data)
            
            stats = {
                "Trung bình (Mean)": mean_val,
                "Phương sai (S²)": var_val,
                "Độ lệch chuẩn (S)": std_val,
                "Khoảng biến thiên (R)": range_val
            }
            
            # Lưu chuỗi kết quả để tí nữa gửi cho AI
            current_stats = str(stats)

            # Hiển thị bảng
            st.success("✅ Kết quả tính toán:")
            st.table(pd.DataFrame(stats.items(), columns=["Chỉ số", "Giá trị"]))
            
            # Vẽ biểu đồ
            st.write("---")
            st.subheader("Biểu đồ hộp (Boxplot)")
            fig = px.box(df, y="GiaTri", points="all")
            st.plotly_chart(fig, use_container_width=True)
            
        except ValueError:
            st.error("❌ Lỗi nhập liệu: Em hãy kiểm tra lại, chỉ nhập số và dấu phẩy nhé!")

# === CỘT PHẢI: CHATBOT ===
with col2:
    st.subheader("2. Trợ lý AI giải đáp 🤖")
    st.write("Em có thắc mắc gì về kết quả bên cạnh không?")
    
    # Khởi tạo lịch sử chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Tin nhắn chào mừng
        st.session_state.messages.append({"role": "assistant", "content": "Chào em! Thầy là trợ lý AI. Em nhập số liệu bên kia rồi hỏi thầy nhé."})

    # Hiển thị lịch sử
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Ô nhập liệu chat
    if prompt := st.chat_input("Ví dụ: Tại sao độ lệch chuẩn lại cao thế?"):
        
        # Hiển thị câu hỏi của học sinh
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Tạo ngữ cảnh (Context) gửi cho AI
        context = f"""
        Bạn là một giáo viên Toán thân thiện, vui tính dạy lớp 10.
        
        Học sinh đang có dãy số liệu: {data_input}
        Kết quả tính toán máy tính ra là: {current_stats}
        
        Câu hỏi của học sinh: {prompt}
        
        Yêu cầu:
        1. Giải thích dựa trên chính xác con số của học sinh.
        2. Nếu học sinh hỏi về ý nghĩa, hãy giải thích đơn giản (ví dụ: độ lệch chuẩn lớn nghĩa là học lực không đều).
        3. Không giải bài tập về nhà khác, chỉ tập trung vào Thống kê.
        """

        try:
            # Gửi cho AI xử lý
            response = model.generate_content(context)
            ai_reply = response.text
            
            # Hiển thị câu trả lời
            with st.chat_message("assistant"):
                st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        except Exception as e:
            st.error("Mạng đang bận, em thử lại chút nữa nhé.")
            
