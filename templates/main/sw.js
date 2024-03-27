"use strict";
importScripts("sw-toolbox.js");
toolbox.precache(["/","static/css/styles.css", "static/js/main.js"]);
toolbox.router.get("static/img/*", toolbox.cacheFirst);
toolbox.router.get("/*", toolbox.networkFirst, { networkTimeoutSeconds: 5});