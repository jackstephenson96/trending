# -*- coding: utf-8 -*-

# Helpful links:
# https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/
#zip -r ../trending.zip .

import logging
import random
import gettext

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type

from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

from alexa import data, util

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# some limits
LIMIT = 50


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        # logger.info(_("This is an untranslated message"))

        speech = _(data.WELCOME)
        speech += " " + _(data.HELP)
        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(_(
            data.GENERIC_REPROMPT))
        return handler_input.response_builder.response


class AboutIntentHandler(AbstractRequestHandler):
    """Handler for about intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AboutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AboutIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.ABOUT))
        return handler_input.response_builder.response

class AuthorIntentHandler(AbstractRequestHandler):
    """Handler for author intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AuthorIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In  AuthorIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.AUTHOR))
        return handler_input.response_builder.response


class OneBasicIntentHandler(AbstractRequestHandler):
    """Handler for basic 1 event US request."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("OneBasicIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In OneBasicIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        trend = util.gettrends()[0]
        logger.info(str(trend['trend']))
        session_attr["trend"] = trend['trend']
        speech = ("The top google search in the U.S. is {}."
            ).format(trend['trend'])
    
        handler_input.response_builder.speak(speech).ask(speech)

        # handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response
## TODO: match can_handle return string syntax, fit to above


class OneAdvancedIntentHandler(AbstractRequestHandler):
    """Handler for a single location request."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("OneAdvancedIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In OneAdvancedIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots

        if slots["location"].value:
            location = slots['location'].value
            if location.lower() in data.AMERICA:
                geo = 'US'
            else:
                geo = util.get_country_code(location)
                if not geo:
                    speech = ("Sorry, invalid country, please try again with a country that uses google ")

            trend = util.gettrends(geo=geo)
            speech = ("The top google search in {} is {}"
            ).format(location, trend[0]['trend'])
        else:
            speech = ("Sorry, invalid country, please try again with a country that uses google ")
            #not used yet
            reprompt = "Ask for top google search in a location where google allowed"

        # handler_input.response_builder.speak(speech)
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class MultipleBasicIntentHandler(AbstractRequestHandler):
    """Handler for multiple basic USA requests."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("MultipleBasicIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In MultipleBasicIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots

        if slots['number'].value:
            number = int(slots['number'].value)
        else:
            number = 3

        speech = ("The top {} google searches in the US are"
        ).format(str(number)) 
        trend = util.gettrends(geo=util.get_country_code(location), num=number)

        if number == 1:
            speech = ("The top google search in the U.S. is {}").format(trend[0]['trend'])
        elif number > 1 and number < LIMIT:
            for t in trend[:-1]:
                speech = speech + t['trend'] + ", "
            speech = speech + "and " + trend[-1]['trend']

        else:
            speech = ("invalid number, please ask for a number greater than zero and less than {}"
            ).format(str(LIMIT))

        # handler_input.response_builder.speak(speech)
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

class MultipleAdvancedIntentHandler(AbstractRequestHandler):
    """Handler for number intent w location."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("MultipleAdvancedIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In MultipleAdvancedIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        slots = handler_input.request_envelope.request.intent.slots

        if slots["location"].value:
            location = slots['location'].value
            if location.lower() in data.AMERICA:
                geo = 'US'
            else:
                geo = util.get_country_code(location)
                if not geo:
                    speech = ("Sorry, invalid country, please try again with a country that uses google ")

            if not slots['number'].value:
                number = 3
            else:
                number = int(slots['number'].value)

            speech = ("The top {} google searches in {} are "
            ).format(str(number), location) 
            trend = util.gettrends(geo=geo, num=number)

            if number == 1:
                speech = ("The top google search in {} is {}").format(location, trend[0]['trend'])
            elif number > 1 and number < LIMIT:
                for t in trend[:-1]:
                    speech = speech + t['trend'] + ", "
                speech = speech + "and " + trend[-1]['trend']

            else:
                speech = ("invalid number, please ask for a number greater than zero and less than {}"
                ).format(str(LIMIT))
        else:
            speech = ("Sorry, invalid country, please try again with a country that uses google ")
        # handler_input.response_builder.speak(speech)
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.HELP)).ask(_(data.HELP))
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.STOP)).set_should_end_session(True)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent or Yes/No without
    restaurant info intent.

     2018-May-01: AMAZON.FallackIntent is only currently available in
     en-US locale. This handler will not be triggered except in that
     locale, so it can be safely deployed for any locale."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.FallbackIntent")(handler_input) or
                ("restaurant" not in session_attr and (
                    is_intent_name("AMAZON.YesIntent")(handler_input) or
                    is_intent_name("AMAZON.NoIntent")(handler_input))
                 ))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.FALLBACK).format(data.SKILL_NAME)).ask(_(
            data.FALLBACK).format(data.SKILL_NAME))

        return handler_input.response_builder.response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.

    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        logger.info("Original request was {}".format(
            handler_input.request_envelope.request))

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'base', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes[
            "_"] = i18n.gettext


# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AboutIntentHandler())
sb.add_request_handler(AuthorIntentHandler())
sb.add_request_handler(MultipleAdvancedIntentHandler())
sb.add_request_handler(MultipleBasicIntentHandler())
sb.add_request_handler(OneAdvancedIntentHandler())
sb.add_request_handler(OneBasicIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add locale interceptor to the skill.
sb.add_global_request_interceptor(LocalizationInterceptor())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
