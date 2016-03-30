from __future__ import division

import subprocess

def extract_shots_with_ffprobe(src_video, threshold=0):
    """
    uses ffprobe to produce a list of shot 
    boundaries (in seconds)
    
    Args:
        src_video (string): the path to the source 
            video
        threshold (float): the minimum value used 
            by ffprobe to classify a shot boundary
    
    Returns: 
        List[(float, float)]: a list of tuples of floats 
        representing predicted shot boundaries (in seconds) and 
        their associated scores
    """
    scene_ps = subprocess.Popen(("ffprobe", 
                                "-show_frames",
                                "-of",
                                "compact=p=0", 
                                "-f",
                                "lavfi",
                                "movie=" + src_video + ",select=gt(scene\," + str(threshold) + ")"),
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
    output = scene_ps.stdout.read()
    boundaries = extract_boundaries_from_ffprobe_output(output)
    return boundaries

def extract_boundaries_from_ffprobe_output(output):
    """
    extracts the shot boundaries from the string output
    producted by ffprobe
    
    Args:
        output (string): the full output of the ffprobe
            shot detector as a single string
    
    Returns: 
        List[(float, float)]: a list of tuples of floats 
        representing predicted shot boundaries (in seconds) and 
        their associated scores
    """
    boundaries = []
    for line in output.split('\n')[15:-1]:
        boundary = float(line.split('|')[4].split('=')[-1])
        score = float(line.split('|')[-1].split('=')[-1])
        boundaries.append((boundary, score))
    return boundaries
