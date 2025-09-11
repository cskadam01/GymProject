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
import { LandingPage } from "./pages/Landing/LandingPage";
import { AuthWrapper } from "./AuthWrapper";
import { Asf } from "./pages/asf";
import { ForgotPass } from "./pages/Login/ForgotPass";
import { NewPassword } from "./pages/Profile/NewPassword/newPassword";

function App() {
  return (
    <Router>
      <Routes>
        {/* Nyilvános route-ok */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/asf" element={<Asf />}/>
        <Route path="forgot-password" element={<ForgotPass/>}/>

        {/* Védett route-ok AuthWrapperrel */}
        <Route
          path="/profile"
          element={
            <AuthWrapper>
              <Profile />
            </AuthWrapper>
          }
        />
        <Route
          path="/new-password"
          element={
            <AuthWrapper>
              <NewPassword />
            </AuthWrapper>
          }
        />
        

        <Route
          path="/browse-exercises"
          element={
            <AuthWrapper>
              <BrowseExercises />
            </AuthWrapper>
          }
        />
        <Route
          path="/diary"
          element={
            <AuthWrapper>
              <Diary />
            </AuthWrapper>
          }
        />
        <Route
          path="/diary/:id"
          element={
            <AuthWrapper>
              <OpenedExer />
            </AuthWrapper>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;