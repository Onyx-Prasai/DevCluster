import numpy as np
from typing import Dict, Tuple

class Scorer:
    """
    A class to compute a score based on the distance between an input array and a centroid, with additional 
    contextual interpretation.
    """

    def __init__(self,
                 label: int,
                 input_array: np.ndarray,
                 centroid: np.ndarray,
                 interpretation: Dict[int, str],
                 scores: Dict[int, Tuple[float, float]],
                 max_distance: float = 10.0,
                 min_distance: float = 0.0):
        """
        Initializes the Scorer object with the given parameters.

        Args:
            label (int): The label associated with the input array.
            input_array (np.ndarray): The input array for which the score is to be computed.
            centroid (np.ndarray): The centroid to compare the input array against.
            interpretation (Dict[int, str]): A dictionary mapping label integers to corresponding string interpretations.
            scores (Dict[int, Tuple[float, float]]): A dictionary mapping labels to score tuples (primary score, secondary score).
            max_distance (float, optional): The maximum distance used for normalization. Defaults to 10.0.
            min_distance (float, optional): The minimum distance used for normalization. Defaults to 0.0.
        """
        self.label = label
        self.centroid = centroid
        self.input_array = input_array
        self.max_distance = max_distance
        self.min_distance = min_distance
        self.interpretation = interpretation
        self.scores = scores

    def compute_distance(self) -> float:
        """
        Computes the Euclidean distance between the input array and the centroid.

        Returns:
            float: The Euclidean distance between the input array and the centroid.
        """
        return np.linalg.norm(self.input_array - self.centroid)

    def compute_score(self) -> Tuple[str, float]:
        """
        Computes the score based on the normalized distance between the input array and the centroid, 
        then adds a corresponding score from the `scores` dictionary.

        The score is normalized using the `min_distance` and `max_distance` attributes, and then adjusted 
        using the label's score from the `scores` dictionary.

        Returns:
            Tuple[str, float]: A tuple containing the interpretation string for the label and the computed score.
        """
        distance = self.compute_distance()
        normalized_distance = (distance - self.min_distance) / (self.max_distance - self.min_distance)

        # Calculate the final score using the normalized distance and the label-specific score
        distance_range = self.max_distance - self.min_distance
        score = normalized_distance * distance_range + self.scores.get(self.label, (0.0, 0.0))[0]

        # Fetch the interpretation for the label
        interpretation = self.interpretation.get(self.label, "No interpretation available")

        return interpretation, score
