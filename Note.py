

class Note:

    """
    This class doesn't need to stay, but the idea is that maybe we could have
    multiple types of notes that have different required attributes, data types
    for those attributes, methods, etc. but allow any optional attributes to be
    specified at time of creation.  They all have the same constructors, though.
    These notes can be mixed-and-matched both "statically" through class 
    inheritance or dynamically by constructing new notes combining 
    (and/or changing) the properties of existing notes in a prototype-inhertance
    sort of way.

    TODO: What can go wrong?
    """

    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            setattr(self, key, value)