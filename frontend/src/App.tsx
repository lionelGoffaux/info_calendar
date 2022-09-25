import {CourseSelector} from "./CourseSelector";
import {Hero} from "./Hero";
import {NavBar} from "./NavBar";
import {Container} from "./Container";
import {CoursesContext} from "./contexts";
import {useState} from "react";

function App() {

  const [coursesList, setCoursesList] = useState([]);

  return (<CoursesContext.Provider value={{coursesList, setCoursesList}}>
      <NavBar/>
      <Hero/>
      <Container>
        <CourseSelector/>
      </Container>
    </CoursesContext.Provider>
  )
}

export default App
