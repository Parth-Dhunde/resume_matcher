import os
import re
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import JsonResponse
from .resume_utils import extract_resume_text, extract_keywords, calculate_match_score, validate_pdf_file

def home(request):
    print(f"Request method: {request.method}")
    print(f"POST data keys: {list(request.POST.keys())}")
    print(f"FILES data keys: {list(request.FILES.keys())}")
    
    if request.method == 'POST':
        if 'clear' in request.POST:
            return redirect(request.path)
        
        # Get uploaded resume and job description
        resume_file = request.FILES.get('resume')
        job_description = request.POST.get('job_description', '')
        resume_filename = resume_file.name if resume_file else ''
        
        print(f"Processing request - Resume: {resume_filename}, Job desc length: {len(job_description)}")
        
        # Initialize variables
        match_score = None
        remaining_score = None
        matched_keywords = []
        missing_keywords = []
        error_message = None
        
        if resume_file and job_description:
            print("Both resume and job description provided")
            
            # Validate file
            if not validate_pdf_file(resume_file):
                error_message = "Please upload a valid PDF file (max 10MB)."
                print("File validation failed")
            else:
                print("File validation passed")
                try:
                    # Save resume file temporarily
                    fs = FileSystemStorage()
                    filename = fs.save(resume_file.name, resume_file)
                    resume_path = fs.path(filename)
                    print(f"Saved file to: {resume_path}")
                    
                    # Extract text from PDF
                    resume_text = extract_resume_text(resume_path)
                    print(f"Extracted text length: {len(resume_text)}")
                    
                    if not resume_text.strip():
                        error_message = "Could not extract text from PDF. Please ensure it's not password-protected."
                        print("No text extracted from PDF")
                    else:
                        # Extract keywords from both resume and job description
                        print("Extracting keywords from resume...")
                        resume_keywords = extract_keywords(resume_text)
                        print(f"Resume keywords: {resume_keywords}")
                        
                        print("Extracting keywords from job description...")
                        job_keywords = extract_keywords(job_description)
                        print(f"Job keywords: {job_keywords}")
                        
                        if not job_keywords:
                            error_message = "Could not extract keywords from job description. Please provide more detailed description."
                            print("No job keywords extracted")
                        else:
                            # Calculate the match score and get matched/missing keywords
                            print("Calculating match score...")
                            match_score, matched_keywords, missing_keywords = calculate_match_score(resume_keywords, job_keywords)
                            remaining_score = 100 - match_score
                            print(f"Match score calculated: {match_score}%")
                            
                            # Clean up temporary file
                            try:
                                os.remove(resume_path)
                                print("Temporary file cleaned up")
                            except:
                                print("Could not clean up temporary file")
                                pass
                                
                except Exception as e:
                    error_message = f"Error processing file: {str(e)}"
                    print(f"Exception occurred: {e}")
                    # Clean up on error
                    try:
                        if 'resume_path' in locals():
                            os.remove(resume_path)
                            print("Cleaned up file on error")
                    except:
                        print("Could not clean up file on error")
                        pass
        else:
            print("Missing resume or job description")
            if not resume_file:
                error_message = "Please upload a PDF resume."
            elif not job_description:
                error_message = "Please provide a job description."
        
        print(f"Final results - Score: {match_score}, Matched: {len(matched_keywords)}, Missing: {len(missing_keywords)}, Error: {error_message}")
        
        # Pass values to the template
        return render(request, 'matcher/index.html', {
            'match_score': match_score,
            'remaining_score': remaining_score,
            'matched_keywords': matched_keywords,
            'missing_keywords': missing_keywords,
            'job_description': job_description,
            'resume_filename': resume_filename,
            'error_message': error_message,
        })
    
    # If GET request, just render the form
    return render(request, 'matcher/index.html')

def ajax_process(request):
    """AJAX endpoint for processing with progress updates"""
    if request.method == 'POST':
        # Simulate processing steps
        return JsonResponse({
            'status': 'processing',
            'progress': 50,
            'message': 'Analyzing resume...'
        })
    return JsonResponse({'error': 'Invalid request'})