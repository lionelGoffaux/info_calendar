import React from "react";

export const CoursesContext =  React.createContext({coursesList: [] as string[], setCoursesList: (coursesList: any) => {}});