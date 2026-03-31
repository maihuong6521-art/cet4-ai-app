import streamlit as st
from zhipuai import ZhipuAI
import matplotlib.pyplot as plt

# ====== 页面配置 ======
st.set_page_config(page_title="英语四级助手", page_icon="📚")

# ====== API ======
client = ZhipuAI(api_key="979f64fab58848979d0f987fba0a71bc.LD4ioUYQd6laD8Dg")

# ====== 标题 ======
st.title("📚 英语四级智能学习助手")
st.caption("AI助力四级高分 🚀")

# ====== 功能 ======
option = st.selectbox("选择功能", ["📖 单词学习", "📄 阅读理解", "✍️ 作文批改"])

# ====== 输入方式 ======
input_mode = st.radio("输入方式", ["⌨️ 手动输入", "🎤 语音输入"])

user_input = ""

# ====== 语音输入（可选）======
if input_mode == "🎤 语音输入":
    st.info("点击开始录音，说一句英语（需麦克风）")
    if st.button("🎤 开始录音"):
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("录音中...")
            audio = r.listen(source)
            try:
                user_input = r.recognize_google(audio)
                st.success("识别结果：" + user_input)
            except:
                st.error("识别失败，请重试")

else:
    user_input = st.text_area("请输入内容：", height=200)

# ====== 按钮 ======
if st.button("🚀 开始分析"):
    if user_input:

        if option == "📖 单词学习":
            prompt = f"解释单词并给例句：{user_input}"

        elif option == "📄 阅读理解":
            prompt = f"翻译并总结：{user_input}"

        else:
            prompt = f"""
批改四级作文：
{user_input}
给评分（0-15）+ 修改建议
"""

        with st.spinner("AI分析中..."):
            response = client.chat.completions.create(
                model="glm-4",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content

        st.success("分析完成")
        st.write(result)

        # ====== 分数可视化（核心加分🔥）======
        if option == "✍️ 作文批改":
            import re
            match = re.search(r"\d+", result)
            if match:
                score = int(match.group())

                st.subheader("📊 作文评分可视化")

                fig, ax = plt.subplots()
                ax.bar(["你的分数"], [score])
                ax.set_ylim(0, 15)

                st.pyplot(fig)

        # ====== 学习建议 ======
        st.subheader("🧠 学习建议")
        st.info("建议每天练习30分钟阅读 + 背10个高频单词，坚持2周效果明显")

    else:
        st.warning("请输入内容")