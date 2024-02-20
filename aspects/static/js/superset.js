/* Javascript for SupersetXBlock. */
function SupersetXBlock(runtime, element, context) {
  const dashboard_uuid = context.dashboard_uuid;
  const superset_url = context.superset_url;
  const superset_token = context.superset_token;
  const xblock_id = context.xblock_id

  function initSuperset(supersetEmbeddedSdk) {
    embedDashboard(dashboard_uuid, superset_url, superset_token, xblock_id);
  }

  if (typeof require === "function") {
    require(["supersetEmbeddedSdk"], function (supersetEmbeddedSdk) {
      window.supersetEmbeddedSdk = supersetEmbeddedSdk;
      initSuperset();
    });
  } else {
    loadJS(function () {
      initSuperset();
    });
  }
}

function loadJS(callback) {
  if (window.supersetEmbeddedSdk) {
    callback();
  } else {
    $.getScript("https://cdn.jsdelivr.net/npm/@superset-ui/embedded-sdk@0.1.0-alpha.10/bundle/index.min.js")
      .done(function () {
        callback();
      })
      .fail(function () {
        console.error("Error loading supersetEmbeddedSdk.");
      });
  }
}
