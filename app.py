
import streamlit as st
import random

st.set_page_config(
    page_title="FisioGlucosa IA",
    page_icon="🧠",
    layout="centered"
)

st.title("FisioGlucosa IA")
st.caption("Sistema de aprendizaje adaptativo sobre hiperglucemia")

QUESTIONS = [
    {
        "id": 1,
        "level": 1,
        "topic": "Hiperglucemia",
        "question": "¿Qué describe mejor la hiperglucemia?",
        "options": {
            "A": "Disminución de la glucosa sanguínea.",
            "B": "Aumento de la glucosa sanguínea.",
            "C": "Disminución de la insulina después de comer.",
            "D": "Aumento exclusivo de glucosa dentro de las células."
        },
        "correct": "B",
        "feedback": {
            "A": "Esa alternativa describe una disminución de la glucemia, no una hiperglucemia.",
            "B": "La hiperglucemia corresponde a una concentración elevada de glucosa en la sangre.",
            "C": "La hiperglucemia se define por el nivel de glucosa sanguínea, no únicamente por cambios en la insulina.",
            "D": "El concepto se refiere principalmente a la elevación de glucosa en la sangre."
        }
    },
    {
        "id": 2,
        "level": 1,
        "topic": "Insulina",
        "question": "Después de una comida rica en carbohidratos aumenta la glucosa sanguínea. ¿Qué hormona aumenta principalmente como respuesta?",
        "options": {
            "A": "Glucagón.",
            "B": "Insulina.",
            "C": "Adrenalina.",
            "D": "Hormona del crecimiento."
        },
        "correct": "B",
        "feedback": {
            "A": "El glucagón participa principalmente en aumentar la disponibilidad de glucosa cuando esta disminuye.",
            "B": "El aumento de glucosa estimula la secreción de insulina por las células beta pancreáticas.",
            "C": "La adrenalina puede aumentar la disponibilidad de glucosa durante el estrés, pero no es la principal respuesta posprandial.",
            "D": "La hormona del crecimiento no es la principal respuesta reguladora después de una comida."
        }
    },
    {
        "id": 3,
        "level": 2,
        "topic": "GLUT4",
        "question": "En músculo esquelético, la insulina favorece la captación de glucosa principalmente mediante:",
        "options": {
            "A": "GLUT4.",
            "B": "Hemoglobina.",
            "C": "Na+/K+-ATPasa.",
            "D": "Canales de calcio."
        },
        "correct": "A",
        "feedback": {
            "A": "La señalización de insulina favorece la translocación de GLUT4 hacia la membrana celular.",
            "B": "La hemoglobina transporta gases respiratorios y no introduce glucosa en las células.",
            "C": "La Na+/K+-ATPasa mantiene gradientes iónicos, pero no transporta glucosa.",
            "D": "Los canales de calcio transportan iones, no glucosa."
        }
    },
    {
        "id": 4,
        "level": 2,
        "topic": "Resistencia a la insulina",
        "question": "¿Qué significa resistencia a la insulina?",
        "options": {
            "A": "Las células responden de manera reducida a la acción de la insulina.",
            "B": "La sangre deja de contener glucosa.",
            "C": "El páncreas deja siempre de producir insulina.",
            "D": "Las células responden demasiado a la insulina."
        },
        "correct": "A",
        "feedback": {
            "A": "En la resistencia a la insulina, los tejidos responden menos eficazmente a la hormona.",
            "B": "La glucosa no desaparece de la sangre; incluso puede aumentar.",
            "C": "Puede existir resistencia a la insulina aunque el páncreas siga produciendo insulina.",
            "D": "La resistencia implica menor sensibilidad, no mayor sensibilidad."
        }
    },
    {
        "id": 5,
        "level": 3,
        "topic": "Glucogénesis",
        "question": "¿Qué proceso permite almacenar glucosa en forma de glucógeno?",
        "options": {
            "A": "Glucogénesis.",
            "B": "Glucogenólisis.",
            "C": "Gluconeogénesis.",
            "D": "Lipólisis."
        },
        "correct": "A",
        "feedback": {
            "A": "La glucogénesis sintetiza glucógeno a partir de glucosa.",
            "B": "La glucogenólisis degrada glucógeno.",
            "C": "La gluconeogénesis produce glucosa a partir de precursores no glucídicos.",
            "D": "La lipólisis moviliza triglicéridos."
        }
    },
    {
        "id": 6,
        "level": 3,
        "topic": "Producción hepática",
        "question": "En resistencia hepática a la insulina, puede ocurrir que:",
        "options": {
            "A": "El hígado continúe produciendo glucosa a pesar de existir glucosa elevada en sangre.",
            "B": "El hígado deje de funcionar inmediatamente.",
            "C": "Toda la glucosa desaparezca de la circulación.",
            "D": "Desaparezcan todas las hormonas pancreáticas."
        },
        "correct": "A",
        "feedback": {
            "A": "Una señal inhibitoria de insulina menos efectiva puede favorecer una producción hepática inapropiada de glucosa.",
            "B": "Resistencia a la insulina no significa insuficiencia hepática inmediata.",
            "C": "La glucosa puede permanecer elevada en la sangre.",
            "D": "Las hormonas pancreáticas continúan existiendo."
        }
    },
    {
        "id": 7,
        "level": 4,
        "topic": "Integración",
        "question": "Una persona presenta glucosa elevada, insulina elevada y disminución de la captación de glucosa por músculo. ¿Qué interpretación integra mejor estos datos?",
        "options": {
            "A": "Respuesta compensatoria de insulina frente a una menor sensibilidad periférica.",
            "B": "Ausencia total de insulina.",
            "C": "Sensibilidad excesiva del músculo a la insulina.",
            "D": "Ausencia completa de secreción pancreática."
        },
        "correct": "A",
        "feedback": {
            "A": "La combinación es compatible con resistencia periférica e hiperinsulinemia compensatoria.",
            "B": "El caso indica explícitamente que la insulina está elevada.",
            "C": "Una sensibilidad elevada favorecería mayor captación de glucosa.",
            "D": "La presencia de insulina elevada demuestra que existe secreción pancreática."
        }
    },
    {
        "id": 8,
        "level": 4,
        "topic": "Homeostasis",
        "question": "Una persona sana presenta un aumento transitorio de glucosa después de comer y luego vuelve hacia su rango habitual. ¿Qué concepto explica mejor este fenómeno?",
        "options": {
            "A": "Homeostasis mediante retroalimentación negativa.",
            "B": "Fallo irreversible pancreático.",
            "C": "Retroalimentación positiva ilimitada.",
            "D": "Ausencia completa de regulación hormonal."
        },
        "correct": "A",
        "feedback": {
            "A": "La respuesta hormonal contrarresta el cambio inicial y favorece el retorno hacia el rango fisiológico.",
            "B": "El retorno de la glucosa hacia su rango habitual indica regulación funcional.",
            "C": "Una retroalimentación positiva amplificaría el cambio.",
            "D": "Precisamente existe regulación hormonal."
        }
    }
]

