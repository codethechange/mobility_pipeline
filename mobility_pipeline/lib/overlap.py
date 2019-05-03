from shapely.geometry import Polygon

def computeOverlap(enclosing, polygons):
    overlapPercentages = []
    for idx in range(len(polygons)):
        intersection = polygons[idx].intersection(enclosing)
        curr_percent = intersection.area / polygons[idx].area
        overlapPercentages.append(curr_percent)
    return overlapPercentages
