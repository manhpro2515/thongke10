import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Lớp học Đảo ngược: Toán 10", page_icon="📚", layout="wide")

hide_style = """<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- KẾT NỐI AI ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("⚠️ Lỗi: Giáo viên chưa cấu hình API Key trong mục Secrets.")
    st.stop()

st.title("📚 Nhiệm Vụ Về Nhà: Đo độ phân tán (Toán 10)")
st.markdown("---")

# ==========================================
# PHẦN 1: VIDEO BÀI GIẢNG (CỦA BẠN)
# ==========================================
st.header("📺 Phần 1: Xem video bài giảng")
st.info("📌 **Nhiệm vụ:** Em hãy xem kỹ video dưới đây. Nội dung video chia làm 4 phần, hãy ghi chép lại công thức trước khi làm bài tập phía dưới.")

# Tích hợp chính xác video bạn yêu cầu
st.video("https://www.youtube.com/watch?v=HWdBv4Oqzeg") 

st.markdown("---")

# ==========================================
# PHẦN 2: BÀI TẬP KIỂM TRA (BÁM SÁT VIDEO)
# ==========================================
st.header("📝 Phần 2: Kiểm tra mức độ hiểu bài")
st.write("Dựa vào các công thức cô giáo đã dạy trong video, em hãy chọn đáp án đúng nhất cho các câu hỏi sau:")

with st.form("quiz_form"):
    # Câu 1: Khoảng biến thiên (Phút 02:50 trong video)
    q1 = st.radio("1. Khoảng biến thiên (R) của mẫu số liệu thể hiện điều gì và được tính như thế nào?",
                  options=[
                      "A. Là tổng của tất cả các số liệu.", 
                      "B. Là hiệu số giữa giá trị lớn nhất và giá trị nhỏ nhất.", 
                      "C. Là giá trị nằm chính giữa của dãy số.", 
                      "D. Là trung bình cộng của giá trị lớn nhất và nhỏ nhất."
                  ], index=None)
    
    # Câu 2: Tứ phân vị (Phút 08:00 trong video)
    q2 = st.radio("2. Theo định nghĩa trong video, Khoảng tứ phân vị (kí hiệu là ∆Q) được tính bằng công thức nào?",
                  options=[
                      "A. ∆Q = Q2 - Q1", 
                      "B. ∆Q = Q3 + Q1", 
                      "C. ∆Q = Q3 - Q1", 
                      "D. ∆Q = Q3 - Q2"
                  ], index=None)
    
    # Câu 3: Phương sai và Độ lệch chuẩn (Phút 12:20 trong video)
    q3 = st.radio("3. Mối liên hệ giữa Độ lệch chuẩn (S) và Phương sai (S²) là gì?",
                  options=[
                      "A. Độ lệch chuẩn bằng bình phương của Phương sai.", 
                      "B. Độ lệch chuẩn bằng một nửa Phương sai.", 
                      "C. Độ lệch chuẩn bằng căn bậc hai của Phương sai.", 
                      "D. Hai đại lượng này luôn bằng nhau."
                  ], index=None)
    
    # Câu 4: Giá trị bất thường (Phút 16:45 trong video)
    q4 = st.radio("4. Dựa vào biểu đồ hộp, một giá trị được coi là 'bất thường' (quá nhỏ) nếu nó rơi vào trường hợp nào sau đây?",
                  options=[
                      "A. Nhỏ hơn Q1 - 1.5 × ∆Q", 
                      "B. Nhỏ hơn Q1 - ∆Q", 
                      "C. Nhỏ hơn Q2", 
                      "D. Lớn hơn Q3 + 1.5 × ∆Q"
                  ], index=None)

    submit_btn = st.form_submit_button("Nộp bài kiểm tra 🚀")

# Xử lý kết quả khi học sinh bấm nộp bài
if submit_btn:
    score = 0
    feedback = []
    
    if q1 and q1.startswith("B"):
        score += 1
        feedback.append("✅ **Câu 1: Chính xác.** Khoảng biến thiên R = Max - Min.")
    else:
        feedback.append("❌ **Câu 1: Sai.** Em hãy xem lại phút 02:50 của video nhé, R là hiệu của Max và Min.")

    if q2 and q2.startswith("C"):
        score += 1
        feedback.append("✅ **Câu 2: Chính xác.** Khoảng tứ phân vị ∆Q = Q3 - Q1.")
    else:
        feedback.append("❌ **Câu 2: Sai.** Xem lại phút 08:00. ∆Q là khoảng cách giữa tứ phân vị thứ ba và thứ nhất.")

    if q3 and q3.startswith("C"):
        score += 1
        feedback.append("✅ **Câu 3: Chính xác.** Độ lệch chuẩn S = √(S²).")
    else:
        feedback.append("❌ **Câu 3: Sai.** Xem lại phút 12:20. Độ lệch chuẩn là căn bậc hai của phương sai.")

    if q4 and q4.startswith("A"):
        score += 1
        feedback.append("✅ **Câu 4: Rất xuất sắc!** Đây là kiến thức ở phút 16:45 của video để tìm giá trị ngoại lai.")
    else:
        feedback.append("❌ **Câu 4: Sai.** Em xem lại phần 'Phát hiện số liệu bất thường bằng biểu đồ hộp' ở cuối video nhé.")

    # Hiển thị điểm
    st.write("### 📊 Điểm số của em:")
    if score == 4:
        st.success(f"🎉 Giỏi quá! Đạt {score}/4 điểm. Em đã nắm vững toàn bộ kiến thức trong video.")
        st.balloons()
    elif score >= 2:
        st.info(f"👍 Khá lắm! Đạt {score}/4 điểm. Hãy đọc lại nhận xét bên dưới để sửa các câu sai nhé.")
    else:
        st.warning(f"😅 Đạt {score}/4 điểm. Đừng lo, em hãy vừa mở lại video vừa xem các gợi ý ở dưới.")
    
    for f in feedback:
        st.write(f)

st.markdown("---")

# ==========================================
# PHẦN 3: AI CHATBOT (GIA SƯ RIÊNG)
# ==========================================
st.header("🤖 Trợ lý AI giải đáp thắc mắc")
st.write("Có đoạn nào trong video thầy/cô giảng nhanh quá em nghe chưa kịp không? Hãy nhắn tin hỏi AI nhé!")

if "chat_msgs" not in st.session_state:
    st.session_state.chat_msgs = [{"role": "assistant", "content": "Chào em! Em đã xem xong video chưa? Có công thức nào làm khó em không?"}]

for msg in st.session_state.chat_msgs:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_prompt := st.chat_input("Ví dụ: Tại sao phải dùng đến độ lệch chuẩn trong khi đã có phương sai?"):
    st.session_state.chat_msgs.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    context = f"""
    Bạn là giáo viên Toán 10. Học sinh vừa xem video bài giảng về "Các số đặc trưng đo độ phân tán" (Khoảng biến thiên, tứ phân vị, phương sai, độ lệch chuẩn, giá trị ngoại lai).
    Học sinh đang làm bài tập củng cố trên web.
    Câu hỏi của học sinh: "{user_prompt}"
    
    Yêu cầu: Giải thích thân thiện, dễ hiểu, có thể lấy ví dụ về điểm số để minh họa. Khuyến khích học sinh xem lại video nếu cần.
    """
    try:
        response = model.generate_content(context)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.chat_msgs.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("Hệ thống AI đang bảo trì, em thử lại sau 1 phút nhé.")
