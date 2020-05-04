import React from 'react';

export default function Todo(props) {
    let name = props.name;
    if (props.completed) {
        name = <del>{name}</del>;
    }

    return (
        <div>
            {name}
            <button
                onClick={e => props.setCompleted(props.idx, !props.completed)}
            >
                Toggle complete
            </button>
        </div>
    );
}
