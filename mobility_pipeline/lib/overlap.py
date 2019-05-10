"""Determines overlap between a shape and a list of polygons """

def compute_overlap(enclosing, polygons):
    """Computes the percentage overlap of enclosing with each polygon in list of polygons"""
    overlap_percentages = []
    for _, polygon in enumerate(polygons):
        intersection = polygon.intersection(enclosing)
        curr_percent = intersection.area / polygon.area
        overlap_percentages.append(curr_percent)
    return overlap_percentages
