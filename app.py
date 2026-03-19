import streamlit as st
import google.generativeai as genai

# ==========================================
# CẤU HÌNH TRANG & CSS MINECRAFT (GỘP CHUNG)
# ==========================================
st.set_page_config(page_title="Lớp học Pixel: Toán 10", page_icon="⛏️", layout="wide")

# CSS NHÚNG TRỰC TIẾP (Không cần file style.css bên ngoài)
minecraft_css = """
<style>
/* Tải font chữ Pixel từ Google Fonts cho an toàn và ổn định */
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

/* Ép toàn bộ trang và các thành phần của Streamlit dùng font Pixel */
html, body, [class*="css"], .stTextInput input, .stRadio label, .stMarkdown p {
    font-family: 'VT323', monospace !important;
    font-size: 1.2rem !important;
}

/* Ẩn menu mặc định */
#MainMenu {visibility: hidden;} 
footer {visibility: hidden;}

/* Khung Tiêu đề chính (Khối Đất) */
.minecraft-header {
    font-size: 2.5rem !important;
    color: white;
    background-color: #5d3a1a;
    padding: 15px;
    border: 6px solid #3d2311;
    text-align: center;
    box-shadow: 4px 4px 0px #000000;
    margin-bottom: 20px;
}

/* Khung Tiêu đề phụ (Khối Kim Cương/Nước) */
.minecraft-header-2 {
    font-size: 1.8rem !important;
    color: white;
    background-color: #3b82f6;
    padding: 10px;
    border: 4px solid #1d4ed8;
    box-shadow: 3px 3px 0px #000000;
    margin-top: 15px;
    margin-bottom: 10px;
}

/* Chữ hiển thị chung */
.minecraft-text {
    font-size: 1.4rem !important;
    color: #1f2937;
}

/* Ép nút bấm của Streamlit thành khối Ngọc Lục Bảo */
div.stButton > button {
    background-color: #10b981 !important;
    color: white !important;
    border: 4px solid #047857 !important;
    border-radius: 0px !important;
    font-size: 1.5rem !important;
    box-shadow: 3px 3px 0px #000000 !important;
    font-family: 'VT323', monospace !important;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #34d399 !important;
    border-color: #059669 !important;
}

/* Khung Chat */
.minecraft-chat-user {
    background-color: #fcd34d;
    color: #000;
    padding: 10px;
    border: 3px solid #d97706;
    margin-bottom: 10px;
    box-shadow: 2px 2px 0px #000;
}
.minecraft-chat-assistant {
    background-color: #86efac;
    color: #000;
    padding: 10px;
    border: 3px solid #16a34a;
    margin-bottom: 10px;
    box-shadow: 2px 2px 0px #000;
}
</style>
"""
st.markdown(minecraft_css, unsafe_allow_html=True)

# Khởi tạo các biến môi trường
if "chat_msgs" not in st.session_state:
    st.session_state.chat_msgs = [{"role": "assistant", "content": "Chào em! Chào mừng tới lớp học pixel. Có phần nào chưa rõ trong bài Đo xu thế trung tâm không?"}]
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = []

# ==========================================
# KẾT NỐI AI
# ==========================================
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    system_instruction = """
    Bạn là một giáo viên Toán 10 nhiệt huyết, thân thiện, và là một fan cứng của tựa game Minecraft. 
    Học sinh đang học bài "Các số đặc trưng đo xu thế trung tâm" (Số trung bình, Trung vị, Tứ phân vị, Mốt).
    Quy tắc trả lời:
    1. Giọng điệu gần gũi, xưng "thầy/cô" và gọi học sinh là "em".
    2. Giải thích dễ hiểu, luôn cố gắng lấy ví dụ thực tế liên quan tới Minecraft (như điểm số xây nhà, số lượng block gỗ, mức lương ngọc lục bảo của dân làng) để minh họa.
    3. Không bao giờ giải hộ bài tập ngay lập tức, hãy gợi ý từng bước.
    """
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
    
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
except Exception as e:
    st.error("⚠️ Lỗi: Giáo viên chưa cấu hình API Key trong mục Secrets.")
    st.stop()

