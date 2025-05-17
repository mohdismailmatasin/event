import os
import sys
import time
from tqdm import tqdm
import shutil

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

def move_with_progress(src, dst):
    if not os.path.exists(src):
        print(f"Source '{src}' does not exist.")
        sys.exit(1)

    # If moving a file to a directory, adjust dst
    if os.path.isfile(src) and os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))

    total_size = get_size(src)
    copied = 0
    start_time = time.time()

    try:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc='Moving', ncols=80, bar_format='{l_bar}{bar:30}| {percentage:3.0f}% [{n_fmt}/{total_fmt}, {elapsed}<{remaining}, {rate_fmt}]') as pbar:
            if os.path.isfile(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                    while True:
                        buf = fsrc.read(1024 * 1024)
                        if not buf:
                            break
                        fdst.write(buf)
                        copied += len(buf)
                        elapsed = time.time() - start_time
                        speed = copied / elapsed if elapsed > 0 else 0
                        pbar.set_postfix({'Speed': f'{speed/1024/1024:.2f} MB/s', 'Percent': f'{copied/total_size*100:.2f}%'})
                        pbar.update(len(buf))
                shutil.copystat(src, dst)
                os.remove(src)
            else:
                for dirpath, dirnames, filenames in os.walk(src):
                    rel_path = os.path.relpath(dirpath, src)
                    target_dir = os.path.join(dst, rel_path)
                    os.makedirs(target_dir, exist_ok=True)
                    for filename in filenames:
                        src_file = os.path.join(dirpath, filename)
                        dst_file = os.path.join(target_dir, filename)
                        with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
                            while True:
                                buf = fsrc.read(1024 * 1024)
                                if not buf:
                                    break
                                fdst.write(buf)
                                copied += len(buf)
                                elapsed = time.time() - start_time
                                speed = copied / elapsed if elapsed > 0 else 0
                                pbar.set_postfix({'Speed': f'{speed/1024/1024:.2f} MB/s', 'Percent': f'{copied/total_size*100:.2f}%'})
                                pbar.update(len(buf))
                        shutil.copystat(src_file, dst_file)
                        os.remove(src_file)
                shutil.rmtree(src)
    except Exception as e:
        print(f"Error during move: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: python {os.path.basename(sys.argv[0])} <source> <destination>')
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]
    move_with_progress(src, dst)
