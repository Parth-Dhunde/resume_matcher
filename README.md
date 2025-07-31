# 🧠 AI-Powered Resume & Job Matching Advisor

This Django web application uses Natural Language Processing (NLP) to analyze and match a candidate's resume against a given job description. It extracts key information from the resume (in PDF format) and the job description text and provides a **match percentage score** to help determine the best fit.

---

## 🚀 Features

- 📄 Upload PDF resumes
- 📝 Paste or type job descriptions
- 🔍 Extracts keywords from both sources using `KeyBERT`
- 📊 Calculates a match percentage using **cosine similarity**
- 🧠 Built with AI/NLP tools like `pdfminer`, `KeyBERT`, and `scikit-learn`
- 🌐 Django backend with clean interface

---

## 🛠️ Tech Stack

- 🐍 Python 3
- 🌐 Django 5.x
- 📄 pdfminer.six
- 🔍 KeyBERT
- 🤖 scikit-learn
- 🧠 NLP & AI for keyword extraction and matching

---

## 📦 Installation

### 🔹 Clone the Repository

```bash
git clone https://github.com/Parth-Dhunde/resume_matcher.git
cd resume_matcher
