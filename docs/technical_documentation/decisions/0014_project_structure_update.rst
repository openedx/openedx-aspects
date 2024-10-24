14. Project Structure Updates
#############################

Status
******

Superseded by `ADR 15 Repository Consolidation`_.

Context
*******

This ADR builds upon, and in some cases, supersedes `ADR 8 Project Structure`_.

The Aspects requirements for version 1 include adding a new LMS plugin that could potentially live in another repository. We have many repositories to maintain currently, including one LMS plugin that is unlikely to be used for anything outside of Aspects.

This ADR offers guiding principles to address these issues:

* Adding a new repository to the project will increase the maintenance burden and complexity of the overall project.
* We already have an Aspects-specific LMS plugin project.
* The openedx-aspects repository has been a shell, holding only documentation and project management infrastructure.
* There are license conflicts between repositories.

Decisions
*********

**Aspects repo**

This repo (`openedx-aspects`_) remains the primary Aspects repository where the project decisions and documentation are stored. However, we will also move all Aspects-specific LMS plugin functionality into this repository, including the code currently stored in `openedx-event-sink-clickhouse`_ and code being contributed from EduNEXT to support Superset embedding from `platform_plugin_superset`_ which we will take over and continue to build upon.

This repo should also be used to store any common code or configuration between Tutor and non-Tutor Aspects deployments.

**Re-licensing**

Both `openedx-event-sink-clickhouse` and `platform_plugin_superset` are licensed under the AGPL3. Pending approval from Axim legal and EduNEXT, those repositories will be licensed to Apache 2 as part of being moved into this project. This work was already underway to allow for greater community extensibility of Aspects.

**Other LMS plugins**

The `event-routing-backends`_ repository will remain separate as it is useful outside of Aspects.

**Proposed project structure**

The thought is to reorganize the file structure of the repository to match that created by our Django app cookiecutter. The combined projects would coexist in the same space, utilizing the usual Open edX Django setup of a single apps.py, templates folder, configuration files, etc. as they will be installed together.

**Configuration**

Event sinks and embedded dashboards can be configured individually, allowing each set of features to be enabled or disabled simply by not configuring them. For instance, event sink configuration would like this::

    settings.ASPECTS_EVENT_SINK_MODEL_CONFIG = {
        "auth_user": {
            "module": "django.contrib.auth.models",
            "model": "User",
        },
        "user_profile": {
            "module": "common.djangoapps.student.models",
            "model": "UserProfile",
        },
        "course_overviews": {
            "module": "openedx.core.djangoapps.content.course_overviews.models",
            "model": "CourseOverview",
        },
        "external_id": {
            "module": "openedx.core.djangoapps.external_user_ids.models",
            "model": "ExternalId",
        },
    }

So omitting that setting or leaving it empty would disable all event sinks. Specific configuration for dashboard embeds is a work in progress, but would work similarly::

    settings.ASPECTS_SUPERSET_EMBEDS = {
      // Key is the tab name in the "Reports" section of the Instructor Dashboard
      "Course Dashboard": {
        // This is the link to Superset to embed, including any filters
        "embed_link": "...",
        // This would be an LMS permissions filter or function needed to view the embed
        "permissions": ...,
      },
      "Learner Groups": {
        "embed_link": "...",
        "permissions": ...?,
      },
      ...
    }

Again, omitting the setting or leaving it empty would prevent the entire "Reports" tab from showing up.


Consequences
************

* `openedx-event-sink-clickhouse` and `platform_plugin_superset` will be consolidated into `openedx-aspects`_ and re-licensed to Apache 2. `openedx-event-sink-clickhouse` will be archived under the `openedx-unsupported`_ Github organization.

Rejected Alternatives
*********************

* Separate repositories for Aspects specific platform plugins

* Including these plugins in `tutor-contrib-aspects`_ .
  This project is already quite complicated, and conflating the concerns of code and configuration will result in an more complicated and confusing codebase with different testing, documentation, and deployment needs.

Supersedes `ADR 6 Areas of responsibility`_.
Supersedes `ADR 8 Project Structure`_.

.. _ADR 6 Areas of responsibility: 0006_areas_of_responsibility.html
.. _ADR 8 Project Structure: 0008_project_structure.html
.. _ADR 15 Repository Consolidation: 0015_repository_consolidation.html
.. _event-routing-backends: https://github.com/openedx/event-routing-backends
.. _openedx-aspects: https://github.com/openedx/openedx-aspects
.. _openedx-event-sink-clickhouse: https://github.com/openedx/openedx-event-sink-clickhouse
.. _openedx-unsupported: https://github.com/openedx-unsupported
.. _tutor-contrib-aspects: https://github.com/openedx/tutor-contrib-aspects
.. _platform_plugin_superset: https://github.com/eduNEXT/platform-plugin-superset/
