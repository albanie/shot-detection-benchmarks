from __future__ import division

import scenedetect

def extract_shots_with_pyscenedetect(src_video, threshold=0, min_scene_length=15,  fps=25):
    """
    uses pyscenedetect to produce a list of shot 
    boundaries (in seconds)
    
    Args:
        src_video (string): the path to the source 
            video
        threshold (int): the minimum value used 
            by pyscenedetect to classify a shot boundary
        min_scene_length (int): the minimum number of frames
            permitted per shot. 
        fps (int): the frame rate of the video
    
    Returns: 
        List[(float, float)]: a list of tuples of floats 
        representing predicted shot boundaries (in seconds) and 
        their associated scores
    """
    scene_detectors = scenedetect.detectors.get_available()
    timecode_formats = scenedetect.timecodes.get_available()
    detection_method = 'content'
    detector = None
    start_time, duration, end_time = None, None, None
    
    # Setup scenedetect defaults
    downscale_factor = 1
    frame_skip = 0
    stats_writer = None
    quiet_mode, save_images = False, False
    
    detector = scene_detectors['content'](threshold, min_scene_length)
    scene_list = list()
    timecode_list = [start_time, duration, end_time]
    video_fps, frames_read = scenedetect.detect_scenes_file(
                            path = src_video,
                            scene_list = scene_list,
                            detector_list = [detector],
                            stats_writer = stats_writer,
                            downscale_factor = downscale_factor,
                            frame_skip = frame_skip,
                            quiet_mode = quiet_mode,
                            save_images = save_images,
                            timecode_list = timecode_list)
    boundaries = [(pair[0] / fps, pair[1]) for pair in scene_list]
    return boundaries
