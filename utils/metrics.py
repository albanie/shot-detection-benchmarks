from __future__ import division

import csv

def evaluate_shot_predictions(ranked_predictions, boundaries, tolerance=0.1):
    """
    evaluates predictions against ground truth boundaries 
    
    Predictions are matched greedily (predictions with higher 
    scores are matched first) and no boundary can be matched 
    twice.
    
    Args:
        ranked_predictions (List[(float, float)]): a list of 
            tuples floats representing predicted shot boundaries (in seconds) 
            and their respective score, ranked in order of descending score
        boundaries (List[float]): a list of floats representing 
            ground truth shot_boundaires (in seconds)
        tolerance (float): the maximum allowable difference between 
            a prediction and the ground truth boundary

    Returns: 
        List[bool]: a list of True/False values corresponding 
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

def evaluate_accuracy(predictions, boundaries, tolerance=0.1):
    """
    evaluates prediction accuracy against ground truth boundaries 
    
    Ground truth boundaries are matched greedily against predictions
    
    Args:
        predictions (List[float]): a list of floats representing 
            predicted shot boundaries (in seconds)        
        boundaries (List[float]): a list of floats representing 
            ground truth shot_boundaires (in seconds)
        tolerance (float): the maximum allowable difference between 
            a prediction and the ground truth boundary

    Returns: 
        List[bool]: a list of True/False values corresponding 
            to whether each prediction matched a shot boundary 
            within the given tolerance.
    """
    results = []
    remaining_predictions = predictions[:]
    for i, boundary in enumerate(boundaries):
        match = closest_match(boundary, remaining_predictions, tolerance)
        if match is not None:
            results.append(True)
            remaining_predictions[match] = None
        else:
            results.append(False)
    accuracy = sum(results) / len(results)
    return accuracy

def closest_match(elem, targets, tolerance):
    """
    finds the closest match for elem in targets
    that lies within the given tolerance.
    
    Returns: 
        int/None: An int describing the 
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
    
    Returns: 
        List[float]: a list of floats representing 
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

def get_precision_recall(results, num_pos):
    """
    calculates the precision and recall from 
    the classifier results
    
    Args:
        results (List[bool]): a list of booleans where a 
            True represents a true positive and a False
            represents a false positive
        num_pos (int): the total number of positive samples
            in the test set
    
    Returns:
        (float, float): a tuple containing the calculated 
            precision and recall.
    """
    true_pos, false_pos = 0, 0
    recall, precision = [0,], [1,]
    for result in results:
        if result:
            true_pos = true_pos + 1
        else:
            false_pos = false_pos + 1
        precision.append(true_pos / (true_pos + false_pos))
        recall.append(true_pos / num_pos)
    return (precision, recall)
