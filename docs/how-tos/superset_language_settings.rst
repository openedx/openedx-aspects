.. _superset-language-settings:

Changing Superset language settings
###################################

By changing the following Tutor configuration variables you can change the default
language:

.. code-block:: yaml

    SUPERSET_DEFAULT_LOCALE: en
    SUPERSET_SUPPORTED_LANGUAGES:
      en:
        flag: us
        name: English
      es:
        flag: es
        name: Spanish
      it:
        flag: it
        name: Italian
      fr:
        flag: fr
        name: French
      zh:
        flag: cn
        name: Chinese
      ja:
        flag: jp
        name: Japanese
      de:
        flag: de
        name: German
      pt:
        flag: pt
        name: Portuguese
      pt_BR:
        flag: br
        name: Brazilian Portuguese
      ru:
        flag: ru
        name: Russian
      ko:
        flag: kr
        name: Korean
      sk:
        flag: sk
        name: Slovak
      sl:
        flag: si
        name: Slovenian
      nl:
        flag: nl
        name: Dutch

Where the first key is the abbreviation of the language to use, "flag" is which flag
icon is displayed in the user interface for choosing the language, and "name" is the
displayed name for that language. The mapping above shows all of the current languages
supported by Superset, but please note that different languages have different levels
of completion and support at this time.
