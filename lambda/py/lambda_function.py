# -*- coding: utf-8 -*-

# HowTo skill: A simple skill that shows how to use python's
# gettext module for localization, for multiple locales.

import logging
import gettext

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from alexa import data, util


sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Clase que implementa la acción al realizar al abrir la skill
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        
        #Este código es para hacer una aplicación multi-idioma, nosotros trabajaremos sólo en español
        #locale = handler_input.request_envelope.request.locale
        #item = util.get_random_item(locale)
        food = util.get_random_item()
        
        #Devuelve como mensaje el texto guardado en la variable MENSAJE_BIENVENIDA del fichero alexa/data.py
        #Consulta también la lista de "comida" para devolver uno de ellas.
        speech = _(data.MENSAJE_BIENVENIDA).format(
            _(data.SKILL_NAME), food)
        reprompt = _(data.BIENVENIDA_REPREGUNTA)

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

#Clase genérica de ejemplo, hay que crear una de estas por cada intención. En este caso utilizamos la intención "EJEMPLO" 
# con la entidad (o como lo llaman en Amazon, slot) "ENTIDAD_EJEMPLO"
# OJO! Además de programa la clase, luego habría que añadir la función al SkillBuilder, ejemplo en la línea 287 del script.
'''
class EJEMPLOIntentHandler(AbstractRequestHandler):
    """Handler for EJEMPLO Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("EJEMPLOIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In EJEMPLOIntentHandler")
        
        #Busca en el mensaje recibido si lleva la entidad ENTIDAD_EJEMPLO, si no la lleva, deja la variable "entidad_recibida" vacía
        try:
            entidad_recibida = handler_input.request_envelope.request.intent.slots[
                "ENTIDAD_EJEMPLO"].value.lower()
        except AttributeError:
            logger.info("No se detectó ninguna entidad en la petición.")
            entidad_recibida = None

        # Aquí pondríamos el código que viéramos pertinente para modelar la respuesta a dar a la intención
        
        #Guardamos en la variable speech la respuesta que tendrá Alexa
        speech = "Mensaje de salida en respuesta a la entidad {} informada".format(ENTIDAD_EJEMPLO)
        handler_input.response_builder.speak(speech) 
       
        #Si queremos que además de responder haga una nueva pregunta, podemos añadir la llamada a la función "ask"
        #pasándole como parámetro la variable reprompt
        reprompt = "¿Estás contento con la respuesta?"
        handler_input.response_builder.speak(speech).ask(
                reprompt)

        return handler_input.response_builder.response
'''

#Siguiendo el ejemplo anterior, he creado una clase para implementar la intención "RecetaIntent"
#La intención "RecetaIntent" puede llevar una entidad llamada "Comida"
#Se busca la comida pedida por el usuario en la lista de recetas que tenemos implementadas en el fichero alexa/data.py
#Y si se encuentra, se la contamos al usuario
class RecetaIntentHandler(AbstractRequestHandler):
    """Handler for Receta Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("RecetaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RecetaIntentHandler")
        
        #Código para la internazionalización, nosotros no la usamos
        #locale = handler_input.request_envelope.request.locale
        #_ = handler_input.attributes_manager.request_attributes["_"]
        
        #Busca en el mensaje recibido si lleva una entidad, si no la tuviera, la variable nombre_comida queda vacía
        try:
            nombre_comida = handler_input.request_envelope.request.intent.slots[
                "Comida"].value.lower()
        except AttributeError:
            logger.info("No se detectó ninguna entidad en la petición.")
            nombre_comida = None
        
        #Creamos un título de la tarjeta a partir del nombre de la Skill y de la comida informada
        card_title = _(data.TITULO_DE_TARJETA).format(
            _(data.SKILL_NAME), nombre_comida)
        
        #Cargamos el diccionario de recetas almacenado en el fichero alexa/data.py
        mis_recetas = util.load_locale_specific_recipe()

        # Si encontramos entre las recetas guardadas la comida solicitada, la buscamos en mis_recetas, y se la comunicamos al usuario
        if nombre_comida in mis_recetas:
            receta = mis_recetas[nombre_comida]
            handler_input.response_builder.speak(receta).set_card(
                SimpleCard(card_title, receta))
        else:
            #Si la comida solicitada no está entre nuestras recetas, preguntamos de nuevo.
            speech = _(data.RECETA_NO_ENCONTRADA_MENSAJE)
            reprompt = _(data.RECETA_NO_ENCONTRADA_REPREGUNTA)
            #Si se detectó una comida solicitada, se personaliza la respuesta con ella, si no, no se indica
            if nombre_comida:
                speech += _(data.RECETA_NO_ENCONTRADA_CON_COMIDA).format(
                    nombre_comida)
            else:
                speech += _(data.RECETA_NO_ENCONTRADA_SIN_COMIDA)
            speech += reprompt
            
            #Se devuelve como resultado de la función para que conteste con el speech y el reprompt.
            handler_input.response_builder.speak(speech).ask(
                reprompt)

        return handler_input.response_builder.response

#Clase que gestiona la intención predefinidad de pedir ayuda
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        #locale = handler_input.request_envelope.request.locale
        nombre_comida = util.get_random_item()
        
        #Devuelve como mensaje lo guardado en la variable MENSAJE_DE_AYUDA del fichero alexa/data.py
        speech = _(data.MENSAJE_DE_AYUDA).format(nombre_comida)
        
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

#Clase que gestiona la intención predefinida de repetición
class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        session_attributes = handler_input.attributes_manager.session_attributes
        handler_input.response_builder.speak(
            session_attributes['speech']).ask(
            session_attributes['reprompt'])
        return handler_input.response_builder.response

#Clase que gestiona la intención predefinida de cancelar o parar
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handler for Cancel and Stop Intents."""
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        
        #Devuelve como mensaje lo guardado en la variable MENSAJE_DE_PARADA del fichero alexa/data.py
        speech = _(data.MENSAJE_DE_PARADA).format(_(data.SKILL_NAME))
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response

#Clase que gestiona la intención predefinida en el caso de que no encuentre ninguna otra
#No funciona en castellano, sólo está implementada para el lenuaje en-US
class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        #locale = handler_input.request_envelope.request.locale
        item = util.get_random_item()
        
        help_message = _(data.MENSAJE_DE_AYUDA).format(item)
        help_reprompt = _(data.REPEGUNTA_DE_AYUDA).format(item)
        speech = _(data.MENSAJE_FINAL).format(
            _(data.SKILL_NAME)) + help_message
        reprompt = _(data.MENSAJE_FINAL).format(
            _(data.SKILL_NAME)) + help_reprompt

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

#Clase que gestiona el final de sesión y la guarda en logs
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for SessionEndedRequest."""
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

#Clase que gestiona la captura de excepciones
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Global exception handler."""
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        logger.error(exception, exc_info=True)
        logger.info("Original request was {}".format(
            handler_input.request_envelope.request))

        speech = _("Sorry, I can't understand the command. Please say again!!")
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

#Clase que gestiona la caché para repeticiones
class CacheSpeechForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the output speech and reprompt to session attributes,
    for repeat intent.
    """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["speech"] = response.output_speech
        session_attr["reprompt"] = response.reprompt

#Clase que detecta la localización del usuario
class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'data', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes[
            "_"] = i18n.gettext

#
sb.add_request_handler(LaunchRequestHandler())
#sb.add_request_handler(EJEMPLOIntentHandler())
sb.add_request_handler(RecetaIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_response_interceptor(CacheSpeechForRepeatInterceptor())

lambda_handler = sb.lambda_handler()
