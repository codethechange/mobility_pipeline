from shapely.geometry import Polygon

def computeOverlap(enclosing, polygons):
    areaEnclosed = enclosing.area
    overlapPercentages = []
    for idx in range(len(polygons)):
        intersection = polygons[idx].intersection(enclosing)
        curr_percent = intersection.area / areaEnclosed
        overlapPercentages.append(curr_percent)
    return overlapPercentages

polygon1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
polygon2 = Polygon([(0, 0), (0, 3), (3, 3), (3, 0)])
polygons = [polygon1, polygon2]
enclosing = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])

print(computeOverlap(enclosing, polygons))