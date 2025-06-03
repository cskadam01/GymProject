import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";
import { Login } from "./pages/Login/login";
import { Register } from "./pages/Register/register";
import { Profile } from "./pages/Profile/profile";
import { BrowseExercises } from "./pages/BrowseExercises/browseExercises";

function App() {
    return(
        <>
        <Router>
            <Routes>
            <Route path="/login-user" element={<Login/>}/>
            <Route path="/register-user" element={<Register/>}/>
            <Route path="/profile" element={<Profile/>}/>
            <Route path="/browse-exercises" element={<BrowseExercises/>}/>


           
            
            </Routes>


        </Router>
            
        
        </>


    )

}
export default App
