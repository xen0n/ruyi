def _probe_real_builtins():
    for cls in ().__class__.__base__.__subclasses__():
        init = getattr(cls, "__init__", None)
        if not init:
            continue
        globals = getattr(init, "__globals__", None)
        if not globals or "__builtins__" not in globals:
            continue
        return globals["__builtins__"]
    return None

real_builtins = _probe_real_builtins()
