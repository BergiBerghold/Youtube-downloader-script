from datetime import timedelta
import pytube
import glob
import time
import os

output_dir = 'tracks_set_3'
max_retries = 5


def download(url, path):
    yt = pytube.YouTube(url)
    video = yt.streams.filter(only_audio=True).first()

    out_file = video.download(output_path=path)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)


with open('tracklist_set_3.txt', 'r') as f:
    song_names = f.readlines()

song_names = [x.strip() for x in song_names]

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

downloaded_tracks = glob.glob(f'{output_dir}/*.mp3')
downloaded_tracks = [x.split('/')[-1][:-4] for x in downloaded_tracks]

start_time = time.perf_counter()
download_counter = 0

song_names = song_names[90:]

for idx, song_name in enumerate(song_names):
    for i in range(max_retries):
        try:
            s = pytube.Search(song_name)
        except Exception as e:
            print(f'Exception while searching caught: {e}')
        else:
            break

    title = s.results[0].title
    url = s.results[0].watch_url

    if title in downloaded_tracks:
        print(f'Track "{title}" already downloaded. Skipping...')
        continue

    print(f'Downloading track "{title}" - File {idx+1}/{len(song_names)}')

    if download_counter != 0:
        remaining_files = len(song_names) - idx
        remaining_time = (time.perf_counter() - start_time) / download_counter * remaining_files

        print(f'Remaining total time est. {timedelta(seconds=remaining_time)}')

    print('')

    for i in range(max_retries):
        try:
            download(s.results[0].watch_url, output_dir)
        except Exception as e:
            print(f'Exception while downloading caught: {e}')
        else:
            break

    download_counter += 1
