import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Tự học: Độ phân tán", page_icon="🎓")

# --- KẾT NỐI AI ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ Giáo viên chưa thiết lập API Key trong Secrets.")
    st.stop()

# --- KHỞI TẠO TRẠNG THÁI (SESSION STATE) ---
# Biến này để lưu xem học sinh đang học đến bài mấy
if "step" not in st.session_state:
    st.session_state.step = 1

# --- HÀM HỖ TRỢ: AI CHẤM BÀI ---
def check_answer_with_ai(question, correct_val, student_val, unit=""):
    """Dùng AI để nhận xét câu trả lời của học sinh"""
    
    # Tính sai số chấp nhận được (cho phép sai lệch 0.1)
    try:
        is_correct = abs(float(student_val) - float(correct_val)) < 0.1
    except:
        is_correct = False

    if is_correct:
        st.balloons() # Thả bóng bay chúc mừng
        st.success("🎉 Chính xác! Em làm tốt lắm.")
        msg = f"Chúc mừng! Đáp án {student_val} là hoàn toàn chính xác. Em đã hiểu bài rồi đó."
        return True, msg
    else:
        # Nhờ AI gợi ý
        prompt = f"""
        Bạn là giáo viên Toán lớp 10. 
        Câu hỏi: {question}
        Đáp án đúng: {correct_val}.
        Học sinh trả lời: {student_val}.
        
        Nhiệm vụ: Hãy chỉ ra chỗ sai hoặc đưa ra gợi ý nhẹ nhàng để học sinh tính lại. 
        Tuyệt đối KHÔNG nói toẹt đáp án đúng ra. Chỉ gợi ý cách tính thôi.
        Văn phong: Khích lệ, vui vẻ.
        """
        response = model.generate_content(prompt)
        st.warning("🤔 Chưa đúng rồi, thử lại nhé!")
        st.write(response.text)
        return False, response.text

# --- GIAO DIỆN CHÍNH ---
st.title("🎓 Nhiệm vụ về nhà: Chinh phục Độ Phân Tán")
st.markdown("Chào mừng em đến với bài học tự chủ. Hãy hoàn thành từng nhiệm vụ để mở khóa kiến thức nhé!")

# Thanh tiến độ
progress_bar = st.progress(0)
if st.session_state.step == 1: progress_bar.progress(10)
elif st.session_state.step == 2: progress_bar.progress(40)
elif st.session_state.step == 3: progress_bar.progress(70)
elif st.session_state.step == 4: progress_bar.progress(100)

st.markdown("---")

# === TRẠM 1: KHOẢNG BIẾN THIÊN (RANGE) ===
if st.session_state.step == 1:
    st.header("📍 Trạm 1: Khoảng biến thiên (R)")
    st.info("💡 Kiến thức: Khoảng biến thiên R = Giá trị lớn nhất - Giá trị nhỏ nhất")
    
    st.write("Cho mẫu số liệu điểm thi của tổ 1: **{6, 8, 3, 9, 10, 5}**")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        ans1 = st.number_input("Nhập khoảng biến thiên R của mẫu trên:", step=0.1)
    
    if st.button("Kiểm tra Trạm 1"):
        # Đáp án đúng: Max(10) - Min(3) = 7
        correct, msg = check_answer_with_ai("Tính khoảng biến thiên của {6, 8, 3, 9, 10, 5}", 7, ans1)
        if correct:
            st.session_state.step = 2 # Mở khóa trạm 2
            st.rerun() # Tải lại trang

