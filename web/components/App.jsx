import React, { Component } from 'react';
import {} from 'react-bootstrap/lib';
import Start from './Start.jsx';

/**
 * The toplevel application component to render as the root node.
 */
class App extends Component {
    state = { isGameStarted: false }

    onStart = (values) => {
        const state = Object.assign({}, values, { isGameStarted: true });
        this.setState(state);
    }

    render() {
        const { isGameStarted } = this.state;

        return (
            <div>
                {isGameStarted ?
                    (<div>game active!</div>) :
                    (<Start onStart={this.onStart} />)
                }
            </div>
        )
    }
}

export default App;
