import {ADD_TODO, SET_COMPLETED} from './actionTypes';

const initialState = {
    todos: []
};

export function rootReducer(state, action) {
    if (state === undefined) {
        return initialState;
    }

    let newState = {...state};

    switch (action.type) {
        case ADD_TODO:
            const newTodo = {
                id: action.id,
                ...action.payload
            };
            newState.todos = (state.todos === undefined)
                ? [ newTodo ]
                : state.todos.concat(newTodo);
            break;
        case SET_COMPLETED:
            newState.todos = (state.todos === undefined)
                ? []
                : state.todos.map(todo => (todo.id === action.payload.id)
                    ? {...todo, completed: action.payload.completed}
                    : todo);
            break;
        default:
            break;
    }

    return newState;
};