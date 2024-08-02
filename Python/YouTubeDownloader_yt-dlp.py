print("Загрузка библиотек, пожалуйста, подождите", end="...", flush=True)
import yt_dlp
import os
import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
print(" готово!\n")

def download_youtube_video(url, resolution, output_path):
    try:
        print(f"Connecting to {url}")

        # Конфигурация yt_dlp для скачивания видео и аудио отдельно
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio',
            'outtmpl': {
                'audio': os.path.join(output_path, '%(title)s_audio.%(ext)s'),
                'video': os.path.join(output_path, '%(title)s_video.%(ext)s'),
                'default': os.path.join(output_path, '%(title)s_%(resolution)s.%(ext)s')
            },
            'noprogress': False,
            'progress_hooks': [lambda d: print(d['status'], d.get('downloaded_bytes', 0), 'bytes downloaded') if d['status'] == 'downloading' else None],
            'postprocessors': [{
                'key': 'FFmpegMetadata',
            }],
        }

        print(f"Start downloading VIDEO as '{output_path}/video.mp4'")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            # Paths to downloaded files
            video_file = os.path.join(output_path, ydl.prepare_filename({'title': '%(title)s', 'resolution': resolution, 'ext': 'video.%(ext)s'}))
            audio_file = os.path.join(output_path, ydl.prepare_filename({'title': '%(title)s', 'resolution': resolution, 'ext': 'audio.%(ext)s'}))
            output_file = os.path.join(output_path, ydl.prepare_filename({'title': '%(title)s', 'resolution': resolution, 'ext': 'mp4'}))

        print(f"\nVideo and audio are saved separately in {output_path}")
        print(f"Merging video and audio into {output_file}")

        # Merge video and audio
        ffmpeg_merge_video_audio(video_file, audio_file, output_file, vcodec='copy', acodec='aac', ffmpeg_output=True)

        print(f"\nFinal video saved as {output_file}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Please enter the required parameters.")
        url = input("Enter YouTube video URL: ")
        resolution = input("Enter desired resolution (e.g., 1080p): ")
        output_path = input("Enter the path to save the video: ")
    else:
        url = sys.argv[1]
        resolution = sys.argv[2]
        output_path = sys.argv[3]

    download_youtube_video(url, resolution, output_path)
