# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = _("Recetario")
MENSAJE_BIENVENIDA = _("Bienvenido a {}. Puedes preguntar por ejemplo, por la receta de {}... Ahora, ¿cómo puedo ayudarte?")
BIENVENIDA_REPREGUNTA = _("Para pedir más instrucciones, puedes pedirme ayuda.")
TITULO_DE_TARJETA = _("{}. Receta de {}.")
MENSAJE_DE_AYUDA = _("Puedes preguntar por ejemplo, ¿cuál es la receta de {}?, o puedes salir... ¿cómo puedo ayudarte?")
REPEGUNTA_DE_AYUDA = _("Puedes preguntar por ejemplo, ¿cuál es la receta de {}?, o puedes salir... ¿cómo puedo ayudarte?")
MENSAJE_FINAL = _("El {} no puede ayudarte con eso.")
MENSAJE_DE_PARADA = _("¡Adiós! ¡Que te salga bien la receta!")
MENSAJE_DE_REPETICION = _("Intenta diciendo... repetir.")
RECETA_NO_ENCONTRADA_MENSAJE = _("Lo siento, ahora mismo no conozco ")
RECETA_NO_ENCONTRADA_CON_COMIDA = _("la receta de {}. ")
RECETA_NO_ENCONTRADA_SIN_COMIDA = _("esa receta. ")
RECETA_NO_ENCONTRADA_REPREGUNTA = _("¿Con qué otra cosa podría ayudarte?")

RECETAS = {
    'croquetas': 'Haces una bechamel, echas el relleno, y las rebozas.',
    'paella': 'Pide consejo a tu amigo valenciano, para que no acabes haciendo un arroz con cosas.',
    'cocido': 'Echa a la olla sin miedo garbanzos, verdura y carne de segunda... y que el calor y el tiempo haga la magia.',
    'macarrones': 'Agua a hervir, los tiras, y a esperar lo que ponga en el paquete.',
    'pizza': 'A primeros de mes, llama a tu pizzero de confianza; a final de mes, calienta el horno, y háztela tú.',
    'lentejas': 'Descongela el tupper que te ha hecho tu mama, y caliéntalas en el microondas.',
    'pulpo': 'Lo hagas como lo hagas, no te olvides de darle una buena paliza.'
}
