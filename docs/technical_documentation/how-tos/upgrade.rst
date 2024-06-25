.. upgrade-aspects:

How-to Upgrade Aspects
**********************

At least in the early phases of existence, Aspects is intended to have a faster upgrade cycle than Open edX named releases. It's expected that many operators will want to upgrade between releases to get features as they become available, but the upgrade process should be the same whether it's happening as part of a named release upgrade or in between.

As for any upgrade you should take a backup snapshot of your environment before beginning, especially make sure you have a recent backup of your ClickHouse database. Then follow these steps, which are basically the same as installation:

- Install the version you would like from tutor-contrib-aspects, or for the latest: ``pip install --upgrade tutor-contrib-aspects``
- Save your tutor configuration: ``tutor config save``
- Build your openedx image (in case there are upgrades to LMS/Studio plugins): ``tutor images build openedx --no-cache``
- Initialize Aspects to get the latest schema and reports, for a tutor local install: ``tutor local do init -l aspects``

In a case where the release has special instructions, such as when new xAPI transforms have been added and you may need to replay tracking logs, they will be included in the release announcement.
