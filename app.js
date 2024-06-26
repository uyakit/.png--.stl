/**
Copyright (c) 2024 Yuya KITANO
Released under the MIT license
https://opensource.org/licenses/mit-license.php
*/

'use strict';

const PORT = process.env.PORT || 3000;
const express = require("express");
const app = express();
const path = require("path");
const logger = require("./lib/log/logger.js");
const logger_access = require("./lib/log/logger-access.js");
const logger_application = require("./lib/log/logger-application.js");


// https://www.tohoho-web.com/ex/express.html#post-parameters
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Static resources routing.
app.use("/public", express.static(path.join(__dirname, "/public")));
app.use("/views", express.static(path.join(__dirname, "/views")));
app.use("/app", express.static(path.join(__dirname, "/app")));
app.use("/logs", express.static(path.join(__dirname, "/logs")));

// Set access log.  #after Static Web Apps
app.use(logger_access());

// Dynamic resources routing.
app.use("/", require("./routes/index.js"));

// Set application log.
app.use(logger_application());

// Execute web application.
app.listen(PORT, () => {
	logger.application.info(`Application listening at :${PORT}`);
});
