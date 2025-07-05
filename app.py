import streamlit as st
import requests
import os
from datetime import date
from dotenv import load_dotenv
import plotly.graph_objects as go

# ──────────────────────────────────────────────
# 1. Load API key and configure page
# ──────────────────────────────────────────────

API_KEY = st.secrets["general"]["WEATHER_API_KEY"]
st.sidebar.write("🔑 API KEY:", API_KEY)


st.set_page_config(page_title="Daily Weather Planner", page_icon="🌦️", layout="wide")

# Hide Streamlit menu & footer
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 2. Sidebar inputs
# ──────────────────────────────────────────────
st.sidebar.header("🌍 Weather Settings")
city = st.sidebar.text_input("City", "Bangalore")
unit = st.sidebar.radio("Units", ["Celsius", "Fahrenheit"])
show_weather = st.sidebar.checkbox("Show Weather Card", value=True)

# ──────────────────────────────────────────────
# 3. Utility Functions
# ──────────────────────────────────────────────
@st.cache_data(ttl=1800)
def fetch_weather(city, unit):
    unit_param = "metric" if unit == "Celsius" else "imperial"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit_param}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def weather_icon(code: str) -> str:
    mapping = {"2": "⛈️", "3": "🌦️", "5": "🌧️", "6": "❄️", "7": "🌫️", "800": "☀️", "80": "☁️"}
    return mapping.get(code[:1], "🌡️") if code != "800" else mapping["800"]

def generate_weather_tip(weather):
    desc = weather["weather"][0]["main"].lower()
    wind = weather["wind"]["speed"]
    humidity = weather["main"]["humidity"]
    if "rain" in desc: return "☔ Carry an umbrella — it's rainy!"
    if "snow" in desc: return "❄️ Bundle up, it's snowing!"
    if "clear" in desc: return "😎 Clear skies ahead — perfect for outdoor plans!"
    if "cloud" in desc: return "⛅ Might be gloomy, plan accordingly."
    if "storm" in desc: return "⚡ Stay safe — storm approaching."
    if wind > 10: return "💨 Windy outside — secure loose items!"
    if humidity > 85: return "🌫️ High humidity — stay hydrated."
    return "🌍 Weather looks fine — have a great day!"

# ──────────────────────────────────────────────
# 4. Weather Display
# ──────────────────────────────────────────────
if show_weather:
    weather = fetch_weather(city, unit)
    if weather and weather.get("main"):
        icon = weather_icon(str(weather["weather"][0]["id"]))
        desc = weather["weather"][0]["description"].title()
        temp = weather["main"]["temp"]
        feels_like = weather["main"]["feels_like"]
        humidity = weather["main"]["humidity"]
        wind = weather["wind"]["speed"]

        # Responsive font sizes (mobile-friendly)
        st.markdown("""
            <style>
            .main-title   {font-size:8vw;line-height:1.1;margin:0;}
            .sub-title    {font-size:5vw;margin:0 0 12px 0;}
            @media(min-width:768px){
                .main-title{font-size:48px;}
                .sub-title{font-size:24px;}
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<p class='main-title'>{icon} {temp}°{unit[0]}</p>"
            f"<p class='sub-title'>{desc}</p>",
            unsafe_allow_html=True
        )

        # Weather chart
        metrics = {
            f"Feels Like (°{unit[0]})": feels_like,
            "Humidity (%)": humidity,
            "Wind Speed (m/s)": wind
        }
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(metrics.keys()),
            y=list(metrics.values()),
            mode='lines+markers',
            line=dict(color='royalblue', width=3),
            marker=dict(size=10, color='orange')
        ))
        fig.update_layout(
            title="📈 Weather Conditions Overview",
            height=300,
            margin=dict(l=10, r=10, t=40, b=20),
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

        tip = generate_weather_tip(weather)
        st.success(f"🧠 Smart Tip: {tip}")
    else:
        st.warning("⚠️ Weather data not available. Check city or API key.")

# ──────────────────────────────────────────────
# 5. Task Manager Section
# ──────────────────────────────────────────────
st.subheader("📝 Task Manager")

DATA_PATH = "data"
TASK_FILE = os.path.join(DATA_PATH, "tasks.txt")
os.makedirs(DATA_PATH, exist_ok=True)
if not os.path.exists(TASK_FILE):
    open(TASK_FILE, "w", encoding="utf-8").close()

# Load tasks
if "tasks" not in st.session_state:
    with open(TASK_FILE, "r", encoding="utf-8") as f:
        raw = [line.strip() for line in f if line.strip()]
    st.session_state.tasks = [
        {"text": t.split("|")[0], "date": t.split("|")[1], "cat": t.split("|")[2]}
        if "|" in t else {"text": t, "date": str(date.today()), "cat": "General"}
        for t in raw
    ]

# Add task
with st.expander("➕ Add New Task"):
    new_text = st.text_input("Task description")
    col1, col2 = st.columns(2)
    with col1:
        due_date = st.date_input("Due date", value=date.today())
    with col2:
        category = st.selectbox("Category", ["General", "Work", "Personal"])
    if st.button("Add Task"):
        if new_text:
            st.session_state.tasks.append({"text": new_text, "date": str(due_date), "cat": category})
            with open(TASK_FILE, "a", encoding="utf-8") as f:
                f.write(f"{new_text}|{due_date}|{category}\n")
            st.success("✅ Task added successfully.")
        else:
            st.warning("Please enter a task description.")

# Show tasks
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        checked = st.checkbox(
            f"**{task['text']}** _(due {task['date']}, {task['cat']})_",
            key=f"task_{i}"
        )
        if checked:
            st.session_state.tasks.pop(i)
            with open(TASK_FILE, "w", encoding="utf-8") as f:
                for t in st.session_state.tasks:
                    f.write(f"{t['text']}|{t['date']}|{t['cat']}\n")
            st.rerun()
else:
    st.info("No tasks yet. Use **Add New Task** above.")

st.markdown("---")
st.caption("🚀 Built with Streamlit • Weather from OpenWeatherMap")

