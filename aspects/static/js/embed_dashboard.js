function embedDashboard(dashboard_uuid, superset_url, superset_token, xblock_id) {
  xblock_id = xblock_id || "";
  window.supersetEmbeddedSdk
    .embedDashboard({
      id: dashboard_uuid, // given by the Superset embedding UI
      supersetDomain: superset_url, // your Superset instance
      mountPoint: document.getElementById(`superset-embedded-container-${xblock_id}`), // any html element that can contain an iframe
      fetchGuestToken: () => superset_token, // function that returns a Promise with the guest token
      dashboardUiConfig: {
        // dashboard UI config: hideTitle, hideTab, hideChartControls, filters.visible, filters.expanded (optional)
        hideTitle: true,
        filters: {
          expanded: false,
        },
        hideTab: true,
        hideChartControls: false,
        hideFilters: true,
      },
    })
    .then((dashboard) => {
      mountPoint = document.getElementById("superset-embedded-container");
      /*
      Perform extra operations on the dashboard object or the container
      when the dashboard is loaded
      */
    });
}
if (window.dashboard_uuid !== undefined) {
  embedDashboard(window.dashboard_uuid, window.superset_url, window.superset_token, window.xblock_id);
}
