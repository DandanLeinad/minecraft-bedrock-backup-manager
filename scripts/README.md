# 📋 Git Hooks de Validação de Licença

Este diretório contém scripts para gerenciar headers de licença AGPL.

## 🚀 Setup Initial

### Windows (PowerShell)

```powershell
# 1. Adicionar licença em todos os arquivos existentes
python scripts/add_license_header.py

# 2. Ativar pre-commit hook
# (O hook está em .git/hooks/pre-commit - já funciona automaticamente no próximo commit)

# 3. Testar o hook manualmente
python scripts/validate_license_header.py
```

### Linux/Mac

```bash
# 1. Adicionar licença em todos os arquivos existentes
python scripts/add_license_header.py

# 2. Tornar hook executável
chmod +x .git/hooks/pre-commit

# 3. Testar o hook manualmente
python scripts/validate_license_header.py
```

## 📝 Scripts Disponíveis

### `add_license_header.py`

Adiciona automaticamente header de licença em arquivos Python sem header.

**Uso:**

```bash
# Todos os arquivos do projeto
python scripts/add_license_header.py

# Diretório específico
python scripts/add_license_header.py src/backup_manager_mvp

# Arquivo específico
python scripts/add_license_header.py file.py
```

**Exemplo:**

```
🔍 Procurando arquivos .py em: C:\Users\danie\Projects\Python\backup_manager_mvp

📁 Encontrados 15 arquivo(s) .py

✅ tests/conftest.py - já tem header
➕ tests/unit/models/test_world_model.py - header adicionado
➕ src/backup_manager_mvp/main.py - header adicionado
...

✨ Resumo: 12 arquivo(s) atualizado(s), 3 já tinham header
```

### `validate_license_header.py`

Valida que todos os arquivos Python staged para commit têm header de licença.

**Uso Manual:**

```bash
python scripts/validate_license_header.py
```

**Automático:**

Executado automaticamente **antes de cada commit** pelo hook `.git/hooks/pre-commit`.

**Exemplo - Validação Falha:**

```
❌ ERRO: Arquivos sem header de licença AGPL:

   • src/backup_manager_mvp/new_feature.py
   • tests/unit/services/test_new_service.py

📝 Execute para adicionar headers automaticamente:
   python scripts/add_license_header.py

💡 Depois execute: git add [arquivos] && git commit
```

## 🔄 Fluxo de Trabalho

### ✅ Novo arquivo → Commit:

```bash
# 1. Criar arquivo novo (vazio ou sem header)
touch src/backup_manager_mvp/new_feature.py

# 2. Adicionar código...

# 3. Stage arquivo
git add src/backup_manager_mvp/new_feature.py

# 4. Tentar commit
git commit -m "feat: novo recurso"

# ❌ Hook bloqueia - arquivo sem header!

# 5. Adicionar header automaticamente
python scripts/add_license_header.py

# 6. Stage novamente
git add src/backup_manager_mvp/new_feature.py

# 7. Commit (agora passa!)
git commit -m "feat: novo recurso"

# ✅ Success!
```

### Arquivo existente sem header:

```bash
# Adicionar header em todos os .py
python scripts/add_license_header.py

# Verificar:
git status

# Stage todos:
git add src/ tests/

# Commit:
git commit -m "chore: adicionar headers AGPL"
```

## 🛠️ Comportamento do Hook

O hook **`.git/hooks/pre-commit`** faz o seguinte:

1. ✅ Antes de cada commit, valida arquivos `.py` staged
2. ✅ Verifica se todos têm header AGPL
3. ❌ Se algum não tiver, **bloqueia o commit**
4. 📝 Mostra instruções de como resolver
5. ✅ Permite retry após adicionar headers

## ⚠️ Exceções (Ignorados pelo Hook)

Estes diretórios **não são validados**:

- `.git/` — Repo git
- `.venv/` — Virtual environment
- `__pycache__/` — Cache Python
- `.pytest_cache/` — Cache pytest
- `build/` — Build artifacts
- `dist/` — Distribuição
- `htmlcov/` — Reports de cobertura

## 🔧 Desabilitar Temporariamente

Se precisar fazer commit **sem validação** (raramente):

```bash
# Pular pre-commit hook
git commit --no-verify -m "sua mensagem"
```

⚠️ **Não recomendado!** Use apenas em emergências.

## 📚 Referência

- **Headers:** AGPL-3.0-or-later (https://www.gnu.org/licenses/agpl-3.0.html)
- **Copyright:** DandanLeinad © 2026
- **Documentação:** Ver [LICENSE](../LICENSE)

---

💡 **Dica:** Execute `python scripts/add_license_header.py` regularmente para manter todos os arquivos em compliance!
