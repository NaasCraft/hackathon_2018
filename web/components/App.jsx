import React, { Component } from 'react';
import { Grid } from 'react-bootstrap/lib';
import Start from './Start.jsx';
import ActiveGame from './ActiveGame.jsx';
import api from '../util/api.js';

/**
 * The toplevel application component to render as the root node.
 */
class App extends Component {
    state = {
        gameId: null,
        winner: null,
        isGameStarted: false,
    }

    onStart = (values) => {
        return api.start({
            name: values.gameName,
            team_red: values.redTeamName,
            team_blue: values.blueTeamName,
            max_goals: values.maxGoals,
        }, (err, res) => {
            if (err) {
                return console.log(err);
            }
            const state = Object.assign({}, values, {
                gameId: res.id,
                isGameStarted: true,
            });
            this.setState(state);
        });
    }

    onEnd = () => {
        const { gameId } = this.state;
        return api.end(gameId, err => {
            if (err) {
                return console.log(err);
            }
            this.setState({
                blueTeamScore: 0,
                redTeamScore: 0,
                isGameStarted: false,
                winner: null,
            });
        });
    }

    setWinner = (res) => {
        const maxGoals = Number(res.max_goals);
        if (res.score_red >= maxGoals) {
            return this.setState({ winner: this.state.redTeamName })
        }
        if (res.score_blue >= maxGoals) {
            return this.setState({ winner: this.state.blueTeamName })
        }
    }

    timer = () => {
        const { gameId, isGameStarted } = this.state;
        if (isGameStarted) {
            return api.status(gameId, (err, res) => {
                if (err) {
                    return console.log(err);
                }
                this.setWinner(res);
                return this.setState({
                    blueTeamScore: res.score_blue,
                    redTeamScore: res.score_red,
                    isPaused: res.paused,
                });
            });
        }
    };

    incrementTeamOneScore = () =>
        api.update(this.state.gameId, 1, 'red');

    decrementTeamOneScore = () =>
        api.update(this.state.gameId, -1, 'red');

    incrementTeamTwoScore = () =>
        api.update(this.state.gameId, 1, 'blue');

    decrementTeamTwoScore = () =>
        api.update(this.state.gameId, -1, 'blue');

    componentDidMount = () =>
        this.setState({ interval: setInterval(this.timer, 100) });

    render() {
        const {
            isGameStarted,
            gameName,
            redTeamName,
            blueTeamName,
            winner,
            redTeamScore,
            blueTeamScore,
        } = this.state;

        return (
            <div>
                {isGameStarted ?
                    (<ActiveGame
                        gameName={gameName}
                        redTeamName={redTeamName}
                        redTeamScore={redTeamScore}
                        blueTeamName={blueTeamName}
                        blueTeamScore={blueTeamScore}
                        winner={winner}
                        incrementTeamOneScore={this.incrementTeamOneScore}
                        decrementTeamOneScore={this.decrementTeamOneScore}
                        incrementTeamTwoScore={this.incrementTeamTwoScore}
                        decrementTeamTwoScore={this.decrementTeamTwoScore}
                        onEnd={this.onEnd}
                    />) :
                    (<Start onStart={this.onStart} />)
                }
            </div>
        )
    }
}

export default App;
