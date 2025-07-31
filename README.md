# 🔍 AI-Powered Resume & Job Matcher

A sophisticated Django web application that uses AI to match resumes with job descriptions, providing detailed analysis and actionable insights.

## ✨ Features

### 🎯 **Core Functionality**
- **AI-Powered Matching**: Uses KeyBERT and advanced NLP to extract and match keywords
- **Weighted Scoring**: Important skills (Python, React, AWS, etc.) are weighted higher
- **Synonym Matching**: Recognizes variations (JS = JavaScript, ML = Machine Learning)
- **PDF Processing**: Extracts text from PDF resumes with error handling

### 🎨 **Modern UI/UX**
- **Dark/Light Mode**: Toggle with persistent preference
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Animated Charts**: Smooth score animations with center labels
- **Drag & Drop**: Intuitive file upload with visual feedback
- **Loading Spinner**: Progress indicator during processing

### 🚀 **Advanced Features**
- **File Validation**: Checks PDF size (max 10MB) and type
- **Error Handling**: Clear error messages for various scenarios
- **Keyboard Shortcuts**: Ctrl+Enter to submit form
- **Form Persistence**: Content stays after submission
- **Auto Cleanup**: Temporary files deleted after processing

### 📊 **Enhanced Analysis**
- **Keyword Categorization**: Technical, soft skills, tools, etc.
- **Visual Feedback**: Color-coded badges for matched/missing keywords
- **Detailed Results**: Shows exact matched and missing keywords
- **Score Breakdown**: Weighted scoring based on keyword importance

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone the repository
git clone <https://github.com/Parth-Dhunde/resume_matcher>
cd resume_matcher

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to use the application.

## 📁 Project Structure

```
resume_matcher/
├── manage.py
├── requirements.txt
├── README.md
├── resume_matcher_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── matcher/
    ├── __init__.py
    ├── views.py
    ├── urls.py
    ├── resume_utils.py
    └── templates/
        └── matcher/
            └── index.html
```

## 🔧 Configuration

### Key Settings (settings.py)
- `DEBUG = True` for development
- `ALLOWED_HOSTS = []` for local development
- `MEDIA_ROOT` for file uploads
- `STATIC_URL` for static files

### Environment Variables
Create a `.env` file for production:
```
SECRET_KEY=ph41kpas3z
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

## 🚀 Deployment

### Local Development
```bash
python manage.py runserver
```

### Production (using Gunicorn)
```bash
pip install gunicorn
gunicorn resume_matcher_project.wsgi
```

### Docker (optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "resume_matcher_project.wsgi"]
```

## 🎯 How It Works

### 1. **File Upload & Validation**
- User uploads PDF resume (max 10MB)
- System validates file type and size
- Drag & drop support with visual feedback

### 2. **Text Extraction**
- PDF text extraction using pdfminer
- Error handling for password-protected files
- Text cleaning and normalization

### 3. **Keyword Analysis**
- KeyBERT extracts relevant keywords
- Synonym matching for common variations
- Weighted scoring for important skills

### 4. **Matching Algorithm**
- Jaccard similarity for keyword matching
- Weighted scoring based on keyword importance
- Detailed matched/missing keyword analysis

### 5. **Results Display**
- Animated chart with score visualization
- Color-coded keyword badges
- Clear success/error feedback

## 🎨 UI Features

### **Dark Mode**
- Toggle between light and dark themes
- Persistent preference storage
- Smooth color transitions

### **Responsive Design**
- Mobile-first approach
- Adaptive layouts for all screen sizes
- Touch-friendly interface

### **Animations**
- Smooth fade-in effects
- Animated chart loading
- Progressive badge animations

### **User Experience**
- Loading spinners during processing
- Progress indicators
- Clear error messages
- Keyboard shortcuts

## 🔍 Technical Details

### **AI/ML Components**
- **KeyBERT**: Keyword extraction using BERT embeddings
- **Scikit-learn**: Cosine similarity calculations
- **PDFMiner**: PDF text extraction
- **Sentence Transformers**: Advanced NLP processing

### **Performance Optimizations**
- File cleanup after processing
- Efficient keyword extraction
- Cached model loading
- Responsive UI updates

### **Security Features**
- File type validation
- Size limits (10MB max)
- CSRF protection
- Input sanitization

## 🐛 Troubleshooting

### Common Issues

**1. PDF not processing**
- Ensure PDF is not password-protected
- Check file size (max 10MB)
- Verify PDF is not corrupted

**2. No keywords extracted**
- Provide more detailed job description
- Ensure resume has sufficient text content
- Check for special characters

**3. Low match scores**
- Add more relevant keywords to job description
- Ensure resume includes required skills
- Consider industry-specific terminology

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **KeyBERT** for keyword extraction
- **Bootstrap** for responsive design
- **Chart.js** for data visualization
- **Django** for the web framework

---

**Made with ❤️ for better job matching**
