#!/usr/bin/env python
"""
Script to update existing scholarships with internal application settings
Run: python update_scholarships.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarmatch_project.settings')
django.setup()

from scholarships.models import Scholarship

# Update all scholarships to use internal application
scholarships = Scholarship.objects.all()
updated_count = 0

for scholarship in scholarships:
    # Set default requirements based on program level
    if not scholarship.required_documents:
        if scholarship.program_level == 'phd':
            scholarship.required_documents = ['transcript', 'cv_resume', 'statement_of_purpose', 'research_proposal', 'letters_of_recommendation']
            scholarship.required_forms = ['research_interests', 'career_goals']
        elif scholarship.program_level == 'masters':
            scholarship.required_documents = ['transcript', 'cv_resume', 'statement_of_purpose', 'letters_of_recommendation']
            scholarship.required_forms = ['personal_statement']
        else:
            scholarship.required_documents = ['transcript', 'cv_resume', 'statement_of_purpose']
            scholarship.required_forms = ['personal_statement']
    
    # Enable internal application
    scholarship.use_internal_application = True
    scholarship.save()
    updated_count += 1
    print(f"Updated: {scholarship.title}")

print(f"\nSuccessfully updated {updated_count} scholarships!")
print("\nNow you can:")
print("1. Go to any scholarship detail page")
print("2. Click 'Apply Now' button")
print("3. See the dynamic application form with required documents/forms")

