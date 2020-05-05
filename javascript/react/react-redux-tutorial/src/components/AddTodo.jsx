import React from 'react';
import {connect} from 'react-redux';
import {addTodo} from '../redux/actions';

function AddTodo(props) {
    const [ value, setValue ] = React.useState('');
    return (
        <div>
            <input
                value={value}
                onChange={e => setValue(e.target.value)}
            />
            <button
                onClick={() => props.addTodo(value)}
            >
                Add
            </button>
        </div>
    );
}

export default connect(
    null,
    {addTodo}
)(AddTodo);