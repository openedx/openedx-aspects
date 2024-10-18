Individual Learner Dashboard Reports
####################################

The Individual Learner Dashboard Reports focus on relevant information about each learner’s performance and information, including course enrollment and activity logs, to give a general overview. Suppose the name, username, and email address columns are empty in the learner summary. In that case, your site operator has omitted limited personally identifiable information from being displayed on your Open edX instance. The Individual Learner Dashboard can only be filtered by one or more individual learners if the Operator has chosen to display limited personally identifiable information on your instance. 

One particular benefit of this dashboard is that it gives the course delivery team a general view of the course performance while zooming in and out on each learner, combining the `Course Dashboard <https://docs.openedx.org/projects/openedx-aspects/en/latest/reference/course_overview_dashboard.html>`_ and `At Risk Learner Dashboard <https://docs.openedx.org/projects/openedx-aspects/en/latest/reference/learner_groups_dashboard.html>`_ information. As with the rest of the Aspects dashboards, this dashboard’s charts apply cross-filters to charts whose data sets contain the same name.

.. image:: /_static/individual_learner_dashboard.png

This dashboard's data information is divided into two sections: the Learner Summary and the pages, problems, videos, and help reports.

1. Learner Summary:
===================

This section has a table that provides a detailed overview of individual learner performance within a specific course or course run. It offers valuable insights into student engagement, progress, and overall performance. The table columns are:

- **Username:** A unique identifier assigned to each learner.
- **Name:** The learner's full name or preferred name.
- **Email:** The learner's email address.
- **Course Name:** The title or name of the course.
- **Course Run:** A specific instance or version of the course.
- **Enrollment Date:** The date when the learner initially enrolled in the course.
- **Last Visited:** The date of the learner's last activity within the course.
- **Passed/Failed:** Indicates whether the learner has completed the course or not.
- **Enrollment Track:** Specifies the type of enrollment (e.g., honor, verified, audit).
- **Enrollment Status:** Indicates the current enrollment status of the learner (e.g., registered, active, inactive).
- **Grade Range:** The possible range of grades for the course.
- **Course Grade %:** The learner's actual percentage grade achieved in the course.

.. image:: /_static/learner_summary.png

2. Pages, Problems, Videos & Help:
==================================

These metrics give you information about users’ engagement with the course and its specific content, particularly Pages, Problems, and Videos. To see these metrics, just choose the tab you want to see. 

Pages:
------
This tab shows page engagement metrics by section and subsection, cumulative interactions, and engagement over time. 

.. image:: /_static/individual_pages.png

Problems:
---------
These metrics show the learners’ engagement with the problems and assessments created in the course. The attempts and results information help understand each problem’s performance.

.. image:: /_static/individual_problems.png

Coursewide averages showing the average percent correct and average number of attempts across the course are displayed to the left of selected learner metrics to help compare the selected learner to the rest of those engaging with the course. 

.. image:: /_static/individual_problems_2.png

Videos:
-------
These metrics show how the learners have engaged with your course video content, including how many partial and completed videos they have seen. Here, you will find tables like:

- Video Engagement per Section/Subsection
- Video Engagement per Section
- Video Engagement per Subsection
- Partial and Full Video Views
- Partial and Full Video Views
- Number of Views across Video Duration

.. image:: /_static/individual_videos.png

.. image:: /_static/individual_videos_2.png

Help:
-----
The Help tab at the bottom of the course dashboard is a valuable resource for users seeking assistance or additional information. It typically provides quick access to relevant documentation and support materials related to the course and the platform.

.. image:: /_static/help_tab.png

.. note:: Remember that you can change the filters of these reports by accessing Superset through the link above the reports. For more information, visit the `How to Apply Filters page <https://docs.openedx.org/projects/openedx-aspects/en/latest/course_team/how-tos/apply_filters.html>`_.

.. seealso:: If you want to refresh the information displayed in the report, click the **More Options** button (three vertical dots) in the upper right corner of each metric and select the Force Refresh option. For more information, visit the `How to Update the Data <https://docs.openedx.org/projects/openedx-aspects/en/latest/course_team/how-tos/update_data.html>`_.