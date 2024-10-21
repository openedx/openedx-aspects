Filters
#######

Filters in Superset for Open edX Aspects are powerful tools that allow users to refine and customize their view of course and learner data. By applying specific criteria, users can isolate and analyze subsets of data, enabling more profound insights into course performance, learner engagement, and other vital metrics. 

These filters provide a flexible and efficient way to:

- Compare courses: Identify similarities and differences between courses.
- Analyze learner behavior: Understand how learners interact with course content.
- Identify trends and patterns: Discover trends in course performance and learner engagement.
- Troubleshoot issues: Pinpoint areas where courses may need improvement.

By leveraging these filters, users can gain valuable insights into the effectiveness of their online courses and make data-driven decisions to improve the learning experience.

Their key functionalities are:

1. Customization: Users can create precise filters to meet their unique analysis needs.
2. Flexibility: Filters can be combined to create complex queries.
3. Efficiency: Quickly isolate relevant data for in-depth analysis.
4. Visualization: Filters can be integrated with visualizations to create informative dashboards.

Types of Filters
****************

There are three main types of filters in Superset dashboards:

- **Course Filters:** These filters allow you to specify which courses you want to see data for. For example, in the following image, the course filters include Organization, Course Name, and Course Run, which are currently set to specific examples.  

.. image:: /_static/course_filters.png


- **Time Filters:** These filters allow you to specify the period you want to see data for. The "Date" filter in the image is currently set to "No filter." There is also a "Time Grain" filter that you can use to change the time interval shown in the graph (e.g., day, week, month).

.. image:: /_static/time_filters.png

- **Individual Learner Filters:** These filters on the Individual Learner Dashboard allow you to filter the enrollment, engagement, and performance information for a single learner in your course at a time. By default, no filter is applied to the Name, Username, or Email filter.  

Filters for the Course Comparison Dashboard:
============================================

The `Course Comparison Dashboard <https://docs.openedx.org/projects/openedx-aspects/en/latest/reference/course_comparison_dashboard.html>`_ has different filters that allow you to refine your search and compare and analyze the performance of other courses or versions of the same course.  Let’s find the function of these filters.

- **Organization filter:** This allows you to filter the courses or course runs you are viewing and comparing throughout the Course Comparison Dashboard by the Organization with which the course or course run is associated. You can filter this by multiple organizations or leave the filter blank to compare courses or course runs across the instance.

- **Tag Filter:** This filter will allow you to filter the course and course run data in this dashboard by courses with one or more filtered tags applied to the entire course. For example, if you wish to see all of your microbiology courses, use a microbiology course level tag filter to compare only courses and course runs that share the microbiology tag. You can filter by multiple tags. For example, you can filter on biochemistry and microbiology. The resulting courses and course run on this dashboard will include all courses with the biochemistry, or the microbiology tag or courses or course runs that have both tags applied to the whole course/course run. This filter will only work for instances running the Redwood Release or later.

- **Course Name filter:** This filter allows you to filter the courses or course runs you compare by one or more courses. Applying a course filter and navigating to the Run Metrics tab in the dashboard can be a powerful way to compare all runs of the same course.

- **Course Run filter:** This allows you to filter the course you compare by one or more course runs.

.. image:: /_static/filters_comparison.png

Additional Considerations About Filters:
========================================

- Data granularity: The granularity of the data available for filtering will vary depending on the specific implementation of Superset for Open edX Aspects.
- Performance: The performance of filters can be impacted by the size and complexity of the dataset.

In essence, filters in Superset for Open edX Aspects are essential tools for data exploration and analysis, providing users with valuable insights into the performance of their online courses.

