def evaluate_shot_predictions(ranked_predictions, boundaries, tolerance=0.1):
    """
    evaluates predictions against ground truth boundaries 
    
    Predictions are matched greedily (predictions with higher 
    scores are matched first) and no boundary can be matched 
    twice.
    
    Args:
        ranked_predictions (list): a list of floats representing 
            predicted shot boundaries (in seconds), ranked in 
            order of descending score
        boundaries (list): a list of floats representing 
            ground truth shot_boundaires (in seconds)
        tolerance (float):

    returns (list): a list of True/False values corresponding 
        to whether each prediction matched a shot boundary 
        within the given tolerance.
    """
    results = []
    remaining_boundaries = boundaries[:]
    for i, prediction in enumerate(ranked_predictions):
        match = closest_match(prediction[0], remaining_boundaries, tolerance)
        if match is not None:
            results.append(True)
            remaining_boundaries[match] = None
        else:
            results.append(False)
    return results

def closest_match(elem, targets, tolerance):
    """
    finds the closest match for elem in targets
    that lies within the given tolerance.
    
    returns (int/None): An int describing the 
    position of the closest possible match if 
    a match occurs, and None otherwise.
    """
    closest_idx = None
    closest_diff = 1e6 
    for idx, target in enumerate(targets):
        if target is not None:
            diff = abs(elem - target)
            if diff <= min(tolerance, closest_diff):
                closest_idx = idx
                closest_diff = diff
    return closest_idx

def get_ground_truth(csv_path):
    """
    retrieves the ground truth shot detections
    
    Args:
        csv_path: file path to the csv file containing
            human annotated shot boundaries
    
    returns (list): a list of floats representing 
        ground truth shot boundaries (in seconds)
    """
    ground_truth_shot_boundaries = []
    with open(csv_path, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            num_seconds = 60 * float(row[0]) + float(row[1])
            ground_truth_shot_boundaries.append(num_seconds)
    return ground_truth_shot_boundaries
