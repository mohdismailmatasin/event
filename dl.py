import os
import sys
import time
from tqdm import tqdm
import shutil
import threading
from queue import Queue
import argparse
import requests


def get_size(path):
    total_size = 0
    if os.path.isfile(path):
        total_size = os.path.getsize(path)
    else:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    return total_size


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Download/copy files or directories with progress bar.')
    parser.add_argument('destination', help='Destination path')
    parser.add_argument('source', help='Source path')
    parser.add_argument('--mirror', action='store_true', help='Mirror directory structure and attributes (default: True)')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Number of threads for parallel copy (default: 1)')
    args = parser.parse_args()
    return args


def copy_file_with_progress(src_file, dst_file, pbar, start_time, copied_ref, lock, mirror):
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
    with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
        while True:
            buf = fsrc.read(1024 * 1024)
            if not buf:
                break
            fdst.write(buf)
            with lock:
                copied_ref[0] += len(buf)
                elapsed = time.time() - start_time
                speed = copied_ref[0] / elapsed if elapsed > 0 else 0
                pbar.set_postfix({'Speed': f'{speed/1024/1024:.2f} MB/s', 'Percent': f'{copied_ref[0]/pbar.total*100:.2f}%'})
                pbar.update(len(buf))
    if mirror:
        shutil.copystat(src_file, dst_file)


def is_url(path):
    return path.startswith('http://') or path.startswith('https://')


def download_url_with_progress(url, dst):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    copied = 0
    start_time = time.time()
    with open(dst, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading', ncols=80, bar_format='{l_bar}{bar:30}| {percentage:3.0f}% [{n_fmt}/{total_fmt}, {elapsed}<{remaining}, {rate_fmt}]') as pbar:
        for chunk in response.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
                copied += len(chunk)
                elapsed = time.time() - start_time
                speed = copied / elapsed if elapsed > 0 else 0
                pbar.set_postfix({'Speed': f'{speed/1024/1024:.2f} MB/s', 'Percent': f'{copied/total_size*100:.2f}%'})
                pbar.update(len(chunk))


def download_with_progress(src, dst, mirror=True, threads=1):
    if is_url(src):
        # If destination is a directory, use the filename from the URL
        if os.path.isdir(dst):
            filename = os.path.basename(src)
            dst = os.path.join(dst, filename)
        download_url_with_progress(src, dst)
        return
    if not os.path.exists(src):
        print(f"Source '{src}' does not exist.")
        sys.exit(1)

    if os.path.isfile(src) and os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))

    total_size = get_size(src)
    copied = [0]
    start_time = time.time()
    lock = threading.Lock()

    try:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading', ncols=80, bar_format='{l_bar}{bar:30}| {percentage:3.0f}% [{n_fmt}/{total_fmt}, {elapsed}<{remaining}, {rate_fmt}]') as pbar:
            if os.path.isfile(src):
                copy_file_with_progress(src, dst, pbar, start_time, copied, lock, mirror)
            else:
                # Gather all files to copy
                file_pairs = []
                for dirpath, dirnames, filenames in os.walk(src):
                    rel_path = os.path.relpath(dirpath, src)
                    target_dir = os.path.join(dst, rel_path)
                    for filename in filenames:
                        src_file = os.path.join(dirpath, filename)
                        dst_file = os.path.join(target_dir, filename)
                        file_pairs.append((src_file, dst_file))
                # Multithreaded copy
                def worker():
                    while True:
                        try:
                            src_file, dst_file = q.get_nowait()
                        except Exception:
                            break
                        copy_file_with_progress(src_file, dst_file, pbar, start_time, copied, lock, mirror)
                        q.task_done()
                q = Queue()
                for pair in file_pairs:
                    q.put(pair)
                threads_list = []
                for _ in range(threads):
                    t = threading.Thread(target=worker)
                    t.start()
                    threads_list.append(t)
                q.join()
                if mirror:
                    for dirpath, dirnames, _ in os.walk(src):
                        rel_path = os.path.relpath(dirpath, src)
                        target_dir = os.path.join(dst, rel_path)
                        if os.path.exists(target_dir):
                            shutil.copystat(dirpath, target_dir)
    except Exception as e:
        print(f"Error during download: {e}")
        sys.exit(1)


if __name__ == '__main__':
    args = parse_args()
    download_with_progress(args.source, args.destination, mirror=args.mirror, threads=args.threads)
