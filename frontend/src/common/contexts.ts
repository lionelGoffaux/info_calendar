import React from 'react';
const setCoursesList: React.Dispatch<React.SetStateAction<string[]>> = () => {};
export const CoursesContext = React.createContext({coursesList: [] as string[], setCoursesList});
