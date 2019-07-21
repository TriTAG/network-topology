"""Null discretizer and discrete geometry representations."""
from .abstractdiscretizer import AbsDiscretizer
from .abstractgeom import AbsDiscreteGeometry


class NullDiscretizer(AbsDiscretizer):
    """Null implementaiton of discretizer."""

    def discretize(self, tolerance):
        """Discretize the geometry, returns AbsDiscreteGeometry."""
        return NullDiscreteGeometry()

    def addShape(self, shape):
        """Add shape to be discretized."""

    def addEndpoints(self, lineStrings):
        """Add endpoints of the linestrings to the representation."""


class NullDiscreteGeometry(AbsDiscreteGeometry):
    """Null implementation of discrete geometry."""

    def skeletonize(self, splitAtEndpoints, topology):
        """Generate a SkeletonGraph of the geometry."""
