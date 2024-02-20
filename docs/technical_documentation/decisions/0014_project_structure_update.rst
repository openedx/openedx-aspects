14. Project Structure Updates
#############################

Status
******

Draft -> Accepted

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

Consequences
************

* `openedx-event-sink-clickhouse` and `platform_plugin_superset` will be consolidated into `openedx-aspects`_ and re-licensed to Apache 2. `openedx-event-sink-clickhouse` will be archived under the `openedx-unsupported`_ Github organization.

Rejected Alternatives
*********************

**Separate repositories for Aspects specific platform plugins**

**Including these plugins in `tutor-contrib-aspects`_ **

This project is already quite complicated, and conflating the concerns of code and configuration will result in an more complicated and confusing codebase with different testing, documentation, and deployment needs.

Supersedes `ADR 6 Areas of responsibility`_.
Supersedes `ADR 8 Project Structure`_.

.. _ADR 6 Areas of responsibility: 0006_areas_of_responsibility.rst
.. _ADR 8 Project Structure: 0008_project_structure.rst
.. _event-routing-backends: https://github.com/openedx/event-routing-backends
.. _openedx-aspects: https://github.com/openedx/openedx-aspects
.. _openedx-event-sink-clickhouse: https://github.com/openedx/openedx-event-sink-clickhouse
.. _openedx-unsupported: https://github.com/openedx-unsupported
.. _tutor-contrib-aspects: https://github.com/openedx/tutor-contrib-aspects
.. _platform_plugin_superset: https://github.com/eduNEXT/platform-plugin-superset/
