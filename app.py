import streamlit as st
import google.generativeai as genai

# ==========================================
# CẤU HÌNH TRANG & KHỞI TẠO STATE
# ==========================================
st.set_page_config(page_title="Lớp học Đảo ngược: Toán 10", page_icon="📚", layout="wide")

# Ẩn menu mặc định của Streamlit để giao diện sạch hơn
hide_style = """<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# Khởi tạo các biến môi trường (Session State) để lưu trữ dữ liệu khi trang tải lại
if "chat_msgs" not in st.session_state:
    st.session_state.chat_msgs = [{"role": "assistant", "content": "Chào em! Thầy/cô AI ở đây. Em đã xem xong video chưa? Có công thức nào làm khó em không?"}]
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = []

# ==========================================
# KẾT NỐI AI & CẤU HÌNH NHÂN VẬT (PERSONA)
# ==========================================
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Định hướng sư phạm cho AI
    system_instruction = """
    Bạn là một giáo viên Toán 10 nhiệt huyết, thân thiện và kiên nhẫn. 
    Học sinh của bạn đang tự học bài "Các số đặc trưng đo độ phân tán" qua video (gồm: Khoảng biến thiên, Tứ phân vị, Phương sai, Độ lệch chuẩn, Giá trị ngoại lai).
    Quy tắc trả lời:
    1. Giọng điệu gần gũi, xưng "thầy/cô" và gọi học sinh là "em".
    2. Giải thích dễ hiểu, luôn cố gắng lấy ví dụ thực tế (như điểm số bài kiểm tra, chiều cao lớp học) để minh họa.
    3. Không bao giờ giải hộ bài tập ngay lập tức, hãy gợi ý từng bước.
    4. Nếu học sinh hỏi kiến thức cũ, hãy nhắc các em có thể xem lại video bài giảng.
    """
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
    
    # Khởi tạo bộ nhớ cho AI (Chỉ tạo 1 lần)
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
except Exception as e:
    st.error("⚠️ Lỗi: Giáo viên chưa cấu hình API Key trong mục Secrets.")
    st.stop()

# ==========================================
# TIÊU ĐỀ & THÔNG TIN HỌC SINH
# ==========================================
st.title("📚 Nhiệm Vụ Về Nhà: Đo độ phân tán (Toán 10)")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("👤 Họ và tên của em:", placeholder="Nhập họ và tên...")
with col2:
    student_class = st.text_input("🏫 Lớp:", placeholder="Ví dụ: 10A1")

if not student_name or not student_class:
    st.info("👋 Em hãy nhập Họ tên và Lớp ở trên để bắt đầu bài học nhé!")
    st.stop() # Dừng chạy các phần dưới nếu chưa nhập tên

# ==========================================
# PHẦN 1: VIDEO BÀI GIẢNG
# ==========================================
st.header("📺 Phần 1: Xem video bài giảng")
st.info("📌 **Nhiệm vụ:** Em hãy xem kỹ video dưới đây. Ghi chép lại công thức trước khi làm bài tập phía dưới nhé.")
st.video("https://www.youtube.com/watch?v=HWdBv4Oqzeg") 
st.markdown("---")

# ==========================================
# PHẦN 2: BÀI TẬP KIỂM TRA
# ==========================================
st.header("📝 Phần 2: Kiểm tra mức độ hiểu bài")
st.write(f"Chào **{student_name}**, dựa vào các công thức đã học trong video, em hãy chọn đáp án đúng nhất:")

with st.form("quiz_form"):
    q1 = st.radio("1. Khoảng biến thiên (R) của mẫu số liệu thể hiện điều gì và được tính như thế nào?",
                  options=[
                      "A. Là tổng của tất cả các số liệu.", 
                      "B. Là hiệu số giữa giá trị lớn nhất và giá trị nhỏ nhất.", 
                      "C. Là giá trị nằm chính giữa của dãy số.", 
                      "D. Là trung bình cộng của giá trị lớn nhất và nhỏ nhất."
                  ], index=None)
    
    q2 = st.radio("2. Theo định nghĩa trong video, Khoảng tứ phân vị (kí hiệu là ∆Q) được tính bằng công thức nào?",
                  options=[
                      "A. ∆Q = Q2 - Q1", 
                      "B. ∆Q = Q3 + Q1", 
                      "C. ∆Q = Q3 - Q1", 
                      "D. ∆Q = Q3 - Q2"
                  ], index=None)
    
    q3 = st.radio("3. Mối liên hệ giữa Độ lệch chuẩn (S) và Phương sai (S²) là gì?",
                  options=[
                      "A. Độ lệch chuẩn bằng bình phương của Phương sai.", 
                      "B. Độ lệch chuẩn bằng một nửa Phương sai.", 
                      "C. Độ lệch chuẩn bằng căn bậc hai của Phương sai.", 
                      "D. Hai đại lượng này luôn bằng nhau."
                  ], index=None)
    
    q4 = st.radio("4. Dựa vào biểu đồ hộp, một giá trị được coi là 'bất thường' (quá nhỏ) nếu nó rơi vào trường hợp nào sau đây?",
                  options=[
                      "A. Nhỏ hơn Q1 - 1.5 × ∆Q", 
                      "B. Nhỏ hơn Q1 - ∆Q", 
                      "C. Nhỏ hơn Q2", 
                      "D. Lớn hơn Q3 + 1.5 × ∆Q"
                  ], index=None)

    submit_btn = st.form_submit_button("Nộp bài kiểm tra 🚀")

# Xử lý kết quả
if submit_btn:
    score = 0
    feedback = []
    st.session_state.wrong_answers = [] # Xóa dữ liệu sai cũ
    
    if q1 and q1.startswith("B"): score += 1
    else: 
        feedback.append("❌ **Câu 1:** Xem lại phút 02:50. Khoảng biến thiên R = Max - Min.")
        st.session_state.wrong_answers.append("Khoảng biến thiên")

    if q2 and q2.startswith("C"): score += 1
    else: 
        feedback.append("❌ **Câu 2:** Xem lại phút 08:00. ∆Q = Q3 - Q1.")
        st.session_state.wrong_answers.append("Khoảng tứ phân vị")

    if q3 and q3.startswith("C"): score += 1
    else: 
        feedback.append("❌ **Câu 3:** Xem lại phút 12:20. Độ lệch chuẩn là căn bậc hai của phương sai.")
        st.session_state.wrong_answers.append("Mối liên hệ giữa Phương sai và Độ lệch chuẩn")

    if q4 and q4.startswith("A"): score += 1
    else: 
        feedback.append("❌ **Câu 4:** Xem lại phút 16:45 (Phát hiện số liệu bất thường).")
        st.session_state.wrong_answers.append("Giá trị ngoại lai (bất thường)")

    st.session_state.quiz_submitted = True

    # --- TÍCH HỢP NGỮ CẢNH VÀO AI (Bí mật mớm thông tin cho AI) ---
    if len(st.session_state.wrong_answers) > 0:
        hidden_context = f"[Thông tin hệ thống: Học sinh {student_name} vừa làm bài kiểm tra và làm sai các phần kiến thức sau: {', '.join(st.session_state.wrong_answers)}. Bạn hãy chủ động gợi ý giải thích lại các phần này một cách nhẹ nhàng nếu học sinh bắt đầu trò chuyện.]"
        try:
            st.session_state.chat_session.send_message(hidden_context)
        except:
            pass # Bỏ qua nếu có lỗi mạng tạm thời

    # Hiển thị điểm
    st.write("### 📊 Kết quả của em:")
    if score == 4:
        st.success(f"🎉 Giỏi quá {student_name}! Em đạt {score}/4 điểm. Nắm kiến thức rất vững!")
        st.balloons()
    elif score >= 2:
        st.warning(f"👍 Khá lắm {student_name}! Đạt {score}/4 điểm. Đọc kỹ gợi ý bên dưới để sửa lỗi nhé.")
    else:
        st.error(f"😅 {student_name} đạt {score}/4 điểm. Đừng lo, hãy hỏi thầy/cô AI ở phần dưới để được giải thích lại nhé!")
    
    for f in feedback:
        st.write(f)
        
    # Gợi ý giáo viên: Tại đây có thể thêm code lưu thông tin (Tên, Lớp, Điểm) vào Google Sheets.

st.markdown("---")

# ==========================================
# PHẦN 3: AI CHATBOT (GIA SƯ RIÊNG)
# ==========================================
st.header("🤖 Trợ lý AI giải đáp thắc mắc")
st.write(f"Có phần nào chưa rõ, {student_name} cứ nhắn tin hỏi thầy/cô AI ở đây nhé!")

# Hiển thị lịch sử tin nhắn
for msg in st.session_state.chat_msgs:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Khung nhập chat
if user_prompt := st.chat_input("Ví dụ: Cô ơi, giải thích lại giúp em Phương sai là gì với ạ?"):
    # Thêm tin nhắn user vào giao diện
    st.session_state.chat_msgs.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Gửi tin nhắn tới AI qua Session để giữ bộ nhớ
    try:
        response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.chat_msgs.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("Hệ thống AI đang bảo trì, em thử lại sau 1 phút nhé.")
