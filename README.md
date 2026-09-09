# systematic-debugging Skill 🐛

[English version](README.en.md)

Skill para resolver **bugs complejos e issues de performance** con método científico: reproducir de forma determinista, formular hipótesis refutables, aplicar una corrección quirúrgica mínima y verificar la no-regresión. Reemplaza el "prueba y error" caótico por un proceso verificable de 4 pasos.

## 🎯 Objetivo

Convertir la depuración en un proceso reproducible y auditable: cada bug se resuelve con un **test mínimo que falla antes y pasa después** (TDD inverso), una **causa raíz confirmada por evidencia** (no por intuición) y un **diff mínimo sin side-effects**.

## 🧭 Los 4 Pasos

1. **Reproducción determinista y test mínimo aislado** — Si no se reproduce, no es un bug (regla del fantasma). Crear un test RED y usar `git bisect` para regresiones.
2. **Análisis causal e hipótesis refutables** — Una hipótesis falsable por vez, descartando capas (frontend, backend, datos, configuración) con experimentos mínimos. Para performance: medir antes de tocar.
3. **Corrección quirúrgica mínima** — Menor diff posible, sin refactor oportunista, hasta dejar el test GREEN.
4. **Verificación de no-regresión** — Suite relacionada verde, revisión del mismo patrón en otras partes del código y lecciones aprendidas documentadas.

## ⚡ Uso Inmediato

```bash
# 1. Reproducir: escribir el test que falla
pytest tests/unit/test_bug_reproduction.py -k "test_reproduce_bug" -v

# 2. Si es una regresión, localizar el commit culpable
git bisect start
git bisect bad HEAD
git bisect good <commit-conocido-bueno>

# 3. Corregir con el mínimo diff y verificar
pytest tests/unit/ -v
```

## 🚫 Anti-Patrones (Prohibido)

- "Prueba y error" sin reproducción ni hipótesis.
- Fix sin test que proteja la regresión.
- Refactor oportunista dentro de un fix.
- Optimización sin perfilado previo.
- Dar por resuelto sin correr la suite.

## 🏛️ Estructura de la Skill

```
systematic-debugging/
├── SKILL.md            # Metodología de 4 pasos, checklist y anti-patrones
├── README.md           # Documentación en español
├── README.en.md        # Documentación en inglés
├── metadata.json       # Manifiesto y tags de la skill
└── LICENSE             # MIT — ATX
```

---

**Licencia**: MIT — ATX