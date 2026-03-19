import streamlit as st
import google.generativeai as genai
import random

# ==========================================
# CẤU HÌNH TRANG & CSS MINECRAFT
# ==========================================
st.set_page_config(page_title="Lớp học Đảo ngược: Toán 10", page_icon="⛏️", layout="wide")

# Hàm load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# LOAD FILE CSS MÀU MINECRAFT (XEM Ở DƯỚI)
local_css("style.css")

hide_style = """<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# Khởi tạo các biến môi trường
if "chat_msgs" not in st.session_state:
    st.session_state.chat_msgs = [{"role": "assistant", "content": "Chào em! Chào mừng tới lớp học pixel. Có phần nào chưa rõ trong bài Xu thế trung tâm không?"}]
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = []

# ==========================================
# KẾT NỐI AI & PERSONNEL (CẬP NHẬT THEO PHONG CÁCH)
# ==========================================
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Định hướng sư phạm mới, AI cũng xưng hô kiểu dân chơi Minecraft
    system_instruction = """
    Bạn là một giáo viên Toán 10 nhiệt huyết, thân thiện, và là một fan cứng của Minecraft. 
    Quy tắc trả lời:
    1. Giọng điệu gần gũi, xưng "thầy/cô" và gọi học sinh là "em".
    2. Giải thích dễ hiểu, luôn cố gắng lấy ví dụ thực tế liên quan tới Minecraft (như điểm số xây nhà, số lượng block, mức lương thợ mỏ) để minh họa.
    3. Không bao giờ giải hộ bài tập ngay lập tức, hãy gợi ý từng bước.
    """
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
    
    # Khởi tạo bộ nhớ cho AI
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
except Exception as e:
    st.error("⚠️ Lỗi: Giáo viên chưa cấu hình API Key trong mục Secrets.")
    st.stop()

# ==========================================
# TIÊU ĐỀ & THÔNG TIN HỌC SINH (PIXEL FONT)
# ==========================================
# Sử dụng thẻ div và class để áp dụng CSS
st.markdown('<div class="minecraft-header">📈 Nhiệm Vụ Về Nhà: Đo xu thế trung tâm (Toán 10)</div>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("👤 Họ và tên:", placeholder="Nhập tên...")
with col2:
    student_class = st.text_input("🏫 Lớp:", placeholder="Ví dụ: 10A1")

if not student_name or not student_class:
    st.markdown('<div class="minecraft-text">👋 Em hãy nhập Họ tên và Lớp ở trên để bắt đầu nhé!</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# PHẦN 1: VIDEO BÀI GIẢNG (BLOCK BORDER)
# ==========================================
st.markdown('<div class="minecraft-header-2">📺 Phần 1: Xem video bài giảng</div>', unsafe_allow_html=True)
st.markdown('<div class="minecraft-box-video">', unsafe_allow_html=True)
st.video("https://www.youtube.com/watch?v=HWdBv4Oqzeg") 
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# PHẦN 2: BÀI TẬP KIỂM TRA (MINECRAFT BUTTON)
# ==========================================
st.markdown('<div class="minecraft-header-2">📝 Phần 2: Kiểm tra mức độ hiểu bài</div>', unsafe_allow_html=True)
st.markdown(f'<div class="minecraft-text">Chào **{student_name}**, dựa vào các kiến thức đã học trong video, em hãy chọn đáp án đúng nhất:</div>', unsafe_allow_html=True)

with st.form("quiz_form"):
    q1 = st.radio("1. Số trung bình cộng (Mean) của một mẫu số liệu được tính bằng cách nào?",
                  options=[
                      "A. Lấy tổng tất cả các giá trị chia cho số lượng số liệu.", 
                      "B. Lấy giá trị lớn nhất cộng giá trị nhỏ nhất chia đôi.", 
                      "C. Chọn giá trị xuất hiện nhiều nhất.", 
                      "D. Lấy giá trị nằm chính giữa."
                  ], index=None)
    
    q2 = st.radio("2. Để tìm Trung vị (Median), bước ĐẦU TIÊN phải làm là gì?",
                  options=[
                      "A. Tính tổng.", 
                      "B. Sắp xếp các số liệu.", 
                      "C. Đếm số lần xuất hiện.", 
                      "D. Loại bỏ các giá trị ngoại lai."
                  ], index=None)
    
    q3 = st.radio("3. Mốt (Mode) mang ý nghĩa gì?",
                  options=[
                      "A. Giá trị nằm chính giữa.", 
                      "B. Trung bình cộng tất cả.", 
                      "C. Giá trị xuất hiện với tần số lớn nhất.", 
                      "D. Hiệu giữa giá trị lớn nhất và nhỏ nhất."
                  ], index=None)
    
    q4 = st.radio("4. Khi mẫu số liệu có chứa các 'giá trị bất thường' (rất lớn hoặc rất nhỏ), ta nên sử dụng đại lượng nào?",
                  options=[
                      "A. Số trung bình", 
                      "B. Trung vị", 
                      "C. Khoảng biến thiên", 
                      "D. Phương sai"
                  ], index=None)

    # Nút bấm nộp bài được custom bằng CSS
    submit_btn = st.form_submit_button("Nộp bài 🚀")

# Xử lý kết quả
if submit_btn:
    score = 0
    feedback = []
    st.session_state.wrong_answers = [] 
    
    if q1 and q1.startswith("A"): score += 1
    else: 
        feedback.append("❌ Câu 1 sai.")
        st.session_state.wrong_answers.append("Cách tính Số trung bình")

    if q2 and q2.startswith("B"): score += 1
    else: 
        feedback.append("❌ Câu 2 sai.")
        st.session_state.wrong_answers.append("Các bước tìm Trung vị")

    if q3 and q3.startswith("C"): score += 1
    else: 
        feedback.append("❌ Câu 3 sai.")
        st.session_state.wrong_answers.append("Khái niệm Mốt")

    if q4 and q4.startswith("B"): score += 1
    else: 
        feedback.append("❌ Câu 4 sai.")
        st.session_state.wrong_answers.append("Giá trị bất thường")

    st.session_state.quiz_submitted = True

    # --- TÍCH HỢP NGỮ CẢNH VÀO AI ---
    if len(st.session_state.wrong_answers) > 0:
        hidden_context = f"[Thông tin hệ thống: Học sinh {student_name} vừa làm bài và làm sai: {', '.join(st.session_state.wrong_answers)}. Bạn chủ động gợi ý giải thích lại.]"
        try:
            st.session_state.chat_session.send_message(hidden_context)
        except:
            pass 

    st.markdown('<div class="minecraft-header-2">📊 Kết quả:</div>', unsafe_allow_html=True)
    if score == 4:
        st.success(f"🎉 Xuất sắc {student_name}! Em đạt {score}/4 điểm. Xứng đáng 1 block Kim cương!")
        st.balloons()
    else:
        st.error(f"😅 {student_name} đạt {score}/4 điểm. Hỏi thầy/cô AI ở dưới nhé!")
    
    for f in feedback:
        st.markdown(f'<div class="minecraft-feedback">{f}</div>', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# PHẦN 3: AI CHATBOT (CHÚC VUI VẺ)
# ==========================================
st.markdown('<div class="minecraft-header-2">🤖 Trợ lý AI giải đáp thắc mắc</div>', unsafe_allow_html=True)
st.markdown(f'<div class="minecraft-text">Có phần nào chưa rõ, {student_name} cứ nhắn tin nhé!</div>', unsafe_allow_html=True)

# Hiển thị lịch sử tin nhắn
for msg in st.session_state.chat_msgs:
    if msg["role"] == "user":
        st.markdown(f'<div class="minecraft-chat-user">You: {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="minecraft-chat-assistant">Thầy/Cô AI: {msg["content"]}</div>', unsafe_allow_html=True)

# Khung nhập chat
if user_prompt := st.chat_input("Ví dụ: Vì sao có giá trị bất thường thì dùng Trung vị?"):
    st.session_state.chat_msgs.append({"role": "user", "content": user_prompt})
    st.markdown(f'<div class="minecraft-chat-user">You: {user_prompt}</div>', unsafe_allow_html=True)

    try:
        response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
             # Bạn có thể bỏ dòng st.chat_message mặc định này
             # và chỉ dùng st.markdown với CSS ở dưới
             st.markdown(f'<div class="minecraft-chat-assistant">Thầy/Cô AI: {response.text}</div>', unsafe_allow_html=True)
        st.session_state.chat_msgs.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("AI đang bị Lag, thử lại nhé.")
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
