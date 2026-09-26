
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


LOGO_FILE = Path(__file__).parent / "logo_ucsh.png"

CUSTOM_CSS = """
<style>
    /* Diseño base */
    .stApp {
        background: linear-gradient(180deg, #f4f8ff 0%, #eef7f2 100%);
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1.5rem;
        max-width: 760px;
    }

    .app-hero {
        background: linear-gradient(135deg, rgba(30, 78, 121, 0.10), rgba(72, 160, 111, 0.10));
        border: 1px solid rgba(30, 78, 121, 0.18);
        border-radius: 16px;
        padding: 0.9rem 1rem 0.75rem 1rem;
        margin-bottom: 0.8rem;
    }

    .app-hero h1 {
        color: #16324f;
        margin: 0.25rem 0 0.15rem 0;
        font-size: 1.7rem;
        line-height: 1.15;
    }

    .app-hero p {
        color: #2f4f4f;
        margin-bottom: 0;
        font-size: 0.95rem;
        line-height: 1.35;
    }

    .soft-card {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(22, 50, 79, 0.10);
        border-radius: 14px;
        padding: 0.8rem 0.9rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 6px 18px rgba(22, 50, 79, 0.05);
    }

    div[data-testid="stMetricValue"] {
        color: #16324f;
    }

    div[data-testid="stProgressBar"] > div > div > div {
        background-color: #2e8b57;
    }

    /* Botones cómodos en pantalla táctil */
    .stButton > button {
        min-height: 44px;
        border-radius: 10px;
        font-weight: 600;
    }

    /* CELULAR */
    @media (max-width: 640px) {
        .main .block-container {
            padding-top: 0.45rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            padding-bottom: 1rem;
        }

        .app-hero {
            padding: 0.65rem 0.75rem;
            border-radius: 12px;
            margin-bottom: 0.6rem;
        }

        .app-hero h1 {
            font-size: 1.35rem;
            line-height: 1.1;
            margin-top: 0.15rem;
        }

        .app-hero p {
            font-size: 0.82rem;
            line-height: 1.25;
        }

        h2 {
            font-size: 1.18rem !important;
            line-height: 1.25 !important;
        }

        h3 {
            font-size: 1.05rem !important;
            line-height: 1.25 !important;
        }

        p, label, .stMarkdown, div[data-testid="stRadio"] {
            font-size: 0.92rem;
            line-height: 1.35;
        }

        div[data-testid="stAlert"] {
            padding: 0.7rem 0.75rem;
            font-size: 0.88rem;
        }

        .soft-card {
            padding: 0.65rem 0.7rem;
            border-radius: 12px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.25rem;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.75rem;
        }

        .stButton > button {
            min-height: 46px;
            font-size: 0.95rem;
        }

        /* Reduce separación entre alternativas */
        div[role="radiogroup"] > label {
            padding-top: 0.15rem;
            padding-bottom: 0.15rem;
        }
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="app-hero">', unsafe_allow_html=True)
    if LOGO_FILE.exists():
        st.image(str(LOGO_FILE), width=110)
    st.markdown(
        "<h1>FisioGlucosa IA</h1>"
        "<p>Sistema de aprendizaje adaptativo sobre hiperglucemia</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

MAX_MAIN_QUESTIONS = 10
MAX_LEVEL = 4

PRAISE = [
    "¡Muy bien!",
    "¡Genial!",
    "¡Fantástico!",
    "¡Excelente!",
    "¡Bien hecho!",
    "¡Te felicito!",
    "¡Muy buena respuesta!",
    "¡Perfecto!"
]

defaults = {
    "started": False,
    "name": "",
    "level": 1,
    "score": 0,
    "attempts": 0,
    "main_questions_answered": 0,
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
    "last_praise": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def get_question(qid):
    return next((q for q in QUESTIONS if q["id"] == qid), None)


def available_questions(level, exclude_id=None):
    pool = [
        q for q in QUESTIONS
        if q["level"] == level
        and q["id"] != exclude_id
        and q["id"] not in st.session_state.answered_ids
    ]
    if not pool:
        pool = [
            q for q in QUESTIONS
            if q["level"] == level and q["id"] != exclude_id
        ]
    return pool


def choose_question(level=None, exclude_id=None):
    level = level or st.session_state.level
    pool = available_questions(level, exclude_id=exclude_id)
    return random.choice(pool) if pool else None


def set_new_question(level=None, exclude_id=None):
    q = choose_question(level=level, exclude_id=exclude_id)
    if q:
        st.session_state.current_id = q["id"]
        st.session_state.last_question_topic = q["topic"]
    else:
        st.session_state.finished = True


def next_level_from_progress():
    # Reparte 10 preguntas principales en 2-2-3-3
    n = st.session_state.main_questions_answered
    if n < 2:
        return 1
    elif n < 4:
        return 2
    elif n < 7:
        return 3
    return 4


def finish_if_needed():
    if st.session_state.main_questions_answered >= MAX_MAIN_QUESTIONS:
        st.session_state.finished = True
        return True
    return False


def get_unique_praise():
    options = [x for x in PRAISE if x != st.session_state.last_praise]
    choice = random.choice(options if options else PRAISE)
    st.session_state.last_praise = choice
    return choice


if not st.session_state.started:
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.subheader("Bienvenido(a)")
    name = st.text_input("Nombre del estudiante")

    st.info(
        "Realizarás **10 preguntas** sobre hiperglucemia.\n\n"
        "Las preguntas irán **aumentando progresivamente en complejidad**. "
        "Si respondes correctamente, avanzarás hacia contenidos más desafiantes. "
        "Si te equivocas, no pasa nada: practicaremos un poco más, recibirás una explicación "
        "y tendrás otra oportunidad para comprender el concepto antes de continuar."
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Comenzar actividad", use_container_width=True, disabled=not name.strip()):
        st.session_state.name = name.strip()
        st.session_state.started = True
        st.session_state.level = 1
        set_new_question(level=1)
        st.rerun()

    st.stop()


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

    st.write(f"**Preguntas principales completadas:** {st.session_state.main_questions_answered} de {MAX_MAIN_QUESTIONS}")

    if st.session_state.concepts_mastered:
        st.write("**Fortalezas observadas:**")
        st.write(", ".join(st.session_state.concepts_mastered))

    if st.session_state.concepts_difficult:
        st.write("**Conceptos que conviene reforzar:**")
        st.write(", ".join(st.session_state.concepts_difficult))

    if accuracy >= 80:
        st.success("Buen desempeño general. Has logrado avanzar con seguridad a través de los contenidos.")
    elif accuracy >= 60:
        st.info("Buen progreso. Hay algunos conceptos que conviene repasar para consolidar el aprendizaje.")
    else:
        st.warning("Este resultado indica que algunos conceptos necesitan más práctica. El objetivo es aprender, no solo acertar.")

    if st.button("Reiniciar actividad", use_container_width=True):
        reset_app()

    st.stop()


st.write(f"**Estudiante:** {st.session_state.name}")
st.progress(min(st.session_state.main_questions_answered / MAX_MAIN_QUESTIONS, 1.0))
st.write(f"Pregunta principal: **{st.session_state.main_questions_answered + 1} de {MAX_MAIN_QUESTIONS}**")
st.write(f"Nivel de complejidad: **{st.session_state.level} de {MAX_LEVEL}**")


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


if st.session_state.verification_mode:
    parent_q = get_question(st.session_state.verification_parent_id)
    vq = st.session_state.verification_question

    st.warning(
        "Mira, aquí te lo explico mejor.\n\n"
        f"{parent_q['remediation']}\n\n"
        "Ahora intenta responder esta pregunta de comprobación. "
        "No es la misma pregunta anterior: queremos verificar que comprendiste la idea."
    )

    st.subheader(vq["question"])

    choice = st.radio(
        "Selecciona una alternativa:",
        options=list(vq["options"].keys()),
        format_func=lambda x: f"{x}) {vq['options'][x]}",
        index=None,
        key=f"verification_{parent_q['id']}"
    )

    if st.button("Responder comprobación", use_container_width=True, disabled=choice is None):
        st.session_state.attempts += 1

        if choice == vq["correct"]:
            st.session_state.score += 1
            praise = get_unique_praise()
            st.session_state.feedback_type = "success"
            st.session_state.feedback_text = (
                f"{praise} {vq['feedback']} "
                "Ahora sí podemos continuar."
            )
            if parent_q["topic"] not in st.session_state.concepts_mastered:
                st.session_state.concepts_mastered.append(parent_q["topic"])

            st.session_state.verification_mode = False
            st.session_state.verification_question = None
            st.session_state.verification_parent_id = None
            st.session_state.errors_in_topic = 0
            st.session_state.show_continue = True

            st.session_state.main_questions_answered += 1
            if not finish_if_needed():
                st.session_state.level = next_level_from_progress()
                set_new_question(level=st.session_state.level, exclude_id=parent_q["id"])

        else:
            st.session_state.feedback_type = "warning"
            st.session_state.feedback_text = (
                "Todavía cuesta un poco, pero está bien. "
                "Vamos a reforzar la idea antes de seguir.\n\n"
                f"**Explicación:** {parent_q['remediation']}\n\n"
                "Fíjate especialmente en qué variable cambia, qué hormona participa "
                "y cuál debería ser la respuesta fisiológica."
            )
            if parent_q["topic"] not in st.session_state.concepts_difficult:
                st.session_state.concepts_difficult.append(parent_q["topic"])

            st.session_state.verification_mode = False
            st.session_state.verification_question = None
            st.session_state.verification_parent_id = None
            st.session_state.errors_in_topic = 0
            st.session_state.show_continue = True

            # Sigue en el mismo nivel y con otra pregunta distinta
            set_new_question(level=parent_q["level"], exclude_id=parent_q["id"])

        st.rerun()

    st.stop()


current = get_question(st.session_state.current_id)

if current is None:
    set_new_question(level=st.session_state.level)
    current = get_question(st.session_state.current_id)

if current is None:
    st.session_state.finished = True
    st.rerun()

st.subheader(current["question"])

choice = st.radio(
    "Selecciona una alternativa:",
    options=list(current["options"].keys()),
    format_func=lambda x: f"{x}) {current['options'][x]}",
    index=None,
    key=f"q_{current['id']}_{st.session_state.main_questions_answered}"
)

if st.button("Responder", use_container_width=True, disabled=choice is None):
    st.session_state.attempts += 1

    if choice == current["correct"]:
        st.session_state.score += 1
        praise = get_unique_praise()

        st.session_state.feedback_type = "success"
        st.session_state.feedback_text = (
            f"{praise} {current['feedback'][choice]}\n\n"
            f"**Concepto trabajado:** {current['topic']}"
        )
        st.session_state.show_continue = True
        st.session_state.errors_in_topic = 0

        if current["topic"] not in st.session_state.concepts_mastered:
            st.session_state.concepts_mastered.append(current["topic"])

        if current["id"] not in st.session_state.answered_ids:
            st.session_state.answered_ids.append(current["id"])

        st.session_state.main_questions_answered += 1

        if not finish_if_needed():
            st.session_state.level = next_level_from_progress()
            set_new_question(level=st.session_state.level, exclude_id=current["id"])

    else:
        st.session_state.errors_in_topic += 1

        if current["topic"] not in st.session_state.concepts_difficult:
            st.session_state.concepts_difficult.append(current["topic"])

        if st.session_state.errors_in_topic == 1:
            st.session_state.feedback_type = "error"
            st.session_state.feedback_text = (
                "Tranquilo(a), no pasa nada. Te explico.\n\n"
                f"{current['feedback'][choice]}\n\n"
                f"**Concepto que estamos practicando:** {current['topic']}\n\n"
                "Vamos a practicar otra pregunta del mismo nivel antes de avanzar."
            )
            st.session_state.show_continue = True

            # No cuenta como pregunta principal completada porque aún no se domina
            set_new_question(level=current["level"], exclude_id=current["id"])

        else:
            st.session_state.verification_mode = True
            st.session_state.verification_question = current["verification"]
            st.session_state.verification_parent_id = current["id"]
            st.session_state.feedback_text = None
            st.session_state.feedback_type = None
            st.session_state.show_continue = False

    st.rerun()
