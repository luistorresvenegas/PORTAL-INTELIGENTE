from pathlib import Path
import ast
import hashlib


print("=" * 110)
print("PORTAL INTELIGENTE DE EMPLEO · R1.4-B")
print("VERIFICACIÓN REAL DEL CIERRE INSTITUCIONAL")
print("SOLO LECTURA")
print("=" * 110)


EXPECTED_SHA = (
    "fd68c8ed4497d6bbf9e046f0f374b07346b2c03f03f86f1f4b7fc60b7f39b9dd"
)

EXPECTED_TEXT = (
    "Este análisis utiliza la información disponible en tu CV y en la oferta. "
    "Es una orientación para tomar mejores decisiones y no garantiza avanzar "
    "en un proceso de selección."
)


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


# ==============================================================================================
# 1. LOCALIZAR R1.4-B
# ==============================================================================================

candidates = [
    Path(
        "/content/PORTAL_V01810_R14B/streamlit_app_v01810r14b.py"
    ),
    Path(
        "/content/streamlit_app_v01810r14b.py"
    ),
]

portal = None


for path in candidates:

    if path.exists():
        portal = path
        break


if portal is None:

    for path in Path("/content").rglob(
        "streamlit_app_v01810r14b.py"
    ):

        portal = path
        break


if portal is None:

    raise FileNotFoundError(
        "❌ No se encontró R1.4-B."
    )


source = portal.read_text(
    encoding="utf-8"
)

sha_before = sha256_file(
    portal
)


print()
print(
    "✅ Archivo:",
    portal,
)

print(
    "✅ SHA:",
    sha_before,
)


if sha_before != EXPECTED_SHA:

    raise RuntimeError(
        "❌ El SHA no corresponde a R1.4-B aprobada."
    )


print(
    "✅ Hash R1.4-B confirmado"
)


# ==============================================================================================
# 2. AST / COMPILACIÓN
# ==============================================================================================

tree = ast.parse(
    source
)

compile(
    source,
    str(portal),
    "exec",
)


print(
    "✅ AST válido"
)

print(
    "✅ Archivo compila"
)


# ==============================================================================================
# 3. LEER EL VALOR REAL DE CIERRE_INSTITUCIONAL_V018902
# ==============================================================================================

valor_cierre = None
linea_cierre = None


for node in tree.body:

    if isinstance(
        node,
        ast.Assign,
    ):

        for target in node.targets:

            if (
                isinstance(
                    target,
                    ast.Name,
                )
                and
                target.id
                ==
                "CIERRE_INSTITUCIONAL_V018902"
            ):

                linea_cierre = node.lineno

                try:
                    valor_cierre = ast.literal_eval(
                        node.value
                    )

                except Exception:
                    valor_cierre = None


    elif isinstance(
        node,
        ast.AnnAssign,
    ):

        target = node.target

        if (
            isinstance(
                target,
                ast.Name,
            )
            and
            target.id
            ==
            "CIERRE_INSTITUCIONAL_V018902"
        ):

            linea_cierre = node.lineno

            try:
                valor_cierre = ast.literal_eval(
                    node.value
                )

            except Exception:
                valor_cierre = None


print()
print("-" * 110)
print("CIERRE INSTITUCIONAL")
print("-" * 110)


if linea_cierre is None:

    print(
        "❌ No se encontró la definición "
        "CIERRE_INSTITUCIONAL_V018902"
    )

else:

    print(
        f"✅ Constante encontrada en línea {linea_cierre}"
    )


if valor_cierre is None:

    print(
        "❌ No fue posible evaluar el valor estático de la constante"
    )

else:

    print()
    print(
        "Valor real:"
    )

    print(
        repr(
            valor_cierre
        )
    )


# ==============================================================================================
# 4. COMPARACIÓN EXACTA
# ==============================================================================================

coincide_exacto = (
    valor_cierre
    ==
    EXPECTED_TEXT
)


print()
print(
    "✅ Texto EXACTO preservado"
    if coincide_exacto
    else
    "❌ El texto real difiere del cierre institucional esperado"
)


if valor_cierre is not None and not coincide_exacto:

    print()
    print(
        "Esperado:"
    )

    print(
        repr(
            EXPECTED_TEXT
        )
    )

    print()
    print(
        "Obtenido:"
    )

    print(
        repr(
            valor_cierre
        )
    )


# ==============================================================================================
# 5. COMPROBAR QUE render_analisis_profesional_v01877 LO USA
# ==============================================================================================

render_node = None


for node in tree.body:

    if (
        isinstance(
            node,
            ast.FunctionDef,
        )
        and
        node.name
        ==
        "render_analisis_profesional_v01877"
    ):

        render_node = node
        break


usa_constante = False


if render_node is not None:

    for node in ast.walk(
        render_node
    ):

        if (
            isinstance(
                node,
                ast.Name,
            )
            and
            node.id
            ==
            "CIERRE_INSTITUCIONAL_V018902"
        ):

            usa_constante = True
            break


print()
print(
    "✅ render_analisis_profesional_v01877() "
    "usa CIERRE_INSTITUCIONAL_V018902"
    if usa_constante
    else
    "❌ No se confirmó el uso del cierre institucional "
    "en render_analisis_profesional_v01877()"
)


# ==============================================================================================
# 6. INTEGRIDAD FINAL
# ==============================================================================================

sha_after = sha256_file(
    portal
)


intacta = (
    sha_before
    ==
    sha_after
)


print()
print("-" * 110)
print("RESULTADO")
print("-" * 110)


print(
    "✅ R1.4-B permanece byte por byte intacta"
    if intacta
    else
    "❌ R1.4-B cambió"
)


if (
    coincide_exacto
    and
    usa_constante
    and
    intacta
):

    print()
    print(
        "✅ CIERRE INSTITUCIONAL VALIDADO"
    )

    print(
        "✅ El ❌ anterior fue un falso negativo "
        "de la búsqueda textual del laboratorio."
    )

    print()
    print(
        "✅ R1.4-B PUEDE CONSIDERARSE "
        "ESTRUCTURALMENTE SUPERADA"
    )

else:

    print()
    print(
        "⚠️ R1.4-B todavía requiere revisión "
        "antes del despliegue visual."
    )


print()
print("=" * 110)
print("FIN VERIFICACIÓN CIERRE INSTITUCIONAL")
print("=" * 110)
