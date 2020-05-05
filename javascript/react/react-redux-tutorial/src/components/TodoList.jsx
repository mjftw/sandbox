import React from 'react';
import {connect} from 'react-redux';
import Todo from './Todo';
import AddTodo from './AddTodo';


function TodoList(props) {
    return (
        <div>
            <AddTodo addTodo={props.addTodo} />
            {props.todos.map(todo =>
                <Todo
                    key={todo.id}
                    name={todo.name}
                    id={todo.id}
                    setCompleted={props.setCompleted}
                    completed={todo.completed}
                />
            )}
        </div>
    );
}


function mapStateToProps(state) {
    const todos = state.todos || [];
    return {todos};
}

export default connect(
    mapStateToProps
)(TodoList);
