import streamlit as st
import google.generativeai as genai

# ==========================================
# CẤU HÌNH TRANG & CSS MINECRAFT
# ==========================================
st.set_page_config(page_title="Lớp học Đảo ngược: Toán 10", page_icon="⛏️", layout="wide")

# Hàm load CSS
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Chưa tìm thấy file style.css. Giao diện Minecraft sẽ không hiển thị đầy đủ.")

# LOAD FILE CSS MÀU MINECRAFT
local_css("style.css")

hide_style = """<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# Khởi tạo các biến môi trường
if "chat_msgs" not in st.session_state:
    st.session_state.chat_msgs = [{"role": "assistant", "content": "Chào em! Chào mừng tới lớp học pixel. Có phần nào chưa rõ trong bài Đo xu thế trung tâm không?"}]
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
    Bạn là một giáo viên Toán 10 nhiệt huyết, thân thiện, và là một fan cứng của tựa game Minecraft. 
    Học sinh đang học bài "Các số đặc trưng đo xu thế trung tâm" (Số trung bình, Trung vị, Tứ phân vị, Mốt).
    Quy tắc trả lời:
    1. Giọng điệu gần gũi, xưng "thầy/cô" và gọi học sinh là "em".
    2. Giải thích dễ hiểu, luôn cố gắng lấy ví dụ thực tế liên quan tới Minecraft (như điểm số xây nhà, số lượng block gỗ, mức lương ngọc lục bảo của dân làng) để minh họa.
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
        st.session_state.wrong_answers.append("Lý do sử dụng Trung vị thay vì Số trung bình khi có giá trị bất thường")

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
             st.markdown(f'<div class="minecraft-chat-assistant">Thầy/Cô AI: {response.text}</div>', unsafe_allow_html=True)
        st.session_state.chat_msgs.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("AI đang bị Lag, thử lại nhé.")
    
