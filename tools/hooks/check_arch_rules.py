import ast
import pathlib
import sys


LEGACY_MARKERS = ("legacy",)
PREDICTOR_APP_LAYERS = (
    "entrypoints",
    "service",
    "ports",
    "adapters",
    "dtos",
    "exceptions",
)
DISALLOWED_IMPORT_PREFIXES_BY_LAYER = {
    "service": ("predictor_app.entrypoints", "fastapi"),
    "ports": ("predictor_app.adapters", "predictor_app.entrypoints", "fastapi"),
    "adapters": ("predictor_app.entrypoints",),
}


def _is_legacy_file(file_path: pathlib.Path) -> bool:
    normalized_path = str(file_path).lower()
    for marker in LEGACY_MARKERS:
        if marker in normalized_path:
            return True
    return False


def _module_matches_prefix(module_name: str, prefix: str) -> bool:
    return module_name == prefix or module_name.startswith(f"{prefix}.")


def _extract_predictor_app_layer(file_path: pathlib.Path) -> str | None:
    file_parts = file_path.parts

    for index, part in enumerate(file_parts):
        if part != "predictor_app":
            continue

        if index + 1 >= len(file_parts):
            return None

        candidate_layer = file_parts[index + 1]
        if candidate_layer in PREDICTOR_APP_LAYERS:
            return candidate_layer

        return None

    return None


def _collect_layer_direction_violations(
    file_path: pathlib.Path,
    syntax_tree: ast.Module,
) -> list[str]:
    layer = _extract_predictor_app_layer(file_path=file_path)
    if layer is None:
        return []

    disallowed_prefixes = DISALLOWED_IMPORT_PREFIXES_BY_LAYER.get(layer, ())
    if len(disallowed_prefixes) == 0:
        return []

    violations: list[str] = []

    for node in ast.walk(syntax_tree):
        imported_modules: list[str] = []
        line_number = 0

        if isinstance(node, ast.Import):
            line_number = node.lineno
            for alias_node in node.names:
                imported_modules.append(alias_node.name)

        if isinstance(node, ast.ImportFrom) and node.module is not None:
            line_number = node.lineno
            imported_modules.append(node.module)

        for imported_module in imported_modules:
            for disallowed_prefix in disallowed_prefixes:
                if _module_matches_prefix(
                    module_name=imported_module,
                    prefix=disallowed_prefix,
                ):
                    violations.append(
                        f"{file_path}:{line_number} Layer '{layer}' cannot import '{imported_module}'.",
                    )
                    break

    return violations


def _collect_violations(file_path: pathlib.Path) -> list[str]:
    source_code = file_path.read_text(encoding="utf-8")
    syntax_tree = ast.parse(source_code, filename=str(file_path))

    violations: list[str] = []

    for node in ast.walk(syntax_tree):
        if isinstance(node, ast.ImportFrom):
            violations.append(
                f"{file_path}:{node.lineno} Avoid 'from x import y'; use module imports.",
            )

        if isinstance(node, ast.Global):
            violations.append(f"{file_path}:{node.lineno} Avoid 'global' statements.")

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"hasattr", "getattr"}:
                violations.append(
                    f"{file_path}:{node.lineno} Avoid reflection helpers like {node.func.id}().",
                )

        if isinstance(node, ast.Name) and node.id == "Optional":
            violations.append(
                f"{file_path}:{node.lineno} Use '| None' instead of Optional.",
            )

    violations.extend(
        _collect_layer_direction_violations(
            file_path=file_path,
            syntax_tree=syntax_tree,
        ),
    )

    return violations


def main() -> int:
    all_violations: list[str] = []

    for raw_path in sys.argv[1:]:
        file_path = pathlib.Path(raw_path)

        if not file_path.exists():
            continue

        if _is_legacy_file(file_path=file_path):
            continue

        if file_path.suffix != ".py":
            continue

        all_violations.extend(_collect_violations(file_path=file_path))

    if all_violations:
        for violation in all_violations:
            print(violation)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
