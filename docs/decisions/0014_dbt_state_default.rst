14. dbt State Management
########################

Status
******

Accepted

Context
*******

In developing Aspects we've moved as much as possible of the ClickHouse schema to dbt for ease of management, documentation, and testing. As part of that work, we've materialized some of our large datasets to materialized views. A side effect of this is that every time dbt is run, it will recreate these large datasets leading to potentially large downtimes that are unnecessary if nothing has changed.

Decision
********

**Only run models that have changed, or that are downstream of certain changes**

dbt allows the model selector ``state:modified+``, which will compare the current project state to the last run and skip any unchanged models. This will also rebuild all models downstream of the changed model so that they all have the most current data. What counts as "changed" is a complicated topic, but our decision is to accept changes to the following as "modified":

- Macros - if a macro that a model uses has changed, we consider it modified
- Configuration - if a config block in a model changes, we consider it modified
- `var` / `env_var` - when a variable used in a model has changed, we consider it modified

We do *not* consider the following as marking a model modified:

- Tests which reference a model

More details can be found in the `dbt docs`_

**Run only modified models by default**

As repeatedly running init / dbt commands should be as fast as possible, we will make ``state:modified+`` the default. A potentially long downtime should be a positive choice, not an accident.


Consequences
************

#. Since dbt will need to know the prior state to understand which models to skip, we must store the ``manifest.json`` file created on each run. This means adding a new persistent file mount in docker compose and kubernetes.
#. Our dbt wrapper scripts will need to be aware of this flag so that they can choose between running without the ``state`` selector on initial population of the database, and running with it on subsequent runs.
#. Certain dbt commands that get passed through our command wrappers may not work with the ``state`` selector. We will need a flag to disable it, and operators running those commands will need to know when to use the flag.

Rejected Alternatives
*********************

* Rebuilding every model every run- this is the default mode of dbt and makes sure everything is as fresh as possible, but the cost of hours rebuilding tables is just too high in production systems.

* Applying special logic to materialized views to try to detect changes to the schema of models tables, and skipping them if they haven't changed. dbt doesn't provide facilities for these comparisons and they are likely to be complicated with many more side effects than we are comfortable with. It is likely that the dbt-clickhouse provider would not take accept such a change.

References
**********

* `dbt docs`_ on state comparison

.. _dbt docs: //docs.getdbt.com/reference/node-selection/state-comparison-caveats
