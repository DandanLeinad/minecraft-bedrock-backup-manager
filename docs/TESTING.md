# 🧪 Testes

## Executar

```bash
# Todos
uv run pytest

# Específico
uv run pytest tests/unit/models/ -v

# Com cobertura
uv run pytest --cov=src --cov-report=html
```

## Status

- **149 testes** passando
- **100% modelos** (WorldModel, BackupModel)
- **92% services** (BackupService, WorldService)
- Estrutura: `tests/unit/` com mirrors de `src/`

## Anatomia de um Teste

```python
def test_example():
    # ARRANGE: Preparar dados
    world = WorldModel(
        folder_name="abc123=",
        levelname="Meu Mundo",
        path=Path("C:/path"),
        account_id="123",
        version=[1, 26, 0, 0, 0]
    )

    # ACT: Executar
    result = world.levelname

    # ASSERT: Validar
    assert result == "Meu Mundo"
```

## Workflow

1. Escrever teste (RED)
2. Escrever código mínimo (GREEN)
3. Refatorar (REFACTOR)

Sempre rodar `uv run pytest` antes de commitar.
