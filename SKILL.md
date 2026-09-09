---
name: systematic-debugging
description: "Structured methodology for resolving complex bugs and performance issues through deterministic reproduction, refutable hypotheses, minimal surgical fixes, and regression verification."
license: MIT
metadata:
  version: "1.0.0"
  author: "ATX"
  category: "debugging"
  requirements: "git (bisect), pytest o framework de tests del proyecto, herramientas de profiling del lenguaje"
---

# Skill: Systematic Debugging 🐛

Metodología estructurada para resolver bugs complejos e issues de performance sin caer en "prueba y error" caótico. Se basa en el método científico: **reproducir → hipotetizar → corregir → verificar**.

---

## 🚀 Disparadores de Activación

- Error de build (`npm run build` falla).
- Tests unitarios o E2E fallidos.
- Regresiones reportadas por el Dev Revisor o QA.
- Problemas de rendimiento (latencia, memory leaks).
- Cuando el usuario dice "algo no funciona", "hay un bug", "investiga este error".

---

## 🧭 Metodología (4 Pasos Formales)

### Paso 1: Reproducción Determinista y Test Mínimo Aislado

> **Regla del fantasma**: Si no se reproduce de forma consistente, no es un bug — es un fantasma. No se corrige lo que no se ha visto.

1. **Confirmar el error de forma consistente**: registrar el input exacto, el estado del sistema y el stack trace completo. Buscar el mínimo input que lo dispara.
2. **Aislar el alcance**: reducir el caso al mínimo. ¿Es frontend, backend, datos, o configuración?
3. **Crear un test automático que falle (RED)**: escribir un test mínimo e independiente que reproduzca el fallo de forma determinista (TDD inverso). El test debe fallar ANTES del fix y pasar DESPUÉS.
4. **Si es una regresión conocida**: usar `git bisect` para localizar el commit que introdujo el fallo.

**Criterio de salida del Paso 1**: existe un test (o reproducción scripted) que falla de forma reproducible y demuestra el bug sin ambigüedad.

---

### Paso 2: Análisis Causal e Hipótesis Refutables

1. **Formular hipótesis falsables**: escribir cada hipótesis como "si la causa es X, entonces el comportamiento Y debe observarse". Una hipótesis por vez.
2. **Aislar por capas**: descartar sistemáticamente frontend, backend, datos, configuración e infraestructura con experimentos mínimos (no con conjeturas).
3. **Instrumentar de forma dirigida**: añadir logs, trazas o profiling SOLO en los puntos donde la hipótesis predice una observación. No instrumentar al azar.
4. **Descartar o confirmar**: cada experimento debe poder refutar la hipótesis. Si el experimento no puede fallar, no sirve como evidencia.
5. **Para issues de rendimiento**: medir antes de tocar. Perfilar (cProfile, Chrome DevTools, profilers del lenguaje) para localizar el cuello de botella real en lugar de adivinar.

**Criterio de salida del Paso 2**: una causa raíz confirmada por evidencia (test, log, perfil o bisect), no por intuición.

---

### Paso 3: Corrección Quirúrgica Mínima

1. **Menor diff posible**: corregir SOLO la causa raíz confirmada. Un problema por fix.
2. **Evitar side-effects**: no refactorizar código no relacionado, no reformatear, no "aprovechar" para arreglar otras cosas. Cada cambio extra es un nuevo riesgo de regresión.
3. **Implementar el fix para pasar el test (GREEN)**: el test del Paso 1 debe pasar con el fix y fallar sin él.
4. **Respetar los patrones del código existente**: la corrección debe ser consistente con el estilo y arquitectura del proyecto.

**Criterio de salida del Paso 3**: el diff contiene únicamente la corrección de la causa raíz y el test que la protege.

---

### Paso 4: Verificación de No-Regresión

1. **Verificar RED → GREEN**: el test mínimo pasa después del fix y se confirma que fallaba antes.
2. **Ejecutar la suite relacionada**: correr los tests unitarios e integración del dominio afectado (no solo el test nuevo). Si el proyecto tiene E2E, correr los flujos críticos tocados.
3. **Prevención proactiva**: revisar si el mismo patrón de error existe en otras partes del código (misma API mal usada, misma condición de carrera, mismo timeout).
4. **Documentar las lecciones aprendidas**: si el bug revela un gap en el proceso o en las pruebas, registrarlo en la tabla de "Lecciones Aprendidas" del workflow y proponer una prueba o check que lo prevenga.

**Criterio de salida del Paso 4**: suite verde + patrón revisado en el resto del código + lección documentada si aplica.

---

## ✅ Checklist de Resolución Completa

- [ ] El error se reproduce de forma determinista (test RED).
- [ ] Existe una hipótesis confirmada por evidencia.
- [ ] El diff es mínimo y sin side-effects.
- [ ] El test pasa (GREEN) y la suite relacionada está verde.
- [ ] El mismo patrón fue revisado en otras partes del código.
- [ ] La lección aprendida quedó documentada (si aplica).

---

## 🚫 Anti-Patrones (Prohibido)

- **"Prueba y error"**: cambiar código al azar hasta que "parezca funcionar". Sin reproducción ni hipótesis, no hay fix, hay suerte.
- **Fix sin test**: corregir un bug sin dejar un test que lo proteja de regresiones.
- **Refactor oportunista**: tocar código no relacionado dentro de un fix (mezcla cambios y dificulta el review y el bisect).
- **Optimización adivinada**: optimizar por intuición sin perfilado previo.
- **Cambio sin verificación**: dar por resuelto un bug sin correr la suite.

---

## 📖 Glosario

- **TDD inverso**: escribir primero el test que reproduce el fallo, verlo fallar (RED), aplicar el fix y verlo pasar (GREEN).
- **git bisect**: búsqueda binaria sobre el historial de commits para localizar el commit que introdujo una regresión.
- **Hipótesis refutable/falsable**: afirmación causal que un experimento concreto puede demostrar falsa. Si nada puede refutarla, no es una hipótesis útil.

---

*Systematic Debugging Skill v1.0.0 — MIT License — ATX*