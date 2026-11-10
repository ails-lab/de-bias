"""Rebuilds the production model directory from models/manifest.tsv.

    python models/fetch_models.py TARGET

TARGET becomes STANZA_RESOURCES_DIR. The Hugging Face models that Stanza's POS and NER models load
go to TARGET/huggingface. Run the app with HF_HOME=TARGET/huggingface and HF_HUB_OFFLINE=1, so
transformers uses these pinned revisions instead of fetching whatever is newest.

Every file is pinned by commit, never by tag: Stanza has re-pushed models under an existing version
tag (stanza-fr v1.10.0 moved past the lemma model production uses). The *_customized.pt lemma models
are rebuilt with model_preprocessing/, so run this with the app's dependencies installed; they only
come out byte-identical with the pinned torch version. Files that already exist are skipped.
Afterwards every file is checked against its sha256 in the manifest, and the script exits non-zero
on any mismatch. Generated files are only checked on Linux: torch.save writes a .data/serialization_id
record that is built by iterating a std::unordered_set of record names, so it depends on the C++
standard library. Their contents are the same on macOS, but the file hashes differ.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO_ROOT, 'models', 'manifest.tsv')


def read_manifest():
    with open(MANIFEST) as fp:
        return [line.rstrip('\n').split('\t') for line in fp if not line.startswith('#')]


def destination(target, kind, path, source):
    if kind == 'huggingface':
        repo, commit = source.split('@')
        return os.path.join(target, 'huggingface', 'hub', 'models--' + repo.replace('/', '--'),
                            'snapshots', commit, path[len(repo) + 1:])
    return os.path.join(target, path)


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + '.part'
    with urllib.request.urlopen(url) as r, open(tmp, 'wb') as fp:
        shutil.copyfileobj(r, fp, 1 << 20)
    os.replace(tmp, dest)


def fetch(target, rows):
    for kind, path, _, source in rows:
        dest = destination(target, kind, path, source)
        if os.path.isfile(dest):
            continue
        if kind == 'stanza':
            repo, commit = source.split('@')
            print(f'downloading {path}')
            # stanza-{lang} repos keep files under models/ without the language prefix.
            download(f'https://huggingface.co/{repo}/resolve/{commit}/models/{path.split("/", 1)[1]}', dest)
        elif kind == 'huggingface':
            repo, commit = source.split('@')
            print(f'downloading {path}')
            download(f'https://huggingface.co/{repo}/resolve/{commit}/{path[len(repo) + 1:]}', dest)
            # transformers resolves the 'main' revision through this file when offline.
            refs = os.path.join(target, 'huggingface', 'hub', 'models--' + repo.replace('/', '--'), 'refs')
            os.makedirs(refs, exist_ok=True)
            with open(os.path.join(refs, 'main'), 'w') as fp:
                fp.write(commit)
        elif kind == 'file':
            print(f'copying {path}')
            shutil.copyfile(os.path.join(REPO_ROOT, source), dest)

    # Generated models patch downloaded ones, so they run after every download.
    for kind, path, _, source in rows:
        if kind == 'generated' and not os.path.isfile(os.path.join(target, path)):
            print(f'generating {path}')
            subprocess.run([sys.executable, source], cwd=REPO_ROOT, check=True,
                           env={**os.environ, 'STANZA_RESOURCES_DIR': target})


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def verify(target, rows):
    mismatched = []
    for kind, path, expected, source in rows:
        dest = destination(target, kind, path, source)
        if sha256(dest) != expected:
            mismatched.append(dest)
    return mismatched


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('target')
    args = parser.parse_args()
    target = os.path.abspath(args.target)
    rows = read_manifest()
    fetch(target, rows)
    if sys.platform != 'linux':
        print('not on Linux: skipping the sha256 check of generated files')
        rows = [row for row in rows if row[0] != 'generated']
    mismatched = verify(target, rows)
    if mismatched:
        sys.exit('sha256 does not match models/manifest.tsv:\n  ' + '\n  '.join(mismatched))
    print(f'{len(rows)} files match models/manifest.tsv')


if __name__ == '__main__':
    main()
