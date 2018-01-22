import request from 'superagent';
import safeJSONParse from './safeJSONParse';

/**
 * Make a request to the api with the given parameters.
 * @param {String} method - The HTTP method to use for the request.
 * @param {String} path - The API route path.
 * @param {Function} cd - The callback function.
 * @return {undefined}
 */
function routeRequest(method, path, query, cb) {
    request(method, path)
        .query(query)
        .end((err, res) => {
            if (err) {
                return cb(err);
            }
            const { parseErr, data } = safeJSONParse(res.text);
            if (parseErr) {
                return cb(parseErr);
            }
            return cb(null, data);
        });
}

export default routeRequest;
