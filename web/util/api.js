import routeRequest from './routeRequest';
import getAPIURL from './getAPIURL';

const api = {
    /**
     * Initiate a new game.
     * @param {Object} query - The query object with the technology information.
     * @param {String} query.name - The name of the game.
     * @param {String} query.team_1 - The name of the first team.
     * @param {String} query.team_2 - The name of the second team.
     * @param {Function} cb - The callback function.
     * @return {undefined}
     */
    start(query, cb) {
        return routeRequest('POST', `${getAPIURL()}/start`, query, cb);
    },

    /**
     * End a game.
     * @param {Number} id - The unique ID of the game to end.
     * @param {Function} cb - The callback function.
     * @return {undefined}
     */
    end(id, cb) {
        return routeRequest('POST', `${getAPIURL()}/end/id`, query, cb);
    },

    /**
     * Get the game status.
     * @param {Number} id - The unique ID of the game to get the status of.
     * @param {Function} cb - The callback function.
     * @return {undefined}
     */
    status(id, cb) {
        return routeRequest('GET', `${getAPIURL()}/status/id`, query, cb);
    },
};

export default api;