if "started" not in st.session_state:
    st.session_state.started = False
if "level" not in st.session_state:
    st.session_state.level = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "errors_in_level" not in st.session_state:
    st.session_state.errors_in_level = 0
if "answered_ids" not in st.session_state:
    st.session_state.answered_ids = []
if "current_id" not in st.session_state:
    st.session_state.current_id = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "finished" not in st.session_state:
    st.session_state.finished = False
if "name" not in st.session_state:
    st.session_state.name = ""

def get_candidates(level):
    return [
        q for q in QUESTIONS
        if q["level"] == level and q["id"] not in st.session_state.answered_ids
    ]

def choose_question():
    candidates = get_candidates(st.session_state.level)
    if not candidates:
        # Si ya usó las disponibles del nivel, permitir reutilizar otra del mismo nivel.
        candidates = [q for q in QUESTIONS if q["level"] == st.session_state.level]
    if not candidates:
        return None
    return random.choice(candidates)

def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if not st.session_state.started:
    st.subheader("Inicio")
    name = st.text_input("Nombre del estudiante")
    st.info(
        "Responderás preguntas adaptativas sobre hiperglucemia. "
        "Si aciertas, avanzarás en dificultad. Si fallas, recibirás una explicación y permanecerás en el mismo nivel."
    )
    if st.button("Comenzar", use_container_width=True, disabled=not name.strip()):
        st.session_state.name = name.strip()
        st.session_state.started = True
        q = choose_question()
        st.session_state.current_id = q["id"] if q else None
        st.rerun()
    st.stop()

