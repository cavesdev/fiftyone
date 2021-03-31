"""
Sample media utilities.

| Copyright 2017-2021, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import multiprocessing

import eta.core.utils as etau
import eta.core.video as etav

import fiftyone.core.utils as fou


# Valid media types
# @todo convert to a MediaType enum class?
VIDEO = "video"
IMAGE = "image"
MEDIA_TYPES = {IMAGE, VIDEO}


def get_media_type(filepath):
    """Gets the media type for the given filepath.

    Args:
        filepath: a filepath

    Returns:
        the media type
    """
    # @todo use `etav.is_supported_video_file` instead?
    if etav.is_video_mime_type(filepath):
        return VIDEO

    # @todo don't assume all non-video samples are images!
    return IMAGE


def export_media(inpaths, outpaths, move_media=False, num_workers=None):
    """Exports the media at the given input paths to the given output paths.

    Args:
        inpaths: the list of input paths
        outpaths: the list of output paths
        move_media (False): whether to move (True) or copy (False) the source
            media into its output destination
        num_workers (None): the number of processes to use. By default,
            ``multiprocessing.cpu_count()`` is used
    """
    num_files = len(inpaths)
    if num_files == 0:
        return

    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    inputs = list(zip(inpaths, outpaths))
    op = _do_move_file if move_media else _do_copy_file

    with fou.ProgressBar(total=num_files, iters_str="files") as pb:
        with multiprocessing.Pool(processes=num_workers) as pool:
            for _ in pb(pool.imap_unordered(op, inputs)):
                pass


def _do_move_file(args):
    inpath, outpath = args
    etau.move_file(inpath, outpath)


def _do_copy_file(args):
    inpath, outpath = args
    etau.copy_file(inpath, outpath)


class MediaTypeError(TypeError):
    """Exception raised when a problem with media types is encountered."""

    pass
