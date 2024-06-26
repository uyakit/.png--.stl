const logger = require("./logger.js").application;

module.exports = function(options) {
	return function (err, req, res, next) {
		logger.error(err.message);
		next(err);
	};
};