"""
Site éducatif : Python, ou comment laisser l'ordinateur faire le travail ennuyeux.
Pour le lancer sur ton ordinateur :  streamlit run streamlit_app.py
"""
import io

import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(page_title="Python pour débutants", page_icon="🐍", layout="centered")


# ---------------------------------------------------------------------------
# Petites fonctions utiles
# ---------------------------------------------------------------------------
def image_par_defaut(texte="Image par défaut"):
    """Crée une image grise avec un texte. On l'utilise quand une image est introuvable."""
    image = Image.new("RGB", (480, 240), color=(210, 214, 220))
    dessin = ImageDraw.Draw(image)
    dessin.text((150, 110), texte, fill=(60, 60, 60))
    return image


def charger_image(contenu):
    """Essaie d'ouvrir une image. Si ça rate, renvoie l'image par défaut au lieu de planter."""
    try:
        image = Image.open(io.BytesIO(contenu))
        image.load()
        return image, None
    except Exception as erreur:  # fichier vide, abîmé, pas une image...
        return image_par_defaut(), erreur


DOSSIERS = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".pdf": "Documents", ".docx": "Documents", ".txt": "Documents",
    ".mp4": "Vidéos", ".mov": "Vidéos",
    ".mp3": "Musique", ".wav": "Musique",
}


def trier_fichiers(noms):
    """Range des noms de fichiers dans des dossiers selon leur extension."""
    resultat = {}
    for nom in noms:
        nom = nom.strip()
        if not nom:
            continue
        extension = "." + nom.rsplit(".", 1)[-1].lower() if "." in nom else ""
        dossier = DOSSIERS.get(extension, "Autres")
        resultat.setdefault(dossier, []).append(nom)
    return resultat


# ---------------------------------------------------------------------------
# Page 1 : Accueil
# ---------------------------------------------------------------------------
def accueil():
    st.title("🐍 Python pour débutants")
    st.subheader("Laisser l'ordinateur faire le travail ennuyeux")

    st.write(
        "Salut ! Ce site est fait pour les élèves qui n'ont jamais programmé. "
        "Pas besoin de tout comprendre d'un coup : chaque page explique une idée "
        "avec des mots simples, un exemple et un petit exercice."
    )
    st.write(
        "Python est un langage de programmation facile à lire. On l'utilise pour "
        "créer des sites, analyser des données, et surtout pour **faire faire aux "
        "ordinateurs les tâches répétitives** à notre place."
    )

    st.markdown("### Les pages du site")
    st.page_link(page_bases, label="Les bases de Python", icon="📘")
    st.page_link(page_erreurs, label="Gérer les erreurs", icon="🛟")
    st.page_link(page_auto, label="L'automatisation des tâches", icon="⚙️")
    st.page_link(page_sources, label="Sources", icon="🔗")

    st.info("Conseil : fais les pages dans l'ordre, et essaie les exercices avant de lire les réponses.")


# ---------------------------------------------------------------------------
# Page 2 : Les bases de Python
# ---------------------------------------------------------------------------
def bases():
    st.title("📘 Les bases de Python")
    st.write("**L'idée générale :** un programme, c'est une suite d'instructions. Voici les quatre briques de base.")

    with st.expander("1. Les variables : des boîtes avec un nom", expanded=True):
        st.write("Une variable garde une information pour qu'on puisse la réutiliser.")
        st.code('prenom = "Sara"\nage = 15\nprint("Salut", prenom)', language="python")

    with st.expander("2. Les conditions : prendre une décision"):
        st.write("Avec `if`, le programme fait quelque chose seulement si une condition est vraie.")
        st.code(
            'note = 14\n'
            'if note >= 10:\n'
            '    print("Réussi !")\n'
            'else:\n'
            '    print("À retravailler")',
            language="python",
        )

    with st.expander("3. Les boucles : répéter sans se fatiguer"):
        st.write("Une boucle `for` répète des instructions pour chaque élément d'une liste.")
        st.code(
            'fruits = ["pomme", "banane", "kiwi"]\n'
            'for fruit in fruits:\n'
            '    print("J\'aime la", fruit)',
            language="python",
        )

    with st.expander("4. Les fonctions : un mini-programme réutilisable"):
        st.write("Une fonction regroupe des instructions sous un nom. On l'écrit une fois, on l'utilise partout.")
        st.code(
            'def doubler(nombre):\n'
            '    return nombre * 2\n\n'
            'print(doubler(7))  # affiche 14',
            language="python",
        )

    st.markdown("### Essaie toi-même")
    nombre = st.number_input("Choisis un nombre pour la fonction doubler()", value=7, step=1)
    st.write(f"doubler({nombre}) donne **{nombre * 2}**")

    st.markdown("### Petit exercice")
    reponse = st.radio(
        "Que va afficher ce code ?  `x = 3`  puis  `print(x + 4)`",
        ["Je choisis...", "x + 4", "7", "34"],
    )
    if reponse == "7":
        st.success("Bravo ! x vaut 3, donc 3 + 4 = 7.")
    elif reponse != "Je choisis...":
        st.error("Pas tout à fait. Python remplace x par 3 puis calcule 3 + 4.")