if st.session_state.finished:
    st.success(f"Actividad finalizada, {st.session_state.name}.")
    st.metric("Puntaje", f"{st.session_state.score} aciertos")
    st.metric("Intentos", st.session_state.attempts)
    accuracy = (
        round((st.session_state.score / st.session_state.attempts) * 100)
        if st.session_state.attempts else 0
    )
    st.metric("Porcentaje de aciertos", f"{accuracy}%")
    st.write(f"Nivel máximo alcanzado: **{st.session_state.level}**")
    if st.button("Reiniciar actividad", use_container_width=True):
        reset_app()
    st.stop()

st.write(f"**Estudiante:** {st.session_state.name}")
st.progress(min(st.session_state.level / 4, 1.0))
st.write(f"Nivel actual: **{st.session_state.level} de 4**")

current = next((q for q in QUESTIONS if q["id"] == st.session_state.current_id), None)
if current is None:
    current = choose_question()
    if current:
        st.session_state.current_id = current["id"]
    else:
        st.session_state.finished = True
        st.rerun()

st.subheader(current["question"])

choice = st.radio(
    "Selecciona una alternativa:",
    options=list(current["options"].keys()),
    format_func=lambda x: f"{x}) {current['options'][x]}",
    index=None
)

if st.button("Responder", use_container_width=True, disabled=choice is None):
    st.session_state.attempts += 1
    correct = choice == current["correct"]

    if correct:
        st.session_state.score += 1
        st.session_state.errors_in_level = 0
        st.session_state.answered_ids.append(current["id"])
        st.session_state.feedback = ("success", "¡Correcto! " + current["feedback"][choice])

        if st.session_state.level < 4:
            st.session_state.level += 1
        else:
            if len([x for x in st.session_state.answered_ids if x in [q["id"] for q in QUESTIONS if q["level"] == 4]]) >= 2:
                st.session_state.finished = True

    else:
        st.session_state.errors_in_level += 1
        extra = ""
        if st.session_state.errors_in_level == 2:
            extra = " Has cometido dos errores en este nivel: revisa la relación entre el estímulo, la hormona y la respuesta fisiológica."
        elif st.session_state.errors_in_level >= 3:
            extra = " Recomendación: vuelve a identificar qué variable está alterada y qué mecanismo homeostático debería compensarla."
        st.session_state.feedback = ("error", "Incorrecto. " + current["feedback"][choice] + extra)

    next_q = choose_question()
    if next_q:
        st.session_state.current_id = next_q["id"]

    st.rerun()

if st.session_state.feedback:
    kind, msg = st.session_state.feedback
    if kind == "success":
        st.success(msg)
    else:
        st.error(msg)

with st.expander("¿Cómo funciona la adaptación?"):
    st.write(
        """
        - Respuesta correcta: aumenta el nivel de dificultad.
        - Respuesta incorrecta: mantiene el mismo nivel.
        - Dos errores consecutivos: agrega una microexplicación.
        - Tres o más errores: entrega una orientación adicional antes de continuar.
        """
    )
