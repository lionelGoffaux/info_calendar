import {useContext} from "react";
import {CoursesContext} from "../common/contexts";

export function CourseCheckbox({calendar, course}: { calendar:string, course: String}) {

  const {coursesList, setCoursesList} = useContext(CoursesContext);
  const courseFullName = calendar + "/" + course;

  const toggleCourse = () => {
    if (coursesList.includes(courseFullName)) {
      setCoursesList((courses: string[]) => courses.filter((c: string) => c !== courseFullName));
    } else {
      setCoursesList((courses: string[]) => [...courses, courseFullName].sort());
    }
  }

  return <>
    <div className="form-control lg:px-5">
      <label className="label cursor-pointer flex items-center">
        <span className="label-text">{course}</span>
        <input type="checkbox" className="toggle toggle-accent" checked={coursesList.includes(courseFullName)} onChange={() => toggleCourse()}/>
      </label>
    </div>
  </>
}