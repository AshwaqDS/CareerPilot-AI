# 🚀 CareerPilot AI

### AI-Powered Career Assistant for Jobs, Resumes, Interviews & Career Planning

CareerPilot AI is an AI-powered career assistant built with **Python, Streamlit, and Google Gemini**. It helps students, fresh graduates, and job seekers with career planning, job recommendations, resume guidance, interview preparation, skill-gap analysis, and career roadmaps.

---

## ✨ Features

- 🎯 Job Recommendations
- 📄 Resume Guidance
- 🎤 Interview Preparation
- 🧠 Skill Gap Analysis
- 🗺️ Career Roadmaps
- 💬 AI Career Assistant

---

## 🛠️ Technology Stack

- **Python**
- **Streamlit**
- **Google Gemini / Google GenAI SDK**
- **python-dotenv**
- **Git & GitHub**
- **AWS EC2**
- **Ubuntu**

---

## 🏗️ Project Structure

```text
CareerPilot-AI/
├── app.py
├── config.py
├── prompts.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── src/
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AshwaqDS/CareerPilot-AI.git
cd CareerPilot-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Never upload your real API key to GitHub.

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## ☁️ AWS EC2 Deployment

CareerPilot AI is deployed on an **AWS EC2 Ubuntu server**.

### Deployment Steps

```bash
git clone https://github.com/AshwaqDS/CareerPilot-AI.git
cd CareerPilot-AI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

The AWS EC2 Security Group must allow **TCP port 8501** for external browser access.

### Deployment Flow

```text
Local Development
       ↓
GitHub
       ↓
AWS EC2
       ↓
Ubuntu
       ↓
Streamlit
       ↓
Web Browser
```

---

## 🌐 Live Deployment

### 🚀 CareerPilot AI

**Live Application:**  
http://51.21.181.245:8501

> The EC2 public IP may change if the instance is stopped and restarted unless an Elastic IP is configured.

---

## 💡 Example Queries

- What jobs can I apply for as a fresher?
- How can I improve my resume?
- Give me interview questions for a Data Analyst role.
- What skills should I learn to become a Data Analyst?
- Create a career roadmap for me.
- Analyze my current skills and identify my skill gaps.

---

## 🎯 Target Users

- 🎓 Students
- 👨‍🎓 Fresh Graduates
- 💼 Entry-Level Job Seekers
- 🔄 Career Changers
- 📈 Professionals

---

## 🔒 Security

Never commit sensitive information to GitHub.

```text
.env
*.pem
```

Never expose API keys, AWS private keys, passwords, or access tokens.

---

## 🚀 Future Improvements

- Real-time job search
- Resume upload and analysis
- Personalized job matching
- Advanced skill assessment
- Company-specific interview preparation
- Job application tracking
- Job alerts
- User authentication
- HTTPS production deployment

---

## 👨‍💻 Author

**Mohammed Ashwaq**

**GitHub:**  
https://github.com/AshwaqDS

**Project Repository:**  
https://github.com/AshwaqDS/CareerPilot-AI

---

## ⭐ Project

If you find CareerPilot AI useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is created for educational and portfolio purposes.

---

## 🙏 Acknowledgements

Built using **Python, Streamlit, Google Gemini, GitHub, and AWS EC2**.

---

### 🚀 CareerPilot AI

**An AI-powered assistant for career planning, job preparation, and professional development.**
