10. Localization of user-facing content
#######################################

Status
******

Accepted

Context
*******

.. note:: Terminology

    * A "locale" is a specific language and region.
      
      E.g., Spanish is spoken in several locales: ``es-ar`` (Argentina),  ``es-mx`` (Mexico), ``es-es`` (Spain), etc.

    * Internationalization (i18n) is the process of developing products that can be adapted to different languages and
      cultures.

    * Localization (l10n) is the process of adapting a product or content for a specific locale.


Open edX is used worldwide. So for Aspects to be a fully-supported part of the Open edX ecosystem, it must at least
support translations for user-facing content, page layout for left-to-right and right-to-left languages. It may also
support localized representations of dates and calendars.

Superset provides Aspect's user interface, and it supports a subset of locales for translating/displaying the menus and
pages that the application serves. However, Superset does not translate its application or asset data, i.e. the
dashboards and charts shown to users. Superset also has some open issues related to localization (e.g.  `issue#25258`_).

Aspects must maintain and display translated versions of its supported Superset assets.

Decision
********

* Aspects build process will support extracting user-facing content from Superset assets for translation, the production
  of translated dashboards and charts, and synchronization of the latest translations to the project.
* Normal Aspects users (non-superusers) will only see the dashboards and charts that match their preferred language as
  selected in the LMS.
* Open edX superusers using Aspects will see all translations of all Superset assets, so that they are able 
* All Superset users may choose their preferred locale for Superset menus and pages from the "Languages" menu after
  logging in; this will not be chosen automatically from their Open edX preferred language.
* Aspects will contribute to Superset's i18n and l10n efforts where possible.

Consequences
************

#. Aspects will configure Superset to run with a set of locales that best matches those locales Open edX supports.
#. Aspects will create translated copies of all user-facing Superset assets (dashboards and charts).
#. Access to these translated dashboards will be gated by role-based access controls (RBAC) using locale-specific roles.
   Users are added to the locale-specific role that best matches their preferred language in Open edX, and so are
   granted access to the appropriate translated dashboards and charts.
#. Like other Open edX projects, translations for the Aspects project will be maintained in Transifex.
#. Translations will be automatically synchronized using the Transifex Github App as per `OEP-58`_.

Rejected Alternatives
*********************

**Translate assets on the fly with javascript**

Another way to implement translations in the browser is using javascript and a mapping between English words/phrases and
the translated words/phrases (e.g. `simple-translator`_). However, this approach cannot discern the context around how
words/phrases are used, and so providing accurate translations for complex content can be difficult or impossible. This
approach would also slow page load times and would provide a sub-standard user experience.

References
**********


.. _OEP-58: https://docs.openedx.org/projects/openedx-proposals/en/latest/architectural-decisions/oep-0058-arch-translations-management.html
.. _issue#25258: https://github.com/apache/superset/issues/25258
.. _simple-translator: https://github.com/andreasremdt/simple-translator
