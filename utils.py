import os
import importlib.util
import inspect

def discoverTests():
    for root, _, files in os.walk("."):
        for filename in files:
            if filename.startswith('test_') and filename.endswith('.py'):
                full_path = os.path.join(root, filename)
                module_name = full_path.replace(os.sep, ".").lstrip("./").rstrip(".py")
                module_name = module_name.replace(".py", "").replace("..", ".")

                spec = importlib.util.spec_from_file_location(module_name, full_path)
                mod = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(mod)
                except Exception as e:
                    print(f"Could not import {full_path}: {e}")
                    continue

                for name in dir(mod):
                    attr = getattr(mod, name)
                    if callable(attr) and name.startswith('test'):
                        yield f"{module_name}.{name}", attr