# ---------------------------------------------------------------------------
# Page 3 : Gérer les erreurs
# ---------------------------------------------------------------------------
def erreurs():
    st.title("🛟 Gérer les erreurs")
    st.write(
        "**L'idée générale :** une erreur ne doit pas faire planter tout le programme. "
        "On peut la prévoir et décider quoi faire à la place."
    )

    st.markdown("### Sans protection, tout s'arrête")
    st.code(
        'image = ouvrir_image("photo_introuvable.png")  # erreur ici\n'
        'print("Cette ligne ne sera jamais atteinte")',
        language="python",
    )

    st.markdown("### Avec try et except, le programme continue")
    st.code(
        'try:\n'
        '    image = ouvrir_image("photo.png")\n'
        'except Exception:\n'
        '    image = image_par_defaut()  # plan B\n'
        'print("Le programme continue !")',
        language="python",
    )
    st.write(
        "`try` veut dire « essaie ». `except` veut dire « si ça rate, fais ça à la place »."
    )

    st.markdown("### Démonstration : l'image par défaut")
    st.write(
        "Envoie une vraie image, puis essaie avec un fichier qui n'est pas une image "
        "(un PDF, un texte...). Le site ne plante pas : il affiche une image par défaut."
    )
    fichier = st.file_uploader("Choisis un fichier", key="demo_image")
    if fichier is not None:
        image, erreur = charger_image(fichier.getvalue())
        if erreur is None:
            st.image(image, caption="Image chargée correctement")
        else:
            st.image(image, caption="Image par défaut")
            st.warning(
                "Ce fichier n'est pas une image lisible. Le programme a utilisé une image "
                "par défaut au lieu de faire planter toute l'application."
            )

    st.markdown("### Petit exercice")
    reponse = st.radio(
        "Quel mot-clé sert à dire « si ça rate, fais ça à la place » ?",
        ["Je choisis...", "try", "except", "print"],
        key="exo_erreurs",
    )
    if reponse == "except":
        st.success("Exact ! `except` attrape l'erreur et lance le plan B.")
    elif reponse != "Je choisis...":
        st.error("Pas tout à fait. `try` essaie, mais c'est `except` qui gère l'erreur.")


# ---------------------------------------------------------------------------
# Page 4 : Automatisation
# ---------------------------------------------------------------------------
def automatisation():
    st.title("⚙️ L'automatisation des tâches")
    st.write(
        "**L'idée générale :** de simples scripts Python peuvent faire en quelques "
        "secondes des tâches qui nous prendraient des heures à la main. "
        "C'est comme ça que Python libère du temps humain."
    )

    st.markdown("### Exemple 1 : trier des fichiers")
    st.write("Voici le principe : un dictionnaire associe chaque extension à un dossier.")
    st.code(
        'dossiers = {".jpg": "Images", ".pdf": "Documents", ".mp4": "Vidéos"}\n\n'
        'for nom in noms_de_fichiers:\n'
        '    extension = "." + nom.split(".")[-1].lower()\n'
        '    dossier = dossiers.get(extension, "Autres")\n'
        '    print(nom, "->", dossier)',
        language="python",
    )

    st.write("Essaie : écris des noms de fichiers (un par ligne) et regarde comment ils sont rangés.")
    exemple = "vacances.jpg\ncours_maths.pdf\nfilm.mp4\nnotes.txt\nmystere.xyz"
    texte = st.text_area("Noms de fichiers", value=exemple, height=140)
    resultat = trier_fichiers(texte.splitlines())
    if resultat:
        for dossier, noms in sorted(resultat.items()):
            st.markdown(f"**📁 {dossier}**")
            for nom in noms:
                st.write(f"- {nom}")
    else:
        st.info("Écris au moins un nom de fichier.")

    st.markdown("### Exemple 2 : renommer en lot")
    st.write("Imagine 100 photos à renommer. Une boucle le fait pour toi.")
    st.code(
        'for numero in range(1, 4):\n'
        '    print(f"vacances_{numero:03d}.jpg")',
        language="python",
    )
    prefixe = st.text_input("Début du nom", value="vacances")
    quantite = st.slider("Nombre de fichiers", 1, 20, 5)
    st.write("Résultat :")
    st.code("\n".join(f"{prefixe}_{n:03d}.jpg" for n in range(1, quantite + 1)))

    st.markdown("### Petit exercice")
    reponse = st.radio(
        "Dans le tri de fichiers, que se passe-t-il pour un fichier d'extension inconnue ?",
        ["Je choisis...", "Le programme plante", "Il va dans le dossier « Autres »", "Il est supprimé"],
        key="exo_auto",
    )
    if reponse == "Il va dans le dossier « Autres »":
        st.success("Oui ! Grâce à `dossiers.get(extension, \"Autres\")`, il y a toujours un plan B.")
    elif reponse != "Je choisis...":
        st.error("Regarde la dernière ligne du code : `get` renvoie « Autres » quand l'extension n'est pas connue.")


# ---------------------------------------------------------------------------
# Page 5 : Sources
# ---------------------------------------------------------------------------
def sources():
    st.title("🔗 Sources")
    st.write("Voici les sites que j'ai utilisés pour apprendre et vérifier mes exemples.")
    st.link_button("Documentation officielle de Python (en français)", "https://docs.python.org/fr/3/")
    st.link_button("Documentation de Streamlit", "https://docs.streamlit.io")
    st.link_button("Streamlit Community Cloud (hébergement gratuit)", "https://docs.streamlit.io/deploy/streamlit-community-cloud")
    st.caption("Ajoute ici les autres sources que tu as vraiment utilisées (cours, livres, vidéos).")


# ---------------------------------------------------------------------------
# Navigation (le menu du site)
# ---------------------------------------------------------------------------
page_accueil = st.Page(accueil, title="Accueil", icon="🏠", url_path="accueil", default=True)
page_bases = st.Page(bases, title="Les bases de Python", icon="📘", url_path="bases")
page_erreurs = st.Page(erreurs, title="Gérer les erreurs", icon="🛟", url_path="erreurs")
page_auto = st.Page(automatisation, title="Automatisation", icon="⚙️", url_path="automatisation")
page_sources = st.Page(sources, title="Sources", icon="🔗", url_path="sources")

navigation = st.navigation([page_accueil, page_bases, page_erreurs, page_auto, page_sources])
navigation.run()