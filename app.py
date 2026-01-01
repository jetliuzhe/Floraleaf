import streamlit as st
import google.generativeai as genai

# 1. 网页标题设置
st.set_page_config(page_title="我的 AI 助手", page_icon="🤖")
st.title("🤖 欢迎来到我的 AI 聊天室")

# 2. 获取我们在网页后台设置的密码 (API Key)
# 这一步是让网页去读取保险箱里的钥匙
try:
    my_api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("还没有设置 API Key 哦！请去 Streamlit 的设置里添加。")
    st.stop()

# 3. 启动 Google 的 AI 大脑
genai.configure(api_key=my_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. 记住我们聊过什么 (记忆功能)
if "history" not in st.session_state:
    st.session_state.history = []

# 5. 把之前的聊天记录显示出来
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 等待用户输入问题
if user_input := st.chat_input("在这里输入你想问的问题..."):
    # 显示刚才用户说的话
    with st.chat_message("user"):
        st.markdown(user_input)
    # 把用户的话存进记忆
    st.session_state.history.append({"role": "user", "content": user_input})

    # AI 开始思考并回答
    try:
        response = model.generate_content(user_input)
        bot_reply = response.text
        
        # 显示 AI 的回答
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        # 把 AI 的话存进记忆
        st.session_state.history.append({"role": "assistant", "content": bot_reply})
        
    except Exception as e:
        st.error(f"AI 累了，休息一下：{e}")
