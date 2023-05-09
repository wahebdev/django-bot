import os


import ffmpeg
from subprocess import check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import asyncio




def get_codec(filepath, channel='v:0'):
    output = check_output(['ffprobe', '-v', 'error', '-select_streams', channel,
                           '-show_entries', 'stream=codec_name,codec_tag_string', '-of',
                           'default=nokey=1:noprint_wrappers=1', filepath])
    return output.decode('utf-8').split()


async def run(cmd: str):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')


async def encode(filepath, output_filepath):

    if os.path.isfile(output_filepath):
        print('Skipping "{}": file already exists'.format(output_filepath))
        return output_filepath
    print(filepath)
    # Get the video channel codec
    video_codec = get_codec(filepath, channel='v:0')
    if video_codec == []:
        print('Skipping: no video codec reported')
        return None
    video_opts = '-preset ultrafast -c:v libx265 -crf 27 -map 0:v'

    audio_codec = get_codec(filepath, channel='a:0')
    if audio_codec == []:
        audio_opts = ''
    elif audio_codec[0] == 'aac':
        audio_opts = '-c:a copy -map 0:a'
    else:
        audio_opts = '-c:a aac -map 0:a'
    subtitle_opts = " -c:s copy -map 0:s? "
    cmdl = (['ffmpeg', '-i', filepath] + video_opts.split() + audio_opts.split() + subtitle_opts.split() + [
        output_filepath, '-y'])
    cmd = ' '.join(cmdl)
    await run(cmd)
    return output_filepath


def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, in_filename + ".jpg")
    os.makedirs(path, exist_ok=True)
    open(out_filename, 'a').close()
    try:
        (
            ffmpeg
                .input(in_filename, ss=ttl)
                .output(out_filename, vframes=1)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
        return None


def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
        return metadata.get('duration').seconds
    else:
        return 0


def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
        return metadata.get("width"), metadata.get("height")
    else:
        return 1280, 720
