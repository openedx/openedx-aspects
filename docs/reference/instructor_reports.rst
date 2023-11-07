.. _instructor-reports:

Instructor Reports
##################

The Instructor Dashboard contains charts that are of interest to course authors and course staff

The dashboard is visible to all Course Staff, Global Staff and Superusers on Open edX.

Course Staff may only see event data from the courses they are staff members for.

.. _instructor_filters:

Filters
*******

You can filter the data used by these charts by applying various options from the Filters panel.

For example, to see enrollments for one or more Organizations, add the desired Organizations to the Organization filter list and click the "Apply Filters" button to change the data shown in the charts.

.. note: Ensure the "Time range" filter is set to the desired date/time range. By default, only the previous month of data is shown.

.. _course-enrollment-tab:

Course Enrollment
*****************

Course Enrollment charts can help you understand how many students are enrolled in your course by showing how enrollments have changed over time and which enrollment modes students are choosing.

.. _enrollments-per-day:

Currently Enrolled Learners Per Day
===================================

Shows the cumulative total of unique enrolled learners based on their enrollment state at the end of each day of the selected time range.

If a learner was enrolled previously, but has left the course since, they are not counted as of the date they left. If they re-enroll in the course they will be counted again.

.. _enrollments-by-mode:

Enrollments By Enrollment Mode
==============================

Shows the current count of active enrollments by their most recent enrollment mode (audit, verified, etc) for the selected time range.

For example, if a learner upgraded from Audit to Verified they will only be counted once as Verified. Learners who have un-enrolled in the course are not counted.

.. _enrollment-events-per-day:

Enrollment Events Per Day
=========================

Shows a count of the number of enrollments and un-enrollments per day of the selected time range.

Learners can enroll and unenroll multiple times, in this chart each individual enrollment and unenrollment will be counted.


.. _problem-engagement-tab:

Problem Engagement
******************

Problem Engagement charts can help you learn which problems your students have engaged with or skipped, and the relative difficulty of problems across your course.

.. note:: Select a course from the Filters panel to populate these charts.

.. _problem-responses:

Responses Per Problem
=====================

Shows the number of students who have responded to a question, and whether they have ever answered correctly.

Students can answer some questions multiple times, but this chart counts each student only once per question.

.. _problem-course-grade:

Course Grade Distribution
=========================

Shows the distribution of grades for a course (out of 100%) for the selected time range.

Grades are grouped in ranges of 10%.


.. _problem-performance-tab:

Problem Performance
*******************

Problem Performance charts help show the difficulty of your problems by showing you which answers your students choose and which require many tries or hints to complete successfully.

.. note: Select a problem from the Filters panel to populate these charts.

.. _problem-dist-responses:

Distribution of Responses
=========================

Shows how often an answer (or combination of answers for multi-select problems) is selected by learners for the selected time range.

Some problems allow learners to submit a response more than once; this chart will include all of the responses in that case.

.. _problem-dist-grades:

Distribution of Problem Grades
==============================

Shows the number of students who scored within a certain percentage of points for this problem for the selected time range.

For problems that are pass/fail it will only show the lowest and highest percentage ranges.

.. _problem-dist-attempts:

Distribution of Attempts
========================

Shows the number of attempts that students needed to make before getting the problem's answer correct.

This only counts students who eventually answered correctly.

.. _problem-dist-hints-correct:

Distribution of Hints Per Correct Answer
========================================

Shows counts of the number of times hints (including displaying the answer itself) were displayed for each learner who eventually answered the problem correctly.

Problems with no hint or answer display configured are grouped under "0".


.. _video-engagement-tab:

Video Engagement
****************

These charts can help you understand which videos are watched, and rewatched, most often. It can also show how many users use the closed captions and transcript features on your videos, and how often.

.. note: Select a course from the Filters panel to populate these charts.

.. _video-watches:

Watches Per Video
=================

Shows how many unique learners have watched each video, and how many repeat views each video got, for the selected time range.

If a video has never been played it will not appear in this chart.

.. _video-transcripts-captions:

Transcripts/Captions Per Video
==============================

Shows how many learners are using the video's transcripts or closed captions for the selected time range.

If the video has no transcripts or captions the chart will be empty.


.. _video-performance-tab:

Video Performance
*****************

This section allows you to see which parts of a particular video are most watched or skipped.

.. note: Select a video from the Filters panel to populate these charts.


.. _video-watched-segments:

Watched Video Segments
======================

Shows which parts of a video are most watched, and which are most re-watched, for the selected time range.

Each segment represents 5 seconds of the video.


.. _forum-interaction-tab:

Forum Interaction
*****************

These charts show usage data for the course discussion forum.

.. note: Currently only the official Open edX discussion forum sends user events to Aspects. Forums integrated via LTI will not show data here.

.. _forum-users:

Distinct Forum Users
====================

Shows the number of unique forum users for the selected time range.

.. _forum-posts-per-user:

Posts Per User
==============

Shows the total number of posts (threads and replies) made by each forum user.
