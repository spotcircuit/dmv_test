import os
import shutil

# Create archive directory
archive_dir = 'archive'
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

# Files to archive
files_to_archive = [
    'VA_DMV_100_Unique_Questions_Quiz.py',
    'quiz_data.py',
    'templates/test.html.bak'
]

# Move files to archive
for file in files_to_archive:
    if os.path.exists(file):
        shutil.move(file, os.path.join(archive_dir, os.path.basename(file)))
