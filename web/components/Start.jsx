import React, { Component } from 'react';
import { FormGroup, Form, FormControl, ControlLabel, InputGroup, Button, Col, Grid, Row }
    from 'react-bootstrap/lib';

/**
 * The form to start a game.
 */
 class Start extends React.Component {
    state = {
        name: '',
        teamOneName: '',
        teamTwoName: '',
        maxScore: '',
    }

    // TODO: Add validation.

    onClick = () => this.props.onStart(this.state);

    handleChangeName = (e) =>
        this.setState({ name: e.target.value });

    handleChangeTeamOneName = (e) =>
        this.setState({ teamOneName: e.target.value });

    handleChangeTeamTwoName = (e) =>
        this.setState({ teamTwoName: e.target.value });

    handleChangeMaxScore = (e) =>
        this.setState({ maxScore: e.target.value });

 	render() {
 		return (
            <Grid>
                <Row className="show-grid">
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
                                    value={this.state.name}
                                    onChange={this.handleChangeName}
                                    type="name"
                                />
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="formHorizontalTeam1">
                            <Col componentClass={ControlLabel} sm={2}>
                                Team 1 Name
                            </Col>
                            <Col sm={10}>
                                <FormControl
                                    type="team1"
                                    value={this.state.teamOneName}
                                    onChange={this.handleChangeTeamOneName}
                                />
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="formHorizontalTeam2">
                            <Col componentClass={ControlLabel} sm={2}>
                                Team 2 Name
                            </Col>
                            <Col sm={10}>
                                <FormControl
                                    type="team2"
                                    value={this.state.teamTwoName}
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
                                    type="maxScore"
                                    value={this.state.maxScore}
                                    onChange={this.handleChangeMaxScore}
                                />
                            </Col>
                        </FormGroup>
                        <FormGroup>
                            <Col smOffset={2} sm={10}>
                                <Button type="submit" onClick={this.onClick}>
                                    Start!
                                </Button>
                            </Col>
                        </FormGroup>
                    </Form>
                </Row>
            </Grid>
 		);
 	}
}

export default Start;
