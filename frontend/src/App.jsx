import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";
import { Login } from "./pages/Login/login";
import { Register } from "./pages/Register/register";
import { Profile } from "./pages/Profile/profile";
import { BrowseExercises } from "./pages/BrowseExercises/browseExercises";
import { Diary } from "./pages/Diary/diary";
import { OpenedExer } from "./pages/Diary/Diarybyid/diarybyid";

function App() {
    return(
        <>
        <Router>
            <Routes>
            <Route path="/login" element={<Login/>}/>
            <Route path="/register" element={<Register/>}/>
            <Route path="/profile" element={<Profile/>}/>
            <Route path="/browse-exercises" element={<BrowseExercises/>}/>
            <Route path="/diary" element={<Diary/>}/>
            <Route path="/diary/:id" element={<OpenedExer />} />


           
            
            </Routes>


        </Router>
            
        
        </>


    )

}
export default App
