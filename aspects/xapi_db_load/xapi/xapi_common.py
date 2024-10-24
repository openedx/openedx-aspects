"""
Base class for all fake xAPI events.
"""


class XAPIBase:
    """
    Base class to handle some common functionality.

    Should be turned into a proper ABC when we have a chance.
    """

    verb = None
    verb_display = None

    def __init__(self, load_generator):
        if not self.verb:
            raise NotImplementedError(
                f"XAPIBase is abstract, add your verb in subclass {type(self)}."
            )
        self.parent_load_generator = load_generator
