# Weather-Based-Daily-Task-Planner

# 🌤️ Weather-Based Daily Planner

A Streamlit-powered productivity web app that helps users plan their daily tasks while checking real-time weather conditions — ideal for outdoor planning, scheduling, and improving daily decisions.

---

## 📌 Overview

This project combines two daily needs into one simple tool:
- ✅ A **Task Manager** to create, categorize, and manage tasks with due dates.
- 🌦️ A **Weather Dashboard** that shows current temperature, humidity, wind speed, and AI-based suggestions like “Carry an umbrella!”



## 🚀 Live Demo

👉 [Click to View the Live App](https://your-username-weather-task-planner.streamlit.app)  



## 🔧 Features

- 🌍 **City-Based Weather**: View live weather updates using OpenWeatherMap API.
- 📝 **To-Do List**: Add, categorize, and mark tasks as complete.
- 📊 **Weather Visualization**: Line charts for temperature, humidity, and wind.
- 🤖 **AI Weather Tips**: Smart suggestions based on current weather (e.g., “Take a jacket!”).
- 💾 **Session State Storage**: Tasks are stored and persisted locally in `tasks.txt`.

---

## 🛠️ Technologies Used

| Layer         | Technology                  |
|--------------|------------------------------|
| Frontend     | Streamlit                    |
| Backend      | Python                       |
| API          | OpenWeatherMap               |
| Data Viz     | Plotly                       |
| Utils        | dotenv, datetime, requests   |

---

## 📁 Project Structure
weather_task_planner/
├── app.py # Main Streamlit app
├── requirements.txt # Dependencies
├── .env # Environment variables (your API key)
├── data/
│ └── tasks.txt # Local task storage
└── README.md # Project documentation


##Get your free OpenWeather API key
WEATHER_API_KEY=your_openweather_api_key

##Run the app
streamlit run app.py


💡 Sample Weather Suggestion Logic
If it’s raining → “Carry an umbrella!”
If temperature > 35°C → “Stay hydrated!”
If wind > 10 m/s → “Watch out for strong winds!”


🧠 Learning Outcomes
Used Streamlit to build interactive web apps
Integrated OpenWeatherMap API using requests
Applied Plotly for responsive line charts
Improved error handling, UX, and session state logic


📌 Future Enhancements
🌐 Deploy on Streamlit Cloud permanently
🔔 Add task reminders/notifications
🔐 User login for personalized task lists
📅 Sync tasks with Google Calendar
