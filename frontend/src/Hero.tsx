import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCopy} from '@fortawesome/free-solid-svg-icons';
import {useContext, useEffect, useState} from "react";
import { fromByteArray } from 'base64-js';

import bg_image from './img/bg.jpg'
import {CoursesContext} from "./contexts";

export function Hero() {

  const [url, setUrl] = useState("https://"+location.hostname+"/calendar.ics")
  const {coursesList} = useContext(CoursesContext);

  useEffect(() => {
    const jsonList = JSON.stringify(coursesList);
    const b64 = fromByteArray(new TextEncoder().encode(jsonList));
    setUrl("https://"+location.hostname+"/calendar.ics?l="+b64)
  }, [coursesList])

  return <div className="flex flex items-center justify-center p-5  md:p-0 md:h-[500px] md:max-h-[500px] relative">
    <div className="hidden md:inline md:absolute inset-0 overflow-hidden w-full">
      <img src={bg_image} className='w-full' />
    </div>
    <div className="md:absolute md:bg-base-100/60 md:inset-0"></div>
    <div className="form-control w-full md:w-1/2">
      <div className="input-group z-10">
        <input type="text" className="input input-bordered w-full" value={url}/>
        <button className="btn btn-square btn-info">
          <FontAwesomeIcon icon={faCopy} />
        </button>
      </div>
    </div>
  </div>;
}