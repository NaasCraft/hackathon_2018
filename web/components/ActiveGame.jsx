import React, { Component } from 'react';
import { Button, Modal, Col, Grid, Row } from 'react-bootstrap/lib';
import redPlayer from '../../images/soccerplayer_red.jpg';
import bluePlayer from '../../images/soccerplayer_blue.jpg';

/**
 * The form to start a game.
 */
 class ActiveGame extends React.Component {
    state = {
        gameName: 'Round 1',
        time: '00:00',
        currentCount: 0,
    }

    getControls = (team) => {
        const incrementHandler = team === 'redTeam' ?
            this.props.incrementTeamOneScore : this.props.incrementTeamTwoScore;

        const decrementHandler = team === 'redTeam' ?
            this.props.decrementTeamOneScore : this.props.decrementTeamTwoScore;

        const style = {
            display: 'flex',
            flexDirection: 'column',
        };
        return (
            <Col style={style}>
                <Button bsSize="xsmall" onClick={incrementHandler}>
                    <i className="fa fa-plus" aria-hidden="true" />
                </Button>
                <Button bsSize="xsmall" onClick={decrementHandler}>
                    <i className="fa fa-minus" aria-hidden="true" />
                </Button>
            </Col>
        )
    }

    getModal = (winner) => {
        return (
            <Modal
    			bsSize="large"
                show={true}
    			aria-labelledby="contained-modal-title-lg"
    		>
    			<Modal.Body>
                    <div style={{
                        display: 'flex',
                        justifyContent: 'center',
                    }}
                    >
                        <h1>{winner} wins!</h1>
                    </div>
    			</Modal.Body>
                <Modal.Footer>
                    <Button onClick={this.props.onEnd} block>New Game</Button>
                </Modal.Footer>
    		</Modal>)
    }

    timer = () => this.setState({ currentCount: ++this.state.currentCount });

    getFormattedTime = () => {
        const { currentCount } = this.state;
        return `${new Date(1000 * currentCount).toISOString().substr(14, 5)}`;
    }

    componentDidMount = () =>
        this.setState({ interval: setInterval(this.timer, 1000) });

    componentWillUnmount = () => clearInterval(this.state.interval);

 	render() {
        const {
            gameName,
            redTeamName,
            blueTeamName,
            redTeamScore,
            blueTeamScore,
            winner,
            time,
        } = this.props;

 		return (
            <div>
                {winner ? this.getModal(winner) :
                (<Grid>
                    <Row className="show-grid">
                        <h1 style={{
                            textAlign: 'center',
                            fontSize: '3em',
                        }}>
                            {gameName}
                        </h1>
                        <Col sm={5}>
                            <h1 style={{
                                color: '#d8031c',
                                textAlign: 'center',
                                fontSize: '3em',
                            }}>
                                {redTeamName}
                            </h1>
                            <h1 style={{
                                color: '#d8031c',
                                textAlign: 'center',
                                fontSize: '8em',
                            }}>
                                {redTeamScore || 0}
                            </h1>
                        </Col>
                        <Col sm={2}>
                            <h1 style={{textAlign: 'center'}}>
                                {this.getFormattedTime()}
                            </h1>
                            <div style={{
                                display: 'flex',
                                justifyContent: 'center',
                            }}>
                                <Button
                                    bsSize="small"
                                    onClick={this.props.onEnd}
                                >
                                    End Game
                                </Button>
                            </div>
                            <div style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                marginTop: '20px',
                            }}>
                                {this.getControls('redTeam')}
                                {this.getControls('blueTeam')}
                            </div>
                        </Col>
                        <Col sm={5}>
                            <h1 style={{
                                color: '#1716d7',
                                textAlign: 'center',
                                fontSize: '3em',
                            }}>
                                {blueTeamName}
                            </h1>
                            <h1 style={{
                                color: '#1716d7',
                                textAlign: 'center',
                                fontSize: '8em',
                            }}
                            >
                                {blueTeamScore || 0}
                            </h1>
                        </Col>
                    </Row>
                </Grid>)}
            </div>
        );
 	}
}

export default ActiveGame;
