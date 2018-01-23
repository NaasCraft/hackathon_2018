import routeRequest from './routeRequest';
import getAPIURL from './getAPIURL';

const api = {
    /**
     * Initiate a new game.
     * @param {Object} body - The body object with the technology information.
     * @param {String} body.name - The name of the game.
     * @param {String} body.team_red - The name of the first team.
     * @param {String} body.team_blue - The name of the second team.
     * @param {String} body.max_goals - The goals needed to win.
     * @param {Function} cb - The callback function.
     * @return {undefined}
     */
    start(body, cb) {
        return routeRequest('POST', `${getAPIURL()}/start`, body, cb);
    },

    /**
     * End a game.
     * @param {Number} id - The unique ID of the game to end.
     * @param {Function} cb - The callback function.
     * @return {undefined}
     */
    end(id, cb) {
        return routeRequest('POST', `${getAPIURL()}/end/${id}`, {}, cb);
    },

    /**
     * Get the game status.
     * @param {Number} id - The unique ID of the game to get the status of.
     * @param {Function} cb - The callback function.
     * @return {undefined}
     */
    status(id, cb) {
        return routeRequest('GET', `${getAPIURL()}/status/${id}`, {}, cb);
    },

    update(id, difference, team) {
        const body = {
            team,
            difference,
        }
        return routeRequest('POST', `${getAPIURL()}/update/${id}`, body,
            err => {
                if (err) {
                    return console.log(err);
                }
            });
    },
};

export default api;
