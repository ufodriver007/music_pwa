"use strict";
importScripts("sw-toolbox.js");
toolbox.precache(["/","static/css/styles.css", "static/js/main.js", "static/css/all.min.css", "static/css/bootstrap.min.css", "static/css/css2.css", "static/js/bootstrap.bundle.min.js", "static/js/cookie.js", "static/js/dexie.js"]);
toolbox.router.get("static/img/*", toolbox.cacheFirst);
toolbox.router.get("/*", toolbox.networkFirst, { networkTimeoutSeconds: 5});