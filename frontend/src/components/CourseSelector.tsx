import {useQuery} from 'react-query';
import {useState} from "react";

import {getCalendars} from "../common/api";
import {CourseList} from "./CourseList";

export function CourseSelector() {

  const {data, isLoading, error} = useQuery('calendars', getCalendars);
  const [selectedCalendar, setSelectedCalendar] = useState(0);

  const tabDefaultClass = "tab md:tab-lg flex-1";

  const generateTab = (calendar: string, index: number) => {
    const tabClass = selectedCalendar === index ? tabDefaultClass + ' tab-active' : tabDefaultClass;
    return <div key={calendar} className={tabClass} onClick={() => setSelectedCalendar(index)}>{calendar}</div>
  };

  if (isLoading)
    return <h1>loading...</h1>


  if (!data || error)
    return <h1>error...</h1>


  return <>
    <div className="tabs tabs-boxed justify-center md:my-10">
      {data.map(generateTab)}
    </div>

    <CourseList calendar={data[selectedCalendar]} />
  </>
}