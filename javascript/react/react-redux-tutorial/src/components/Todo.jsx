import React from 'react';
import {connect} from 'react-redux';
import {setCompleted} from '../redux/actions';

function Todo(props) {
    let name = props.name;
    if (props.completed) {
        name = <del>{name}</del>;
    }

    return (
        <div>
            {name}
            <button
                onClick={e => props.setCompleted(props.id, !props.completed)}
            >
                Toggle complete
            </button>
        </div>
    );
}

export default connect(
    null,
    {setCompleted}
)(Todo);