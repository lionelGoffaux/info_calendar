import {useQuery} from "react-query";
import {getCourses} from "./api";
import {CourseCheckbox} from "./CourseCheckbox";

export function CourseList({calendar}: { calendar: string}) {
  const {data, isLoading, error} = useQuery(['courses', calendar], () => getCourses(calendar));

  if (isLoading)
    return <h1>loading...</h1>

  if (error)
    return <h1>error...</h1>

  return <>
    <ul className="mx-3 mt-2 lg:flex lg:flex-wrap">
      {data.map((course: string) => <li className="lg:w-1/2 2xl:w-1/4 md:h-16" key={calendar+course}>
        <CourseCheckbox calendar={calendar} course={course}/>
      </li>)}
    </ul>
  </>
}