import yt_dlp
import os
import subprocess

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def download_high_quality_video(url, output_path="."):
    ffmpeg_installed = check_ffmpeg()
    
    if ffmpeg_installed:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                },
                {
                    'key': 'FFmpegEmbedSubtitle',
                },
                {
                    'key': 'FFmpegMetadata',
                },
                {
                    'key': 'FFmpegPostProcessor',
                    'args': ['-codec:v', 'libx264', '-crf', '18', '-preset', 'slow', '-codec:a', 'aac', '-b:a', '192k'],
                },
            ],
        }
    else:
        print("ffmpeg is not installed. Downloading best available single-file format.")
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print("Fetching video information...")
            info = ydl.extract_info(url, download=False)
            title = info['title']
            print(f"Downloading: {title}")
            
            ydl.download([url])
            
            print(f"Download complete. File saved in {output_path}")
        except Exception as e:
            print(f"Error during download: {str(e)}")

def main():
    url = input("Enter the YouTube video URL: ")
    download_high_quality_video(url)

if __name__ == "__main__":
    main()