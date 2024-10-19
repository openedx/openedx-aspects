Course Comparison Dashboard Reports
###################################

The Course Comparison Dashboard allows you to compare the courses in your instance using high-level data to help you identify trends in how your users interact with the content. It also enables you to understand which courses have more or less success or are more popular to create better strategies for your initiative. You can even compare subsets of courses by using the filters available on the dashboard's filters panel.

.. image:: /_static/comparison_dashboard_1.png

The information about the compared courses will be divided into two tabs: **Course Metrics** and **Run Metrics**. The Course Metrics tab provides that information for those who want to compare aggregate data for all runs of one course against all runs of another course. For those who wish to compare course runs to other course runs, the Runs Metrics tab provides the same types of information as the Course Metrics tab, but at the run level. Let’s learn more about it.

Course Metrics:
===============

The Course Metrics tab contains information about the selected courses, including enrollment counts, high-level problem performance and course grade information, and the video engagement of each course.

Unlike the `Course Dashboards <https://docs.openedx.org/projects/openedx-aspects/en/latest/reference/course_overview_dashboard.html>`_, here you will see a compendium of the information of the courses you are comparing instead of the details of each course. However, even if you don't drill down into the details, you will have access to the most relevant values to assess the performance of one course compared to another, including the count of recently-active and at-risk students in the course, so you know how many of them may be at risk of losing or dropping out of the course.

.. image:: /_static/course_metrics.png

Run Metrics:
============
This tab will contain information on the different course runs, including enrollments, performance data, and video engagement. With this information, you can compare a course delivered more than once on your platform and evaluate when and under what circumstances it performed best.

.. image:: /_static/run_metrics.png

.. note:: If you select one course or organization in the Course Metrics, a cross-filter will activate in the Run Metrics data. You can learn more about `Cross filter here <https://docs.openedx.org/projects/openedx-aspects/en/latest/course_team/how-tos/cross_filter.html>`_.

Data Sections:
**************

The Course Metrics and Run Metrics tab will allow you to display the course information in the following sections:

Course Info:
------------
The Course Info table allows users to sort the courses or course runs they compare by their principal features, such as name, organization, the link to their information in the Course Dashboard, the current enrollees, the number of students active in the last seven days, and their course-level tags.

.. image:: /_static/course_info.png

Enrollment Counts:
------------------
The Enrollment Counts table allows users to see the enrollment breakdown of courses or courses run by current enrollment to see which courses are the most and least popular or by a specific enrollment track available on their instance. For example, if their enrollment track only has Verified and Unverified Enrollees, this table should show a Verified Enrollees and an Unverified Enrollees column. This information might answer the question: what courses or course runs are the most learners pursuing certificates for?

.. image:: /_static/enrollment_counts.png

Learner Performance Breakdown:
------------------------------
The Learner Performance Breakdown visually conveys how much of your currently enrolled learner base for each course is active, how many learners have passed, and how many are at risk of not completing the course. This last group represents learners who have enrolled in the course, have done something other than visit the course homepage, have not yet passed the course, and have not visited the course in seven or more days. By default, this graph shows the top 10 courses or course runs by total current enrollment. If a user applies a filter, this graph will update to show the top 10 courses or course runs of the courses that have been filtered.

.. image:: /_static/learner_performance_breakdown.png

Learner Performance:
--------------------
The Learner Performance table allows users to view and sort the courses or course runs they are comparing by high-level learner performance metrics and other metrics, such as the average of correct answers in the first attempt across the entire course or course run that measures how well matched your learners are to the difficulty level of the problems in that course. This is useful for evaluating if the metric is too high and the problems may be too easy. If the metric is lower, the problems may be too complex for your students. If very high or deficient numbers appear for a course, users can navigate to the course dashboard for a single course to dig a little deeper into which problems may be causing the most problems for learners. This metric represents the percentage of learners who submitted the correct response on the first attempt across all problems in the course only among learners who have submitted a response to each problem.

.. image:: /_static/learner_performance.png

Video Engagement:
-----------------
The Video Engagement table presents important video metrics for all filtered courses or course runs for comparison. These metrics can be sorted to identify any outliers quickly. The percentage of video seconds watched metric gives a quick overview of how much video content learners who have started a video in the course are watching. A high percentage of video seconds re-watched can indicate that there may be one or more videos in the course that are unclear or confusing to learners. The number of videos and average video length metrics provide additional context for these measurements. For example, a low percentage of video seconds watched for a course might be because the average video length is long. 

.. image:: /_static/video_engagement.png

How to Access Course Comparison Dashboard?
******************************************

This dashboard's essential feature is that it can only be accessed from Superset. You can access it via the link to Superset in the Reports tab in the Instructor section from any course in the LMS. If the user's instance does not show the link at the top of the other dashboards, you must connect with your instance administrator. 

.. seealso:: To learn more about `Superset click here <https://docs.openedx.org/projects/openedx-aspects/en/latest/course_team/concepts/superset_overview.html>`_.

.. seealso:: To learn more about accessing Superset, `visit this documentation <https://docs.openedx.org/projects/openedx-aspects/en/latest/administrator/how-tos/access_superset.html>`_.

Also, depending on the combination of Django permissions of your Open edx Platform and your course role, you might or might not be able to access this dashboard.

.. image:: /_static/matrix_permissions.png

Another critical point is that depending on your role and permissions in Superset, you will see more or fewer data from your Open edX instance courses in this dashboard. For example, if you only have a `Course Delivery Team role <https://docs.openedx.org/projects/openedx-aspects/en/latest/course_team/concepts/role_and_permissions.html>`_, you can see only the courses or course runs to which you have been added as staff. But if you have the `role of superuser or administrator <https://docs.openedx.org/projects/openedx-aspects/en/latest/administrator/concepts/role_description.html>`_, you will see all the course data.


