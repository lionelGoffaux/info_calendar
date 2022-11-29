import axios from "axios";

const request = axios.create({
  baseURL: import.meta.env.VITE_API_ENDPOINT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

export async function getCalendars() {
  const response = await request.get("/list_calendars");
  return response.data;
}

export async function getCourses(calendarName: string) {
  const response = await request.get(`/courses/${calendarName}`);
  return response.data;
}
