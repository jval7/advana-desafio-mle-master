# AGENTS.md

## Objetivo
Este documento define estándares obligatorios para colaborar en este repositorio con consistencia técnica, mantenibilidad y calidad de entrega.

## Arquitectura
- Trabajar con **Clean Architecture** (arquitectura limpia / hexagonal).
- El dominio debe permanecer desacoplado de frameworks, librerías externas e infraestructura.
- Los casos de uso deben orquestar reglas de negocio y depender de abstracciones.
- Adaptadores e infraestructura deben implementar puertos definidos por el dominio/aplicación.

## Reglas Obligatorias de Código
1. **No reflection**: Do not use `hasattr()`, `getattr()`, or similar reflection.
2. **Module imports only**: Import full modules, not direct objects (`import package.module`, not `from x import y`).
3. **No global**: Do not use `global`.
4. **Type hints with `|`**: Use `str | None`, not `Optional[str]`.
5. **Imports at top**: Keep all imports at the top of the file.
6. **Always use Pydantic**: Use Pydantic for all data models.
7. **Specific exceptions**: Handle errors with specific exceptions; do not use `except Exception` unless there is explicit justification to avoid stopping the main app.
8. **Follow the Zen of Python**.
9. **Third-party libraries**: When using third-party libraries, first inspect their source code; if that is not enough, use the official documentation.

## Pre-commit Standard
Usar la siguiente configuración como estándar del proyecto (`.pre-commit-config.yaml`):

```yaml
minimum_pre_commit_version: "3.6.0"
default_stages: [pre-commit]
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-merge-conflict
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.2
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.18.2
    hooks:
      - id: mypy
        args: [--strict]

  - repo: local
    hooks:
      - id: check-arch-rules
        name: check-arch-rules
        entry: python tools/hooks/check_arch_rules.py
        language: system
        types: [python]

      - id: unit-tests-pre-push
        name: unit-tests-pre-push
        entry: pytest -q
        language: system
        pass_filenames: false
        stages: [pre-push]
```
