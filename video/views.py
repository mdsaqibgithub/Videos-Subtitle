import re, os
from django.shortcuts import redirect, render, get_object_or_404
from .forms import VideoUploadForm
from .models import Subtitle, Video
import subprocess

# View to handle video upload
def upload_video(request):
     # Handle video upload
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            process_video(video)
            return redirect('upload_video')  # Refresh the page after uploading

    else:
        form = VideoUploadForm()

    # List all uploaded videos
    videos = Video.objects.all()

    return render(request, 'upload.html', {'form': form, 'videos': videos})

# Function to process the uploaded video and extract subtitles using FFmpeg


def process_video(video):
    video_path = video.video_file.path
    srt_subtitle_path = f'{os.path.splitext(video_path)[0]}.srt'  # .srt file path
    vtt_subtitle_path = f'{os.path.splitext(video_path)[0]}.vtt'  # .vtt file path

    # Command to extract subtitles from video using FFmpeg
    command = ['ffmpeg', '-i', video_path, '-map', '0:s:0', srt_subtitle_path]

    try:
        # Run FFmpeg command to extract .srt subtitles
        subprocess.run(command, check=True)

        # If FFmpeg successfully created the .srt file, convert it to .vtt
        if os.path.exists(srt_subtitle_path):
            with open(srt_subtitle_path, 'r', encoding='utf-8') as srt_file:
                srt_content = srt_file.read()

            # Create the .vtt file and convert the .srt content to .vtt format
            with open(vtt_subtitle_path, 'w', encoding='utf-8') as vtt_file:
                vtt_file.write("WEBVTT\n\n")  # Add WebVTT header
                vtt_file.write(srt_content.replace(",", "."))  # Replace commas with periods for timing

            # Save the .vtt subtitle file in the database
            Subtitle.objects.create(video=video, subtitle_file=vtt_subtitle_path)

    except subprocess.CalledProcessError:
        print(f"Failed to process subtitles for video: {video.title}")
    except Exception as e:
        print(f"Error occurred: {e}")




# View to display the list of uploaded videos
def video_list(request):
    videos = Video.objects.all()  # Get all video objects from the database
    return render(request, 'video_list.html', {'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    subtitles = Subtitle.objects.filter(video=video).first()

    if subtitles:
        # Replace .srt with .vtt in the subtitle file URL
        subtitle_url = subtitles.subtitle_file.url.replace('.srt', '.vtt')
    else:
        subtitle_url = None

    return render(request, 'detail.html', {
        'video': video,
        'subtitle_url': subtitle_url,
        'subtitles': subtitles
    })

def search_subtitles(request, video_id):
    query = request.GET.get('query')
    video = get_object_or_404(Video, id=video_id)
    subtitle = Subtitle.objects.filter(video=video).first()

    if subtitle and query:
        # Open and search the subtitle file
        with open(subtitle.subtitle_file.path, 'r') as f:
            subtitles_content = f.read()

        # Use regex to find matching lines
        matches = re.findall(r"(\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}\n.*%s.*\n)" % re.escape(query), subtitles_content, re.IGNORECASE)
        return render(request, 'search_results.html', {
            'video': video,
            'query': query,
            'matches': matches
        })

    return render(request, 'search_results.html', {
        'video': video,
        'query': query,
        'matches': []
    })
