"""Functions for getting attributes of geometry."""

import math


class GeometryProcessor(object):
    """Class for processing geometric functions."""

    def areaCentroidMoments(self, polygon):
        """Compute the area, centroid, and moment components of a polygon."""
        psum, xmsum, ymsum = 0, 0, 0
        xxsum, yysum, xysum = 0, 0, 0
        if polygon.exterior.is_ccw:
            factor = 1
        else:
            factor = -1
        for (x1, y1), (x2, y2) in zip(polygon.exterior.coords[:-1],
                                      polygon.exterior.coords[1:]):
            z = (x1*y2 - x2*y1) * factor
            z1 = y1 + y2
            z2 = x1 + x2
            psum += z
            ymsum += z1*z
            xmsum += z2*z
            yysum += (x1*z2 + x2*x2)*z
            xxsum += (y1*z1 + y2*y2)*z
            xysum += (x2*y2 + x1*y1 + z1*z2)*z
        area = abs(psum)/2.
        cx = xmsum/(6.*area)
        cy = ymsum/(6.*area)
        sxx = xxsum/12.
        syy = yysum/12.
        sxy = -xysum/24.
        return area, (cx, cy), (sxx, syy, sxy)

    def principalAxis(self, polygon):
        """Compute the principal axis and aspect ratio of a polygon."""
        area, (cx, cy), (sxx, syy, sxy) = self.areaCentroidMoments(polygon)
        sxx -= cy * cy * area
        syy -= cx * cx * area
        sxy += cx * cy * area
        sc = sxx + syy
        sxx /= sc
        syy /= sc
        sxy /= sc
        if abs(sxy) < 1e-6:
            if syy > sxx:
                return (-1, 0), math.sqrt(syy/sxx)
            else:
                return (0, -1), math.sqrt(sxx/syy)
        e2 = sxy*sxy - sxx*syy
        e3 = max(0, 1. + 4.*e2)
        eig1 = (1. + math.sqrt(e3))/2.
        eig2 = (1. - math.sqrt(e3))/2.
        dx = -(sxx - min(eig1, eig2))
        dy = sxy
        return self.normalize(dx, dy), math.sqrt(eig1/eig2)

    def normalize(self, x, y):
        """Normalize vector components."""
        d = math.sqrt(x*x + y*y)
        x /= d
        y /= d
        return x, y
