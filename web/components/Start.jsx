import React, { Component } from 'react';
import { FormGroup, Form, FormControl, ControlLabel, InputGroup, Button, Col,
    Grid, Row } from 'react-bootstrap/lib';

/**
 * The form to start a game.
 */
 class Start extends React.Component {
    state = {
        gameName: '',
        redTeamName: '',
        blueTeamName: '',
        maxGoals: '',
    }

    onClick = () => this.props.onStart(this.state);

    handleChangeName = (e) =>
        this.setState({ gameName: e.target.value });

    handleChangeTeamOneName = (e) =>
        this.setState({ redTeamName: e.target.value });

    handleChangeTeamTwoName = (e) =>
        this.setState({ blueTeamName: e.target.value });

    handleChangeMaxScore = (e) =>
        this.setState({ maxGoals: e.target.value });

 	render() {
 		return (
            <Grid>
                <h1 style={{textAlign: 'center'}}>
                    New Game
                </h1>
                <Form horizontal>
                    <FormGroup controlId="formHorizontalGameName">
                        <Col componentClass={ControlLabel} sm={2}>
                            Game Name
                        </Col>
                        <Col sm={10}>
                            <FormControl
                                value={this.state.gameName}
                                onChange={this.handleChangeName}
                            />
                        </Col>
                    </FormGroup>
                    <FormGroup controlId="formHorizontalTeam1">
                        <Col componentClass={ControlLabel} sm={2}>
                            Red Team Name
                        </Col>
                        <Col sm={10}>
                            <FormControl
                                value={this.state.redTeamName}
                                onChange={this.handleChangeTeamOneName}
                            />
                        </Col>
                    </FormGroup>
                    <FormGroup controlId="formHorizontalTeam2">
                        <Col componentClass={ControlLabel} sm={2}>
                            Blue Team Name
                        </Col>
                        <Col sm={10}>
                            <FormControl
                                value={this.state.blueTeamName}
                                onChange={this.handleChangeTeamTwoName}
                            />
                        </Col>
                    </FormGroup>
                    <FormGroup controlId="formHorizontalMaxScore">
                        <Col componentClass={ControlLabel} sm={2}>
                            Max Score
                        </Col>
                        <Col sm={10}>
                            <FormControl
                                value={this.state.maxGoals}
                                onChange={this.handleChangeMaxScore}
                            />
                        </Col>
                    </FormGroup>
                    <FormGroup>
                        <Col smOffset={2} sm={10}>
                            <Button
                                onClick={this.onClick}
                                bsSize="large"
                                block
                            >
                                Start!
                            </Button>
                        </Col>
                    </FormGroup>
                </Form>
            </Grid>
 		);
 	}
}

export default Start;
