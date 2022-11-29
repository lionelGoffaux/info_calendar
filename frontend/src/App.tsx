import {CourseSelector} from "./components/CourseSelector";
import {Hero} from "./components/Hero";
import {NavBar} from "./components/NavBar";
import {Container} from "./components/Container";
import {CoursesContext} from "./common/contexts";
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
