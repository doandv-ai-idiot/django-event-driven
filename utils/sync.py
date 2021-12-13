import hashlib
import os
import shutil
from pathlib import Path

BLOCK_SIZE = 65536


def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCK_SIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCK_SIZE)
    return hasher.hexdigest()


def sync(source, dest):
    source_hashes = {}
    for folder, _, files in os.walk(source):
        for fn in files:
            source_hashes[hash_file(Path(folder) / fn)] = fn
    seen = set()
    for folder, _, files in os.walk(dest):
        for fn in files:
            dest_path = Path(folder) / fn
            dest_hash = hash_file(dest_path)
            seen.add(dest_hash)

            if dest_hash not in source_hashes:
                dest_path.remove()
            elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])
    for src_hash, fn in source_hashes.items():
        if src_hash not in seen:
            shutil.copy(Path(source) / fn, Path(dest) / fn)


# Abstract
def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


def determine_actions(source_hashes, dest_hashes, source, dest):
    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            source_path = Path(source) / filename
            dest_path = Path(dest) / filename
            yield 'copy', source_path, dest_path
        elif dest_hashes[sha] != filename:
            old_dest_path = Path(dest) / dest_hashes[sha]
            new_dest_path = Path(dest) / filename
            yield 'move', old_dest_path, new_dest_path
    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            yield 'delete', dest / filename


def sync_using_abstract(source, dest):
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)

    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    for action, *paths in actions:
        if action == 'copy':
            shutil.copyfile(*paths)
        if action == 'move':
            shutil.move(*paths)
        if action == 'delete':
            os.remove(paths[0])
