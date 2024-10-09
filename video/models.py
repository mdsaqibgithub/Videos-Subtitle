from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)  # Required title for the video
    video_file = models.FileField(upload_to='videos/')  # Video file storage path
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically add upload time

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)  # Link subtitles to a video
    subtitle_file = models.FileField(upload_to='subtitles/')  # Store subtitle file (.srt or .vtt)
    subtitle_text = models.TextField(blank=True, null=True)  # Optionally store extracted subtitle text

    def __str__(self):
        return f"Subtitle for {self.video.title}"
