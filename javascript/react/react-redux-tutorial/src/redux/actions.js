import {ADD_TODO, SET_COMPLETED} from './actionTypes';

let nextTodoId = 0;
export const addTodo = name => ({
    type: ADD_TODO,
    payload: {
        id: nextTodoId++,
        completed: false,
        name
    }
});

export const setCompleted = (id, completed) => ({
    type: SET_COMPLETED,
    payload: {
        id,
        completed
    }
});