# ==========================================
# GIAO DIỆN
# ==========================================
st.markdown('<div class="minecraft-header">📈 Nhiệm Vụ Về Nhà: Đo xu thế trung tâm</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("👤 Họ và tên:", placeholder="Nhập tên...")
with col2:
    student_class = st.text_input("🏫 Lớp:", placeholder="Ví dụ: 10A1")

if not student_name or not student_class:
    st.markdown('<div class="minecraft-text">👋 Em hãy nhập Họ tên và Lớp ở trên để bắt đầu nhé!</div>', unsafe_allow_html=True)
    st.stop()

st.markdown('<div class="minecraft-header-2">📺 Phần 1: Xem video bài giảng</div>', unsafe_allow_html=True)
st.video("https://www.youtube.com/watch?v=HWdBv4Oqzeg") 

st.markdown('<div class="minecraft-header-2">📝 Phần 2: Kiểm tra mức độ hiểu bài</div>', unsafe_allow_html=True)
st.markdown(f'<div class="minecraft-text">Chào **{student_name}**, hãy chọn đáp án đúng nhất:</div>', unsafe_allow_html=True)

with st.form("quiz_form"):
    q1 = st.radio("1. Số trung bình cộng của một mẫu số liệu được tính bằng cách nào?",
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

    submit_btn = st.form_submit_button("Nộp bài 🚀")

if submit_btn:
    score = 0
    feedback = []
    st.session_state.wrong_answers = [] 
    
    if q1 and q1.startswith("A"): score += 1
    else: 
        feedback.append("❌ Câu 1 sai: Trung bình là tổng chia cho số lượng.")
        st.session_state.wrong_answers.append("Cách tính Số trung bình")

    if q2 and q2.startswith("B"): score += 1
    else: 
        feedback.append("❌ Câu 2 sai: Phải luôn sắp xếp dãy số trước khi tìm trung vị.")
        st.session_state.wrong_answers.append("Các bước tìm Trung vị")

    if q3 and q3.startswith("C"): score += 1
    else: 
        feedback.append("❌ Câu 3 sai: Mốt là giá trị xuất hiện nhiều nhất.")
        st.session_state.wrong_answers.append("Khái niệm Mốt")

    if q4 and q4.startswith("B"): score += 1
    else: 
        feedback.append("❌ Câu 4 sai: Khi có giá trị bất thường, phải dùng Trung vị.")
        st.session_state.wrong_answers.append("Lý do sử dụng Trung vị khi có giá trị bất thường")

    st.session_state.quiz_submitted = True

    if len(st.session_state.wrong_answers) > 0:
        hidden_context = f"[Hệ thống: Học sinh làm sai: {', '.join(st.session_state.wrong_answers)}. Hãy chủ động gợi ý giải thích lại.]"
        try: st.session_state.chat_session.send_message(hidden_context)
        except: pass 

    st.markdown('<div class="minecraft-header-2">📊 Kết quả:</div>', unsafe_allow_html=True)
    if score == 4:
        st.success(f"🎉 Xuất sắc {student_name}! Em đạt {score}/4 điểm. Xứng đáng 1 block Kim cương!")
        st.balloons()
    else:
        st.error(f"😅 {student_name} đạt {score}/4 điểm. Kéo xuống hỏi thầy/cô AI nhé!")
    
    for f in feedback:
        st.write(f)

st.markdown("---")

# ==========================================
# PHẦN 3: AI CHATBOT
# ==========================================
st.markdown('<div class="minecraft-header-2">🤖 Trợ lý AI giải đáp thắc mắc</div>', unsafe_allow_html=True)

for msg in st.session_state.chat_msgs:
    if msg["role"] == "user":
        st.markdown(f'<div class="minecraft-chat-user"><b>Học sinh:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="minecraft-chat-assistant"><b>Thầy/Cô AI:</b> {msg["content"]}</div>', unsafe_allow_html=True)

if user_prompt := st.chat_input("Nhắn tin cho giáo viên..."):
    st.session_state.chat_msgs.append({"role": "user", "content": user_prompt})
    st.markdown(f'<div class="minecraft-chat-user"><b>Học sinh:</b> {user_prompt}</div>', unsafe_allow_html=True)

    try:
        response = st.session_state.chat_session.send_message(user_prompt)
        st.markdown(f'<div class="minecraft-chat-assistant"><b>Thầy/Cô AI:</b> {response.text}</div>', unsafe_allow_html=True)
        st.session_state.chat_msgs.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("AI đang bị Lag, thử lại nhé.")
    
