
import json
import random
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="FisioGlucosa IA",
    page_icon="🧠",
    layout="centered"
)

DATA_FILE = Path(__file__).parent / "preguntas_fisioglucosa.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

LEVELS = sorted(set(q["level"] for q in QUESTIONS))
MAX_LEVEL = max(LEVELS)

# ---------- Estado ----------
defaults = {
    "started": False,
    "name": "",
    "level": 1,
    "score": 0,
    "attempts": 0,
    "errors_in_topic": 0,
    "answered_ids": [],
    "current_id": None,
    "feedback_type": None,
    "feedback_text": None,
    "show_continue": False,
    "verification_mode": False,
    "verification_question": None,
    "verification_parent_id": None,
    "finished": False,
    "concepts_mastered": [],
    "concepts_difficult": [],
    "last_question_topic": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------- Utilidades ----------
def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def get_question(qid):
    return next((q for q in QUESTIONS if q["id"] == qid), None)


def candidates_for_level(level):
    unused = [
        q for q in QUESTIONS
        if q["level"] == level and q["id"] not in st.session_state.answered_ids
    ]
    if unused:
        return unused
    return [q for q in QUESTIONS if q["level"] == level]


def choose_question(level=None, exclude_id=None, same_topic=None):
    level = level or st.session_state.level

    pool = [
        q for q in QUESTIONS
        if q["level"] == level
        and q["id"] != exclude_id
        and q["id"] not in st.session_state.answered_ids
    ]

    if same_topic:
        topic_pool = [q for q in pool if q["topic"] == same_topic]
        if topic_pool:
            return random.choice(topic_pool)

    if not pool:
        pool = [
            q for q in QUESTIONS
            if q["level"] == level and q["id"] != exclude_id
        ]

    return random.choice(pool) if pool else None


def set_new_question(level=None, exclude_id=None, same_topic=None):
    q = choose_question(level=level, exclude_id=exclude_id, same_topic=same_topic)
    if q:
        st.session_state.current_id = q["id"]
        st.session_state.last_question_topic = q["topic"]
    else:
        st.session_state.finished = True


def advance_after_correct(current):
    if current["topic"] not in st.session_state.concepts_mastered:
        st.session_state.concepts_mastered.append(current["topic"])

    st.session_state.errors_in_topic = 0
    st.session_state.answered_ids.append(current["id"])

    # Regla: respuesta correcta aumenta dificultad o avanza contenido.
    if st.session_state.level < MAX_LEVEL:
        st.session_state.level += 1
        set_new_question(level=st.session_state.level)
    else:
        remaining_level4 = [
            q for q in QUESTIONS
            if q["level"] == MAX_LEVEL
            and q["id"] not in st.session_state.answered_ids
        ]
        if remaining_level4:
            set_new_question(level=MAX_LEVEL)
        else:
            st.session_state.finished = True


def after_failed_verification(parent_q):
    topic = parent_q["topic"]
    if topic not in st.session_state.concepts_difficult:
        st.session_state.concepts_difficult.append(topic)

    st.session_state.feedback_type = "warning"
    st.session_state.feedback_text = (
        "Todavía cuesta este concepto. Vamos a reforzarlo una vez más con una explicación "
        "más guiada antes de continuar.\n\n"
        f"**Idea clave:** {parent_q['remediation']}\n\n"
        "No necesitas memorizar la respuesta anterior: intenta relacionar el estímulo, "
        "la hormona implicada y el efecto fisiológico."
    )
    st.session_state.show_continue = True
    st.session_state.verification_mode = False
    st.session_state.verification_question = None
    st.session_state.verification_parent_id = None

    # Mantener nivel y cambiar de pregunta.
    set_new_question(
        level=parent_q["level"],
        exclude_id=parent_q["id"],
        same_topic=parent_q["topic"]
    )


# ---------- Encabezado ----------
st.title("FisioGlucosa IA")
st.caption("Sistema de aprendizaje adaptativo sobre hiperglucemia")


# ---------- Inicio ----------
if not st.session_state.started:
    st.subheader("Inicio")
    name = st.text_input("Nombre del estudiante")

    st.info(
        "Responderás preguntas de selección múltiple. "
        "Si respondes correctamente, avanzarás en dificultad. "
        "Si te equivocas, recibirás retroalimentación y continuarás practicando el mismo nivel."
    )

    if st.button("Comenzar", use_container_width=True, disabled=not name.strip()):
        st.session_state.name = name.strip()
        st.session_state.started = True
        set_new_question(level=1)
        st.rerun()

    st.stop()


# ---------- Final ----------
if st.session_state.finished:
    st.success(f"Actividad finalizada, {st.session_state.name}.")

    accuracy = (
        round((st.session_state.score / st.session_state.attempts) * 100)
        if st.session_state.attempts else 0
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Aciertos", st.session_state.score)
    c2.metric("Intentos", st.session_state.attempts)
    c3.metric("Precisión", f"{accuracy}%")

    st.write(f"**Nivel máximo alcanzado:** {st.session_state.level}")

    if st.session_state.concepts_mastered:
        st.write("**Conceptos comprendidos:**")
        st.write(", ".join(st.session_state.concepts_mastered))

    if st.session_state.concepts_difficult:
        st.write("**Conceptos que conviene repasar:**")
        st.write(", ".join(st.session_state.concepts_difficult))

    if st.button("Reiniciar actividad", use_container_width=True):
        reset_app()

    st.stop()


# ---------- Progreso ----------
st.write(f"**Estudiante:** {st.session_state.name}")
st.progress(min(st.session_state.level / MAX_LEVEL, 1.0))
st.write(f"Nivel actual: **{st.session_state.level} de {MAX_LEVEL}**")


# ---------- Feedback pendiente ----------
if st.session_state.feedback_text:
    if st.session_state.feedback_type == "success":
        st.success(st.session_state.feedback_text)
    elif st.session_state.feedback_type == "error":
        st.error(st.session_state.feedback_text)
    else:
        st.warning(st.session_state.feedback_text)

    if st.session_state.show_continue:
        if st.button("Continuar", use_container_width=True):
            st.session_state.feedback_text = None
            st.session_state.feedback_type = None
            st.session_state.show_continue = False
            st.rerun()
        st.stop()


# ---------- Modo verificación ----------
if st.session_state.verification_mode:
    parent_q = get_question(st.session_state.verification_parent_id)
    vq = st.session_state.verification_question

    st.info(
        "Tranquilo, revisemos juntos por qué no está resultando todavía.\n\n"
        f"{parent_q['remediation']}\n\n"
        "**Ahora comprueba si entendiste la idea:**"
    )

    st.subheader(vq["question"])

    choice = st.radio(
        "Selecciona una alternativa:",
        options=list(vq["options"].keys()),
        format_func=lambda x: f"{x}) {vq['options'][x]}",
        index=None,
        key="verification_choice"
    )

    if st.button("Responder verificación", use_container_width=True, disabled=choice is None):
        st.session_state.attempts += 1

        if choice == vq["correct"]:
            st.session_state.score += 1

            if parent_q["topic"] not in st.session_state.concepts_mastered:
                st.session_state.concepts_mastered.append(parent_q["topic"])

            st.session_state.feedback_type = "success"
            st.session_state.feedback_text = (
                "¡Bien! Ahora sí se observa comprensión del concepto. "
                + vq["feedback"]
            )
            st.session_state.show_continue = True
            st.session_state.verification_mode = False
            st.session_state.verification_question = None
            st.session_state.verification_parent_id = None
            st.session_state.errors_in_topic = 0

            # Tras superar la verificación, avanza.
            if parent_q["level"] < MAX_LEVEL:
                st.session_state.level = parent_q["level"] + 1
                set_new_question(level=st.session_state.level)
            else:
                set_new_question(level=MAX_LEVEL, exclude_id=parent_q["id"])
        else:
            after_failed_verification(parent_q)

        st.rerun()

    st.stop()


# ---------- Pregunta normal ----------
current = get_question(st.session_state.current_id)

if current is None:
    set_new_question(level=st.session_state.level)
    current = get_question(st.session_state.current_id)

if current is None:
    st.session_state.finished = True
    st.rerun()

st.caption(f"Tema: {current['topic']}")
st.subheader(current["question"])

choice = st.radio(
    "Selecciona una alternativa:",
    options=list(current["options"].keys()),
    format_func=lambda x: f"{x}) {current['options'][x]}",
    index=None,
    key=f"q_{current['id']}"
)

if st.button("Responder", use_container_width=True, disabled=choice is None):
    st.session_state.attempts += 1

    if choice == current["correct"]:
        st.session_state.score += 1
        st.session_state.feedback_type = "success"
        st.session_state.feedback_text = (
            "¡Muy bien! " + current["feedback"][choice]
        )
        st.session_state.show_continue = True

        advance_after_correct(current)

    else:
        st.session_state.errors_in_topic += 1

        if current["topic"] not in st.session_state.concepts_difficult:
            st.session_state.concepts_difficult.append(current["topic"])

        # Primer error
        if st.session_state.errors_in_topic == 1:
            st.session_state.feedback_type = "error"
            st.session_state.feedback_text = (
                "Esa alternativa no es correcta. "
                + current["feedback"][choice]
                + "\n\nVamos a intentar otra pregunta del mismo nivel."
            )
            st.session_state.show_continue = True

            # Mantiene nivel y presenta otra pregunta distinta.
            set_new_question(
                level=current["level"],
                exclude_id=current["id"],
                same_topic=current["topic"]
            )

        # Segundo error consecutivo
        else:
            st.session_state.verification_mode = True
            st.session_state.verification_question = current["verification"]
            st.session_state.verification_parent_id = current["id"]
            st.session_state.feedback_text = None
            st.session_state.feedback_type = None
            st.session_state.show_continue = False

    st.rerun()
