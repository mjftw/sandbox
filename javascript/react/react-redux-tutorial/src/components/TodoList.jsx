import React from 'react';
import Todo from './Todo';
import AddTodo from './AddTodo';

export default function TodoList(props) {
    return (
        <div>
            <AddTodo addTodo={props.addTodo} />
            {props.todos.map(todo =>
                <Todo
                    id={todo.idx}
                    name={todo.name}
                    idx={todo.idx}
                    setCompleted={props.setCompleted}
                    completed={todo.completed}
                />
            )}
        </div>
    );
}
