import re
import itertools
import datetime
import argparse

from pymediainfo import MediaInfo

parser = argparse.ArgumentParser(description='Cue sheet to tracklist')
parser.add_argument('cue_file', help='Cue sheet file')
parser.add_argument('audio_file', help='CD Rip audio file')
args = parser.parse_args()
cue, audio = args.cue_file, args.audio_file

with open(cue, 'r') as f:
    lines = f.readlines()

titles = list(
    itertools.chain.from_iterable(
        [re.findall('TITLE "(.*)"', l) for l in lines]))
performers = list(
    itertools.chain.from_iterable(
        [re.findall('PERFORMER "(.*)"', l) for l in lines]))
offsets = [
    datetime.datetime.strptime(o[:-3], "%M:%S")
    for o in list(
        itertools.chain.from_iterable(
            [re.findall('INDEX .{2} (.*)', l) for l in lines]))
]

media_info = MediaInfo.parse(audio)
audio_tracks = [t for t in media_info.tracks if t.track_type == 'Audio']

offsets.append(
    datetime.datetime.strptime(audio_tracks[0].other_duration[0],
                               "%M min %S s"))

durations = [offset[1] - offset[0] for offset in zip(offsets, offsets[1:])]

if (len(titles) == len(performers)):
    print("{} - {}".format(titles[0], performers[0]))
    performers = performers[1:]
else:
    print("{}".format(titles[0]))

titles = titles[1:]

for idx, track in enumerate(zip(titles, performers, durations)):
    print("{}. {} - {} ({})".format(idx + 1, track[0], track[1],
                                    str(track[2])[2:]))
