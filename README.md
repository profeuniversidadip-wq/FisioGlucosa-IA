
# FisioGlucosa IA

Prototipo de sistema de aprendizaje adaptativo sobre hiperglucemia.

## Ejecutar en Windows

1. Instalar Python 3.11 o superior.
2. Abrir una terminal en esta carpeta.
3. Ejecutar:

```bash
pip install -r requirements.txt
streamlit run app.py
```

4. El navegador abrirá la aplicación automáticamente.

## Publicación

El proyecto puede subirse a GitHub y desplegarse en Streamlit Community Cloud para obtener una URL accesible desde PC y celular.

## Estado actual

Esta primera versión incluye:
- preguntas de selección múltiple;
- cuatro niveles de dificultad;
- explicación específica según la alternativa seleccionada;
- aumento de dificultad tras una respuesta correcta;
- mantenimiento del nivel tras una respuesta incorrecta;
- apoyo adicional tras errores consecutivos;
- puntaje y porcentaje final.

El banco completo de 40 preguntas puede incorporarse en la siguiente versión.
