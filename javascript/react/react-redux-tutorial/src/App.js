import React, {Component} from 'react';
import TodoList from './components/TodoList';

export default class App extends Component {
    constructor(props) {
        super(props);

        this.setCompleted = this.setCompleted.bind(this);
        this.addTodo = this.addTodo.bind(this);

        this.state = {
            todos: []
        };
    }

    setCompleted(idx, completed) {
        this.setState({
            todos: this.state.todos.map(
                todo => todo.idx === idx ? {...todo, completed} : todo)
        });
    }

    addTodo(name) {
        this.setState({
            todos: this.state.todos.concat({
                name,
                completed: false,
                idx: this.state.todos.length
            })
        });
    }

    render() {
        return (
            <div>
                <TodoList
                    todos={this.state.todos}
                    setCompleted={this.setCompleted}
                    addTodo={this.addTodo}
                />
            </div>
        );
    }
}
