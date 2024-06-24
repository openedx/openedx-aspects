Welcome to the Open edX Aspects documentation!
==============================================

Aspects is an analytics system for Open edX that brings course delivery teams and site operators actionable data about course and learner performance. It is primarily a Tutor plugin that combines data from the Open edX learning management system and Studio. It uses open-source tools to aggregate and transform learning traces into data visualizations.
Aspects capture learning events and transform them into data visualizations. When a learner enrolls in a course, that event is caught in a database and displayed to the course delivery team as a graph of learner enrollments over time. When a course delivery team member adds a new problem to their course and publishes it, the course data is refreshed in the database to show how learners answer the question.

Aspects are being built to help Open edX users answer questions like How many learners were active in a specified period? How often was this problem answered correctly vs. incorrectly? How much of each video did the users watch, and which sections were re-watched most?

By default, Aspects prioritizes learner privacy and does not allow for the identification of learners in the reports. However, this functionality can be added via a tutor setting if desired.

To learn more about working with Aspects in your instance, please review the following documentation, which has been meticulously crafted to be user-friendly and facilitate its utilization by educators, platform managers, and technical personnel. 
To help you navigate the content, we divided it into the roles a person can have on Aspects. The roles for Aspects are: 

- `Administrator <administrator>`_: This role owns the platform as the site operator, can assign roles and permissions to new users, and can create new reports. In this part of the documentation, you will find the operator dashboard and the permissions information. This user usually has the permissions of a Superuser in the platform. 

- `Course delivery team member <course_team>`_: The course delivery team role applies to all course team members, such as content creators, tutors, and professors, who have been added as course staff. They have access to all the dashboards and reports for the courses for which they have been added as staff. Here, you will find information about the principal dashboards and reports, the filters, and the principal functions you need to know to use the analytics system.

- `Technical Documentation <technical_documentation>`_: While developer is not a specific role that can be assigned to someone in Aspects, this third section contains all the technical documentation that any tech member needs to install Aspects and make it work, including the GitHub repositories and DBT and Clickhouse documentation. 


.. toctree::
   :maxdepth: 2

   Reference <reference/index>
<<<<<<< Updated upstream
=======
   Course Delivery Team User <course_team/index>
   Administrator and Site Operator User <administrator/index>
   Technical Documentation <technical_documentation/index>
>>>>>>> Stashed changes


