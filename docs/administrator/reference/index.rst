Reference 
#########

Advanced Configuration Options in ASPECTS
*****************************************

By modifying the configuration files, you can alter the ASPECTs platform differently.

You can configure whether to sync personal information such as user profiles and IDs.

Sentry can be configured in all three services (LMS, Superset, and Ralph)

Extra requirements can be added to the Superset.

Extra Jinja filters can be added, allowing permission checks for other roles and filtering information based on information from other services.
You can change the default language, although the current ASPECTS version only focuses on English language support.

Visit the official superset documentation to learn more: `<https://superset.apache.org/docs/installation/configuring-superset>`_.

Branding
********
Branding is not currently configurable for Aspects. This means that the superset logo will be visible on all the consoles.  However, there is ongoing work to make it configurable to some extent.  `<https://github.com/openedx/tutor-contrib-aspects/issues/222>`_.

Configure Aspects for Production
********************************
To have more information about the different possibilities that you have with Aspects, please visit the :ref:`Production Configuration Documents <production_configuration>`.