# === TRẠM 2: TỨ PHÂN VỊ (QUARTILES) ===
elif st.session_state.step == 2:
    st.header("📍 Trạm 2: Tứ phân vị (Q)")
    st.info("💡 Kiến thức: Sắp xếp mẫu theo thứ tự tăng dần. Q2 là trung vị. Q1 là trung vị nửa đầu, Q3 là trung vị nửa sau.")
    
    st.write("Mẫu số liệu đã sắp xếp: **{3, 5, 6, 8, 9, 10}**")
    
    col1, col2 = st.columns(2)
    with col1:
        q2_ans = st.number_input("Tìm Q2 (Trung vị):", step=0.1)
    with col2:
        iqr_ans = st.number_input("Tìm Khoảng tứ phân vị (Delta_Q = Q3 - Q1):", step=0.1)
        
    if st.button("Kiểm tra Trạm 2"):
        # Mẫu: 3, 5, 6 | 8, 9, 10
        # Q2 = (6+8)/2 = 7
        # Q1 = 5
        # Q3 = 9
        # IQR = 9 - 5 = 4
        
        # Kiểm tra cả 2
        c1, m1 = check_answer_with_ai("Tính Q2 của {3, 5, 6, 8, 9, 10}", 7, q2_ans)
        
        if c1: # Nếu Q2 đúng mới check tiếp IQR để tiết kiệm token
             c2, m2 = check_answer_with_ai("Tính IQR (Q3-Q1) của {3, 5, 6, 8, 9, 10}", 4, iqr_ans)
             if c2:
                 st.session_state.step = 3
                 st.rerun()

# === TRẠM 3: PHƯƠNG SAI & ĐỘ LỆCH CHUẨN ===
elif st.session_state.step == 3:
    st.header("📍 Trạm 3: Phương sai (S²) & Độ lệch chuẩn (S)")
    st.warning("⚠️ Đây là trạm khó nhất! Em hãy dùng máy tính cầm tay để hỗ trợ nhé.")
    
    st.write("Xét mẫu số liệu nhỏ: **{2, 4, 6}**")
    st.write("Số trung bình cộng là: 4")
    
    ans3 = st.number_input("Hãy tính Phương sai mẫu (S²) (Bình phương độ lệch trung bình):", step=0.1)
    
    # Gợi ý công thức
    with st.expander("Xem công thức gợi ý"):
        st.latex(r"S^2 = \frac{(x_1 - \bar{x})^2 + ... + (x_n - \bar{x})^2}{n-1}")
        st.write("Lưu ý: Sách giáo khoa mới thường dùng n-1 (mẫu hiệu chỉnh).")

    if st.button("Kiểm tra Trạm 3"):
        # Mean = 4
        # (2-4)^2 + (4-4)^2 + (6-4)^2 = 4 + 0 + 4 = 8
        # S^2 = 8 / (3-1) = 4
        correct, msg = check_answer_with_ai("Tính phương sai mẫu hiệu chỉnh của {2, 4, 6}", 4, ans3)
        if correct:
            st.session_state.step = 4
            st.rerun()

# === TRẠM 4: TỔNG KẾT ===
elif st.session_state.step == 4:
    st.success("🏆 CHÚC MỪNG EM ĐÃ HOÀN THÀNH KHÓA HỌC!")
    st.image("https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif") # Ảnh động vỗ tay
    
    st.write("""
    **Em đã nắm được:**
    - ✅ Cách tính Khoảng biến thiên (R)
    - ✅ Cách tìm Tứ phân vị (Q1, Q2, Q3)
    - ✅ Ý tưởng về Phương sai (S²)
    
    Ngày mai lên lớp, chúng ta sẽ cùng nhau thảo luận xem **khi nào dùng số nào** nhé!
    """)
    
    if st.button("Làm lại từ đầu"):
        st.session_state.step = 1
        st.rerun()

# --- CHATBOT HỖ TRỢ BÊN CẠNH ---
with st.sidebar:
    st.header("🤖 Trợ lý Toán học")
    st.write("Gặp khó khăn? Hỏi thầy AI ngay tại đây:")
    
    # Chatbot mini
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    user_q = st.text_input("Nhập câu hỏi của em:", key="sidebar_chat")
    if user_q:
        # Prompt ngữ cảnh
        context = f"""
        Học sinh đang học bài "Các số đặc trưng đo độ phân tán" trên web tự học.
        Học sinh đang ở Trạm số: {st.session_state.step}.
        Câu hỏi: {user_q}
        Hãy giải thích ngắn gọn, gợi mở, không giải bài tập trong phần Nhiệm vụ chính.
        """
        try:
            reply = model.generate_content(context).text
            st.info(reply)
        except:
            st.error("Lỗi kết nối.")
