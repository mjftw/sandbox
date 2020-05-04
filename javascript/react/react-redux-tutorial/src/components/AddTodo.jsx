import React from 'react';

export default function AddTodo(props) {
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
