from __future__ import division

import subprocess

def extract_shots_with_shotdetect(src_video, results_tag, threshold=-1):
    """
    uses Johan Mathe's Shotdetect to produce a list of shot 
    boundaries (in seconds) and scores, which are printed 
    to the console
    
    Args:
        src_video (string): the path to the source 
            video
        results_tag (string): a tag used by shotdetect to
            differentiate between different runs
        threshold (float): the minimum value used 
            by ffprobe to classify a shot boundary
    
    Returns: 
        List[(float, float)]: a list of tuples of floats 
        representing predicted shot boundaries (in seconds) and 
        their associated scores
    """
    scene_ps = subprocess.Popen(("shotdetect-cmd", 
                                "-i",
                                src_video,
                                "-s",
                                str(threshold),
                                "-a",
                                results_tag),
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
    output = scene_ps.stdout.read()
    boundaries = extract_boundaries_from_shotdetect_output(output)
    return boundaries

def extract_boundaries_from_shotdetect_output(output):
    """
    extracts the shot boundaries from the string output
    producted by shotdetect
    
    Args:
        output (string): the full output of the shotdetect
            shot detector as a single string
    
    Returns: 
        List[(float, float)]: a list of tuples of floats 
        representing predicted shot boundaries (in seconds) and 
        their associated scores
    """
    data = parse_output(output)
    boundaries = []
    for i in range(0, len(data), 2):
        time = float(data[i].split(':')[-1])/1000
        score = int(data[i + 1].split(':')[-1])
        boundaries.append((time, score))
    return boundaries

def parse_output(output):
    """
    slices the output of the shotdetector to retrieve
    the relevant data
    
    Args:
        output (string): the full output of the shotdetect
            shot detector as a single string
    
    Returns: 
        List[string]: a list of strings containing the data
        held as part of the ouput string"""
    data = output.split(',')
    for i in range(len(data)):
        if 'time:' in data[i]:
            return data[i:]
    return None
