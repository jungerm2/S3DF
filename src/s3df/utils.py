import itertools


def to_vec(values, size=None):
    values = values if isinstance(values, (list, tuple)) else [values]
    size = size or len(values)

    if size > 4:
        raise ValueError(f"Cannot create vector with length {len(values)}.")

    values = itertools.cycle(values[:size])
    values = [v for _, v in zip(range(size), values)]
    return f"vec{size}({', '.join(str(float(v)) for v in values)})"
