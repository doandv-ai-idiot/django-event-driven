import shutil
import tempfile
from pathlib import Path
from sync import sync, determine_actions


# def test_when_a_file_exists_in_the_source_but_not_the_destination():
#     try:
#         source = tempfile.mkdtemp()
#         dest = tempfile.mkdtemp()
#         content = "I am students"
#         (Path(source) / 'my-file.txt').write_text(content)
#         sync(source, dest)
#         expected_path = Path(dest) / "my-file.txt"
#         assert expected_path.exists()
#         assert expected_path.read_text() == content
#     finally:
#         shutil.rmtree(source)
#         shutil.rmtree(dest)
#
#
# def test_when_a_file_has_been_renamed_in_the_source():
#     try:
#         source = tempfile.mkdtemp()
#         dest = tempfile.mkdtemp()
#         content = "I am students"
#         source_path = Path(source) / 'source_filename.txt'
#         old_dest_path = Path(dest) / 'dest_filename.txt'
#         expected_dest_path = Path(dest) / 'source_filename.txt'
#         source_path.write_text(content)
#         old_dest_path.write_text(content)
#         sync(source, dest)
#         assert old_dest_path.exists() is False
#         assert expected_dest_path.read_text() == content
#     finally:
#         shutil.rmtree(source)
#         shutil.rmtree(dest)


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    src_hashes = {"hash1": "fn1"}
    dst_hashes = {}
    actions = determine_actions(src_hashes, dst_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("copy", Path("/src/fn1"), Path("/dst/fn1"))]


def test_when_a_file_has_been_renamed_in_the_source():
    src_hashes = {"hash1": "fn1"}
    dst_hashes = {"hash1": "fn2"}
    actions = determine_actions(src_hashes, dst_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("move", Path("/dst/fn2"), Path("/dst/fn1"))]
