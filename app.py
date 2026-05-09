import streamlit as st
from PIL import Image

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Sync-B",
    page_icon="🧠",
    layout="centered"
)

# --------------------------------------------------
# LOGO
# --------------------------------------------------

logo = Image.open("image (32).png")
# --------------------------------------------------
# FOOD DATABASE
# --------------------------------------------------

FOOD_DATABASE = {

    "café": {
        "type": "natural",
        "macro": "estimulante"
    },

    "pan integral": {
        "type": "natural",
        "macro": "carbohidrato complejo"
    },

    "pan blanco": {
        "type": "procesado",
        "macro": "carbohidrato rápido"
    },

    "huevo": {
        "type": "natural",
        "macro": "proteína"
    },

    "fruta": {
        "type": "natural",
        "macro": "carbohidrato natural"
    },

    "plátano": {
        "type": "natural",
        "macro": "carbohidrato natural"
    },

    "manzana": {
        "type": "natural",
        "macro": "carbohidrato natural"
    },

    "yogur": {
        "type": "natural",
        "macro": "proteína"
    },

    "avena": {
        "type": "natural",
        "macro": "carbohidrato complejo"
    },

    "bollería": {
        "type": "procesado",
        "macro": "azúcar + grasas"
    },

    "galletas": {
        "type": "procesado",
        "macro": "azúcar"
    },

    "zumo industrial": {
        "type": "procesado",
        "macro": "azúcar"
    },

    "cereales azucarados": {
        "type": "procesado",
        "macro": "azúcar"
    },

    "leche": {
        "type": "natural",
        "macro": "proteína/lípidos"
    },

    "queso": {
        "type": "natural",
        "macro": "proteína/lípidos"
    }
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = 1

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def next_page(page):
    st.session_state.page = page


def previous_page(page):
    st.session_state.page = page

def analyze_breakfast(breakfast_text):

    if not breakfast_text:
        return "No se ha registrado desayuno."

    items = [
        x.strip().lower()
        for x in breakfast_text.split(",")
    ]

    natural = 0
    processed = 0

    proteins = 0
    sugars = 0
    complex_carbs = 0

    analysis = []
    recommendations = []

    for item in items:

        if item in FOOD_DATABASE:

            food = FOOD_DATABASE[item]

            # NATURAL / PROCESSED

            if food["type"] == "natural":
                natural += 1
            else:
                processed += 1

            # MACROS

            macro = food["macro"]

            if "proteína" in macro:
                proteins += 1

            if "azúcar" in macro:
                sugars += 1

            if "complejo" in macro:
                complex_carbs += 1

    # --------------------------------------------------
    # FEEDBACK
    # --------------------------------------------------

    if len(items) == 1 and "café" in items:

        analysis.append("""
Aunque el café puede mejorar momentáneamente la activación y la concentración, tomarlo solo y en ayunas podría aumentar la activación del cortisol y generar energía menos estable durante la mañana.

Combinarlo con alimentos ricos en proteínas, fibra o carbohidratos complejos puede ayudarte a mantener una energía más sostenida y evitar bajones posteriores.
""")

        recommendations.append("""
Podrías probar a acompañar el café con alimentos como yogur, fruta, avena, huevos o pan integral para mejorar la estabilidad energética y la saciedad.
""")

    # --------------------------------------------------

    if processed >= 2:

        analysis.append("""
Tu desayuno parece contener una cantidad elevada de alimentos procesados o ricos en azúcares rápidos.

Esto puede provocar picos de glucosa y bajones de energía posteriores, afectando tanto a la concentración como al estado de ánimo.
""")

        recommendations.append("""
Reducir progresivamente la bollería industrial, cereales azucarados o zumos industriales y sustituirlos por alimentos más naturales podría ayudarte a mantener una energía más estable durante el día.
""")

    # --------------------------------------------------

    if sugars >= 2:

        analysis.append("""
La predominancia de azúcares rápidos podría favorecer una energía menos estable durante la mañana y una mayor sensación de cansancio horas después.
""")

        recommendations.append("""
Añadir proteínas o carbohidratos complejos como avena, yogur, huevos o pan integral puede ayudar a reducir los picos de glucosa y mejorar la saciedad.
""")

    # --------------------------------------------------

    if proteins >= 1 and complex_carbs >= 1:

        analysis.append("""
La combinación de proteínas y carbohidratos complejos favorece una liberación de energía más estable y sostenida, ayudando a mantener mejor la concentración y el bienestar físico.
""")

        recommendations.append("""
Mantener desayunos equilibrados como este puede favorecer un mejor rendimiento físico y mental durante la mañana.
""")

    # --------------------------------------------------

    if proteins == 0:

        analysis.append("""
Tu desayuno parece contener poca proteína, lo que podría hacer que la saciedad dure menos tiempo y favorecer bajones energéticos más rápidos.
""")

        recommendations.append("""
Añadir alimentos ricos en proteína como yogur, queso, huevos o frutos secos podría ayudarte a mantener una energía más estable.
""")

    # --------------------------------------------------

    if natural >= processed:

        analysis.append("""
La mayoría de los alimentos registrados son naturales o poco procesados, lo que suele relacionarse con una mejor estabilidad energética y hormonal.
""")

    # --------------------------------------------------

    if not analysis:

        analysis.append("""
Tu desayuno muestra un perfil relativamente equilibrado, aunque pequeños ajustes podrían ayudarte a mejorar todavía más tu energía y bienestar diario.
""")

    # --------------------------------------------------

    final_analysis = "\n\n".join(analysis)

    if recommendations:

        final_analysis += "\n\n💡 Recomendaciones nutricionales:\n\n"
        final_analysis += "\n".join(
            [f"• {r.strip()}" for r in recommendations]
        )

    return final_analysis


def calculate_profile():

    cortisol = 0
    serotonin = 0
    dopamine = 0
    oxytocin = 0

    diagnosis_parts = []
    recommendation_parts = []

    # --------------------------------------------------
    # RESPUESTAS
    # --------------------------------------------------

    sleep_quality = st.session_state.get("sleep_quality")
    wake_energy = st.session_state.get("wake_energy")
    calm = st.session_state.get("calm")
    exercise = st.session_state.get("exercise")
    social = st.session_state.get("social")
    self_esteem = st.session_state.get("self_esteem")

    # --------------------------------------------------
    # CORTISOL
    # --------------------------------------------------

    if sleep_quality in [
        "Tenía sueño pero no dormí",
        "Ni dormí ni tenía sueño"
    ]:
        cortisol += 3

    if calm in [
        "Nunca me siento en calma",
        "Rara vez"
    ]:
        cortisol += 3

    # --------------------------------------------------
    # DOPAMINA
    # --------------------------------------------------

    if wake_energy == "Poca":
        dopamine -= 2

    if exercise in [
        "Sí, mucho",
        "Sí, moderado"
    ]:
        dopamine += 2

    # --------------------------------------------------
    # OXITOCINA
    # --------------------------------------------------

    if social in [
        "Me cuesta bastante",
        "Me cuesta mucho y evito socializar"
    ]:
        oxytocin -= 2

    # --------------------------------------------------
    # SEROTONINA
    # --------------------------------------------------

    if self_esteem == "Baja":
        serotonin -= 2

    # --------------------------------------------------
    # DIAGNÓSTICO PERSONALIZADO
    # --------------------------------------------------

    if cortisol >= 5:

        diagnosis_parts.append("""
Tu cuerpo podría encontrarse actualmente en un estado de hiperactivación mantenida.
La combinación entre descanso insuficiente y baja regulación emocional puede hacer que el organismo permanezca más tiempo en estado de alerta, dificultando la recuperación física y mental.
""")

        recommendation_parts.append("""
Prioriza momentos de desconexión real durante el día.
Reducir estímulos antes de dormir, mantener horarios regulares y realizar actividades relajantes puede ayudarte a disminuir la activación del sistema nervioso.
""")

    if dopamine <= -2:

        diagnosis_parts.append("""
También se observan señales compatibles con fatiga mental y baja activación energética.
Esto puede traducirse en menor motivación, cansancio frecuente y dificultad para mantener la concentración sostenida.
""")

        recommendation_parts.append("""
La exposición a luz natural, el movimiento físico suave y mantener objetivos pequeños y alcanzables pueden ayudarte a mejorar progresivamente tu energía diaria.
""")

    if oxytocin <= -2:

        diagnosis_parts.append("""
Tus respuestas también reflejan cierta tendencia al aislamiento o dificultad para mantener relaciones sociales con comodidad.
El apoyo social y las conexiones emocionales saludables son importantes para el equilibrio emocional y hormonal.
""")

    if serotonin <= -2:

        diagnosis_parts.append("""
La autoestima y la percepción emocional sobre uno mismo también parecen estar influyendo en tu bienestar general.
""")

    if not diagnosis_parts:

        diagnosis_parts.append("""
En general mantienes un estado relativamente equilibrado tanto a nivel físico como emocional.
Tus respuestas reflejan una buena adaptación general a las exigencias del día a día.
""")

        recommendation_parts.append("""
Mantener hábitos saludables y momentos de desconexión seguirá siendo importante para conservar ese equilibrio a largo plazo.
""")

    # --------------------------------------------------
    # HORMONAL
    # --------------------------------------------------

    gender = st.session_state.get("gender")

    if gender != "Mujer":

        hormonal_text = """
Hormonas relacionadas con el estrés como el cortisol podrían estar influyendo en tu descanso y energía diaria.

También es importante favorecer hábitos que estimulen neurotransmisores relacionados con el bienestar, como la serotonina y la dopamina, especialmente mediante descanso adecuado, ejercicio físico y relaciones sociales saludables.
"""

    else:

        reproductive_state = st.session_state.get("reproductive_state")

        if reproductive_state == "Estoy embarazada":

            hormonal_text = """
Durante el embarazo se producen importantes cambios hormonales que pueden influir tanto en el sueño como en el estado emocional y la energía diaria.

Es normal experimentar cambios emocionales o mayor cansancio debido a las variaciones hormonales propias de esta etapa.
"""

        elif reproductive_state == "Estoy en menopausia":

            hormonal_text = """
La menopausia implica cambios hormonales importantes que pueden afectar al descanso, la regulación emocional y la energía física.

Mantener hábitos saludables y actividad física moderada puede ayudarte a mejorar la adaptación física y emocional durante esta etapa.
"""

        else:

            phase = st.session_state.get("cycle_phase")

            hormonal_text = f"""
La fase actual de tu ciclo menstrual ({phase}) puede influir directamente tanto en tu estado emocional como en tu energía y bienestar físico.

Las variaciones hormonales normales del ciclo pueden modificar el descanso, la sensibilidad emocional, la motivación y el nivel de energía.
"""

    diagnosis = "\n\n".join(diagnosis_parts)
    recommendations = "\n\n".join(recommendation_parts)

    return diagnosis, recommendations, hormonal_text


# --------------------------------------------------
# STYLE
# --------------------------------------------------

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Poppins:wght@300;400;500&display=swap');

   html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    color: #1f2937;
}

    .stApp {
    background: linear-gradient(
        180deg,
        #f7f9ff 0%,
        #eef2ff 50%,
        #e0f2fe 100%
    );
}
    p, label, div {
        font-weight: 300;
    }

    .main-title {
        text-align: center;
        font-size: 95px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        letter-spacing: 6px;
        margin-bottom: 0;
        color: #1f2937;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 24px;
        font-weight: 300;
        margin-top: -15px;
        margin-bottom: 20px;
    }

    .glass-box {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 1.5rem;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    color: #1f2937;
}

    .warning-box {
        background: linear-gradient(
            90deg,
            rgba(20,184,166,0.18),
            rgba(59,130,246,0.18)
        );

        border-left: 4px solid #14b8a6;

        padding: 1rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;

        color: white;
    }

    .stButton > button {

        width: 100%;
        border-radius: 16px;
        height: 3.2em;

        font-size: 18px;
        font-weight: 600;

        font-family: 'Orbitron', sans-serif;

        background: linear-gradient(
            90deg,
            #14b8a6,
            #3b82f6
        );

        color: white;
        border: none;

        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        opacity: 0.95;
    }

    h1, h2, h3, h4, h5, h6,
    p, label, div, span {
    color: #1f2937 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# PAGE 1
# --------------------------------------------------

if st.session_state.page == 1:

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.image(logo, width=350)

    st.markdown(
        """
        <h1 class='main-title'>SYNC-B</h1>
        <p class='subtitle'>Evalúa tu salud de forma integrativa</p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='warning-box'>
        <b>Importante:</b> Sync-B no sustituye una valoración médica profesional. Los resultados mostrados son únicamente orientativos.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='glass-box'>
        <h3 style='text-align:center;'>¿Cómo te sientes hoy?</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("START"):
        next_page(2)

# --------------------------------------------------
# PAGE 2
# --------------------------------------------------

elif st.session_state.page == 2:

    st.title("Perfil del usuario")

    gender = st.radio(
        "Selecciona una opción:",
        ["Hombre", "Mujer", "Prefiero no decirlo"],
        key="gender"
    )


    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Atrás"):
            previous_page(1)

    with col2:
        if st.button("Continuar"):

            if gender == "Mujer":
                next_page(3)
            else:
                next_page(4)

# --------------------------------------------------
# PAGE 3
# --------------------------------------------------

elif st.session_state.page == 3:

    st.title("Test 1 · Contexto hormonal")

    reproductive_state = st.radio(
        "Háblanos de tu situación actual",
        [
            "Tengo la regla de forma normal",
            "Estoy embarazada",
            "Estoy en menopausia"
        ],
        key="reproductive_state"
    )

    cycle_phase = None
    disorder = None
    disorder_type = None

    if reproductive_state == "Tengo la regla de forma normal":

        cycle_phase = st.radio(
            "¿En qué fase del ciclo te encuentras?",
            [
                "Fase menstrual",
                "Fase folicular",
                "Ovulación",
                "Fase premenstrual"
            ],
            key="cycle_phase"
        )

        disorder = st.radio(
            "¿Tienes algún trastorno menstrual diagnosticado?",
            ["Sí", "No"],
            key="disorder"
        )

        if disorder == "Sí":

            disorder_type = st.selectbox(
                "¿Cuál?",
                [
                    "SOP",
                    "Endometriosis",
                    "Amenorrea",
                    "Dismenorrea",
                    "Causa desconocida"
                ]
            )

    physical_activity = st.radio(
        "¿Cómo ha sido tu actividad física recientemente?",
        [
            "Hago más ejercicio de lo normal",
            "Hago lo mismo que habitualmente",
            "Hago poco ejercicio",
            "Nunca hago ejercicio"
        ],
        key="physical_activity"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Atrás"):
            previous_page(2)

    with col2:
        if st.button("Continuar al Test 2"):

            next_page(4)

# --------------------------------------------------
# PAGE 4
# --------------------------------------------------

elif st.session_state.page == 4:

    st.title("Test 2 · Estado general")

    sleep_quality = st.radio(
        "1. Sueño y descanso",
        [
            "He dormido bien y descansado",
            "Dormí pero no descansé",
            "Tenía sueño pero no dormí",
            "Ni dormí ni tenía sueño"
        ]
    )

    sleep_hours = st.radio(
        "2. ¿Cuántas horas dormiste?",
        ["<3", "3-5", "5-7", ">7"]
    )

    wake_energy = st.radio(
        "3. ¿Con cuánta energía te despiertas?",
        ["Mucha", "Media", "Poca"]
    )

    breakfast = st.text_input(
        "4. Indica un máximo de 3 alimentos o bebidas que sueles desayunar"
    )

    bathroom = st.radio(
        "5. ¿Vas al baño por la mañana?",
        [
            "Sí",
            "No",
            "A veces"
        ]
    )

    concentration = st.slider(
        "6. ¿Te cuesta concentrarte?",
        1,
        5,
        3
    )

    calm = st.radio(
        "7. ¿Sueles sentir calma emocional?",
        [
            "Nunca me siento en calma",
            "Rara vez",
            "A veces",
            "Frecuentemente",
            "Siempre"
        ]
    )

    self_esteem = st.radio(
        "8. Valora tu autoestima",
        [
            "Alta",
            "Media",
            "Baja"
        ]
    )

    social = st.radio(
        "9. ¿Te cuesta mantener relaciones sociales?",
        [
            "No me cuesta",
            "A veces me cuesta",
            "Me cuesta bastante",
            "Me cuesta mucho y evito socializar"
        ]
    )

    exercise = st.radio(
        "10. ¿Haces ejercicio?",
        [
            "Sí, mucho",
            "Sí, moderado",
            "Ocasionalmente",
            "Nunca"
        ]
    )

    post_exercise = st.radio(
        "11. ¿Cómo te sientes después de hacerlo?",
        [
            "Me siento mejor",
            "Me siento igual",
            "Me siento peor"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("⬅ Atrás"):

            if st.session_state.get("gender") == "Mujer":
                previous_page(3)
            else:
                previous_page(2)

    with col2:

        if st.button("Ver resultados"):

            st.session_state.sleep_quality = sleep_quality
            st.session_state.sleep_hours = sleep_hours
            st.session_state.wake_energy = wake_energy
            st.session_state.breakfast = breakfast
            st.session_state.bathroom = bathroom
            st.session_state.concentration = concentration
            st.session_state.calm = calm
            st.session_state.self_esteem = self_esteem
            st.session_state.social = social
            st.session_state.exercise = exercise
            st.session_state.post_exercise = post_exercise

            next_page(5)

# --------------------------------------------------
# PAGE 5
# --------------------------------------------------

elif st.session_state.page == 5:

    diagnosis, recommendations, hormonal_text = calculate_profile()

    st.title("Resultados")

    st.markdown(
        """
        <div class='warning-box'>
        Los resultados mostrados son únicamente orientativos y no sustituyen una valoración médica profesional.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class='glass-box'>
        <h2>{diagnosis}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Recomendaciones")

    st.write(recommendations)

    st.markdown("---")

    st.subheader("Resumen de tus respuestas")

    st.write(f"**Calidad del sueño:** {st.session_state.get('sleep_quality', 'No registrado')}")
    st.write(f"**Energía al despertar:** {st.session_state.get('wake_energy', 'No registrado')}")
    st.write(f"**Calma emocional:** {st.session_state.get('calm', 'No registrado')}")
    st.write(f"**Ejercicio:** {st.session_state.get('exercise', 'No registrado')}")

    st.markdown("---")

    st.subheader("Contexto hormonal")

    st.write(hormonal_text)

    st.markdown("---")

    st.subheader("🍽 Alimentación y energía")

    food_feedback = analyze_breakfast(
        st.session_state.get("breakfast")
    )

    st.write(food_feedback)

    if st.session_state.get("gender") == "Mujer":

        st.markdown("---")

        st.write(
         f"**Situación actual:** {st.session_state.get('reproductive_state', 'No registrado')}"
        )

       if st.session_state.get("reproductive_state") == "Tengo la regla de forma normal":

           st.write(
               f"**Fase del ciclo:** {st.session_state.get('cycle_phase', 'No registrada')}"
           )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Reiniciar test"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
