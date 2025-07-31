from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .resume_utils import extract_resume_text, extract_keywords, calculate_match_score

def home(request):
    if request.method == 'POST':
        resume_file = request.FILES['resume']
        job_text = request.POST.get('job_desc')

        # Save resume temporarily
        fs = FileSystemStorage()
        filename = fs.save(resume_file.name, resume_file)
        resume_path = fs.path(filename)

        # AI logic
        resume_text = extract_resume_text(resume_path)
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_text)
        match_score = calculate_match_score(resume_keywords, job_keywords)

        return render(request, 'matcher/result.html', {
            'match_score': match_score,
            'resume_keywords': resume_keywords,
            'job_keywords': job_keywords,
        })

    return render(request, 'matcher/index.html')
